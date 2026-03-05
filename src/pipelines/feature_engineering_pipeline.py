from sklearn.base import BaseEstimator, TransformerMixin


class BalanceErrorFeatureGenerator(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()

        X["errorBalanceOrig"] = (
            X["oldbalanceOrg"] - X["amount"] - X["newbalanceOrig"]
        )

        X["errorBalanceDest"] = (
            X["oldbalanceDest"] + X["amount"] - X["newbalanceDest"]
        )

        return X