from fake_useragent import UserAgent


def build_fake_ua() -> str:
    ua = UserAgent()
    return ua.random

