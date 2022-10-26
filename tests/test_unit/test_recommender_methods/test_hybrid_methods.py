import logging
from datetime import datetime, timezone, timedelta
from unittest import TestCase

import pandas as pd
import pytest


# RUN WITH: python -m pytest tests/test_unit/test_hybrid_methods.py
from src.recommender_core.data_handling.data_manipulation import DatabaseMethods, get_redis_connection
from src.recommender_core.recommender_algorithms.hybrid_algorithms.hybrid_methods import select_list_of_posts_for_user, \
    get_most_similar_by_hybrid, boost_by_article_freshness, HybridConstants
from src.recommender_core.recommender_algorithms.user_based_algorithms.user_relevance_classifier.classifier import \
    Classifier, get_df_predicted
from tests.testing_methods.random_posts_generator import get_three_unique_posts

classifier = Classifier()


def test_get_df_predicted():
    test_dict = {'col_1': ['test_1', 'test_2'], 'col2': ['test_3', 'test_4'], 'col_3': ['test_5', 'test_6']}
    df = pd.DataFrame(test_dict)
    target_variable_name = 'col2'
    df_predicted = get_df_predicted(df, target_variable_name='col2')
    assert target_variable_name in df_predicted.columns


def test_select_list_of_posts_for_user():
    test_user_id = 431
    searched_slug_1, searched_slug_2, searched_slug_3 = get_three_unique_posts()

    test_slugs = [searched_slug_1, searched_slug_2, searched_slug_3]
    list_of_slugs, list_of_slugs_from_history = select_list_of_posts_for_user(test_user_id, test_slugs)

    assert(type(list_of_slugs) is list)
    assert(len(list_of_slugs) > 0)
    assert(type(list_of_slugs_from_history) is list)
    assert(len(list_of_slugs_from_history) > 0)


@pytest.fixture()
def test_user_id():
    test_user_id = 999999
    return test_user_id


@pytest.fixture()
def bad_list_of_methods():
    list_of_methods = ["bs", "methods"]
    return list_of_methods


# Bad Day:
def test_get_most_similar_by_hybrid(test_user_id, bad_list_of_methods):
    with pytest.raises(NotImplementedError) as nie:
        print("test_user_id:")
        print(test_user_id)
        print("bad_list_of_methods")
        print(bad_list_of_methods)
        get_most_similar_by_hybrid(user_id=test_user_id, svd_posts_to_compare=None, list_of_methods=bad_list_of_methods)
        assert str(nie) == "Inserted methods must correspond to DB columns."


# Super Bad Day:
@pytest.mark.parametrize("tested_input", [
    '',
    (),
    None,
    'ratings'
])
def test_get_most_similar_by_hybrid_bad_user(tested_input):
    with pytest.raises(TypeError):
        get_most_similar_by_hybrid(user_id=tested_input, list_of_methods=bad_list_of_methods)

@pytest.mark.parametrize("tested_input", [
    '',
    (),
    'ratings'
])
def test_svm_classifier_bad_sample_number(tested_input):
    with pytest.raises(ValueError):
        svm = Classifier()
        assert svm.predict_relevance_for_user(use_only_sample_of=tested_input, user_id=431, relevance_by='stars')
