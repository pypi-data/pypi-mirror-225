#!/usr/bin/env python
"""
Affine transformations for arbitrary dimensions implemented in
    python's scientific stack
"""
import logging
from operator import sub

# from decorator import decorator
import numpy

# from .errors import ConversionError, EstimationError
from .errors import EstimationError
from .utils.utils import NullHandler

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())

try:
    from scipy.linalg import svd  # , LinAlgError
except ImportError as e:
    logger.info(e)
    logger.info('scipy-based linalg may or may not lead '
                'to better parameter fitting')
    from numpy.linalg import svd
    # from numpy.linalg.linalg import LinAlgError


class RestrictedDimensionalityModel(object):
    @classmethod
    def check_fit_input(cls, src, dst, dimension=None):
        dimension = cls.dimension if dimension is None else dimension
        if src.shape[1] != dimension:
            raise ValueError("Dimension of input points {} does not match "
                             "that of the {} dimensional model.".format(
                                 src.shape[1], dimension))


class AbstractAffineModel(object):
    """Base class for Affine, Similarity, Rigid, Translation

    """
    def __init__(self, matrix=None, src=None, dst=None, dim=None,
                 estimate_kwargs=None, **kwargs):
        estimate_kwargs = estimate_kwargs or {}
        if matrix is not None:
            self.params = self.normalize_homogeneous_matrix(matrix)
        elif src is not None and dst is not None:
            self.estimate(src, dst, **estimate_kwargs)
        else:
            self.params = self.normalize_homogeneous_matrix(numpy.eye(dim+1))
        self.check_dimension(self.params.shape[0])

    @staticmethod
    def normalize_homogeneous_matrix(m):
        """load square or rectangular homogenous matrix"""
        def process_square(mat):
            last_row = numpy.pad(numpy.array([1]),
                                 (mat.shape[0]-1, 0), 'constant')
            if numpy.all(mat[-1, :] == last_row):
                return mat[:-1, :]
            else:
                return numpy.insert(mat, mat.shape[0], 0, 1)

        def process_rectangle(mat):
            # shape[1] must be one greater length than shape[0]
            if sub(*mat.shape) != -1:
                raise ValueError(
                    "matrix of shape {} cannot be cast as homogeneous".format(
                        mat.shape))
            return mat

        dimlen = len(set(m.shape))
        dim_switch = {1: process_square,
                      2: process_rectangle}
        try:
            return dim_switch[dimlen](m)
        except KeyError:
            raise ValueError(
                "matrix {} of shape {} cannot be cast as homogenous".format(
                    m, m.shape))

    @classmethod
    def check_fit_input(cls, src, dst, **kwargs):
        if src.shape != dst.shape:
            raise ValueError("mismatched shape for source "
                             "points {} and dest points {}".format(
                                 src.shape, dst.shape))

    @staticmethod
    def points_to_homogenous(points):
        return numpy.insert(points, points.shape[1], 1, 1)

    @staticmethod
    def points_from_homogeneous(points):
        return numpy.true_divide(points[:, :-1], points[:, [-1]])

    def tform(self, points):
        """Transform a set of points with this transformation"""
        pts = self.points_to_homogenous(points)
        newpts = numpy.dot(self.M, pts.T).T
        return self.points_from_homogeneous(newpts)

    def residual_displacement(self, src, dst):
        """"""
        self.check_fit_input(src, dst)
        return dst - self.tform(src)

    def residual_distance(self, src, dst):
        """"""
        return numpy.linalg.norm(self.residual_displacement(src, dst), axis=1)

    @staticmethod
    def fit(*args, **kwargs):  # pragma: nocover
        raise NotImplementedError(
            "No fit method for abstract model -- choose subclass")

    def check_dimension(self, dim, expected=None):
        try:
            expected = self.dimension if expected is None else expected
        except AttributeError:
            return
        if dim != expected:
            raise ValueError(
                "identity dimension {} unallowed for model "
                "constrained to dimension {}".format(dim, expected))

    def estimate(self, src, dst, return_params=True, **kwargs):
        p = self.fit(src, dst, **kwargs)
        self.params = self.normalize_homogeneous_matrix(p)
        if return_params:
            return p

    @classmethod
    def from_estimate(cls, src, dst, **kwargs):
        p = cls.fit(src, dst, **kwargs)
        return cls(matrix=p)

    @property
    def M(self):
        """matrix property defined by fit parameters"""
        return numpy.concatenate((self.params, [numpy.pad(
            numpy.array([1]), (self.params.shape[1]-1, 0), 'constant')]))

    def concatenate(self, model):
        # new_M = numpy.dot(self.M, model.M)
        # new_M = numpy.dot(model.M, self.M)
        # print self.M
        # print model.M
        new_M = numpy.dot(self.M, model.M)
        # print new_M
        # new_M[:-1, -1]
        return AffineModel(matrix=new_M)  # FIXME better class handling

    def invert(self):
        inv_M = numpy.linalg.inv(self.M)
        return self.__class__(matrix=inv_M)  # TODO init class w/ matrix


class AffineModel(AbstractAffineModel):
    @classmethod
    def fit(cls, src, dst):
        """Affine model fitting for arbitrary dimensionality"""
        cls.check_fit_input(src, dst)

        num, dim = src.shape

        M0 = numpy.eye(dim + 1)
        M1 = numpy.eye(dim + 1)

        # FIXME make shaping better
        src_t = src.T
        M0[:dim, dim] = src_t_nmu = -src_t.mean(axis=1)
        src_t_cld = src_t + src_t_nmu.reshape(dim, 1)

        # FIXME make shaping better
        dst_t = dst.T
        M1[:dim, dim] = dst_t_nmu = -dst_t.mean(axis=1)
        dst_t_cld = dst_t + dst_t_nmu.reshape(dim, 1)

        A = numpy.concatenate((src_t_cld, dst_t_cld), axis=0)

        U, S, V = svd(A.T)
        vh = V[:dim].T
        B = vh[:dim]
        C = vh[dim:2*dim]
        t = numpy.concatenate(
            (numpy.dot(C, numpy.linalg.pinv(B)), numpy.zeros((dim, 1))),
            axis=1)
        M = numpy.vstack((t, ((0.0, ) * dim) + (1.0, )))
        M = numpy.dot(numpy.linalg.inv(M1), numpy.dot(M, M0))
        M /= M[dim, dim]
        return numpy.dot(numpy.dot(M1, M0), M)


class AffineModel2D(AffineModel, RestrictedDimensionalityModel):
    dimension = 2

    @classmethod
    def check_fit_input(cls, src, dst, **kwargs):
        super(AffineModel2D, cls).check_fit_input(src, dst, **kwargs)

    @classmethod
    def forrest_fit_2d(cls, A, B):
        cls.check_fit_input(A, B)
        if not all([A.shape[0] == B.shape[0], A.shape[1] == B.shape[1] == 2]):
            raise EstimationError(
                'shape mismatch! A shape: {}, B shape {}'.format(
                    A.shape, B.shape))

        N = A.shape[0]  # total points

        M = numpy.zeros((2 * N, 6))
        Y = numpy.zeros((2 * N, 1))
        for i in range(N):
            M[2 * i, :] = [A[i, 0], A[i, 1], 0, 0, 1, 0]
            M[2 * i + 1, :] = [0, 0, A[i, 0], A[i, 1], 0, 1]
            Y[2 * i] = B[i, 0]
            Y[2 * i + 1] = B[i, 1]

        (Tvec, residuals, rank, s) = numpy.linalg.lstsq(M, Y)
        return Tvec

    @property
    def scale(self):
        """tuple of scale for x, y"""
        return tuple([numpy.sqrt(sum([i ** 2 for i in self.M[:, j]]))
                      for j in range(self.M.shape[1])])[:2]

    @property
    def shear(self):
        """counter-clockwise shear angle"""
        return numpy.arctan2(-self.M[0, 1], self.M[1, 1]) - self.rotation

    @property
    def translation(self):
        """tuple of translation in x, y"""
        return tuple(self.M[:2, 2])

    @property
    def rotation(self):
        """counter-clockwise rotation"""
        return numpy.arctan2(self.M[1, 0], self.M[0, 0])


class AffineModel3D(AffineModel, RestrictedDimensionalityModel):
    dimension = 3

    @classmethod
    def check_fit_input(cls, src, dst, **kwargs):
        super(AffineModel3D, cls).check_fit_input(src, dst, **kwargs)

    @classmethod
    def forrest_fit_3d(cls, A, B):
        cls.check_fit_input(A, B)
        if not all([A.shape[0] == B.shape[0], A.shape[1] == B.shape[1] == 3]):
            raise EstimationError(
                'shape mismatch! A shape: {}, B shape {}'.format(
                    A.shape, B.shape))

        N = A.shape[0]  # total points

        M = numpy.zeros((3 * N, 12))
        Y = numpy.zeros((3 * N, 1))
        for i in range(N):
            M[3 * i, :] = [
                A[i, 0], A[i, 1], A[i, 2],
                0,       0,       0,
                0,       0,       0,
                1,       0,       0]
            M[3 * i + 1, :] = [
                0,       0,       0,
                A[i, 0], A[i, 1], A[i, 2],
                0,       0,       0,
                0,       1,       0]
            M[3 * i + 2, :] = [
                0,       0,       0,
                0,       0,       0,
                A[i, 0], A[i, 1], A[i, 2],
                0,       0,       1]
            Y[3 * i] = B[i, 0]
            Y[3 * i + 1] = B[i, 1]
            Y[3 * i + 2] = B[i, 2]

        (Tvec, residuals, rank, s) = numpy.linalg.lstsq(M, Y)
        logger.debug("residuals: {}, rank: {}".format(residuals, rank))

        M = numpy.zeros((4, 4))
        M[0:3, 0:3] = numpy.reshape(Tvec[0:9], (3, 3))
        M[0:3, 3] = Tvec[9:, 0]
        M[3, 3] = 1
        return M


class SimilarityModel(AbstractAffineModel):
    @classmethod
    def fit(cls, src, dst, rigid=False):
        """umeyama fitting for nd similarity"""
        cls.check_fit_input(src, dst)

        num, dim = src.shape
        src_cld = src - src.mean(axis=0)
        dst_cld = dst - dst.mean(axis=0)
        A = numpy.dot(dst_cld.T, src_cld) / num
        d = numpy.ones((dim, ), dtype=numpy.double)
        if numpy.linalg.det(A) < 0:
            d[dim - 1] = -1
        T = numpy.eye(dim + 1, dtype=numpy.double)

        rank = numpy.linalg.matrix_rank(A)
        if rank == 0:
            raise EstimationError('zero rank matrix A unacceptable -- '
                                  'likely poorly conditioned')

        U, S, V = svd(A)

        if rank == dim - 1:
            if numpy.linalg.det(U) * numpy.linalg.det(V) > 0:
                T[:dim, :dim] = numpy.dot(U, V)
            else:
                s = d[dim - 1]
                d[dim - 1] = -1
                T[:dim, :dim] = numpy.dot(U, numpy.dot(numpy.diag(d), V))
                d[dim - 1] = s
        else:
            T[:dim, :dim] = numpy.dot(U, numpy.dot(numpy.diag(d), V.T))

        fit_scale = (1.0 if rigid else
                     1.0 / src_cld.var(axis=0).sum() * numpy.dot(S, d))

        T[:dim, dim] = dst.mean(axis=0) - fit_scale * numpy.dot(
            T[:dim, :dim], src.mean(axis=0).T)
        T[:dim, :dim] *= fit_scale
        return T


class SimilarityModel2D(SimilarityModel, RestrictedDimensionalityModel):
    dimension = 2

    @classmethod
    def check_fit_input(cls, src, dst, **kwargs):
        super(SimilarityModel2D, cls).check_fit_input(src, dst, **kwargs)


class SimilarityModel3D(SimilarityModel, RestrictedDimensionalityModel):
    dimension = 3

    @classmethod
    def check_fit_input(cls, src, dst, **kwargs):
        super(SimilarityModel3D, cls).check_fit_input(src, dst, **kwargs)


class TranslationModel(AbstractAffineModel):
    @classmethod
    def fit(cls, src, dst):
        cls.check_fit_input(src, dst)
        num, dim = src.shape
        disps = (dst - src).mean(axis=0)
        T = numpy.eye(dim + 1)
        T[:-1, -1] = disps
        return T


class TranslationModel2D(TranslationModel, RestrictedDimensionalityModel):
    dimension = 2

    @classmethod
    def check_fit_input(cls, src, dst, **kwargs):
        super(TranslationModel2D, cls).check_fit_input(src, dst, **kwargs)


class TranslationModel3D(TranslationModel, RestrictedDimensionalityModel):
    dimension = 3

    @classmethod
    def check_fit_input(cls, src, dst, **kwargs):
        super(TranslationModel3D, cls).check_fit_input(src, dst, **kwargs)
