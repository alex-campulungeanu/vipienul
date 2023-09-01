# import logging
import pywinauto
# from pywinauto import actionlogger
from pywinauto.keyboard import send_keys
import win32gui
import win32con
import sys
from libs.logger_service import logger

from modules.auth import authenticate
from constants import CONFIG_FILE, VPN_APP_PATH, LOGIN_FORM_NAME

# TODO: add timestamp to log
""" 
actionlogger.enable()
logger = logging.getLogger('pywinauto')
logger.handlers[0] = logging.FileHandler('log.txt') 
"""

logger.info('ceva scris sa fie')

def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        print ( hex( hwnd ), win32gui.GetWindowText( hwnd ) )
        
def main():
    auth_response = authenticate()
    if not auth_response.is_success:
        input(f'Email or passwor not filled, check {CONFIG_FILE}. \nEnter ENTER to quit.')
        sys.exit()

    app = pywinauto.Application(backend='uia', allow_magic_lookup=True)
    app.start(cmd_line=VPN_APP_PATH)
    app.connect(path=VPN_APP_PATH)

    connect_dlg = app.window(title='Cisco AnyConnect Secure Mobility Client')
    connect_dlg['Connect'].click()

    # app.window(handle=win)

    # win = app.window(best_match='Cisco AnyConnect Secure Mobility ClientDialog')
    login_form = app.window(best_match=LOGIN_FORM_NAME)
    # login_form.dump_tree() 
    login_form.print_control_identifiers()
    login_form['Edit'].wait("enabled", timeout=10)
    login_form['Edit'].set_text(auth_response.email)
    login_form['Next'].click()

    login_form['Edit'].wait("enabled")
    login_form['Edit'].set_text(auth_response.password)

    """ for some reason Sign in button is not recognize, even if he is visible in the page """
    # login_form['Sign in'].wait("enabled", timeout=10, retry_interval=10)
    # login_form['Sign in'].click()

    focused_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())  # type: ignore
    if focused_window == LOGIN_FORM_NAME:
        send_keys("{TAB}")
        send_keys("{TAB}")
        send_keys("{ENTER}")
        # print('befoire send keys  enter')
        # while True:
        #     time.sleep(2)
        #     cur_wind = win32gui.GetWindowText(win32gui.GetForegroundWindow()) # type: ignore
        #     print(cur_wind)
        #     if cur_wind == '4591048':
        #         send_keys("{ENTER}")
        #     # print(win32gui.GetFocus())
        #     # print(win32gui.GetForegroundWindow())
            
    else:
        vpn_wnd = win32gui.FindWindow(0, LOGIN_FORM_NAME)  # type: ignore
        win32gui.SetForegroundWindow(vpn_wnd) # type: ignore
        win32gui.ShowWindow(vpn_wnd, win32con.SW_RESTORE) # type: ignore
        # logger.info('Current focused  window is not Cisco AnyConnect Login')

if __name__ == '__main__':
    print('Start script')
    main()