import os
import getpass
from dataclasses import dataclass

from constants import CONFIG_FILE

@dataclass
class AuthReturn:
    is_success: bool
    email: str
    password: str

def authenticate() -> AuthReturn:
    email = ''
    password = ''
    if os.path.isfile(CONFIG_FILE):
        file_vars = {}
        with open(CONFIG_FILE) as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                key, value = line.strip().split('=', 1)
                file_vars[key] = value
        email = file_vars['EMAIL']
        password = file_vars['PASSWORD']
    else:
        email = input('enter email: ')
        password = getpass.getpass('enter password: ')
        with open(CONFIG_FILE, 'w') as f:
            f.write(f'email={email}\n')
            f.write(f'password={password}')
    
    if email == '' or password == '':
        return AuthReturn(False, '', '')
    else:
        return AuthReturn(True, email, password)