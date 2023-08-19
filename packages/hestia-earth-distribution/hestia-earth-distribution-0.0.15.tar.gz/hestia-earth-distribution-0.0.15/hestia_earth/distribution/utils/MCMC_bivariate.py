import numpy as np
import scipy.stats as st

from hestia_earth.distribution.likelihood import generate_likl_file
from .cycle import YIELD_COLUMN, FERTILISER_COLUMNS


def _compute_MC_likelihood(candidate: list, kernel):
    iso = kernel(candidate)
    sample = kernel.resample(size=10000)
    insample = kernel(sample) < iso
    integral = insample.sum() / float(insample.shape[0])
    return integral


def _get_df_bounds(df, columns):
    df = df[columns].dropna(axis=0, how='any')
    m1, m2 = df[columns[0]].to_list(), df[columns[1]].to_list()
    return (
        m1, m2, min(m1), max(m1), min(m2), max(m2)
    ) if len(m1) > 0 else (
        [], [], None, None, None, None
    )


def _fit_user_data_2d(candidate, df, columns=list, return_z: bool = False):
    m1, m2, xmin, xmax, ymin, ymax = _get_df_bounds(df, columns)
    plottable = xmin != xmax and ymin != ymax and m1 != [] and m2 != []

    values = np.vstack([m1, m2])
    likelihood = _compute_MC_likelihood(candidate, st.gaussian_kde(values)) if plottable else None

    def calculate_Z():
        X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
        positions = np.vstack([X.ravel(), Y.ravel()])

        kernel = st.gaussian_kde(values)
        Z = np.reshape(kernel(positions).T, X.shape)
        return Z / Z.sum()

    return likelihood, calculate_Z() if return_z and plottable else [[xmin, xmax], [ymin, ymax]]


def calculate_fit_2d(candidate: list, country_id: str, product_id: str,
                     columns=[FERTILISER_COLUMNS[0], YIELD_COLUMN],
                     return_z: bool = False):
    """
    Return the likelihood of a combination of candidate values using bivariate distribution.
    The returned probability approximates how reasonable the candidate is by using Monte Carlo integration.
    Any returned probability above 5% should be acceptable.

    Parameters
    ----------
    candidate: list
        List of values to be tested following the order of 'columns', e.g. [250, 8500] by default
        meaning the Nitrogen use is 250 and yield is 8500.
    country_id: str
        Region `@id` from Hestia glossary, e.g. 'GADM-GBR'.
    product_id: str
        Product term `@id` from Hestia glossary, e.g. 'wheatGrain'.
    columns: list
        List of column names in the likelihood csv file, by defualt:
        'Nitrogen (kg N)' and 'Grain yield (kg/ha)'
    return_z: bool
        Whether to calculate Z for plotting. Defaults to `False`.

    Returns
    -------
    likelihood: float
        The probability of how likely the candidate is reasonable, or an
        approximation of what percentage of samples the candidate stands above
    """
    df = generate_likl_file(country_id, product_id)
    return _fit_user_data_2d(candidate, df, columns, return_z=return_z)
