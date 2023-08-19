from typing import AsyncIterable, Generic, Literal, Optional, TypeVar
from .back_off import ExponentialBackoff
import aiohttp

chains = Literal["btc-mainnet", "eth-mainnet", "matic-mainnet", "bsc-mainnet", "avalanche-mainnet", "fantom-mainnet", "moonbeam-mainnet", "moonbeam-moonriver", "rsk-mainnet", "arbitrum-mainnet", "palm-mainnet", "klaytn-mainnet", "heco-mainnet", "nervos-godwoken-mainnet", "axie-mainnet", "evmos-mainnet", "astar-mainnet", "iotex-mainnet", "harmony-mainnet", "cronos-mainnet", "aurora-mainnet", "emerald-paratime-mainnet", "boba-mainnet", "eth-goerli", "matic-mumbai", "avalanche-testnet", "bsc-testnet", "moonbeam-moonbase-alpha", "rsk-testnet", "arbitrum-goerli", "fantom-testnet", "palm-testnet", "heco-testnet", "nervos-godwoken-testnet", "evmos-testnet", "astar-shiden", "iotex-testnet", "harmony-testnet", "aurora-testnet", "scroll-l2-testnet", "scroll-l1-testnet", "covalent-internal-network-v1", "defi-kingdoms-mainnet", "swimmer-mainnet", "boba-avalanche-mainnet", "boba-bobabeam-mainnet", "boba-bnb-mainnet", "boba-rinkeby-testnet", "boba-bobabase-testnet", "boba-bnb-testnet", "boba-avalanche-testnet", "klaytn-testnet", "gather-mainnet", "gather-testnet", "optimism-mainnet", "skale-calypso", "skale-mainnet", "skale-razor", "avalanche-dexalot-mainnet", "skale-omnus", "avalanche-dexalot-testnet", "astar-shibuya", "cronos-testnet", "defi-kingdoms-testnet", "metis-mainnet", "metis-testnet", "milkomeda-a1-mainnet", "milkomeda-a1-devnet", "milkomeda-c1-mainnet", "milkomeda-c1-devnet", "swimmer-testnet", "solana-mainnet", "skale-europa", "meter-mainnet", "meter-testnet", "skale-exorde", "boba-goerli", "neon-testnet", "skale-staging-uum", "skale-staging-lcc", "arbitrum-nova-mainnet", "canto-mainnet", "bittorrent-mainnet", "bittorrent-testnet", "flarenetworks-flare-mainnet", "flarenetworks-flare-testnet", "flarenetworks-canary-mainnet", "flarenetworks-canary-testnet", "kcc-mainnet", "kcc-testnet", "polygon-zkevm-testnet", "linea-testnet", "base-testnet", "mantle-testnet", "scroll-alpha-testnet", "oasys-mainnet", "oasys-testnet", "findora-mainnet", "findora-forge-testnet", "sx-mainnet", "oasis-sapphire-mainnet", "oasis-sapphire-testnet", "optimism-goerli", "polygon-zkevm-mainnet", "horizen-yuma-testnet", "clv-parachain", "energi-mainnet", "energi-testnet", "horizen-gobi-testnet", "eth-sepolia", "skale-nebula", "skale-battleground", "avalanche-meld-testnet", "gunzilla-testnet", "ultron-mainnet", "ultron-testnet", "zora-mainnet", "zora-testnet", "neon-mainnet", "avalanche-shrapnel-mainnet", "base-mainnet", "mantle-mainnet", "avalanche-loco-legends-mainnet", "linea-mainnet", "horizen-eon-mainnet", "avalanche-numbers", "avalanche-dos", "avalanche-step-network", "avalanche-xplus", "avalanche-xanachain", "avalanche-meld-mainnet", "opside-public-zkevm", "opside-law-chain", "avalanche-shrapnel-testnet", "avalanche-loco-legends-testnet", "opside-cb-zkevm", "opside-pre-alpha-testnet", "opside-era7", "opside-xthrill"]
quotes = Literal["USD", "CAD", "EUR", "SGD", "INR", "JPY", "VND", "CNY", "KRW", "RUB", "TRY", "NGN", "ARS", "AUD", "CHF", "GBP"]
user_agent = "com.covalenthq.sdk.python/0.0.7"

T = TypeVar('T')

class Response(Generic[T]):
    data: Optional[T]
    error: bool
    error_code: Optional[int]
    error_message: Optional[str]

    def __init__(self, data: Optional[T], error: bool, error_code: Optional[int], error_message: Optional[str]):
        self.data = data
        self.error = error
        self.error_code = error_code
        self.error_message = error_message

def check_and_modify_response(json_obj):
    """ modify reponse and remove next_update_at """
    for key in list(vars(json_obj).keys()):
        if key == 'next_update_at':
            del vars(json_obj)[key]
        elif isinstance(vars(json_obj)[key], dict):
            check_and_modify_response(vars(json_obj)[key])
            

async def paginate_endpoint(url: str, api_key: str, urls_params, data_class_constructor: T) -> AsyncIterable[T]:
    has_next = True
    page_number = 0
    backoff = ExponentialBackoff()
    data = None

    while has_next:
        try:

            if urls_params.get("page-number") is None:
                urls_params["page-number"] = str(page_number)

            async with aiohttp.ClientSession() as session:
                async with session.get(f"{url}", params=urls_params, headers={"Authorization": f"Bearer {api_key}", "X-Requested-With": user_agent}) as response:
                    data = await response.json()

                if data.get("error") and data.get("error_code") == 429:
                    try:
                        backoff.back_off()
                    except Exception:
                        has_next = False
                        print("An error occured", (data.get("error_code") if data else response.status), ":", data.get("error_message") if data else "401 Authorization Required")
                else:

                    for tx in data.get("data").get("items"):
                        data_class = data_class_constructor(tx)
                        check_and_modify_response(data_class)
                        yield data_class
                    
                    backoff.set_num_attempts(1)

                    if not data.get("error"):
                        pagination = data.get("data", {}).get("pagination")

                        if pagination and not pagination.get("has_more"):
                            has_next = False

                        next_page = int(urls_params.get("page-number")) + 1
                        urls_params["page-number"] = str(next_page)
                    else:
                        has_next = False

        except Exception:
            has_next = False
            print("An error occured", (data.get("error_code") if data else response.status), ":", data.get("error_message") if data else "401 Authorization Required")


