

def check_error(data: dict):
    if data.status == 422:
        if "shopId" in data.error:
            raise Exception(", ".join(data.error['shopId']))
        elif "orderId" in data.error:
            raise Exception(", ".join(data.error['orderId']))
        else:
            raise Exception(str(data.error))
    if data.error:
        raise Exception(data.error)