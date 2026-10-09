def zap_spider(zap, target):
    return zap, target.rstrip("/") + "/start.mvc"


def zap_client_spider(zap, target, max_time):
    return zap, target.rstrip("/") + "/start.mvc", max_time
