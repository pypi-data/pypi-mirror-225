import numpy as np
from sklearn.cross_decomposition import CCA
from scipy.linalg import null_space
from scipy.stats import pearsonr
from permcca.permute import PermutationMultiVar
import pingouin as pg


def can_corr(X_c, Y_c):
    return np.array([pearsonr(X_c[:, i], Y_c[:, i])[0] for i in range(X_c.shape[1])])


def _wilk_statistic(can_corr: np.ndarray):
    return -np.flip(np.cumsum(np.flip(np.log(1 - can_corr**2))))[0]


def _calc_cum_rs(X_c, Y_c, n_comps):
    latent_cum_rs = []
    for k in range(n_comps):
        cca = CCA(n_components=n_comps - k, scale=False)
        tmp_x, tmp_y = cca.fit_transform(X_c[:, k:], Y_c[:, k:])
        permed_rs = can_corr(tmp_x, tmp_y)
        cum_r = _wilk_statistic(permed_rs)
        latent_cum_rs.append(cum_r)

    return np.array(latent_cum_rs)


def permutation_inference(X, Y, n_comps=None, n_perms=1000, fwe_correction=True):
    # TODO: add support for passing model
    # TODO: add support for passing n_jobs
    if X.shape[0] != Y.shape[0]:
        raise ValueError("Y and X do not have same number of rows.")
    if n_comps is None:
        n_comps = min(X.shape[1], Y.shape[1])
    cca = CCA(n_components=n_comps, scale=False)
    cca.fit_transform(X, Y)
    X_c = X @ np.hstack((cca.x_weights_, null_space(cca.x_weights_.T)))
    Y_c = Y @ np.hstack((cca.y_weights_, null_space(cca.y_weights_.T)))
    cnt = np.zeros(n_comps)
    # For each permutation
    seeds = np.random.randint(0, 10000, size=n_perms)
    latent_cum_rs = _calc_cum_rs(X_c, Y_c, n_comps)
    for perm in range(0, n_perms):
        perm_X_c, perm_Y_c = PermutationMultiVar(
            random_state=seeds[perm], shuffle_target=True, selection=None
        ).fit_transform(X_c, Y_c)
        permuted_latent_cum_rs = _calc_cum_rs(perm_X_c, perm_Y_c, n_comps)
        cnt += (permuted_latent_cum_rs >= latent_cum_rs).astype(int)

    # Compute p-values
    punc = np.minimum(cnt / n_perms, 1)
    if fwe_correction:
        p_fwe = pg.multicomp(punc, method="fdr_bh")[1]
        return p_fwe
    else:
        return punc


"""
from concurrent.futures import ThreadPoolExecutor

def permute_and_calc_cum_rs(seed, X_c, Y_c, n_comps):
    perm_X_c, perm_Y_c = PermutationMultiVar(
        random_state=seed, shuffle_target=True, selection=None
    ).fit_transform(X_c, Y_c)
    return _calc_cum_rs(perm_X_c, perm_Y_c, n_comps)

def permutation_inference(X, Y, n_comps=None, n_perms=1000, n_threads=4):
    if X.shape[0] != Y.shape[0]:
        raise ValueError("Y and X do not have same number of rows.")
    if n_comps is None:
        n_comps = min(X.shape[1], Y.shape[1])
    cca = CCA(n_components=n_comps, scale=False)
    cca.fit_transform(X, Y)
    X_c = X @ np.hstack((cca.x_weights_, null_space(cca.x_weights_.T)))
    Y_c = Y @ np.hstack((cca.y_weights_, null_space(cca.y_weights_.T)))
    cnt = np.zeros(n_comps)
    seeds = np.random.randint(0, 10000, size=n_perms)
    latent_cum_rs = _calc_cum_rs(X_c, Y_c, n_comps)
    print(latent_cum_rs)

    with ThreadPoolExecutor(max_workers=n_threads) as executor:
        results = list(executor.map(permute_and_calc_cum_rs, seeds, [X_c]*n_perms, [Y_c]*n_perms, [n_comps]*n_perms))
    
    for permuted_latent_cum_rs in results:
        cnt += (permuted_latent_cum_rs >= latent_cum_rs).astype(int)

    punc = np.minimum(cnt / n_perms, 1)
    return punc
    """
