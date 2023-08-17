from datetime import datetime
from dataclasses import dataclass, field
import json

from py_lava_api.enums import PaymentStatusEnum, TransactionStatus, WalletTypeEnum
from py_lava_api.utils import check_error

    

@dataclass
class Payment:
    id: str
    amount: float
    expired: datetime
    status: PaymentStatusEnum
    shop_id: str
    url: str
    comment: str or None
    merchant_name: str
    exclude_service: list or None
    include_service: list or None
    def __post_init__(self):
        self.amount = float(self.amount)
        self.expired = datetime.strptime(self.expired, "%Y-%m-%d %H:%M:%S")
    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)
    
@dataclass
class PaymentStatus:
    status: TransactionStatus
    error_message: str
    id: str
    shop_id: str
    amount: float
    expire: datetime
    order_id: str
    fail_url: str
    success_url: str
    hook_url: str
    custom_fields: str
    include_service: list or None
    exclude_service: list or None
    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)
    
@dataclass
class PaymentStatusResponse:
    data: PaymentStatus
    status: PaymentStatusEnum
    error: dict = field(default_factory=dict)
    status_check: bool = field(default=False)
    def __post_init__(self):
        check_error(self)    
    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)    

@dataclass
class PaymentResponse:
    data: Payment
    status: PaymentStatusEnum
    error: dict = field(default_factory=dict)
    status_check: bool = field(default=False)
    def __post_init__(self):
        check_error(self)    
    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)
    
@dataclass
class PayoutStatus:
    id: str
    orderId: str
    status: TransactionStatus
    wallet: str
    service: WalletTypeEnum 
    amountPay: float
    commission: float
    amountReceive: float
    tryCount: int
    errorMessage: str or None
    
@dataclass
class PayoutStatusResponse:
    data: PayoutStatus
    status: PaymentStatusEnum
    error: dict = field(default_factory=dict)
    status_check: bool = field(default=False)
    def __post_init__(self):
        check_error(self)    
    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

@dataclass
class PaymentWebhook:
    invoice_id: str
    order_id: str
    status: TransactionStatus
    pay_time: datetime
    amount: int
    custom_fields: str or None
    pay_service: str
    payer_details: str    
    credited: int
    def __post_init__(self):
        self.pay_time = datetime.strptime(self.pay_time, "%Y-%m-%d %H:%M:%S")
    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)
    
@dataclass
class PayoutWebhook:
    payoff_id: str
    status: TransactionStatus
    payoff_time: str
    payoff_service: str
    type: str
    credited: str
    order_id: str
    def __post_init__(self):
        self.payoff_time = datetime.strptime(self.payoff_time, "%Y-%m-%d %H:%M:%S")
    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


@dataclass
class PayoutDetail:
    payoff_id: str
    payoff_status: str
    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


@dataclass
class PayoutResponse:
    data: PayoutDetail
    status: PaymentStatusEnum
    error: dict = field(default_factory=dict)
    status_check: bool = field(default=False)
    def __post_init__(self):
        check_error(self)
        self.status = PaymentStatusEnum(self.status)
    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


@dataclass
class BalanceDetail:
    balance: float
    active_balance: float
    freeze_balance: float
    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


@dataclass
class Balance:
    data: BalanceDetail
    status: PaymentStatusEnum
    status_check: bool
    error: dict = field(default_factory=dict)
    status_check: bool = field(default=False)
    def __post_init__(self):
        check_error(self)
        self.data = BalanceDetail(**self.data)
    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

@dataclass
class Tariff:
    percent: int 
    min_sum: int 
    max_sum: int
    service: WalletTypeEnum
    fix: int
    title: str
    currency: str
    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)
    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

@dataclass
class Tariffs:
    data: list[Tariff]
    status: PaymentStatusEnum
    error: dict = field(default_factory=dict)
    status_check: bool = field(default=False)
    def __post_init__(self):
        check_error(self)
        print(self.data)
        self.data = [Tariff(**i) for i in self.data["tariffs"]]
    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)