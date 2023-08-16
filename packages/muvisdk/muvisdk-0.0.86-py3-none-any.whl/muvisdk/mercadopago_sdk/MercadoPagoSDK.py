import mercadopago
import requests
from mercadopago.http import HttpClient as MpHttpClient
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from .Card import Card
from .CardToken import CardToken
from .Customer import Customer
from .Payment import Payment
from .Refund import Refund


class HttpClient(MpHttpClient):

    def request(self, method, url, maxretries=None, **kwargs):
        retry_strategy = Retry(
            total=maxretries,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        http = requests.Session()
        http.mount("https://", HTTPAdapter(max_retries=retry_strategy))
        with http as session:
            api_result = session.request(method, url, **kwargs)
            response = {
                "status": api_result.status_code,
                "response": api_result.json(),
                "headers": api_result.headers
            }

        return response


class MercadoPagoSDK:
    def __init__(self, merchant: dict, marketplace: bool = False):
        mercadopago_model = 'mp_marketplace' if marketplace else 'mercadopago'

        active = merchant['credentials'][mercadopago_model]['active']
        access_token = merchant['credentials'][mercadopago_model]['access_token'] if active else None

        self.sdk = mercadopago.SDK(access_token, http_client=HttpClient()) if active else None
        self.merchant_id = merchant['_id']
        self.merchant_name = merchant['name']
        self.processor = 'mercadopago'

    def customer(self):
        return Customer(self.processor, self.sdk)
    
    def card(self):
        return Card(self.processor, self.sdk)

    def card_token(self):
        return CardToken(self.processor, self.sdk)
    
    def payment(self):
        return Payment(self.processor, self.sdk, self.merchant_id)

    def refund(self):
        return Refund(self.processor, self.sdk)

    def ok(self):
        return self.sdk is not None
