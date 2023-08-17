"""Example test Case using pytest https://docs.pytest.org/en/7.4.x/index.html"""
import os
import src.integration_wetsuits as wetsuits

class TestEDI:
    """Example test class to cluster tests"""
    message = os.getenv('EDI_TEST_MESSAGE')

    def test_parse_all(self):
        """Assert that all possible edi tags in message are parsed"""
        wetsuits.Edi(self.message).parse_all()

    def test_parse_specific(self):
        """Assert that specified headers and lines are returned"""
        requested_headers = ["deliveryaddressID"]
        requested_lines = ["currency"]
        wetsuits.Edi(self.message).parse_specific(
            requested_headers, requested_lines)
