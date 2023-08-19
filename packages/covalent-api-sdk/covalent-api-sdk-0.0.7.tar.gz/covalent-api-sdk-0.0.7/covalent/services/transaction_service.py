from datetime import datetime
from typing import AsyncIterable, Generic, TypeVar, List, Optional

import requests
from .util.back_off import ExponentialBackoff
from .util.api_helper import check_and_modify_response, chains, quotes, user_agent, Response
import aiohttp

class TransactionResponse:
    update_at: datetime
    """ The timestamp when the response was generated. Useful to show data staleness to users. """
    chain_id: int
    """ The requested chain ID eg: `1`. """
    chain_name: str
    """ The requested chain name eg: `eth-mainnet`. """
    items: List["Transaction"]
    """ List of response items. """

    def __init__(self, data):
        self.updated_at = datetime.fromisoformat(data["updated_at"])
        self.chain_id = int(data["chain_id"])
        self.chain_name = data["chain_name"]
        self.items = [Transaction(item_data) for item_data in data["items"]]

class Transaction:
    block_signed_at: Optional[datetime]
    """ The block signed timestamp in UTC. """
    block_height: Optional[int]
    """ The height of the block. """
    tx_hash: Optional[str]
    """ The requested transaction hash. """
    tx_offset: Optional[int]
    """ The offset is the position of the tx in the block. """
    successful: Optional[bool]
    from_address: Optional[str]
    from_address_label: Optional[str]
    to_address: Optional[str]
    to_address_label: Optional[str]
    value: Optional[int]
    """ The value attached to this tx. """
    value_quote: Optional[float]
    """ The value attached in `quote-currency` to this tx. """
    pretty_value_quote: Optional[str]
    """ A prettier version of the quote for rendering purposes. """
    gas_metadata: Optional["ContractMetadata"]
    """ The requested chain native gas token metadata. """
    gas_offered: Optional[str]
    gas_spent: Optional[str]
    gas_price: Optional[str]
    fees_paid: Optional[int]
    """ The total transaction fees (`gas_price` * `gas_spent`) paid for this tx, denoted in wei. """
    gas_quote: Optional[float]
    """ The gas spent in `quote-currency` denomination. """
    pretty_gas_quote: Optional[str]
    """ A prettier version of the quote for rendering purposes. """
    gas_quote_rate: Optional[float]
    """ The native gas exchange rate for the requested `quote-currency`. """
    log_events: Optional[List["LogEvent"]]

    def __init__(self, data):
        self.block_signed_at = datetime.fromisoformat(data["block_signed_at"]) if "block_signed_at" in data and data["block_signed_at"] is not None else None
        self.block_height = int(data["block_height"]) if "block_height" in data and data["block_height"] is not None else None
        self.tx_hash = data["tx_hash"] if "tx_hash" in data and data["tx_hash"] is not None else None
        self.tx_offset = int(data["tx_offset"]) if "tx_offset" in data and data["tx_offset"] is not None else None
        self.successful = data["successful"] if "successful" in data and data["successful"] is not None else None
        self.from_address = data["from_address"] if "from_address" in data and data["from_address"] is not None else None
        self.from_address_label = data["from_address_label"] if "from_address_label" in data and data["from_address_label"] is not None else None
        self.to_address = data["to_address"] if "to_address" in data and data["to_address"] is not None else None
        self.to_address_label = data["to_address_label"] if "to_address_label" in data and data["to_address_label"] is not None else None
        self.value = int(data["value"]) if "value" in data and data["value"] is not None else None
        self.value_quote = data["value_quote"] if "value_quote" in data and data["value_quote"] is not None else None
        self.pretty_value_quote = data["pretty_value_quote"] if "pretty_value_quote" in data and data["pretty_value_quote"] is not None else None
        self.gas_offered = data["gas_offered"] if "gas_offered" in data and data["gas_offered"] is not None else None
        self.gas_spent = data["gas_spent"] if "gas_spent" in data and data["gas_spent"] is not None else None
        self.gas_price = data["gas_price"] if "gas_price" in data and data["gas_price"] is not None else None
        self.fees_paid = int(data["fees_paid"]) if "fees_paid" in data and data["fees_paid"] is not None else None
        self.gas_quote = data["gas_quote"] if "gas_quote" in data and data["gas_quote"] is not None else None
        self.pretty_gas_quote = data["pretty_gas_quote"] if "pretty_gas_quote" in data and data["pretty_gas_quote"] is not None else None
        self.gas_quote_rate = data["gas_quote_rate"] if "gas_quote_rate" in data and data["gas_quote_rate"] is not None else None
        self.gas_metadata = ContractMetadata(data["gas_metadata"]) if "gas_metadata" in data and data["gas_metadata"] is not None else None
        self.log_events = [LogEvent(item_data) for item_data in data["log_events"]] if "log_events" in data and data["log_events"] is not None else None

class ContractMetadata:
    contract_decimals: Optional[int]
    """ Use contract decimals to format the token balance for display purposes - divide the balance by `10^{contract_decimals}`. """
    contract_name: Optional[str]
    """ The string returned by the `name()` method. """
    contract_ticker_symbol: Optional[str]
    """ The ticker symbol for this contract. This field is set by a developer and non-unique across a network. """
    contract_address: Optional[str]
    """ Use the relevant `contract_address` to lookup prices, logos, token transfers, etc. """
    supports_erc: Optional[List[str]]
    """ A list of supported standard ERC interfaces, eg: `ERC20` and `ERC721`. """
    logo_url: Optional[str]
    """ The contract logo URL. """

    def __init__(self, data):
        self.contract_decimals = int(data["contract_decimals"]) if "contract_decimals" in data and data["contract_decimals"] is not None else None
        self.contract_name = data["contract_name"] if "contract_name" in data and data["contract_name"] is not None else None
        self.contract_ticker_symbol = data["contract_ticker_symbol"] if "contract_ticker_symbol" in data and data["contract_ticker_symbol"] is not None else None
        self.contract_address = data["contract_address"] if "contract_address" in data and data["contract_address"] is not None else None
        self.supports_erc = data["supports_erc"] if "supports_erc" in data and data["supports_erc"] is not None else None
        self.logo_url = data["logo_url"] if "logo_url" in data and data["logo_url"] is not None else None
            

class LogEvent:
    block_signed_at: Optional[datetime]
    """ The block signed timestamp in UTC. """
    block_height: Optional[int]
    """ The height of the block. """
    tx_offset: Optional[int]
    """ The offset is the position of the tx in the block. """
    log_offset: Optional[int]
    tx_hash: Optional[str]
    """ The requested transaction hash. """
    raw_log_topics: Optional[List[str]]
    sender_contract_decimals: Optional[int]
    """ Use contract decimals to format the token balance for display purposes - divide the balance by `10^{contract_decimals}`. """
    sender_name: Optional[str]
    sender_contract_ticker_symbol: Optional[str]
    sender_address: Optional[str]
    sender_address_label: Optional[str]
    sender_logo_url: Optional[str]
    """ The contract logo URL. """
    raw_log_data: Optional[str]
    decoded: Optional["DecodedItem"]

    def __init__(self, data):
        self.block_signed_at = datetime.fromisoformat(data["block_signed_at"]) if "block_signed_at" in data and data["block_signed_at"] is not None else None
        self.block_height = int(data["block_height"]) if "block_height" in data and data["block_height"] is not None else None
        self.tx_offset = int(data["tx_offset"]) if "tx_offset" in data and data["tx_offset"] is not None else None
        self.log_offset = int(data["log_offset"]) if "log_offset" in data and data["log_offset"] is not None else None
        self.tx_hash = data["tx_hash"] if "tx_hash" in data and data["tx_hash"] is not None else None
        self.raw_log_topics = data["raw_log_topics"] if "raw_log_topics" in data and data["raw_log_topics"] is not None else None
        self.sender_contract_decimals = int(data["sender_contract_decimals"]) if "sender_contract_decimals" in data and data["sender_contract_decimals"] is not None else None
        self.sender_name = data["sender_name"] if "sender_name" in data and data["sender_name"] is not None else None
        self.sender_contract_ticker_symbol = data["sender_contract_ticker_symbol"] if "sender_contract_ticker_symbol" in data and data["sender_contract_ticker_symbol"] is not None else None
        self.sender_address = data["sender_address"] if "sender_address" in data and data["sender_address"] is not None else None
        self.sender_address_label = data["sender_address_label"] if "sender_address_label" in data and data["sender_address_label"] is not None else None
        self.sender_logo_url = data["sender_logo_url"] if "sender_logo_url" in data and data["sender_logo_url"] is not None else None
        self.raw_log_data = data["raw_log_data"] if "raw_log_data" in data and data["raw_log_data"] is not None else None
        self.decoded = DecodedItem(data["decoded"]) if "decoded" in data and data["decoded"] is not None else None

class DecodedItem:
    name: Optional[str]
    signature: Optional[str]
    params: Optional[List["Param"]]

    def __init__(self, data):
        self.name = data["name"] if "name" in data and data["name"] is not None else None
        self.signature = data["signature"] if "signature" in data and data["signature"] is not None else None
        self.params = [Param(item_data) for item_data in data["params"]] if "params" in data and data["params"] is not None else None

class Param:
    name: Optional[str]
    type: Optional[str]
    indexed: Optional[bool]
    decoded: Optional[bool]
    value: Optional[str]

    def __init__(self, data):
        self.name = data["name"] if "name" in data and data["name"] is not None else None
        self.type = data["type"] if "type" in data and data["type"] is not None else None
        self.indexed = data["indexed"] if "indexed" in data and data["indexed"] is not None else None
        self.decoded = data["decoded"] if "decoded" in data and data["decoded"] is not None else None
        self.value = data["value"] if "value" in data and data["value"] is not None else None             

class RecentTransactionsResponse:
    address: str
    """ The requested address. """
    update_at: datetime
    """ The timestamp when the response was generated. Useful to show data staleness to users. """
    next_update_at: str
    """ DEPRECATED """
    quote_currency: str
    """ The requested quote currency eg: `USD`. """
    chain_id: int
    """ The requested chain ID eg: `1`. """
    chain_name: str
    """ The requested chain name eg: `eth-mainnet`. """
    current_page: int
    """ The current page of the response. """
    links: "PaginationLinks"
    items: List["Transaction"]
    """ List of response items. """

    def __init__(self, data):
        self.address = data["address"]
        self.updated_at = datetime.fromisoformat(data["updated_at"])
        self.next_update_at = data["next_update_at"]
        self.quote_currency = data["quote_currency"]
        self.chain_id = int(data["chain_id"])
        self.chain_name = data["chain_name"]
        self.current_page = int(data["current_page"])
        self.links = PaginationLinks(data["links"])
        self.items = [Transaction(item_data) for item_data in data["items"]]

class PaginationLinks:
    prev: Optional[str]
    """ URL link to the next page. """
    next: Optional[str]
    """ URL link to the previous page. """

    def __init__(self, data):
        self.prev = data["prev"] if "prev" in data and data["prev"] is not None else None
        self.next = data["next"] if "next" in data and data["next"] is not None else None

class TransactionsBlockResponse:
    update_at: datetime
    """ The timestamp when the response was generated. Useful to show data staleness to users. """
    chain_id: int
    """ The requested chain ID eg: `1`. """
    chain_name: str
    """ The requested chain name eg: `eth-mainnet`. """
    items: List["Transaction"]
    """ List of response items. """

    def __init__(self, data):
        self.updated_at = datetime.fromisoformat(data["updated_at"])
        self.chain_id = int(data["chain_id"])
        self.chain_name = data["chain_name"]
        self.items = [Transaction(item_data) for item_data in data["items"]]

class TransactionsSummaryResponse:
    update_at: datetime
    """ The timestamp when the response was generated. Useful to show data staleness to users. """
    address: str
    """ The requested address. """
    chain_id: int
    """ The requested chain ID eg: `1`. """
    chain_name: str
    """ The requested chain name eg: `eth-mainnet`. """
    items: List["TransactionsSummary"]
    """ List of response items. """

    def __init__(self, data):
        self.updated_at = datetime.fromisoformat(data["updated_at"])
        self.address = data["address"]
        self.chain_id = int(data["chain_id"])
        self.chain_name = data["chain_name"]
        self.items = [TransactionsSummary(item_data) for item_data in data["items"]]

class TransactionsSummary:
    total_count: Optional[int]
    """ The total number of transactions. """
    earliest_transaction: Optional["TransactionSummary"]
    """ The earliest transaction detected. """
    latest_transaction: Optional["TransactionSummary"]
    """ The latest transaction detected. """

    def __init__(self, data):
        self.total_count = int(data["total_count"]) if "total_count" in data and data["total_count"] is not None else None
        self.earliest_transaction = TransactionSummary(data["earliest_transaction"]) if "earliest_transaction" in data and data["earliest_transaction"] is not None else None
        self.latest_transaction = TransactionSummary(data["latest_transaction"]) if "latest_transaction" in data and data["latest_transaction"] is not None else None

class TransactionSummary:
    block_signed_at: Optional[datetime]
    """ The block signed timestamp in UTC. """
    tx_hash: Optional[str]
    """ The requested transaction hash. """
    tx_detail_link: Optional[str]
    """ The link to the transaction details using the Covalent API. """

    def __init__(self, data):
        self.block_signed_at = datetime.fromisoformat(data["block_signed_at"]) if "block_signed_at" in data and data["block_signed_at"] is not None else None
        self.tx_hash = data["tx_hash"] if "tx_hash" in data and data["tx_hash"] is not None else None
        self.tx_detail_link = data["tx_detail_link"] if "tx_detail_link" in data and data["tx_detail_link"] is not None else None
            

async def paginate_endpoint(url: str, api_key: str, urls_params) -> AsyncIterable[Transaction]:
    has_next = True
    backoff = ExponentialBackoff()
    data = None
    while has_next:
        try:

            async with aiohttp.ClientSession() as session:
                async with session.get(f"{url}", params=urls_params, headers={"Authorization": f"Bearer {api_key}", "X-Requested-With": user_agent}) as response:
                    data = await response.json()
        
            if data.get("error") and data.get("error_code") == 429:
                try:
                    backoff.back_off()
                except Exception as error:
                    has_next = False
                    print("An error occured", (data.get("error_code") if data else response.status), ":", data.get("error_message") if data else "401 Authorization Required")
            else:
                for tx in data.get("data").get("items"):
                    data_class = Transaction(tx)
                    check_and_modify_response(data_class)
                    yield data_class
                
                backoff.set_num_attempts(1)

                if not data.get("error"):
                    if data.get("data") is not None and data.get("data").get("links").get("prev") is None:
                        has_next = False
                    url = data.get("data").get("links").get("prev") if data.get("data") is not None and data.get("data").get("links").get("prev") is not None else ""
                else:
                    has_next = False
        except Exception:
            has_next = False
            print("An error occured", (data.get("error_code") if data else response.status), ":", data.get("error_message") if data else "401 Authorization Required")

            
class TransactionService:
    __api_key: str
    def __init__(self, api_key: str):
        self.__api_key = api_key


    def get_transaction(self, chain_name: chains, tx_hash: str, quote_currency: Optional[quotes] = None, no_logs: Optional[bool] = None, with_dex: Optional[bool] = None, with_nft_sales: Optional[bool] = None, with_lending: Optional[bool] = None) -> Response[TransactionResponse]:
        """
        Parameters:

        chain_name (string): The chain name eg: `eth-mainnet`.
        tx_hash (str): The transaction hash.
        quote_currency (string): The currency to convert. Supports `USD`, `CAD`, `EUR`, `SGD`, `INR`, `JPY`, `VND`, `CNY`, `KRW`, `RUB`, `TRY`, `NGN`, `ARS`, `AUD`, `CHF`, and `GBP`.
        no_logs (bool): Omit log events.
        with_dex (bool): Decoded DEX details including protocol (e.g. Uniswap), event (e.g 'add_liquidity') and tokens involved with historical prices. Additional 0.05 credits charged if data available.
        with_nft_sales (bool): Decoded NFT sales details including marketplace (e.g. Opensea) and cached media links. Additional 0.05 credits charged if data available.
        with_lending (bool): Decoded lending details including protocol (e.g. Aave), event (e.g. 'deposit') and tokens involved with prices. Additional 0.05 credits charged if data available.
        """
        success = False
        data: Optional[Response[TransactionResponse]] = None
        response = None
        backoff = ExponentialBackoff()
        while not success:
            try:
                url_params = {}
                
                if quote_currency is not None:
                    url_params["quote-currency"] = str(quote_currency)
                    
                if no_logs is not None:
                    url_params["no-logs"] = str(no_logs)
                    
                if with_dex is not None:
                    url_params["with-dex"] = str(with_dex)
                    
                if with_nft_sales is not None:
                    url_params["with-nft-sales"] = str(with_nft_sales)
                    
                if with_lending is not None:
                    url_params["with-lending"] = str(with_lending)
                    

                response = requests.get(f"https://api.covalenthq.com/v1/{chain_name}/transaction_v2/{tx_hash}/", params=url_params, headers={
                    "Authorization": f"Bearer {self.__api_key}",
                    "X-Requested-With": user_agent
                })

                res = response.json()
                data = Response(**res)

                if data.error and data.error_code == 429:
                    try:
                        backoff.back_off()
                    except Exception:
                        success = True
                        return Response(
                            data=None,
                            error=data.error,
                            error_code=data.error_code if data else response.status_code,
                            error_message=data.error_message if data else "401 Authorization Required"
                        )
                else:
                    data_class = TransactionResponse(data.data)
                    check_and_modify_response(data_class)
                    success = True
                    return Response(
                        data=data_class,
                        error=data.error,
                        error_code=data.error_code if data else response.status_code,
                        error_message=data.error_message if data else "401 Authorization Required"
                    )
            except Exception:
                success = True
                return Response(
                    data=None,
                    error=True,
                    error_code=data.error_code if data is not None else response.status_code if response is not None else None,
                    error_message=data.error_message if data else "401 Authorization Required"
                )
        return Response (
            data=None,
            error=True,
            error_code=data.error_code if data is not None else response.status_code if response is not None else None,
            error_message=data.error_message if data is not None else None
        )
        
    async def get_all_transactions_for_address(self, chain_name: chains, wallet_address: str, quote_currency: Optional[quotes] = None, no_logs: Optional[bool] = None) -> AsyncIterable[Transaction]:
        """
        Parameters:

        chain_name (string): The chain name eg: `eth-mainnet`.
        wallet_address (str): The requested address. Passing in an `ENS`, `RNS`, `Lens Handle`, or an `Unstoppable Domain` resolves automatically.
        quote_currency (string): The currency to convert. Supports `USD`, `CAD`, `EUR`, `SGD`, `INR`, `JPY`, `VND`, `CNY`, `KRW`, `RUB`, `TRY`, `NGN`, `ARS`, `AUD`, `CHF`, and `GBP`.
        no_logs (bool): Omit log events.
        """
        success = False
        response = None
        while not success:
            try:
                url_params = {}
                
                if quote_currency is not None:
                    url_params["quote-currency"] = str(quote_currency)
                
                if no_logs is not None:
                    url_params["no-logs"] = str(no_logs)
                

                async for response in paginate_endpoint(f"https://api.covalenthq.com/v1/{chain_name}/address/{wallet_address}/transactions_v3/", self.__api_key, url_params):
                    yield response

                success = True
            except Exception as error:
                success = True
                yield response
    
    def get_transactions_for_block(self, chain_name: chains, block_height: int, quote_currency: Optional[quotes] = None, no_logs: Optional[bool] = None) -> Response[TransactionsBlockResponse]:
        """
        Parameters:

        chain_name (string): The chain name eg: `eth-mainnet`.
        block_height (int): The requested block height.
        quote_currency (string): The currency to convert. Supports `USD`, `CAD`, `EUR`, `SGD`, `INR`, `JPY`, `VND`, `CNY`, `KRW`, `RUB`, `TRY`, `NGN`, `ARS`, `AUD`, `CHF`, and `GBP`.
        no_logs (bool): Omit log events.
        """
        success = False
        data: Optional[Response[TransactionsBlockResponse]] = None
        response = None
        backoff = ExponentialBackoff()
        while not success:
            try:
                url_params = {}
                
                if quote_currency is not None:
                    url_params["quote-currency"] = str(quote_currency)
                    
                if no_logs is not None:
                    url_params["no-logs"] = str(no_logs)
                    

                response = requests.get(f"https://api.covalenthq.com/v1/{chain_name}/block/{block_height}/transactions_v3/", params=url_params, headers={
                    "Authorization": f"Bearer {self.__api_key}",
                    "X-Requested-With": user_agent
                })

                res = response.json()
                data = Response(**res)

                if data.error and data.error_code == 429:
                    try:
                        backoff.back_off()
                    except Exception:
                        success = True
                        return Response(
                            data=None,
                            error=data.error,
                            error_code=data.error_code if data else response.status_code,
                            error_message=data.error_message if data else "401 Authorization Required"
                        )
                else:
                    data_class = TransactionsBlockResponse(data.data)
                    check_and_modify_response(data_class)
                    success = True
                    return Response(
                        data=data_class,
                        error=data.error,
                        error_code=data.error_code if data else response.status_code,
                        error_message=data.error_message if data else "401 Authorization Required"
                    )
            except Exception:
                success = True
                return Response(
                    data=None,
                    error=True,
                    error_code=data.error_code if data is not None else response.status_code if response is not None else None,
                    error_message=data.error_message if data else "401 Authorization Required"
                )
        return Response (
            data=None,
            error=True,
            error_code=data.error_code if data is not None else response.status_code if response is not None else None,
            error_message=data.error_message if data is not None else None
        )
        
    def get_transaction_summary(self, chain_name: chains, wallet_address: str) -> Response[TransactionsSummaryResponse]:
        """
        Parameters:

        chain_name (string): The chain name eg: `eth-mainnet`.
        wallet_address (str): The requested address. Passing in an `ENS`, `RNS`, `Lens Handle`, or an `Unstoppable Domain` resolves automatically.
        """
        success = False
        data: Optional[Response[TransactionsSummaryResponse]] = None
        response = None
        backoff = ExponentialBackoff()
        while not success:
            try:
                url_params = {}
                

                response = requests.get(f"https://api.covalenthq.com/v1/{chain_name}/address/{wallet_address}/transactions_summary/", params=url_params, headers={
                    "Authorization": f"Bearer {self.__api_key}",
                    "X-Requested-With": user_agent
                })

                res = response.json()
                data = Response(**res)

                if data.error and data.error_code == 429:
                    try:
                        backoff.back_off()
                    except Exception:
                        success = True
                        return Response(
                            data=None,
                            error=data.error,
                            error_code=data.error_code if data else response.status_code,
                            error_message=data.error_message if data else "401 Authorization Required"
                        )
                else:
                    data_class = TransactionsSummaryResponse(data.data)
                    check_and_modify_response(data_class)
                    success = True
                    return Response(
                        data=data_class,
                        error=data.error,
                        error_code=data.error_code if data else response.status_code,
                        error_message=data.error_message if data else "401 Authorization Required"
                    )
            except Exception:
                success = True
                return Response(
                    data=None,
                    error=True,
                    error_code=data.error_code if data is not None else response.status_code if response is not None else None,
                    error_message=data.error_message if data else "401 Authorization Required"
                )
        return Response (
            data=None,
            error=True,
            error_code=data.error_code if data is not None else response.status_code if response is not None else None,
            error_message=data.error_message if data is not None else None
        )
        
    
    