import base64
import hashlib
import logging
import os
import secrets
import sys
import traceback
import uuid
import re
from datetime import datetime, timedelta, date
from urllib.parse import quote

import dateutil.parser
import pytz
import xmltodict
import yaml

from sysnet_pyutils.ident import generate_pid, check_pid, correct_pid, generate_id12

TZ = os.getenv('TZ', 'Europe/Prague')
DEBUG = os.getenv("DEBUG", 'True').lower() in ('true', '1', 't')
LOG_FORMAT = os.getenv('LOG_FORMAT', '%(asctime)s - %(levelname)s in %(module)s: %(message)s')
LOG_DATE_FORMAT = os.getenv('LOG_DATE_FORMAT', '%d.%m.%Y %H:%M:%S')
LOG_FILE = os.getenv('LOG_FILE', None)


class ConfigError(Exception):
    pass


class Singleton(type):
    """
    Třída Singleton
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConfigFlag(object, metaclass=Singleton):
    def __init__(self):
        self.started = True
        self.config = False
        logging.info('ConfigFlag constructor')


CF = ConfigFlag()


class Config(object, metaclass=Singleton):
    """
    Třída Config: správa konfigurace
    """

    def __init__(self, config_path=None, config_dict=None):
        if not CF.config:
            self.loaded = False
            if config_path in [None, '']:
                config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf', 'config.yml')
            self.config_path = config_path
            # Path(self.config_path).mkdir(parents=True, exist_ok=True)
            if config_dict is None:
                logging.warning('Input configuration is empty')
                self.config = {}
            self.config_input = config_dict
            self.init()
            CF.config = True
            logging.info('Config initialized')
        else:
            logging.info('Config is already initialized')

    def init(self):
        if os.path.isfile(self.config_path):
            with open(self.config_path, "r") as yamlfile:
                out = yaml.load(yamlfile, Loader=yaml.FullLoader)
            if bool(out):
                self.config = out
                self.loaded = True
                logging.info('Configuration loaded')
                return self
            self.loaded = False
        self.config = self.config_input
        self.store()
        self.loaded = True
        return self

    def store(self):
        with open(self.config_path, 'w') as yamlfile:
            yaml.dump(self.config, yamlfile)
        logging.info('Configuration stored')
        return True

    def delete_file(self):
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
            return True
        else:
            logging.error('Configuration file does not exist')
            return False

    def replace(self, config_dict):
        self.delete_file()
        self.config = config_dict
        self.store()


def url_safe(url):
    """
    Upraví URL, aby beobsahovalo nepovolené znaky

    :param url: Vstupní URL
    :return: Upravené URL
    """
    return quote(url, safe='/:?=&')


def who_am_i():
    """
    Vrátí název funkce

    :return: název funkce, odkud je voláno
    """
    stack = traceback.extract_stack()
    file_name, code_line, func_name, text = stack[-2]
    return func_name


def unique_list(input_list):
    """
    Vyřadí opakující se položky ze seznamu

    :param input_list:   Vstupní seznam
    :return: Unikátní seznam
    """
    if not isinstance(input_list, list):
        return input_list
    out = []
    for x in input_list:
        if x not in out:
            out.append(x)
    return out


def api_keys_init(agenda='main', amount=4):
    """
    Vygeneruje klíče pro API

    :param agenda: Název agendy, pro kterou se klíče generují
    :param amount: Počet vygenerovaných klíčů
    :return: seznam vygenerovaných klíčů
    """
    out = []
    for i in range(amount):
        out.append(api_key_next('{} {}'.format(agenda, i + 1)))
    return out


def uuid_next(uuid_type=1):
    """
    Vygeneruje UUID

    :param uuid_type: Lze použít pouze typ 1 nebo 4
    :return: uuid
    """
    if uuid_type == 1:
        out = uuid.uuid1()
    else:
        out = uuid.uuid4()
    return out


def pid_next():
    """
    Vygeneruje korektní PID

    :return:    PID
    """
    return generate_pid()


def pid_check(pid):
    """
    Zkontroluje korektnost PID

    :param pid: Vstupní PID
    :return: True/False
    """
    return check_pid(pid)


def pid_correct(pid):
    """
    Opraví PID

    :param pid: Vstupní PID
    :return: Opravený PID
    """
    return correct_pid(pid)


def id12_next(three_char_prefix=None):
    """
    Vygeneruje korektní 12místný alfanumerický identifikátor s pevným prefixem

    :param three_char_prefix:   Tříznakový prefix identifikátoru
    :return:    12místný alfanumerický identifikátor
    """
    return generate_id12(three_char_prefix=three_char_prefix)


def api_key_next(name, length=16):
    """
    Vygeneruje slovník API key {<API Key>: <name>}

    :param name:    Název API klíče
    :param length:  Dělka API klíče
    :return:    Slovník {<API Key>: <name>}
    """
    out = {api_key_generate(length=length): name}
    return out


def api_key_generate(length: int):
    """
    vygeneruje API klíč

    :param length: Dělka API klíče
    :return: API Key
    """
    return secrets.token_urlsafe(length)


def hash_md5(text):
    """
    Vytvoří md5 checksum ze zdrojového textu
    :param text:
    :return:
    """
    if text is None:
        return None
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def hash_sha1(text):
    if text is None:
        return None
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def hash_sha256(text):
    if text is None:
        return None
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hash_sha384(text):
    if text is None:
        return None
    return hashlib.sha384(text.encode("utf-8")).hexdigest()


def is_valid_uuid(value):
    """
    Kontrola validity uuid

    :param value:
    :return:
    """
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False


def is_valid_pid(value):
    """
    Kontrola validity PID
    :param value:
    :return:
    """
    pattern = '^[A-Z,0-9][A-Z,0-9]{10}[A-Z,0-9]$'
    return bool(re.search(pattern, value))


def is_valid_ico(ico):
    """
    Kontrola validity IČO

    :param ico:
    :return:
    """
    __name__ = who_am_i()
    if len(ico) > 8:
        # icoTooLong
        return False
    try:
        digits = list(map(int, list(ico.rjust(8, "0"))))
    except ValueError:
        # icoNotNumber
        logging.error('{} - ICO invalid (not numeric): {}'.format(__name__, ico))
        return False
    remainder = sum([digits[i] * (8 - i) for i in range(7)]) % 11
    cksum = {0: 1, 10: 1, 1: 0}.get(remainder, 11 - remainder)
    if digits[7] != cksum:
        # icoBadChecksum
        logging.error('{} - ICO invalid (bad checksum): {}/{}{}'.format(__name__, ico, ico[:7], cksum))
        return False
    return True


def repair_ico(ico):
    """
    Opraví IČO

    :param ico:
    :return:
    """
    __name__ = who_am_i()
    if len(ico) > 8:
        # icoTooLong
        return None
    try:
        digits = list(map(int, list(ico.rjust(8, "0"))))
    except ValueError:
        # icoNotNumber
        logging.error('{} - ICO invalid (not numeric): {}'.format(__name__, ico))
        return None
    remainder = sum([digits[i] * (8 - i) for i in range(7)]) % 11
    cksum = {0: 1, 10: 1, 1: 0}.get(remainder, 11 - remainder)
    if digits[7] != cksum:
        # icoBadChecksum
        logging.error('{} - ICO invalid (bad checksum): {}/{}{}'.format(__name__, ico, ico[:7], cksum))
        return '{}{}'.format(ico[:7], cksum)
    return ico


def iso_to_local_datetime(isodate):
    """
    ISO string datum do lokálního datetime

    :param isodate: Textové datum v ISO
    :return: lokální datetime
    """
    if isodate is None:
        return None
    local_tz = pytz.timezone(TZ)
    ts = dateutil.parser.parse(isodate)
    out = ts.astimezone(local_tz)
    return out


def convert_hex_to_int(id_hex):
    """
    KOnvertuje hex string na int

    :param id_hex:  Hexadecimální string
    :return: int
    """
    id_int = int(id_hex, base=16)
    return id_int


def increment_date(date_str=None, days=1):
    """
    Inkrementuje datum v textovém formátu ISO o daný počet dní

    :param date_str:    ISO datum v textovém formátu ISO
    :param days:        počet dní
    :return:        ISO datum v textovém formátu ISO
    """
    if date_str is None:
        return None
    if days is None:
        return date_str
    d = datetime.strptime(date_str, '%Y-%m-%d')
    out = d + timedelta(days=days)
    return out.date().isoformat()


def today():
    """
    Vrací ISO 8601 datum dnešního dne

    :return:    ISO 8601 datum dnešního dne
    """
    out = datetime.now()
    return out.date().isoformat()


def tomorrow():
    """
    Vrací ISO 8601 datum zítřejšího dne

    :return:    ISO 8601 datum
    """
    return increment_date(date_str=today(), days=1)


def cs_bool(value=None):
    """
    Vrátí českou textovou hodnotu 'ano'/'ne' pokud je bool(value) True/False

    :param value:  Obecný objekt
    :return:    'ano' or 'ne'
    """
    out = 'ne'
    if bool(value):
        out = 'ano'
    return out


def cron_to_dict(cron):
    """
    Konvertuje cron text do do slovníku

    :param cron: cron text (například '35 21 * * *')
    :return:    dict of cron
    """
    cron_list = cron.split(' ')
    if len(cron_list) != 5:
        return None
    out = {
        'minute': cron_list[0],
        'hour': cron_list[1],
        'day': cron_list[2],
        'month': cron_list[3],
        'day_of_week': cron_list[4]
    }
    return out


def date_to_datetime(date_value):
    """
    Konvertuje date na datetime v lokální časové zóně
    :param date_value:  hodntoda
    :return:        hodnota date v lokální časové zóně
    """
    if date_value is None:
        return None
    out = None
    if type(date_value).__name__ == 'date':
        args = date_value.timetuple()[:6]
        out = datetime(*args, tzinfo=pytz.timezone(TZ))
    elif type(date_value).__name__ == 'datetime':
        out = date_value
    return out


def date_to_iso(date_value):
    """
    Konvertuje hodnotu typu date nebo datetime na ISO string

    :param date_value:
    :return:    hodnota ve formátu ISO
    """
    if date_value is None:
        return None
    if isinstance(date_value, date) or isinstance(date_value, datetime):
        return date_value.isoformat()
    return None


def remove_empty(source_list):
    """
    Odstraní prázdné položky ze seznamu

    :param source_list:
    :return:
    """
    if source_list is None:
        return None
    target_list = []
    for item in source_list:
        if item is not None:
            if bool(item):
                target_list.append(item)
    return target_list


def is_base64(body):
    """
    Kontrola, zda jsou data kódována base64

    :param body:
    :return:
    """
    try:
        if isinstance(body, str):
            # If there's any unicode here, an exception will be thrown and the function will return false
            sb_bytes = bytes(body, 'ascii')
        elif isinstance(body, bytes):
            sb_bytes = body
        else:
            raise ValueError("Argument must be string or bytes")
        return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
    except ValueError as e:
        logging.error('Base64: {}'.format(e))
        return False


def to_base64(body):
    """
    Zajistí, aby data byla v base64

    :param body:
    :return:
    """
    if is_base64(body=body):
        return body
    try:
        if isinstance(body, str):
            # If there's any unicode here, an exception will be thrown and the function will return false
            sb_bytes = bytes(body, 'ascii')
        elif isinstance(body, bytes):
            sb_bytes = body
        else:
            raise ValueError("Argument must be string or bytes")
        return base64.b64encode(sb_bytes)
    except ValueError as e:
        logging.error('Base64: {}'.format(e))
        return None


def encode_string_b64(data: str, encoding='utf-8'):
    """
    Zakóduje string do base64

    :param data:
    :param encoding:
    :return:
    """
    data_bytes = data.encode(encoding=encoding)
    out_bytes = base64.b64encode(data_bytes)
    out = str(out_bytes, encoding)
    return out


def decode_b64_string(b64_data: str, encoding='utf-8'):
    """
    Dekóduje base64 data na string

    :param b64_data:
    :param encoding:
    :return:
    """
    data_bytes = b64_data.encode(encoding=encoding)
    out_bytes = base64.b64decode(data_bytes)
    out = str(out_bytes, encoding)
    return out


def encode_file_b64(filepath, encoding='utf-8'):
    """
    Načte soubor do base64

    :param filepath:
    :param encoding:
    :return:
    """
    with open(filepath, 'rb') as data_file:
        encoded = base64.b64encode(data_file.read())
    out = str(encoded, encoding)
    return out


def decode_b64_to_file(b64_data: str, filepath, encoding='utf-8'):
    """
    Uloží base64 data do souboru

    :param b64_data:
    :param filepath:
    :param encoding:
    :return:
    """
    data_bytes = b64_data.encode(encoding=encoding)
    out_bytes = base64.b64decode(data_bytes)
    with open(filepath, "wb") as binary_file:
        binary_file.write(out_bytes)
    return filepath


class Log(object, metaclass=Singleton):
    """
    Singleton pro logování v celé aplikaci, kde je použit
    """

    def __init__(self, log_file=LOG_FILE):
        self.logger = logging.getLogger(__name__)
        console_handler = logging.StreamHandler(sys.stdout)
        file_handler = None
        if log_file is not None:
            file_handler = logging.FileHandler(log_file)
        if DEBUG:
            self.logger.setLevel(logging.DEBUG)
            console_handler.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
            console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
        console_handler.setFormatter(formatter)
        if file_handler is not None:
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        self.logger.addHandler(console_handler)
        if file_handler is not None:
            self.logger.addHandler(file_handler)
        self.logger.propagate = False
        self.logger.info('LOG created')

    def set_ext_logger(self, ext_logger):
        """
        Nastaví externí logger (například z Djanga nebo Flask)

        :param ext_logger: Esterní logger
        :return:
        """
        if ext_logger is not None:
            self.logger = ext_logger


def to_camel(s):
    temp = re.split('_+', s)
    out = temp[0] + ''.join(map(lambda x: x.title(), temp[1:]))
    return out


def to_snake(s):
    return re.sub('([A-Z]\w+$)', '_\\1', s).lower()


def to_snake_dict(d):
    if isinstance(d, list):
        return [to_snake_dict(i) if isinstance(i, (dict, list)) else i for i in d]
    return {to_snake(a): to_snake_dict(b) if isinstance(b, (dict, list)) else b for a, b in d.items()}


def to_camel_dict(d):
    if isinstance(d, list):
        return [to_camel_dict(i) if isinstance(i, (dict, list)) else i for i in d]
    return {to_camel(a): to_camel_dict(b) if isinstance(b, (dict, list)) else b for a, b in d.items()}


def xml_to_dict(xml_text):
    """
    Parsuje XML string do XML dictionary
    :param xml_text:    XML text
    :return:    XML dictionary
    """
    return xmltodict.parse(xml_text)


def dict_to_xml(xml_dict):
    """
    Parsuje XML dict do XML textu

    :param xml_dict:    XML dictionary
    :return:    XML text
    """
    return xmltodict.unparse(xml_dict)


# verze 1.0.4 =================================================================

ORDER_BASE = 26
CHAR_BASE = 65


def order_to_cites(order: int):
    """
    Konvertuje celočíselnou hodnotu na písmennou

    :param order: celočíselná hodnota např. 1458
    :return:    znaková hodnota např. 'BDB'
    """
    if order is None:
        raise ValueError('Missing value to convert')
    if order < 1:
        raise ValueError('Invalid value to convert: {}'.format(order))
    alpha = []
    for i in range(ORDER_BASE):
        alpha.append(chr(CHAR_BASE + i))
    work = order
    remainder = work % ORDER_BASE
    divide = work // ORDER_BASE
    out = ''
    while (divide > 0) or (remainder > 0):
        if (divide > 0) and (remainder == 0):
            out = '{}{}'.format(alpha[ORDER_BASE - 1], out)
            work = divide - 1
        elif remainder > 0:
            out = '{}{}'.format(alpha[remainder - 1], out)
            work = divide
        remainder = work % ORDER_BASE
        divide = work // ORDER_BASE
    return out


def cites_to_order(cites: str):
    """
    Konvertuje písmennou hodnotu na celočíselnou
    
    :param cites:   znaková hodnota např. 'BDB' 
    :return:    celočíselná hodnota např. 1458
    """
    if cites is None:
        raise ValueError('Missing value to convert')
    pattern = r'^[a-zA-Z]+$'
    m = re.match(pattern, cites)
    if m is None:
        raise ValueError('Invalid value to convert: {}'.format(cites))
    cites = cites.upper()
    characters = []
    characters.extend(cites)
    i = 0
    out = 0
    for item in reversed(characters):
        out += (ord(item) - CHAR_BASE + 1) * ORDER_BASE ** i
        i += 1
    return out
