"""Example test Case using pytest https://docs.pytest.org/en/7.4.x/index.html"""
import os
import src.integration_wetsuits as wetsuits

class TestItsp:
    """Example test class to cluster tests"""
    url = os.getenv('ITSP_TEST_URL')
    token = os.getenv('ITSP_TEST_TOKEN')
    version = "v2"
    timeout = 2

    itspTest = wetsuits.Itsperfect(url, token, version, timeout)

    def test_fetch_all(self):
        """Assert that return is value is correct. Expected value = 20"""
        endpoint_id = "purchaseorders"
        total_data = len(self.itspTest.fetch_all(
            endpoint_id=endpoint_id, batch_size=10, page_limit=2))
        assert total_data == 20

    def test_fetch_all_with_filter(self):
        """Assert that return is value is correct. Expected value = 12"""
        endpoint_id = "agents"
        total_data = len(self.itspTest.fetch_all(
            endpoint_id=endpoint_id, batch_size=20, filters="active eq 1"))
        assert total_data == 12

    def test_fetch_one(self):
        """Assert that return is value is correct. Expected value > 0"""
        endpoint_id = "customer_brands"
        total_data = len(self.itspTest.fetch_one(
            endpoint_id=endpoint_id, item_id=100))
        assert total_data > 0
