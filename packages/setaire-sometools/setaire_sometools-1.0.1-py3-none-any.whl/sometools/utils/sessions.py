import re
import logging
import json
from requests import Session, Response
from requests.cookies import RequestsCookieJar
from requests.adapters import HTTPAdapter
from requests.structures import CaseInsensitiveDict

logger = logging.getLogger("sometools")


def create_cookies(cookieStr: str) -> RequestsCookieJar:
    """创建一个CookieJar实例对象

    Args:
        cookieStr (str): cookie字符串

    Returns:
        RequestsCookieJar: _description_
    """
    cookieJar = RequestsCookieJar()
    if cookieStr:
        cookieStr = cookieStr.strip()
        if cookieStr.startswith("[") and cookieStr.endswith("]"):
            cookies = json.loads(cookieStr)
            return create_cookies_by_list(cookies)

        for cookie in cookieStr.split(";"):
            res = re.search(r"([^=]+)=(.*)", cookie)
            if res:
                k, v = res.groups()
                cookieJar.set(k.strip(), v.strip())

    return cookieJar


def create_cookies_by_list(cookies: list) -> RequestsCookieJar:
    """创建一个CookieJar实例对象

    Args:
        cookies (str): cookie字符串
            用";"隔开

    Returns:
        RequestsCookieJar: _description_
    """
    cookieJar = RequestsCookieJar()
    for cookie in cookies:
        cookieJar.set(cookie["name"], cookie["value"])
    return cookieJar


class RestSession(Session):

    def __init__(self, timeout: float = None, max_retries: int = 0, headers: dict = None, is_raise_for_status: bool = True):
        """

        Args:
            timeout (float, optional): 默认超时时间
            max_retries (int, optional): 最大重试次数
            headers (dict, optional): 默认头部
            is_raise_for_status (bool, optional): 当http状态码错误时抛出异常
        """
        super().__init__()
        self.timeout = timeout
        self.is_raise_for_status = is_raise_for_status
        if max_retries > 0:
            self.mount('http://', HTTPAdapter(max_retries=max_retries))
            self.mount('https://', HTTPAdapter(max_retries=max_retries))
        if not headers:
            headers = {
                "origin": "https://www.bilibili.com",
                "referer": "https://www.bilibili.com",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            }
        self.headers = CaseInsensitiveDict(headers)

    def request(self, method: str, url: str, **kwargs) -> Response:
        kwargs.setdefault("timeout", self.timeout)
        params = kwargs.get('params') or ''
        logger.info(f"[{method.upper()}] {url} {params}")
        res = super().request(method, url, **kwargs)
        if self.is_raise_for_status:
            res.raise_for_status()
        return res
