from hestia_earth.utils.api import search, download_hestia
from hestia_earth.utils.tools import non_empty_list
from hestia_earth.schema import CycleFunctionalUnit

from ..log import logger

_FERT_GROUPS = {
    'N': 'inorganicNitrogenFertiliserUnspecifiedKgN',
    'P2O5': 'inorganicPhosphorusFertiliserUnspecifiedKgP2O5',
    'K2O': 'inorganicPotassiumFertiliserUnspecifiedKgK2O'
}

INDEX_COLUMN = 'cycle.id'
YIELD_COLUMN = 'Grain yield (kg/ha)'
FERTILISER_COLUMNS = [
    'Nitrogen (kg N)',
    'Phosphorus (kg P2O5)',
    'Potassium (kg K2O)',
    'Magnesium (kg Mg)'
    # 'Sulphur (kg S)'
]
PESTICIDE_COLUMN = 'pesticideUnspecifiedAi'  # 'Total pesticides (kg active ingredient)'
IRRIGATION_COLUMN = 'waterSourceUnspecified'  # 'Total water inputs (m3 / ha)'


def _get_fert_group_name(fert_id: str): return fert_id.split('Kg')[-1]


def get_fert_group_id(term_id: str):
    """
    Look up the fertiliser group (N, P2O5, K2O) of a Hestia fertliser term.

    Parameters
    ----------
    term_id: str
        Inorganic or organic fertiliser term `@id` from Hestia glossary, e.g. 'ammoniumNitrateKgN'.

    Returns
    -------
    str
        Fertiliser group '@id', e.g. 'inorganicNitrogenFertiliserUnspecifiedKgN'.
    """
    return _FERT_GROUPS.get(_get_fert_group_name(term_id))


def get_fert_ids():
    """
    Get a list of '@id' of the ferttiliser inputs that can be used to get data.
    """
    return list(_FERT_GROUPS.values())


def get_input_ids():
    """
    Get a list of '@id' of the Input that can be used to get data.
    """
    return get_fert_ids() + [PESTICIDE_COLUMN, IRRIGATION_COLUMN]


def find_cycles(country_id: str, product_id: str, limit: int, recalculated: bool = False):
    country_name = download_hestia(country_id).get('name')
    product_name = download_hestia(product_id).get('name')

    cycles = search({
        'bool': {
            'must': [
                {
                    'match': {'@type': 'Cycle'}
                },
                {
                    'nested': {
                        'path': 'products',
                        'query': {
                            'bool': {
                                'must': [
                                    {'match': {'products.term.name.keyword': product_name}},
                                    {'match': {'products.primary': 'true'}}
                                ]
                            }
                        }
                    }
                },
                {
                    'match': {
                        'site.country.name.keyword': country_name
                    }
                },
                {
                    'match': {
                        'functionalUnit': CycleFunctionalUnit._1_HA.value
                    }
                }
            ],
            'must_not': [{'match': {'aggregated': True}}]
        }
    }, limit=limit)
    logger.info(f"Found {len(cycles)} non-aggregated cycles with product '{product_id}' in '{country_name}'.")
    cycles = [download_hestia(c['@id'], 'Cycle', 'recalculated' if recalculated else None) for c in cycles]
    return non_empty_list(cycles)
