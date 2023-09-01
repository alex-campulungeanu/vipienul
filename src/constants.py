import pathlib
import os

ROOT_DIR = pathlib.Path(__file__).parent.absolute()
VPN_APP_PATH = r"C:\Program Files (x86)\Cisco\Cisco AnyConnect Secure Mobility Client\vpnui.exe"
CONFIG_FILE = os.path.join(ROOT_DIR, '../vipienul.txt')
LOGIN_FORM_NAME = 'Cisco AnyConnect Login'
LOG_FILE_PATH = os.path.join(ROOT_DIR, '../logs/loguru.log')
EMAIL = ''
PASSWORD = ''