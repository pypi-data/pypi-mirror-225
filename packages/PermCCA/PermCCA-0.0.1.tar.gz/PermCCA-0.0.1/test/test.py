# @title new perm cca

import numpy as np
from permcca.inference import permutation_inference
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold
from sklearn.pipeline import Pipeline

X = np.load("../assets/X.npy")
Y = np.load("../assets/Y.npy")

x_preproc = Pipeline(
    [
        ("scale", StandardScaler(with_mean=True, with_std=False)),
        ("var", VarianceThreshold(threshold=0.0)),
        # ("pca", PCA(n_components=10)),
    ]
).fit_transform(X)

y_preproc = Pipeline(
    [
        ("scale", StandardScaler(with_mean=True, with_std=False)),
        ("var", VarianceThreshold(threshold=0.0)),
        # ("pca", PCA(n_components=10)),
    ]
).fit_transform(Y)

for i in range(5, 11):
    p = permutation_inference(x_preproc, y_preproc, i)
    print(p)
