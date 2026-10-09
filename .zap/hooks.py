from urllib.parse import urljoin


app_root = None


def zap_access_target(zap, target):
    global app_root
    app_root = target.rstrip("/") + "/"
    return zap, target


def _spa_target(target):
    root = app_root or target.rstrip("/") + "/"
    return urljoin(root, "start.mvc")


def zap_spider(zap, target):
    return zap, _spa_target(target)


def zap_client_spider(zap, target, max_time):
    return zap, _spa_target(target), max_time
