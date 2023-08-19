import pytest
import os
from datetime import datetime
from covalent import Client


class TestBaseService:
    """ base service testing class """

    @pytest.fixture
    def client(self):
        """ initialize client """
        return Client(os.environ.get('COVALENT_API_KEY'))

    # get block endpoint testing
    def test_get_block_success(self, client: Client):
        """ test for get block endpoint success """
        block = client.base_service.get_block("eth-mainnet", "17679441")
        assert block.error is False
        assert block.data.chain_id == 1
        assert block.data.chain_name == "eth-mainnet"
        assert block.data.items[0].height == 17679441
        assert block.data.items[0].signed_at == datetime.fromisoformat("2023-07-12T19:06:11Z")

    def test_get_block_fail(self, client: Client):
        """ test for get block endpoint fail """
        block_fail = client.base_service.get_block("eth-mainnet", "-1")
        assert block_fail.error is True

    # get resolved address endpoint testing
    def test_get_resolved_address_success(self, client: Client):
        """ test for get resolved address endpoint success """
        res_ens = client.base_service.get_resolved_address("eth-mainnet", "demo.eth")
        assert res_ens.error is False
        assert res_ens.data.items[0].address == "0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de"

        res_rns = client.base_service.get_resolved_address("rsk-mainnet", "dylan.rsk")
        assert res_rns.error is False
        assert res_rns.data.items[0].address == "0x92659ca386f8805f7c480711cee92e0e0eb5406e"

        res_lens = client.base_service.get_resolved_address("eth-mainnet", "@lensprotocol")
        assert res_lens.error is False
        assert res_lens.data.items[0].address == "0x05092cf69bdd435f7ba4b8ef97c9caecf2ba69ad"

        res_unstop_dom = client.base_service.get_resolved_address("eth-mainnet", "jim-unstoppable.x")
        assert res_unstop_dom.error is False
        assert res_unstop_dom.data.items[0].address == "0x57a82545be709963f0182b69f6e9b6f00b977592"

    def test_get_resolved_address_fail(self, client: Client):
        """ test for get resolved address endpoint fail """
        res_fail = client.base_service.get_resolved_address("eth-mainnet", "alice.rsk")
        assert res_fail.error is True

    # get block height endpoint testing
    @pytest.mark.asyncio
    async def test_get_block_height_success(self, client: Client):
        """ test for get block height endpoint success """
        async for res in client.base_service.get_block_heights("eth-mainnet", "2023-01-01", "2023-01-02"):
            assert res is not None

    @pytest.mark.asyncio
    async def test_get_block_height_fail(self, client: Client):
        """ test for get block height endpoint fail """
        async for res in client.base_service.get_block_heights("eth-mainnet", "2023-01-03", "2023-01-02"):
            assert res == "An error occured 400 : Invalid path parameter(s), start_date is after end_date.  start_date: 2023-01-03 end_date: 2023-01-02"
        
    # get logs endpoint testing
    def test_get_logs_success(self, client: Client):
        """ test for get logs endpoint success """
        logs_ = client.base_service.get_logs("eth-mainnet")
        assert logs_.error is False
        assert logs_.data.chain_id == 1
        assert logs_.data.chain_name == "eth-mainnet"
        assert len(logs_.data.items) > 0

    def test_get_logs_fail(self, client: Client):
        """ test for get logs endpoint fail """
        logs_fail = client.base_service.get_logs("eth-mainnet", "-1")
        assert logs_fail.error is True

    # get log events by address endpoint testing
    @pytest.mark.asyncio
    async def test_get_log_events_success(self, client: Client):
        """ test for get log events by address endpoint success """
        async for res in client.base_service.get_log_events_by_address("eth-mainnet", "0xdac17f958d2ee523a2206206994597c13d831ec7", 17679143, "17679148"):
            assert res is not None

    @pytest.mark.asyncio
    async def test_get_log_events_fail(self, client: Client):
        """ test for get log events by address endpoint fail """
        async for res in client.base_service.get_log_events_by_address("eth-mainnet", "0xdac17f958d2ee523a2206206994597c13d831e"):
            assert res == "An error occured 400 : Malformed address provided: 0xdac17f958d2ee523a2206206994597c13d831e"
        
    # get log events by topic hash endpoint testing
    @pytest.mark.asyncio
    async def test_get_log_events_hash_success(self, client: Client):
        """ test for get log events by hash endpoint success """
        async for res in client.base_service.get_log_events_by_topic_hash("eth-mainnet", "0x27f12abfe35860a9a927b465bb3d4a9c23c8428174b83f278fe45ed7b4da2662", 17666774, "17679143"):
            assert res is not None

    @pytest.mark.asyncio
    async def test_get_log_events_hash_fail(self, client: Client):
        """ test for get log events by hash endpoint fail """
        async for res in client.base_service.get_log_events_by_topic_hash("eth-mainnet", "0xdac17f958d2ee523a2206206994597c13d831e", 17666774, "17679143"):
            assert res == "An error occured 400 : topic hash '0xdac17f958d2ee523a2206206994597c13d831e' malformed."
        
    # get all chains endpoint testing
    def test_get_chains_success(self, client: Client):
        """ test for get chains endpoint success """
        all_chains = client.base_service.get_all_chains()
        assert all_chains.error is False
        assert len(all_chains.data.items) > 0

    # get all chains status endpoint testing
    def test_get_chains_status_success(self, client: Client):
        """ test for get chains status endpoint fail """
        chain_status = client.base_service.get_all_chain_status()
        assert chain_status.error is False
        assert len(chain_status.data.items) > 0
