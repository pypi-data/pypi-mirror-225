from covalent import Client
import pytest
import os



class TestTransactionService:
    
    @pytest.fixture
    def client(self):
        return Client(os.environ.get('COVALENT_API_KEY'))

    def test_success_for_get_transaction(self, client: Client):
        res =  client.transaction_service.get_transaction("eth-mainnet", "0xb27a3a3d660b7d679ebbd7065635c8c3613e32eb0ebae24863a6375d73d1a128")
        assert res.error == False
        assert res.data.chain_id == 1
        assert res.data.chain_name == "eth-mainnet"
        assert len(res.data.items) > 0
        assert res.data.items[0].tx_hash == "0xb27a3a3d660b7d679ebbd7065635c8c3613e32eb0ebae24863a6375d73d1a128"
        
            
    def test_incorrect_hash_for_transaction(self, client: Client):
        res =  client.transaction_service.get_transaction("eth-mainnet", "0xtest")
        assert res.error == True
        assert res.data == None
        assert res.error_code == 400
        assert res.error_message == "Transaction Hash '0xtest' malformed"
    
    def test_success_for_get_transaction_summary(self, client: Client):
        res =  client.transaction_service.get_transaction_summary("eth-mainnet", "demo.eth")
        assert res.error == False
        assert res.data.chain_id == 1
        assert res.data.chain_name == "eth-mainnet"
        assert res.data.address == "0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de"
        assert len(res.data.items) > 0
    
    def test_incorrect_address_for_get_transaction_summary(self, client: Client):
        res =  client.transaction_service.get_transaction_summary("eth-mainnet", "0x123")
        assert res.error == True
        assert res.data == None
        assert res.error_code == 400
        assert res.error_message == "Malformed address provided: 0x123"
    
    def test_success_for_transaction_block(self, client: Client):
        res =  client.transaction_service.get_transactions_for_block("eth-mainnet", 17685920)
        assert res.error == False
        assert res.data.chain_name == "eth-mainnet"
        assert res.data.chain_id == 1
        assert res.data.items[0].block_height == 17685920

    def test_invalid_block_height(self, client: Client):
        res =  client.transaction_service.get_transactions_for_block("eth-mainnet", 100000000)
        assert res.error == True
        assert res.data == None
        assert res.error_code == 400
        assert res.error_message == "The parameter 'block_height' cannot be greater than the chains current height. Use the string 'latest' to get the current block height."
    
    def test_no_logs_for_transaction_block(self, client: Client):
        res =  client.transaction_service.get_transactions_for_block("eth-mainnet", 17685920, "CAD", True)
        assert res.error == False
        assert res.data.items[0].log_events == None   
    
    
    @pytest.mark.asyncio
    async def test_success_for_get_all_transactions(self, client: Client):
        async for res in client.transaction_service.get_all_transactions_for_address("eth-mainnet", "demo.eth"):
            assert res is not None
    
    
    @pytest.mark.asyncio
    async def test_malformed_address(self, client: Client):
        async for res in client.transaction_service.get_all_transactions_for_address("eth-mainnet", "0x1233"):
            assert res == "An error occured 400 : Malformed address provided: 0x123123"
    
    @pytest.mark.asyncio
    async def test_quote_currency(self, client: Client):
        async for res in client.transaction_service.get_all_transactions_for_address("eth-mainnet", "demo.eth", "CAD"):
            assert res is not None
    
    
    @pytest.mark.asyncio
    async def test_no_logs_for_get_all_transactions(self, client: Client):
        async for res in client.transaction_service.get_all_transactions_for_address("eth-mainnet", "demo.eth", "CAD", True):
            assert res.log_events == None
    
    
    
    
        
    
    

