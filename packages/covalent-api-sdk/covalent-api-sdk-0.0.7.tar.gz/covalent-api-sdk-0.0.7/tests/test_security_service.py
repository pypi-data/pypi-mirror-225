import pytest
import os
from covalent import Client


class TestSecurityService:
    """ security service testing class """

    @pytest.fixture
    def client(self):
        """ initialize client """
        return Client(os.environ.get('COVALENT_API_KEY'))

    def test_get_approvals_success(self, client: Client):
        """ test for approvals endpoint success """
        get_appr = client.security_service.get_approvals("eth-mainnet", "demo.eth")
        assert get_appr.error is False
        assert get_appr.data.chain_id == 1
        assert get_appr.data.chain_name == "eth-mainnet"
        assert len(get_appr.data.items) > 0

    def test_get_approvals_fail(self, client: Client):
        """ test for approvals endpoint fail """
        fail_appr = client.security_service.get_approvals("eth-mainnet", "demo.ethhh")
        assert fail_appr.error is True