import requests
import json

api_k = '6MNV6HD-6A84BK9-PK7TEGF-FM7N1BV'


class NowPayments:
    def __init__(self, api_key=None) -> None:
        self.url = "https://api.nowpayments.io/v1/{}"
        self.api_key = api_key
        self.headers = {
            'x-api-key': self.api_key
        }

    def __make_request(self, method='GET', headers=None, data=None, url=None):
        final_url = self.url.format(url) if url else self.url
        print(final_url)
        return requests.request(method, final_url, headers=headers, data=data).text

    def get_api_status(self, return_statuscode=False):
        response = self.__make_request(url='status')
        return response

    def autenticate(self, email, password):
        data = {
            "email": email,
            "password": password
        }
        return self.__make_request(method='POST', url='auth', data=data)

    def get_currencies(self):
        return self.__make_request(method='GET', url='currencies', headers=self.headers)

    def get_minimum_payment_amount(self, currency_from, currency_to):
        url = f'min-amount?currency_from={currency_from}&&currency_to={currency_to}'
        return self.__make_request(url=url, headers=self.headers)

    def create_invoice(self, price_amount, price_currency='usd', order_id=None, order_description=None):
        data = json.dumps({
            "price_amount": price_amount,
            "price_currency": price_currency.lower(),
            "order_id": order_id,
            "order_description": order_description,
            "ipn_callback_url": "https://nowpayments.io",
            "success_url": "https://nowpayments.io",
            "cancel_url": "https://nowpayments.io"

        })
        headers = self.headers
        headers['Content-Type'] = 'application/json'
        return self.__make_request(method='POST', url='invoice', data=data, headers=headers)

    def create_payment(self, price_amount, price_currency, pay_currency, order_id='', order_description=''):
        data = json.dumps({
            "price_amount": price_amount,
            "price_currency": price_currency,
            "pay_currency": pay_currency,
            "ipn_callback_url": "https://nowpayments.io",
            "order_id": order_id,
            "order_description": order_description
        })
        headers = self.headers
        headers['Content-Type'] = 'application/json'

        return self.__make_request(method='POST',url='payment', data=data, headers=headers)


# print(NowPayments(api_key=api_k).get_minimum_payment_amount(currency_from='usdttrc20', currency_to='trx'))
print(NowPayments(api_key=api_k).create_payment(price_currency='usd',pay_currency='usdttrc20',price_amount=200, order_id='ID-TEST', order_description='Ejemplo'))
