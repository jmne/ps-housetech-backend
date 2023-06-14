import os

from dotenv import load_dotenv

load_dotenv('../../../.env')

http_proxy = os.getenv('HTTP_PROXY')
https_proxy = os.getenv('HTTPS_PROXY')

proxies = {
    'http': http_proxy,
    'https': https_proxy,
}
