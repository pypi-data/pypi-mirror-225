from .deepl import (
    fetch_deepl,
    deepl_fetch_api,
    deepl_fetch_checker
)
from .krdict import (
    fetch_krdict,
    krdict_fetch_api,
    krdict_fetch_scraper,
    krdict_fetch_checker,
    krdict_results_body,
    krdict_results_pronunciation,
    krdict_results_origin,
    krdict_results_parts_of_speech,
    krdict_results_word_grade,
    krdict_results_definition,
)

__all__ = [
    'fetch_deepl',
    'deepl_fetch_api',
    'deepl_fetch_checker',
    'fetch_krdict',
    'krdict_fetch_api',
    'krdict_fetch_scraper',
    'krdict_fetch_checker',
    'krdict_results_body',
    'krdict_results_pronunciation',
    'krdict_results_origin',
    'krdict_results_parts_of_speech',
    'krdict_results_word_grade',
    'krdict_results_definition',
]
