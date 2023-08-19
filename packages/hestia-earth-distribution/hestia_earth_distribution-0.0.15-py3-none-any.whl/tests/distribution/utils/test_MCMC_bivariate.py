from unittest.mock import patch
import os
import pandas as pd
from tests.utils import fixtures_path

from hestia_earth.distribution.utils.MCMC_bivariate import calculate_fit_2d
from hestia_earth.distribution.utils.cycle import (
    YIELD_COLUMN, FERTILISER_COLUMNS, PESTICIDE_COLUMN, IRRIGATION_COLUMN
)

class_path = 'hestia_earth.distribution.utils.MCMC_bivariate'


def fake_generate_likl_file(folder: str):
    def run(country_id, product_id, *args):
        likl_file = os.path.join(fixtures_path, folder, 'likelihood_files', f"{'_'.join([country_id, product_id])}.csv")
        return pd.read_csv(likl_file, na_values='-') if os.path.exists(likl_file) else pd.DataFrame()
    return run


@patch(f"{class_path}.generate_likl_file", side_effect=fake_generate_likl_file('utils'))
def test_calculate_fit_2d_yield_vs_n(*args):
    likelihood_a, *args = calculate_fit_2d([150, 3500], 'GADM-GBR', 'wheatGrain')
    likelihood_b, *args = calculate_fit_2d([150, 8500], 'GADM-GBR', 'wheatGrain')
    assert likelihood_a < 0.05
    assert likelihood_b > 0.9


@patch(f"{class_path}.generate_likl_file", side_effect=fake_generate_likl_file('utils'))
def test_calculate_fit_2d_yield_vs_p2o5(*args):
    likelihood_c, *args = calculate_fit_2d([80, 2500], 'GADM-GBR', 'wheatGrain',
                                           columns=[FERTILISER_COLUMNS[1], YIELD_COLUMN])
    likelihood_d, *args = calculate_fit_2d([5, 8500], 'GADM-GBR', 'wheatGrain',
                                           columns=[FERTILISER_COLUMNS[1], YIELD_COLUMN])
    assert likelihood_c < 0.05
    assert likelihood_d > 0.9


@patch(f"{class_path}.generate_likl_file", side_effect=fake_generate_likl_file('utils'))
def test_calculate_fit_2d_yield_vs_k2o(*args):
    likelihood_a, *args = calculate_fit_2d([80, 2500], 'GADM-CHN', 'wheatGrain',
                                           columns=[FERTILISER_COLUMNS[2], YIELD_COLUMN])
    likelihood_b, *args = calculate_fit_2d([20, 8500], 'GADM-GBR', 'wheatGrain',
                                           columns=[FERTILISER_COLUMNS[2], YIELD_COLUMN])
    assert likelihood_a is None
    assert likelihood_b > 0.9


@patch(f"{class_path}.generate_likl_file", side_effect=fake_generate_likl_file('utils'))
def test_calculate_fit_2d_yield_vs_pest(*args):
    likelihood_a, *args = calculate_fit_2d([10, 2500], 'GADM-GBR', 'wheatGrain',
                                           columns=[PESTICIDE_COLUMN, YIELD_COLUMN])
    likelihood_b, *args = calculate_fit_2d([0.5, 8500], 'GADM-GBR', 'wheatGrain',
                                           columns=[PESTICIDE_COLUMN, YIELD_COLUMN])
    assert likelihood_a < 0.05
    assert likelihood_b > 0.9


@patch(f"{class_path}.generate_likl_file", side_effect=fake_generate_likl_file('utils'))
def test_calculate_fit_2d_yield_vs_water(*args):
    likelihood_a, *args = calculate_fit_2d([10, 2500], 'GADM-GBR', 'wheatGrain',
                                           columns=[IRRIGATION_COLUMN, YIELD_COLUMN])
    likelihood_b, *args = calculate_fit_2d([0.1, 8500], 'GADM-GBR', 'wheatGrain',
                                           columns=[IRRIGATION_COLUMN, YIELD_COLUMN])
    assert likelihood_a < 0.05
    assert likelihood_b > 0.9
