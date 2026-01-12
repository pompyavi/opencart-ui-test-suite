"""
Test Data Module
================

Test data constants for parameterized tests.
Contains structured data for product and search functionality testing.

Usage:
    from constants.test_data import SEARCH_TESTDATA, PRODUCT_TEST_DATA
    
    @pytest.mark.parametrize('search_term, expected_count', SEARCH_TESTDATA['product_results'])
    def test_search(search_term, expected_count):
        ...
"""

# ============== Product Testing Data ==============

PRODUCT_TEST_DATA = {
    'macbook_products': [
        ('macbook', 'MacBook Pro'),
        ('macbook', 'MacBook Air')
    ],
    'samsung_products': [
        ('samsung', 'Samsung Galaxy Tab 10.1')
    ]
}
"""
Product search and selection test data.

Structure:
    {
        'category': [(search_term, product_name), ...]
    }
    
Usage:
    for search_term, product_name in PRODUCT_TEST_DATA['macbook_products']:
        results = search.search_product(search_term)
        product = results.select_product(product_name)
"""

# ============== Search Testing Data ==============

SEARCH_TESTDATA = {
    'empty_results': [
        ('hello', 0)  # Search term with no results
    ],
    'product_results': [
        ('macbook', 3),  # Search term with 3 results
        ('samsung', 1)   # Search term with 1 result
    ]
}
"""
Search functionality test data.

Structure:
    {
        'category': [(search_term, expected_count), ...]
    }
    
Usage:
    @pytest.mark.parametrize('term, count', SEARCH_TESTDATA['product_results'])
    def test_search_results(term, count):
        results = search.search_product(term)
        assert results.get_search_result_count() == count
"""
