from enum import StrEnum, IntEnum

# class PaymentStatusEnum(StrEnum):
#     created  = "created"
#     success  = "success"
#     rejected = "rejected "
    
class PaymentStatusEnum(IntEnum):
    success = 200
    order_id_must_be_uniq = 422
    sum_lower_then_min = 404
    
class TransactionStatus(StrEnum):
    created = "created"
    success = "success"
    
class WalletTypeEnum(StrEnum):
    lava_payoff = "lava_payoff"
    card_payoff = "card_payoff"
    qiwi_payoff = "qiwi_payoff"
    
class SubtractEnum(IntEnum):
    Payment = 0
    Magazine = 1