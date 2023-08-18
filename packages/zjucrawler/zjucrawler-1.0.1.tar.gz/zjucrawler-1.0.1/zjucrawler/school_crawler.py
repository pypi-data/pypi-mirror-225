# A simple library for fetching data from zju school website
# TODO: school official site monitoring
# TODO: deadlines query
# TODO: school activities announcement/subscription
### Non-firstplace requirements ###
# TODO: McDonald tracking
#! TODO: use copyreg instead of native pickle
import asyncio
import bisect
import json
import os
import pickle
import re
from collections import namedtuple
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import wraps
from itertools import chain
from typing import Callable, Iterable, Iterator, Optional, Tuple
from weakref import WeakKeyDictionary

import aiohttp
import execjs
import pytz
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from sortedcontainers import SortedDict
from webdriver_manager.chrome import ChromeDriverManager

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
}
# WEBDRIVER_PATH = "./chromedriver"
# Deprecated, may enable it when using legacy selenium webdriver
ECRYPTION_FILE = os.path.join(PACKAGE_DIR, 'security.js')
CACHE_FILE = os.path.join(PACKAGE_DIR, "{username}.cache")

ZJUAM_URL = "https://zjuam.zju.edu.cn"
LOGIN_URL = ZJUAM_URL + "/cas/login?service=http://jwbinfosys.zju.edu.cn/default2.aspx"
RSA_PUBKEY_URL = ZJUAM_URL + "/cas/v2/getPubKey"

JWBINFO_URL = "http://jwbinfosys.zju.edu.cn"
GRADES_URL = JWBINFO_URL + f"/xscj.aspx"
EXAMS_URL = JWBINFO_URL + f"/xskscx.aspx"

INIT_GRADES_URL = "http://jwbinfosys.zju.edu.cn/default2.aspx"
INIT_EXAMS_URL = "http://jwbinfosys.zju.edu.cn/default2.aspx"

CHALAOSHI_URL = "https://chalaoshi.2799web.com/"
LOGIN_EXPIRED_KEYWORD = r"<title>Object moved</title>"
TIMEOUT = aiohttp.ClientTimeout(total=30, sock_connect=20, sock_read=20)

os.environ["EXECJS_RUNTIME"] = "Node"

Packed = namedtuple('Packed', ['ok', 'data'])


class LoginFailedException(Exception):
    pass


class NotLoggedInError(Exception):
    pass


class LoginStateExpiredException(Exception):
    pass


class TimedDataDescriptor(object):
    """Descriptor for date with last update time
    set: just set the data
    get: tuple (last update timestamp, data)
    """

    def __set_name__(self, owner, name):
        self.name = '_' + name
        self.last_update_name = '_time_' + name

    def __init__(self, data=None, data_factory: Optional[Callable] = None) -> None:
        self.last_update = datetime.timestamp(datetime.now())
        if data:
            self.initial_data = data
        elif data_factory:
            self.initial_data = data_factory()
        else:
            self.initial_data = None

    def __get__(self, obj, objtype): # can this be simplified? feels trivial when using it
        if obj is None:
            return self
        return (obj.__dict__.setdefault(self.last_update_name, None), obj.__dict__.setdefault(self.name, self.initial_data))

    def __set__(self, obj, value):
        obj.__dict__[self.name] = value
        obj.__dict__[self.last_update_name] = datetime.timestamp(
            datetime.now())


@dataclass
class Exam:
    code: Optional[str] = None
    name: Optional[str] = None
    term: Optional[str] = None
    time_final: Optional[str] = None
    location_final: Optional[str] = None
    seat_final: Optional[str] = None
    time_mid: Optional[str] = None
    location_mid: Optional[str] = None
    seat_mid: Optional[str] = None
    remark: Optional[str] = None
    is_retake: Optional[bool | str] = None
    credits: Optional[float | str] = None

    _datetime_mid: Optional[datetime | bool] = None  # False means no exam
    _datetime_final: Optional[datetime | bool] = None  # False means no exam

    @property
    def datetime_mid(self):
        if self._datetime_mid is not None:
            return self._datetime_mid
        self._datetime_mid = self.site_str2datetime(self.time_mid)
        return self._datetime_mid

    @property
    def datetime_final(self):
        if self._datetime_final is not None:
            return self._datetime_final
        self._datetime_final = self.site_str2datetime(self.time_final)
        return self._datetime_final

    @staticmethod
    def site_str2datetime(time_str):
        # format: YYYY年mm月dd日(HH:mm-HH:mm)
        if time_str is None:
            return False
        time_fmt = r"(?P<year>[0-9]{4})年(?P<month>[0-9]{1,2})月(?P<day>[0-9]{1,2})日\((?P<start_h>[0-9]{1,2}):(?P<start_m>[0-9]{1,2})-(?P<end_h>[0-9]{1,2}):(?P<end_m>[0-9]{1,2})\)"
        t = re.match(time_fmt, time_str)
        if t is None:
            return False
        t = t.groupdict()
        for k, v in t.items():
            t[k] = int(v)
        assert isinstance(t, dict)
        return datetime(year=t["year"], month=t["month"], day=t["day"],
                        hour=t["start_h"], minute=t["start_m"], second=0, tzinfo=pytz.timezone('Asia/Shanghai'))


@dataclass
class Course:
    # WARNING: CHANGE THE ORDER OF ARGS MAY RESULT IN ERROR, SINCE UNPACKING MAY OPERATED ON TUPLE
    code: Optional[str] = None
    name: Optional[str] = None
    score: Optional[str | float] = None
    credit: Optional[str | float] = None
    grade_point: Optional[str | float] = None
    re_exam_score: Optional[str | float] = None
    location: Optional[str] = None
    class_time: Optional[str] = None
    exam: Optional[str] = None
    book: Optional[str] = None
    aliases: Optional[str] = None


class Fetcher(object):
    exams = TimedDataDescriptor(data_factory=lambda: [])
    courses = TimedDataDescriptor(data_factory=lambda: [])
    
    def __init__(self, username=None, password=None, *, simulated=False):
        self.cookies = {}
        self.logged = False
        self.username = username
        self.password = password
        self.ttl = 10 * 60  # seconds
        self.IS_SIMULATED_LOGIN = simulated
        self._version = "1.0.0"

    @staticmethod
    def is_float(*args) -> bool:
        """If all the given arguments(strings) are valid float numbers, return True"""
        for num_str in args:
            try:
                _ = float(num_str)
            except ValueError:
                return False
        return True

    def serialize(self, file: str) -> None:
        if file is None:
            raise ValueError("No file specified")
        with open(file, 'wb') as f:
            pickle.dump(self.__dict__, file=f)

    def unserialize(self, file: str) -> None:
        if file is None:
            raise ValueError("No file specified")
        with open(file, 'rb') as f:
            try:
                saved = pickle.load(file=f)
                if saved["_version"] != self._version:
                    print("WARN: older version cache file")
                    return
            except:
                print("WARN: failed to recover account cache file.")
                return
            if not isinstance(saved, dict):
                raise ValueError("Not a valid fetcher store file")
            self.__dict__ |= saved

    async def simulated_login(self, username: str, password: str) -> Packed:
        # Not work behind a proxy.
        service = Service(ChromeDriverManager().install())
        options = Options()
        additional_options = [
            '--headless',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            'start-maximized',
            '--disable-extensions',
            '--disable-browser-side-navigation',
            'enable-automation',
            '--disable-infobars',
            'enable-features=NetworkServiceInProcess',
        ]
        for option in additional_options:
            options.add_argument(option)
        driver = webdriver.Chrome(service=service, options=options)
        try:
            driver.get(LOGIN_URL)
            driver.find_element(By.ID, "username").send_keys(username)
            driver.find_element(By.ID, "password").send_keys(password)
            driver.find_element(By.ID, "dl").click()
            cookies = driver.get_cookies()
        except Exception as e:
            return Packed(False, repr(e))
        else:
            if "iPlanetDirectoryPro" not in str(cookies):
                # Got invalid cookie
                return Packed(False, f"Wrong password/username! cookies:{cookies}")
            else:
                simplified_cookies = {
                    cookie["name"]: cookie["value"] for cookie in cookies}
                return Packed(True, simplified_cookies)

    async def post_login(self, username: str, password: str) -> Packed:
        # @TODO injection prevention
        assert isinstance(password, str)

        async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(), headers=DEFAULT_HEADERS, timeout=TIMEOUT) as session:
            # _pv0 cookie need to be carried to get a right key pair
            async with session.get(RSA_PUBKEY_URL) as r:
                res_text = await r.text(encoding='utf-8')
                result = json.loads(res_text)
                modulus_hex: str = result['modulus']
                exponent_hex: str = result['exponent']
                for _, cookie in r.cookies.items():
                    session.cookie_jar.update_cookies(
                        {cookie.key: cookie.value})

            enc_script = open(ECRYPTION_FILE, encoding="utf-8").read()
            ctx = execjs.compile(enc_script)
            encrypted_pwd = ctx.call(
                "zjuish_encryption", password, exponent_hex, modulus_hex)

            async with session.get(LOGIN_URL) as r:  # get the 'execution' segment
                res_text = await r.text(encoding='utf-8')
                execution = re.search(
                    r'name="execution" value="(.*?)"', res_text).group(1)  # type: ignore
                for _, cookie in r.cookies.items():
                    session.cookie_jar.update_cookies(
                        {cookie.key: cookie.value})
            data = {
                'username': username,
                'password': encrypted_pwd,
                'authcode': '',
                            'execution': execution,
                            '_eventId': 'submit'
            }
            async with session.post(LOGIN_URL, data=data, allow_redirects=True) as r:  # login
                for _, cookie in r.cookies.items():
                    session.cookie_jar.update_cookies(
                        {cookie.key: cookie.value})
            cookies = session.cookie_jar.filter_cookies(
                ZJUAM_URL)  # type: ignore
            if "iPlanetDirectoryPro" not in str(cookies):
                # Got invalid cookie
                return Packed(False, f"Wrong password/username! Status Code:{r.status}\
                    (expected to be 302) , cookies:{cookies}")
            else:
                simplified_cookies = {
                    cookie.key: cookie.value for _, cookie in cookies.items()}
                return Packed(True, simplified_cookies)

    async def login(self, username, password):
        self.cookies = {}
        if self.IS_SIMULATED_LOGIN == True:
            login_result = await self.simulated_login(username, password)
        else:
            login_result = await self.post_login(username, password)
        if not login_result[0]:
            raise LoginFailedException(
                "Login failed. Maybe the password or username is NOT correct?")
        else:
            self.cookies = login_result[1]
            self.logged = True
            self.username = username
            self.password = password
            self.serialize(CACHE_FILE.format(username=self.username))

    ###
    # Decorators

    @staticmethod
    # FIXME: The cache may be out-dated and need to be updated
    def login_acquired(func):
        @wraps(func)
        async def wrapper(self: 'Fetcher', *args, **kwargs):  # TODO: Reconstruction needed
            if not self.logged or self.username is None:
                try:
                    pwd_provided = self.password
                    self.unserialize(CACHE_FILE.format(
                        username=self.username))
                    if pwd_provided is not None and pwd_provided != "":
                        self.password = pwd_provided
                except FileNotFoundError:
                    pass
                except:
                    print(
                        "WARNING: Unable to recover the cache file for login infos. Has it been modified inadvertently?")
                    pass
            if not self.logged:
                if self.password is not None and self.username is not None:
                    await self.login(self.username, self.password)
                if not self.logged:
                    raise NotLoggedInError("You shall log-in first.")
            try:
                res = await func(self, *args, **kwargs)
                return res
            except LoginStateExpiredException:
                print("Try to relogin.")
                await self.login(self.username, self.password)
                res = await func(self, *args, **kwargs)
                return res
        return wrapper

    @staticmethod
    def cache_after_exec(func):
        @wraps(func)
        async def wrapper(self: 'Fetcher', *args, **kwargs):
            res = await func(self, *args, **kwargs)
            self.serialize(CACHE_FILE.format(username=self.username))
            return res
        return wrapper
    ###
    # Exam ops

    @login_acquired
    async def get_exams(self, year: Optional[str] = None, term: Optional[str] = None) -> Iterable[Exam]:
        """Get student exams info(time, form, remark).\n
        If year or term arg is left as None, it means: all!
        """
        EXAM_SEG_PATTERN = r'class="datagridhead">.*?</tr>(.*?)</table></div>'
        YEAR_SEG_PATTERN = r'id="xnd">(.*?)</select>'
        TERM_SEG_PATTERN = r'id="xqd">(.*?)</select>'
        VALUE_PATTERN = r'value="(.*?)"'
        EXAM_EXTRACT_PATTERN = r"""<td>(?P<code>.*?)</td><td>(?P<name>.*?)</td><td>(?P<credits>.*?)</td><td>(?P<is_retake>.*?)</td><td>(.*?)</td><td>(?P<term>.*?)</td><td>(?P<time_final>.*?)</td><td>(?P<location_final>.*?)</td><td>(?P<seat_final>.*?)</td><td>(?P<time_mid>.*?)</td><td>(?P<location_mid>.*?)</td><td>(?P<seat_mid>.*?)</td><td>(?P<remark>.*?)</td>"""

        headers = DEFAULT_HEADERS | {
            "Accept": """text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9""",
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "keep-alive",
            "Proxy-Connection": "keep-alive",
        }

        def exclude_nbsp(d: dict):
            return {k: (None if v == "&nbsp;" else v.replace("&nbsp;", " ")) for k, v in d.items()}

        async with aiohttp.ClientSession(cookies=self.cookies, headers=headers, timeout=TIMEOUT) as session:
            async with session.get(INIT_EXAMS_URL) as r:
                # get ASP.NET_SessionID cookie
                res_text = await r.text()
                for _, cookie in r.cookies.items():
                    session.cookie_jar.update_cookies(
                        {cookie.key: cookie.value})
                    self.cookies[cookie.key] = cookie.value

            async with session.get(EXAMS_URL + f"?xh={self.username}") as r:
                res_text = await r.text()
                if LOGIN_EXPIRED_KEYWORD in res_text:
                    raise LoginStateExpiredException

            # IMPORTANT: THE DATA IN THE INITIAL VIEW MUST BE CAPTURED

            if year is None:
                # get all possible years
                year_seg = re.search(
                    YEAR_SEG_PATTERN, res_text, flags=re.DOTALL | re.M).group(1)  # type: ignore
                years = re.findall(VALUE_PATTERN, year_seg,
                                   flags=re.DOTALL | re.M)
            else:
                years = [year]

            if term is None:
                # get all possible terms
                term_seg = re.search(
                    TERM_SEG_PATTERN, res_text, flags=re.DOTALL | re.M).group(1)  # type: ignore
                terms = re.findall(VALUE_PATTERN, term_seg,
                                   flags=re.DOTALL | re.M)
            else:
                terms = [term]

            # Chaining all exams in a iterator
            def extract_exams(text: str) -> Iterator[Exam]:
                exam_seg = re.search(
                    EXAM_SEG_PATTERN, text, flags=re.M | re.DOTALL)
                if exam_seg is None:
                    return iter(())
                else:
                    exam_seg = exam_seg.group(1)  # type: ignore
                return (Exam(**exclude_nbsp(exam.groupdict())) for exam in re.finditer(EXAM_EXTRACT_PATTERN, exam_seg))

            res_iter = extract_exams(res_text)
            for year in years:
                for term in terms:
                    viewstate = re.search(
                        r'name="__VIEWSTATE" value="(.*?)"', res_text).group(1)  # type: ignore
                    data = {
                        "__EVENTTARGET": "xnd",
                        "__EVENTARGUMENT": "",
                        "__VIEWSTATE": viewstate,
                        "xnd": year,
                        "xqd": term,
                    }
                    encoded_data = aiohttp.FormData(data, charset="gb2312")
                    async with session.post(EXAMS_URL + f"?xh={self.username}", data=encoded_data) as r:
                        res_text = await r.text()

                    res_iter = chain(res_iter, extract_exams(res_text))
                    # I don't know why the formatter makes it looks like s**t, but let it be.
                    # TODO: using priority queue and sort by time
            res = list(res_iter)
            self.exams = res
            return iter(res)

    @cache_after_exec
    @login_acquired
    # TODO: Fine-grained caching for exams (year/term)
    async def get_all_exams(self) -> Tuple[float, Iterable[Exam]]:
        up_time, cached_exams = self.exams
        if up_time and datetime.timestamp(datetime.now()) - up_time < self.ttl:
            return up_time, iter(cached_exams)
        res = list(await self.get_exams(None, None))
        self.exams = res
        return self.exams
            
    ###

    @cache_after_exec
    @login_acquired
    async def get_timetable(self) -> list[dict]:
        """Get student course timetable"""
        raise NotImplementedError

    @cache_after_exec
    @login_acquired
    async def get_grades(self) -> Iterable[Course]:
        """Get student grades and scores of each course"""
        up_time, cached_courses = self.courses
        if up_time and datetime.timestamp(datetime.now()) - up_time < self.ttl:
            # FIXME: using a decorator to declare a specific cache key; return expired cache as a fallback when update failed
            return iter(cached_courses)
        async with aiohttp.ClientSession(cookies=self.cookies, headers=DEFAULT_HEADERS, timeout=TIMEOUT) as session:
            # @TODO synchronization of self.cookies & parameter is overcomplex. Modify it!
            async with session.get(INIT_GRADES_URL) as r:
                # get ASP.NET_SessionID cookie
                res_text = await r.text()
                for _, cookie in r.cookies.items():
                    session.cookie_jar.update_cookies(
                        {cookie.key: cookie.value})
                    self.cookies[cookie.key] = cookie.value
                    # print(cookie.key, cookie.value)

            async with session.get(GRADES_URL + f"?xh={self.username}") as r:
                res_text = await r.text()
                if LOGIN_EXPIRED_KEYWORD in res_text:
                    raise LoginStateExpiredException
            viewstate = re.search(
                r'name="__VIEWSTATE" value="(.*?)"', res_text).group(1)  # type: ignore
            button2 = re.search(
                r'name="Button2" value="(.*?)"', res_text).group(1)  # type: ignore
            data = {
                "__VIEWSTATE": viewstate,
                "ddlXN": "",
                "ddlXQ": "",
                "txtQSCJ": "",
                "txtZZCJ": "",
                "Button2": button2,  # text of "在校成绩查询", actually a fixed value
            }

            async with session.post(GRADES_URL + f"?xh={self.username}", data=data) as r:
                text = await r.text()
                pattern = r"<td>(?P<code>.*?)</td><td>(?P<name>.*?)</td><td>(?P<score>.*?)</td><td>(?P<credit>.*?)</td><td>(?P<grade_point>.*?)</td><td>(?P<re_exam_score>.*?)</td>"
            res = [Course(**course.groupdict())
                            for course in re.finditer(pattern, text)]
            self.courses = res
            return iter(res)

    @login_acquired
    async def get_GPA(self) -> float:
        credits_sum = 0
        grade_points_sum_weighted = 0.0
        for course in await self.get_grades():
            if self.__class__.is_float(course.score, course.credit, course.grade_point):
                assert course.credit and course.grade_point
                credits_sum += float(course.credit)
                grade_points_sum_weighted += float(course.credit) * \
                    float(course.grade_point)
        if credits_sum != 0:
            return grade_points_sum_weighted / credits_sum
        else:
            return 0.0
    
    @login_acquired
    async def get_abroad_GPA_new(self) -> float:
        """
        Abroad GPA (4.3) since 2022.
        """
        SCORE_MAP = SortedDict({
            95 : 4.3,
            92 : 4.2,
            89 : 4.1,
            86 : 4.0,
            83 : 3.9,
            80 : 3.6,
            77 : 3.3,
            74 : 3,
            71 : 2.7,
            68 : 2.4,
            65 : 2.1,
            62 : 1.8,
            60 : 1.5,
            0 : 0,
        })
        credits_sum = 0
        grade_points_sum_weighted = 0.0
        def get_abroad_point(score: int|str):
            score = int(score)
            pos = SCORE_MAP.bisect(score)
            if pos!=0:
                return SCORE_MAP.values()[pos-1]
            else:
                raise ValueError("Invalid score when converting to grade point")
        
        for course in await self.get_grades():
            if self.__class__.is_float(course.score, course.credit, course.grade_point):
                assert course.credit and course.grade_point
                credits_sum += float(course.credit)
                grade_points_sum_weighted += float(course.credit) * \
                    float(get_abroad_point(course.score))
        if credits_sum != 0:
            return grade_points_sum_weighted / credits_sum
        else:
            return 0.0
    
    @login_acquired
    async def get_abroad_GPA_old(self) -> float:
        """
        Abroad GPA (4.0) before 2022.
        """
        SCORE_MAP = SortedDict({
            86 : 4.0,
            83 : 3.9,
            80 : 3.6,
            77 : 3.3,
            74 : 3.0,
            71 : 2.7,
            68 : 2.4,
            65 : 2.1,
            62 : 1.8,
            60 : 1.5,
            0 : 0,
        })
        credits_sum = 0
        grade_points_sum_weighted = 0.0
        def get_abroad_point(score: int|str):
            score = int(score)
            pos = SCORE_MAP.bisect(score)
            if pos!=0:
                return SCORE_MAP.values()[pos-1]
            else:
                raise ValueError("Invalid score when converting to grade point")
        
        for course in await self.get_grades():
            if self.__class__.is_float(course.score, course.credit, course.grade_point):
                assert course.credit and course.grade_point
                credits_sum += float(course.credit)
                grade_points_sum_weighted += float(course.credit) * \
                    float(get_abroad_point(course.score))
        if credits_sum != 0:
            return grade_points_sum_weighted / credits_sum
        else:
            return 0.0

    @login_acquired
    async def get_avg_score(self) -> float:
        credits_sum = 0
        grade_points_sum_weighted = 0.0
        for course in await self.get_grades():
            if self.__class__.is_float(course.score, course.credit, course.grade_point):
                assert course.credit and course.grade_point
                credits_sum += float(course.credit)
                grade_points_sum_weighted += float(course.credit) * \
                    float(course.score)
        if credits_sum != 0:
            return grade_points_sum_weighted / credits_sum
        else:
            return 0.0
        
    @login_acquired
    async def get_deadlines(self):
        raise NotImplementedError

    @login_acquired
    async def get_activities(self):
        raise NotImplementedError

    @login_acquired
    async def get_notice(self):
        raise NotImplementedError


if __name__ == '__main__':
    async def main():
        username = input("username>>>")
        pwd = input("pwd>>>")
        test = Fetcher(username, pwd, simulated=False)
        print(await test.get_GPA())
        print(await test.get_abroad_GPA_new())
        print(await test.get_abroad_GPA_old())
        print(await test.get_avg_score())
        exams = list(await test.get_all_exams())
        print(exams)
        print(test.__dict__)
        # print(exams[0].datetime_final)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
