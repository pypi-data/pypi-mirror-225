import time
from requests import JSONDecodeError
import requests
import random
from automation_utilities import Exceptions
from automation_utilities.Generator import generate_email, generate_password


def domains():
    return [element['domain'] for element in requests.get('https://api.mail.tm/domains').json()['hydra:member']]


class Account:

    def __init__(
            self,
            address: str = generate_email(random.choice(domains())),
            password: str = generate_password()
    ):
        self.address = address
        self.password = password
        data = {
            'address': address.lower(),
            'password': password
        }
        while True:
            try:
                self.id = requests.post('https://api.mail.tm/accounts', json=data).json()['id']
                break
            except KeyError:
                raise Exceptions.AccountError()
            except JSONDecodeError:
                pass
        while True:
            try:
                token = requests.post('https://api.mail.tm/token', json=data).json()['token']
                break
            except JSONDecodeError:
                pass
        self.headers = {'Authorization': f"Bearer {token}"}

    def messages(self, timeout: float = 30):
        start = time.time()
        while True:
            while True:
                try:
                    resoponse = requests.get('https://api.mail.tm/messages', headers=self.headers).json()
                    break
                except JSONDecodeError:
                    pass
                if time.time() - start > timeout:
                    raise TimeoutError
            if resoponse['hydra:totalItems'] > 0:
                messages = []
                for member in resoponse['hydra:member']:
                    url = f'https://api.mail.tm/messages/{member["id"]}'
                    while True:
                        try:
                            messages.append(requests.get(url, headers=self.headers).json()['html'])
                            break
                        except JSONDecodeError:
                            pass
                if resoponse['hydra:totalItems'] == 1:
                    return messages[0][0]
                else:
                    return messages[0]
            if time.time() - start > timeout:
                raise TimeoutError
