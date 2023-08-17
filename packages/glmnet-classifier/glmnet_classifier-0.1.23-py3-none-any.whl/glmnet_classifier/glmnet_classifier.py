"""
The GlmnetClassifier

===============================================================
Author: Rolf Carlson, Carlson Research, LLC <hrolfrc@gmail.com>
License: 3-clause BSD
===============================================================

"""
import time

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.multiclass import unique_labels
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted

from glmnet_python import cvglmnet
from glmnet_python import cvglmnetCoef
from glmnet_python import cvglmnetPredict


# noinspection PyAttributeOutsideInit
class GlmnetClassifier(ClassifierMixin, BaseEstimator):
    """ The GlmnetClassifier

    Attributes
    ----------
        coef_ : array of shape (n_features, )
            Estimated coefficients for the linear fit problem.  Only
            one target should be passed, and this is a 1D array of length
            n_features.

        n_features_in_ : int
            Number of features seen during :term:`fit`.

        classes_ : list
            The unique class labels

        fit_time_ : float
            The number of seconds to fit X to y

    Examples
    --------
        >>> import numpy
        >>> from sklearn.datasets import make_classification as mc
        >>> X, y = mc(n_features=2, n_redundant=0, n_informative=2, n_clusters_per_class=1, random_state=42)
        >>> numpy.round(X[0:3, :], 2)
        array([[ 1.23, -0.76],
               [ 0.7 , -1.38],
               [ 2.55,  2.5 ]])

        >>> y[0:3]
        array([0, 0, 1])

        >>> cls = GlmnetClassifier().fit(X, y)
        >>> cls.score(X, y)
        0.95

        >>> np.round(cls.coef_, 4)
        array([-0.2463,  1.    ])

        >>> numpy.round(cls.score(X, y), 2)
        0.95

        >>> cls.fit_time_ > 0
        True

        >>> cls.predict(np.array([[3, 5]]))
        array([0])

        >>> cls.predict_proba(np.array([[3, 5]]))
        array([[1., 0.]])

        """

    def __init__(self, alpha=0):
        """ Initialize GlmnetClassifier """
        self.alpha = alpha  # alpha == 1 is Lasso, alpha == 0 is Ridge

    def fit(self, X, y):
        """ Fit the model according to the given training data.

        Parameters
        ----------
            X : {array-like, sparse matrix} of shape (n_samples, n_features)
                Training vector, where n_samples is the number of samples and n_features is the number of features.

            y : array-like of shape (n_samples,)
                Target vector relative to X.

        Returns
        -------
            self
                Fitted estimator.

        """
        if y is None:
            raise ValueError('requires y to be passed, but the target y is None')

        X, y = check_X_y(X, y)
        self.n_features_in_ = X.shape[1]
        self.classes_ = unique_labels(y)
        self.X_ = np.asarray(X, dtype='float64')
        self.y_ = np.asarray(y, dtype='float64')

        # given the task is classification, it would seem that
        # using the recommended family = 'binomial', ptype = 'class'
        # would be best, however, using family = 'gaussian', ptype = 'mse'
        # improves score and appears to run faster.
        start = time.time()

        self.cvfit_ = cvglmnet(
            x=self.X_.copy(),
            y=self.y_.copy(),
            alpha=self.alpha,
            family='gaussian',
            ptype='mse',
            nlambda=100,
            parallel=True
        )

        self.fit_time_ = time.time() - start
        self.coef_ = cvglmnetCoef(self.cvfit_, s='lambda_min')
        self.is_fitted_ = True
        return self

    def decision_function(self, X):
        """ Identify confidence scores for the samples

        Parameters
        ----------
            X : array-like, shape (n_samples, n_features)
                The training input features and samples

        Returns
        -------
            y_d : the decision vector (n_samples)

        """
        check_is_fitted(self, ['is_fitted_', 'X_', 'y_'])
        X = self._validate_data(X, accept_sparse="csr", reset=False)
        return cvglmnetPredict(self.cvfit_, newx=X, s='lambda_1se', ptype='response').ravel()

    def predict(self, X):
        """Predict class labels for samples in X.

        Parameters
        ----------
            X : {array-like, sparse matrix} of shape (n_samples, n_features)
                The data matrix for which we want to get the predictions.

        Returns
        -------
            y_pred : ndarray of shape (n_samples,)
                Vector containing the class labels for each sample.

        """
        if len(self.classes_) < 2:
            y_class = self.y_
        else:
            check_is_fitted(self, ['is_fitted_', 'X_', 'y_'])
            X = check_array(X)
            y_class = cvglmnetPredict(self.cvfit_, newx=X, s='lambda_1se', ptype='class').ravel()
            y_class = list(np.round(y_class).astype(int))
        return y_class

    def predict_proba(self, X):
        """Probability estimates for samples in X.

        Parameters
        ----------
            X : array-like of shape (n_samples, n_features)
                Vector to be scored, where n_samples is the number of samples and
                n_features is the number of features.

        Returns
        -------
            T : array-like of shape (n_samples, n_classes)
                Returns the probability of the sample for each class in the model,
                where classes are ordered as they are in `self.classes_`.

        """
        check_is_fitted(self, ['is_fitted_', 'X_', 'y_'])
        X = check_array(X)
        y_proba = self.decision_function(X)
        class_prob = np.column_stack((1 - y_proba, y_proba))
        return np.asarray(class_prob)

    def _more_tags(self):
        return {
            'poor_score': True,
            'non_deterministic': True,
            'binary_only': True
        }
