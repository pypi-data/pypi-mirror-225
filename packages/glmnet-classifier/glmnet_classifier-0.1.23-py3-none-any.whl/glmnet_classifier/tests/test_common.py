import pytest
from sklearn.utils.estimator_checks import check_estimator

from glmnet_classifier.glmnet_classifier import GlmnetClassifier


@pytest.mark.parametrize(
    "estimator",
    [GlmnetClassifier()]
)
def test_all_estimators(estimator):
    return check_estimator(estimator)
