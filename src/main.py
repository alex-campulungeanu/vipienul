# import logging
import pywinauto
# from pywinauto import actionlogger
from pywinauto.keyboard import send_keys
import win32gui
import win32con
import os.path
import sys
import getpass

VPN_APP_PATH = r"C:\Program Files (x86)\Cisco\Cisco AnyConnect Secure Mobility Client\vpnui.exe"
CONFIG_FILE = 'vipienul.txt'
LOGIN_FORM_NAME = 'Cisco AnyConnect Login'
EMAIL = ''
PASSWORD = ''

if os.path.isfile(CONFIG_FILE):
    file_vars = {}
    with open(CONFIG_FILE) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            key, value = line.strip().split('=', 1)
            file_vars[key] = value
    EMAIL = file_vars['EMAIL']
    PASSWORD = file_vars['PASSWORD']
else:
    EMAIL = input('enter email: ')
    PASSWORD = getpass.getpass('enter password: ')
    with open(CONFIG_FILE, 'w') as f:
        f.write(f'EMAIL={EMAIL}\n')
        f.write(f'PASSWORD={PASSWORD}')

if EMAIL == '' or PASSWORD == '':
    input(f'Email or passwor not filled, check {CONFIG_FILE}. \nEnter ENTER to quit.')
    sys.exit()


# TODO: add timestamp to log
""" 
actionlogger.enable()
logger = logging.getLogger('pywinauto')
logger.handlers[0] = logging.FileHandler('log.txt') 
"""

def main():
    app = pywinauto.Application(backend='uia', allow_magic_lookup=True)
    app.start(cmd_line=VPN_APP_PATH)
    app.connect(path=VPN_APP_PATH)

    connect_dlg = app.window(title='Cisco AnyConnect Secure Mobility Client')
    connect_dlg['Connect'].click()

    # app.window(handle=win)

    # win = app.window(best_match='Cisco AnyConnect Secure Mobility ClientDialog')
    login_form = app.window(best_match=LOGIN_FORM_NAME)

    # login_form.dump_tree() 

    login_form['Edit'].wait("enabled")
    login_form['Edit'].set_text(EMAIL)
    login_form['Next'].click()

    login_form['Edit'].wait("enabled")
    login_form['Edit'].set_text(PASSWORD)

    """ for some reason Sign in button is not recognize, even if he is visible in the page """
    # login_form['Sign in'].wait("enabled", timeout=10, retry_interval=10)
    # login_form['Sign in'].click()

    focused_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())  # type: ignore
    if focused_window == LOGIN_FORM_NAME:
        send_keys("{TAB}")
        send_keys("{TAB}")
        send_keys("{ENTER}")
    else:
        vpn_wnd = win32gui.FindWindow(0, LOGIN_FORM_NAME)  # type: ignore
        win32gui.SetForegroundWindow(vpn_wnd) # type: ignore
        win32gui.ShowWindow(vpn_wnd, win32con.SW_RESTORE) # type: ignore
        # logger.info('Current focused  window is not Cisco AnyConnect Login')

if __name__ == '__main__':
    main()