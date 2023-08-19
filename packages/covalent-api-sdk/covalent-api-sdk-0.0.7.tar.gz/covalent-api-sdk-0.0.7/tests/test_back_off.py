import pytest
from covalent.services.util.back_off import ExponentialBackoff, MaxRetriesExceededError

class TestBackOff:
    """ back off test class """

    @pytest.fixture
    def client(self):
        """ initialize exponential client """
        return ExponentialBackoff(3)

    def test_remove_field(self, client):
        """ test back off functionality """
        num_back_offs = 1
        try:
            for _ in range(3):
                client.back_off()
                num_back_offs = num_back_offs + 1
        except MaxRetriesExceededError as error:
            assert num_back_offs == 3
            assert str(error) == "Max retries (3) exceeded."
