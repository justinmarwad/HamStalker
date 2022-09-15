import requests
from stem import Signal
from stem.control import Controller

class TorHandler:
    def __init__(self, password="PASSWORD"):
        self.password = password
        
        self.session = requests.session()
        self.session.proxies={"http": "socks5://localhost:9050", "https": "socks5://localhost:9050"}

    def get_session(self):
        self.change_session() # auto change session 
        return self.session

    def change_session(self): 
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password=self.password)
            controller.signal(Signal.NEWNYM)
