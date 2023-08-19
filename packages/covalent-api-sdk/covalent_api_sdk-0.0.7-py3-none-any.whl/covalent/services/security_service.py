from datetime import datetime
from typing import Generic, TypeVar, List, Optional
import requests
from .util.back_off import ExponentialBackoff
from .util.api_helper import check_and_modify_response, chains, quotes, user_agent, Response


class ApprovalsResponse:
    address: str
    """ The requested address. """
    update_at: datetime
    """ The timestamp when the response was generated. Useful to show data staleness to users. """
    quote_currency: str
    """ The requested quote currency eg: `USD`. """
    chain_id: int
    """ The requested chain ID eg: `1`. """
    chain_name: str
    """ The requested chain name eg: `eth-mainnet`. """
    items: List["TokensApprovalItem"]
    """ List of response items. """

    def __init__(self, data):
        self.address = data["address"]
        self.updated_at = datetime.fromisoformat(data["updated_at"])
        self.quote_currency = data["quote_currency"]
        self.chain_id = int(data["chain_id"])
        self.chain_name = data["chain_name"]
        self.items = [TokensApprovalItem(item_data) for item_data in data["items"]]

class TokensApprovalItem:
    token_address: Optional[str]
    """ The address for the token that has approvals. """
    token_address_label: Optional[str]
    """ The name for the token that has approvals. """
    ticker_symbol: Optional[str]
    """ The ticker symbol for this contract. This field is set by a developer and non-unique across a network. """
    contract_decimals: Optional[int]
    """ Use contract decimals to format the token balance for display purposes - divide the balance by `10^{contract_decimals}`. """
    logo_url: Optional[str]
    """ The contract logo URL. """
    quote_rate: Optional[float]
    """ The exchange rate for the requested quote currency. """
    balance: Optional[int]
    """ Wallet balance of the token. """
    balance_quote: Optional[float]
    """ Value of the wallet balance of the token. """
    pretty_balance_quote: Optional[str]
    """ A prettier version of the quote for rendering purposes. """
    value_at_risk: Optional[str]
    """ Total amount at risk across all spenders. """
    value_at_risk_quote: Optional[float]
    """ Value of total amount at risk across all spenders. """
    pretty_value_at_risk_quote: Optional[str]
    """ A prettier version of the quote for rendering purposes. """
    spenders: Optional[List["TokenSpenderItem"]]
    """ Contracts with non-zero approvals for this token. """

    def __init__(self, data):
        self.token_address = data["token_address"] if "token_address" in data and data["token_address"] is not None else None
        self.token_address_label = data["token_address_label"] if "token_address_label" in data and data["token_address_label"] is not None else None
        self.ticker_symbol = data["ticker_symbol"] if "ticker_symbol" in data and data["ticker_symbol"] is not None else None
        self.contract_decimals = int(data["contract_decimals"]) if "contract_decimals" in data and data["contract_decimals"] is not None else None
        self.logo_url = data["logo_url"] if "logo_url" in data and data["logo_url"] is not None else None
        self.quote_rate = data["quote_rate"] if "quote_rate" in data and data["quote_rate"] is not None else None
        self.balance = int(data["balance"]) if "balance" in data and data["balance"] is not None else None
        self.balance_quote = data["balance_quote"] if "balance_quote" in data and data["balance_quote"] is not None else None
        self.pretty_balance_quote = data["pretty_balance_quote"] if "pretty_balance_quote" in data and data["pretty_balance_quote"] is not None else None
        self.value_at_risk = data["value_at_risk"] if "value_at_risk" in data and data["value_at_risk"] is not None else None
        self.value_at_risk_quote = data["value_at_risk_quote"] if "value_at_risk_quote" in data and data["value_at_risk_quote"] is not None else None
        self.pretty_value_at_risk_quote = data["pretty_value_at_risk_quote"] if "pretty_value_at_risk_quote" in data and data["pretty_value_at_risk_quote"] is not None else None
        self.spenders = [TokenSpenderItem(item_data) for item_data in data["spenders"]] if "spenders" in data and data["spenders"] is not None else None

class TokenSpenderItem:
    block_height: Optional[int]
    """ The height of the block. """
    tx_offset: Optional[int]
    """ The offset is the position of the tx in the block. """
    log_offset: Optional[int]
    block_signed_at: Optional[datetime]
    """ The block signed timestamp in UTC. """
    tx_hash: Optional[str]
    """ Most recent transaction that updated approval amounts for the token. """
    spender_address: Optional[str]
    """ Address of the contract with approval for the token. """
    spender_address_label: Optional[str]
    """ Name of the contract with approval for the token. """
    allowance: Optional[str]
    """ Remaining number of tokens granted to the spender by the approval. """
    allowance_quote: Optional[float]
    """ Value of the remaining allowance specified by the approval. """
    pretty_allowance_quote: Optional[str]
    """ A prettier version of the quote for rendering purposes. """
    value_at_risk: Optional[str]
    """ Amount at risk for spender. """
    value_at_risk_quote: Optional[float]
    """ Value of amount at risk for spender. """
    pretty_value_at_risk_quote: Optional[str]
    """ A prettier version of the quote for rendering purposes. """
    risk_factor: Optional[str]

    def __init__(self, data):
        self.block_height = int(data["block_height"]) if "block_height" in data and data["block_height"] is not None else None
        self.tx_offset = int(data["tx_offset"]) if "tx_offset" in data and data["tx_offset"] is not None else None
        self.log_offset = int(data["log_offset"]) if "log_offset" in data and data["log_offset"] is not None else None
        self.block_signed_at = datetime.fromisoformat(data["block_signed_at"]) if "block_signed_at" in data and data["block_signed_at"] is not None else None
        self.tx_hash = data["tx_hash"] if "tx_hash" in data and data["tx_hash"] is not None else None
        self.spender_address = data["spender_address"] if "spender_address" in data and data["spender_address"] is not None else None
        self.spender_address_label = data["spender_address_label"] if "spender_address_label" in data and data["spender_address_label"] is not None else None
        self.allowance = data["allowance"] if "allowance" in data and data["allowance"] is not None else None
        self.allowance_quote = data["allowance_quote"] if "allowance_quote" in data and data["allowance_quote"] is not None else None
        self.pretty_allowance_quote = data["pretty_allowance_quote"] if "pretty_allowance_quote" in data and data["pretty_allowance_quote"] is not None else None
        self.value_at_risk = data["value_at_risk"] if "value_at_risk" in data and data["value_at_risk"] is not None else None
        self.value_at_risk_quote = data["value_at_risk_quote"] if "value_at_risk_quote" in data and data["value_at_risk_quote"] is not None else None
        self.pretty_value_at_risk_quote = data["pretty_value_at_risk_quote"] if "pretty_value_at_risk_quote" in data and data["pretty_value_at_risk_quote"] is not None else None
        self.risk_factor = data["risk_factor"] if "risk_factor" in data and data["risk_factor"] is not None else None


class SecurityService:
    __api_key: str
    def __init__(self, api_key: str):
        self.__api_key = api_key


    def get_approvals(self, chain_name: chains, wallet_address: str) -> Response[ApprovalsResponse]:
        """
        Parameters:

        chain_name (string): The chain name eg: `eth-mainnet`.
        wallet_address (str): The requested address. Passing in an `ENS`, `RNS`, `Lens Handle`, or an `Unstoppable Domain` resolves automatically.
        """
        success = False
        data: Optional[Response[ApprovalsResponse]] = None
        response = None
        backoff = ExponentialBackoff()
        while not success:
            try:
                url_params = {}
                

                response = requests.get(f"https://api.covalenthq.com/v1/{chain_name}/approvals/{wallet_address}/", params=url_params, headers={
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
                    data_class = ApprovalsResponse(data.data)
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
        
    
    