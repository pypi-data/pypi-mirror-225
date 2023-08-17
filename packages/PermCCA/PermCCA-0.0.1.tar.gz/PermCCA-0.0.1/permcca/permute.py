import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_array

"""
The way of permutation in CCA analysis is shuffling the identity matrix.
This can be simplified to just shuffling the ids (or indexes) of one feature set, it is the same.
"""


class Permutation(BaseEstimator, TransformerMixin):
    # Shuffling the ids of one feature set

    def __init__(self, random_state=42, shuffle_target=False):
        if isinstance(random_state, (int, np.integer)):
            self.random_state = random_state
        else:
            raise ValueError("random_state must be an integer or None.")
        self.shuffle_target = shuffle_target
        self.perm_ids_x = None
        self.perm_ids_y = None

    def permute(self, ids_len):
        rng = np.random.default_rng(self.random_state)
        self.perm_ids_x = rng.permutation(ids_len)
        if self.shuffle_target:
            self.perm_ids_y = rng.permutation(ids_len)

    def fit(self, x: np.ndarray, y: np.ndarray or None = None):
        self.permute(x.shape[0])
        return self

    def transform(self, x, y=None):
        if y is not None:
            check_array(y)
            if self.shuffle_target:
                return x[self.perm_ids_x, :], y[self.perm_ids_y, :]
            return x[self.perm_ids_x, :], y
        return x[self.perm_ids_x, :]

    def fit_transform(self, X, y=None, **fit_params):
        return self.fit(X, y).transform(X, y)


class PermutationMultiVar(Permutation):
    def __init__(self, random_state=42, shuffle_target=False, selection=None):
        super().__init__(random_state=random_state, shuffle_target=shuffle_target)
        if isinstance(selection, (list, np.ndarray)) or selection is None:
            self.selection = selection
        else:
            raise ValueError("selection must be a list, np.ndarray or None.")

    def _select_rows(self, x):
        # avoid the structured dependency already exists in the data, for example, the family cohort
        if self.selection is None:
            return x
        elif isinstance(self.selection, list):
            # check dimension
            if x.shape[0] != len(self.selection):
                raise ValueError(
                    "The number of rows in x must be equal to the length of selection."
                )
            else:
                return x[self.selection, :]
        elif isinstance(self.selection, np.ndarray):
            # if the selection is a 1d array, it is the same as a list
            if self.selection.ndim == 1:
                if x.shape[0] != len(self.selection):
                    raise ValueError(
                        "The number of rows in x must be equal to the length of selection."
                    )
                else:
                    return x[self.selection, :]
            elif self.selection.ndim == 2:
                if x.shape[0] != self.selection.shape[1]:
                    raise ValueError(
                        "The number of cols in x must be equal to the number of cols in selection."
                    )
                else:
                    return self.selection @ x

    def fit(self, x: np.ndarray, y: np.ndarray = None):
        selected = self._select_rows(x)
        self.permute(selected.shape[0])
        return self

    def transform(self, x, y=None):
        selected_x = self._select_rows(x)
        if y is not None:
            check_array(y)
            selected_y = self._select_rows(y)
            if self.shuffle_target:
                return selected_x[self.perm_ids_x, :], selected_y[self.perm_ids_y, :]
            return selected_x[self.perm_ids_x, :], selected_y
        return selected_x[self.perm_ids_x, :]
