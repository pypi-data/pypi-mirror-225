from covalent import Client
import pytest
import os



class TestXykService:
    
    @pytest.fixture
    def client(self):
        return Client(os.environ.get('COVALENT_API_KEY'))

    def test_get_pools_success(self, client: Client):
        pools = client.xyk_service.get_pools("fantom-mainnet", "spiritswap")

        assert not pools.error
        assert pools.data.chain_id == 250
        assert pools.data.chain_name == "fantom-mainnet"

    def test_get_pools_error(self, client: Client):
        pools_error = client.xyk_service.get_pools("fantom-mainnet", "uniswap_v3")

        assert pools_error.error

    def test_get_pool_by_address_success(self, client: Client):
        pools_address = client.xyk_service.get_pool_by_address("fantom-mainnet", "spiritswap", "0xdbc490b47508d31c9ec44afb6e132ad01c61a02c")

        assert not pools_address.error
        assert pools_address.data.chain_id == 250
        assert pools_address.data.chain_name == "fantom-mainnet"
        assert len(pools_address.data.items) > 0

    def test_get_pool_by_address_error(self, client: Client):
        pools_address_error = client.xyk_service.get_pool_by_address("fantom-mainnet", "uniswap_v2", "0xdbc490b47508d31c9ec44afb6e132ad01c61a02c")
        
        assert pools_address_error.error
    
    def test_address_exchange_balances_success(self, client: Client):
        res = client.xyk_service.get_address_exchange_balances("eth-mainnet", "uniswap_v2", "demo.eth")

        assert res.error == False
        assert res.data.chain_id == 1
        assert res.data.chain_name == "eth-mainnet"
        assert len(res.data.items) > 0
        
    def test_address_exchange_balances_error(self, client: Client):
        res = client.xyk_service.get_address_exchange_balances("eth-mainnet", "uniswap_v3", "demo.eth")

        assert res.error == True
    
    def test_network_exchange_token_success(self, client: Client):
        res = client.xyk_service.get_network_exchange_tokens("fantom-mainnet", "spiritswap")

        assert res.error == False
        assert res.data.chain_id == 250
        assert res.data.chain_name == "fantom-mainnet"
    
    def test_network_exchange_token_error(self, client: Client):
        res = client.xyk_service.get_network_exchange_tokens("fantom-mainnet", "uniswap_v3")

        assert res.error == True
    
    def test_supported_dexes_success(self, client: Client):
        res = client.xyk_service.get_supported_dexes()

        assert res.error == False
        assert len(res.data.items) > 0
        assert res.data.items[0].dex_name == "uniswap_v2"

    def test_signal_network_exchange_token_success(self, client: Client):
        res = client.xyk_service.get_single_network_exchange_token("eth-mainnet", "uniswap_v2", "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599")

        assert res.error == False
        assert len(res.data.items) > 0
        assert res.data.chain_id == 1
        assert res.data.chain_name == "eth-mainnet"
        assert res.data.items[0].dex_name == "uniswap_v2"
        
    def test_single_network_exchange_token_success(self, client: Client):
        res = client.xyk_service.get_single_network_exchange_token("eth-mainnet", "uniswap_v2", "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599")

        assert res.error == False
        assert len(res.data.items) > 0
        assert res.data.chain_id == 1
        assert res.data.chain_name == "eth-mainnet"
        assert res.data.items[0].dex_name == "uniswap_v2"
    
    def test_single_network_exchange_token_error(self, client: Client):
        res = client.xyk_service.get_single_network_exchange_token("eth-mainnet", "uniswap_v3", "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599")

        assert res.error == True
    
    def test_transactions_for_account_address_success(self, client: Client):
        res = client.xyk_service.get_transactions_for_account_address("eth-mainnet", "uniswap_v2", "demo.eth")

        assert res.error == False
        assert res.data.chain_id == 1
        assert res.data.chain_name == "eth-mainnet"
        assert len(res.data.items) > 0
    
    def test_transactions_for_account_address_error(self, client: Client):
        res = client.xyk_service.get_transactions_for_account_address("eth-mainnet", "uniswap_v3", "demo.eth")

        assert res.error == True
    
    def test_transactions_for_token_address_success(self, client: Client):
        res = client.xyk_service.get_transactions_for_token_address("eth-mainnet", "uniswap_v2", "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599")

        assert res.error == False
        assert res.data.chain_id == 1
        assert res.data.chain_name == "eth-mainnet"
        assert len(res.data.items) > 0
    
    def test_transactions_for_token_address_error(self, client: Client):
        res = client.xyk_service.get_transactions_for_token_address("eth-mainnet", "uniswap_v3", "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599")

        assert res.error == True

    def test_transactions_for_exchange_success(self, client: Client):
        res = client.xyk_service.get_transactions_for_exchange("fantom-mainnet", "spiritswap", "0xdbc490b47508d31c9ec44afb6e132ad01c61a02c")

        assert res.error == False
        assert res.data.chain_id == 250
        assert res.data.chain_name == "fantom-mainnet"
        assert len(res.data.items) > 0
    
    def test_transactions_for_exchange_error(self, client: Client):
        res = client.xyk_service.get_transactions_for_exchange("fantom-mainnet", "uniswap_v2", "0xdbc490b47508d31c9ec44afb6e132ad01c61a02c")

        assert res.error == True
        
    def test_ecosystem_chart_data_success(self, client: Client):
        res = client.xyk_service.get_ecosystem_chart_data("fantom-mainnet", "spiritswap")

        assert res.error == False
        assert res.data.chain_id == 250
        assert res.data.chain_name == "fantom-mainnet"
        assert len(res.data.items) > 0
        
    def test_ecosystem_chart_data_error(self, client: Client):
        res = client.xyk_service.get_ecosystem_chart_data("fantom-mainnet", "uniswap_v3")

        assert res.error == True
        
    def test_health_data_success(self, client: Client):
        res = client.xyk_service.get_health_data("eth-mainnet", "uniswap_v2")

        assert res.error == False
        assert res.data.chain_id == 1
        assert res.data.chain_name == "eth-mainnet"
        assert len(res.data.items) > 0
    
    def test_health_data_error(self, client: Client):
        res = client.xyk_service.get_health_data("eth-mainnet", "uniswap_v3")

        assert res.error == True