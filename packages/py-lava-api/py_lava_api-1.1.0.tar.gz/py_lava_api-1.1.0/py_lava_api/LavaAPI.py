import hashlib
import hmac
import json

from py_lava_api.enums import SubtractEnum, WalletTypeEnum
from .models import Balance, PaymentStatusResponse, PayoutResponse, PaymentResponse, PayoutStatusResponse, Tariffs
from requests import post
from dataclasses import dataclass

@dataclass
class LavaAPI:
    __site = "https://api.lava.ru/business/"
    shop_id: str
    key_secret: str
    key_still: str
    payout_webhook: str = ""
    payment_webhook: str = ""
    fail_url: str = ""
    success_url: str = ""

    def __get_header(self, sign: str) -> dict:
        """Получить шапку"""
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "signature": sign,
        }

    def __get_payment(self, amount: float, order_id: str, expire: int = 300, custom_fields: str = "", comment: str = "") -> dict:
        if expire < 0 or expire > 7_200:
            raise Exception("expire must be between 0 and 7_200")
        """Генерация счета"""
        return {
            "sum": amount,
            "orderId": order_id,
            "shopId": self.shop_id,
            "hookUrl": self.payment_webhook,
            "failUrl": self.fail_url,
            "successUrl": self.success_url,
            "expire": expire,
            "customFields": custom_fields,
            "comment": comment,
        }

    def check_payout(self, order_id: str) -> PayoutStatusResponse:
        """"""
        query = {
            "shopId": self.shop_id,
            "orderId": order_id,
        }
        sign = self.__get_sign(query)
        header = self.__get_header(sign)
        response = post(f"{self.__site}/payoff/info",
                        headers=header, json=query)
        return PayoutStatusResponse(**response.json())

    def check_payment(self, order_id: str) -> PaymentStatusResponse:
        """"""
        query = {
            "shopId": self.shop_id,
            "orderId": order_id,
        }
        sign = self.__get_sign(query)
        header = self.__get_header(sign)
        response = post(f"{self.__site}/invoice/status",
                        headers=header, json=query)
        return PaymentStatusResponse(**response.json())

    def __get_payout_transfer(self, amount: float, order_id: str, service: str, wallet_to: str, subtract: str = 0) -> dict:
        """
        Генерация счета
        service: 
            [lava_payoff, qiwi_payoff, card_payoff]
        subtract: 
            0 - с суммы
            1 - с магазина
        """
        return {
            "amount": amount,
            "orderId": order_id,
            "shopId": self.shop_id,
            "service": service,
            "walletTo": wallet_to,
            "subtract": subtract,
            "hookUrl": "https://dosimple.io/bot/api/lava/payout"
        }

    def __get_sign(self, payout: dict):
        json_str = json.dumps(payout).encode()
        return hmac.new(bytes(self.key_secret, 'UTF-8'), json_str, hashlib.sha256).hexdigest()

    def generate_payment(self, amount: float, order_id: str, expire: int = 300, custom_fields: str = "", comment: str = "") -> PaymentResponse:
        """Сгенерировать счет"""
        payout = self.__get_payment(amount, order_id, expire, custom_fields, comment)
        sign = self.__get_sign(payout)
        header = self.__get_header(sign)
        response = post(f"{self.__site}/invoice/create", headers=header, json=payout)
        print(response.json())
        return PaymentResponse(**response.json())

    def get_balance(self) -> Balance:
        """Сгенерировать счет"""
        query = {
            "shopId": self.shop_id
        }
        sign = self.__get_sign(query)
        header = self.__get_header(sign)
        response = post(f"{self.__site}/shop/get-balance",
                        headers=header, json=query)
        return Balance(**response.json())

    def get_tariffs(self) -> Tariffs:
        """Сгенерировать счет"""
        query = {
            "shopId": self.shop_id
        }
        sign = self.__get_sign(query)
        header = self.__get_header(sign)
        response = post(f"{self.__site}/payoff/get-tariffs",
                        headers=header, json=query)
        return Tariffs(**response.json())

    def generate_payout(self, amount: float, order_id: str, service: WalletTypeEnum, wallet_to: str, subtract: SubtractEnum = SubtractEnum.Payment) -> PayoutResponse:
        payout = self.__get_payout_transfer(amount, order_id, service, wallet_to, subtract)
        sign = self.__get_sign(payout)
        header = self.__get_header(sign)
        response = post(f"{self.__site}/payoff/create", headers=header, json=payout)
        print(response.json())
        return PayoutResponse(**response.json())
