import requests
from urllib3 import util


def retrying_session():
    adapter = requests.adapters.HTTPAdapter(
        max_retries=util.Retry(
            total=3,
            allowed_methods=False,
        )
    )

    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
