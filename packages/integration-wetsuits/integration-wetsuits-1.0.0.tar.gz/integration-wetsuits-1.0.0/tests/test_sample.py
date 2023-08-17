"""Example test Case using pytest https://docs.pytest.org/en/7.4.x/index.html"""
def plus_one(number: int):
    """function to test"""
    return number + 1

class TestExample:
    """Example test class to cluster tests"""

    def test_answer(self):
        """Assert that return is value is correct. Expected value = 5"""
        assert plus_one(4) == 5

    def test_answer_false(self):
        """Assert that return is false. Expected return is 3"""
        assert plus_one(2) != 5
