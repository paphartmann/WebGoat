import json
from urllib.parse import urljoin


app_root = None
primed_lessons = False


def zap_access_target(zap, target):
    global app_root
    app_root = target.rstrip("/") + "/"
    return zap, target


def _spa_target(target):
    root = app_root or target.rstrip("/") + "/"
    return urljoin(root, "start.mvc")


def _prime_authenticated_lessons(zap, target):
    global primed_lessons
    if primed_lessons:
        return

    root = app_root or target.rstrip("/") + "/"
    response = zap.urlopen(urljoin(root, "service/lessonmenu.mvc"))
    menu = json.loads(response)
    lesson_paths = [
        lesson["link"].split("#lesson/", 1)[1]
        for category in menu
        for lesson in category.get("children", [])
        if "#lesson/" in lesson.get("link", "")
    ]
    if not lesson_paths:
        raise RuntimeError("Authenticated ZAP session returned no WebGoat lesson links")

    for lesson_path in lesson_paths:
        content = zap.urlopen(urljoin(root, lesson_path))
        if not content or "name='username'" in content:
            raise RuntimeError(f"ZAP could not load authenticated lesson page: {lesson_path}")

    primed_lessons = True
    print(f"Primed {len(lesson_paths)} authenticated lesson pages for ZAP active scanning")


def zap_spider(zap, target):
    _prime_authenticated_lessons(zap, target)
    return zap, _spa_target(target)


def zap_client_spider(zap, target, max_time):
    _prime_authenticated_lessons(zap, target)
    return zap, _spa_target(target), max_time
