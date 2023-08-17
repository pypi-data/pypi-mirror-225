import os
from uuid import uuid4
from re import findall
from ...typing import sha256, Dict, get_type_hints

try:
    import tls_client
except ModuleNotFoundError:
    os.system("pip install tls_client --no-cache-dir")

url = "https://you.com/api/streamingSearch"
model = ['gpt-3.5-turbo']
supports_stream = True
needs_auth = False
working = True

def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    client = tls_client.Session(client_identifier="chrome_108")
    client.headers = {
        "authority": "you.com",
        "accept": "text/event-stream",
        "accept-language": "en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3",
        "cache-control": "no-cache",
        "referer": "https://you.com/search?q=who+are+you&tbm=youchat",
        "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "cookie": f"safesearch_guest=Off; uuid_guest={str(uuid4())}",
        "user-agent": "Mozilla/5.0 (Windows NT 5.1; U;  ; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.52",
    }
    params = {
        "q": messages,
        "page": 1,
        "count": 10,
        "safeSearch": "Off",
        "onShoppingPage": False,
        "mkt": "",
        "responseFilter": "WebPages,Translations,TimeZone,Computation,RelatedSearches",
        "domain": "youchat",
        "queryTraceId": str(uuid4()),
        "chat": [],
    }
    resp = client.get(
        "https://you.com/api/streamingSearch", params=params, timeout_seconds=30
    )
    if "youChatToken" not in resp.text:
        raise Exception("Unable to fetch response.")
    return (
        "".join(findall(r"{\"youChatToken\": \"(.*?)\"}", resp.text))
        .replace("\\n", "\n")
        .replace("\\\\", "\\")
        .replace('\\"', '"')
    )

params = f'ai4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])