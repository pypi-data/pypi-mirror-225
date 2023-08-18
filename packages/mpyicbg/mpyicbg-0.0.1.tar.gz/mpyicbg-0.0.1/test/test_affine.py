#!/usr/bin/env python
import numpy
import pytest

from mpyicbg.transformations import (
    AffineModel, AffineModel2D, AffineModel3D,
    SimilarityModel, SimilarityModel2D, SimilarityModel3D)
from mpyicbg.errors import MPYICBGError


def cross_py23_reload(module):
    try:
        reload(module)
    except NameError:
        import importlib
        importlib.reload(module)


def random_affine(dim, model=AffineModel,
                  do_scale=True, do_translate=True, do_rotate=True,
                  do_shear=True):
    # TODO allow keywork args for scale, translation, rotation
    def build_scale(dim, scale=1.):
        """TODO make this acceptscale arrays!"""
        return (numpy.eye(dim + 1) * numpy.random.rand())[:dim, :dim+1]

    def build_translate(dim, translations):
        m = numpy.eye(dim+1)
        m[:-1, -1] = translations
        return m

    def build_rotate(dim):
        m = numpy.linalg.qr(
            numpy.random.rand(dim, dim))[0]
        return numpy.fliplr(m) * -1.

    random_scale = (model(matrix=(build_scale(dim, numpy.random.rand())))
                    if do_scale else model(dim=dim))
    random_translate = (model(matrix=build_translate(dim, numpy.random.rand(dim)))
                        if do_translate else model(dim=dim))
    random_rotate = (model(matrix=build_rotate(dim))
                     if do_rotate else model(dim=dim))

    return random_translate.concatenate(
        random_rotate.concatenate(
            random_scale))


# FIXME random_affine is actually random_similarity
def random_similarity(*args, **kwargs):
    return random_affine(*args, **dict(kwargs, **{}))


def random_rigid(*args, **kwargs):
    return random_similarity(*args, **dict(kwargs, **{'do_scale': False}))


def random_translation(*args, **kwargs):
    return random_rigid(*args, **dict(kwargs, **{'do_rotate': False}))


get_transformation = {
    'affine': random_affine,
    'similarity': random_similarity,
    'rigid': random_rigid,
    'translation': random_translation}


@pytest.mark.parametrize("dim", [2, 3])
def test_invert_Affine(dim):
    am = random_affine(dim)
    Iam = am.invert()
    assert am.M.shape == (dim + 1, dim + 1)
    assert Iam.M.shape == am.M.shape
    assert numpy.allclose(Iam.concatenate(am).M, numpy.eye(dim + 1))
    assert numpy.allclose(am.concatenate(Iam).M, numpy.eye(dim + 1))


@pytest.mark.parametrize("dim,model,acceptable,model_type",
                         [(2, AffineModel, True, "affine"),
                          (3, AffineModel, True, "affine"),
                          (2, AffineModel2D, True, "affine"),
                          (3, AffineModel2D, False, "affine"),
                          (2, AffineModel3D, False, "affine"),
                          (3, AffineModel3D, True, "affine"),
                          (2, SimilarityModel, True, "similarity"),
                          (3, SimilarityModel, True, "similarity"),
                          (2, SimilarityModel2D, True, "similarity"),
                          (3, SimilarityModel3D, True, "similarity")])
def test_estimation(dim, model, acceptable, model_type):
    src_pts = numpy.random.rand(50, dim)
    if acceptable:
        tform = get_transformation[model_type](dim, model)
    else:
        with pytest.raises(ValueError):
            tform = get_transformation[model_type](dim, model)
        return

    dst_pts = tform.tform(src_pts)

    new_tform = model(src=src_pts, dst=dst_pts)
    print tform.M
    print new_tform.M
    new_dst = new_tform.tform(src_pts)
    assert numpy.allclose(new_tform.M, tform.M)
    assert numpy.allclose(new_dst, dst_pts)
