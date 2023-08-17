""" GlmnetClassifier tests

===============================================================
Author: Rolf Carlson, Carlson Research, LLC <hrolfrc@gmail.com>
License: 3-clause BSD
===============================================================

"""
import pytest
from sklearn.datasets import load_iris

from glmnet_classifier import GlmnetClassifier


@pytest.fixture
def data():
    return load_iris(return_X_y=True)


def test_GlmnetClassifier(data):
    X, y = data
    clf = GlmnetClassifier()

    clf.fit(X, y)
    assert hasattr(clf, 'classes_')
    assert hasattr(clf, 'X_')
    assert hasattr(clf, 'y_')

    y_pred = clf.predict(X)
    assert y_pred.shape == (X.shape[0],)
