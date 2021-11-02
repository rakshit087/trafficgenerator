import sys
import random
import time
from stem import Signal
from stem.control import Controller
import requests
from fake_useragent import UserAgent

address = input("Enter the Web Address of your Site: ")
views = int(input("How many views you want: "))


# Renew the Tor Connection
def renew_connection():
    with Controller.from_port(address="127.0.0.1", port=9051) as controller:
        controller.authenticate(password="")
        controller.signal(Signal.NEWNYM)
        controller.signal(Signal.HUP)
        time.sleep(2)


# Start a new session
def tor_session():
    session = requests.session()
    session.proxies = {}
    session.proxies['http'] = 'socks5://localhost:9050'
    session.proxies['https'] = 'socks5://localhost:9050'
    return session


def visit():
    for num in range(views):
        ua = UserAgent()
        header = {}
        # Visits with random header
        header['User-Agent'] = ua.random
        session = tor_session()
        session.get(address, headers=header)
        time.sleep(10)
        print(num+1)
        # Renews the tor connection for every 10 clicks
        if (num) % 10 == 0:
            renew_connection()

        if num == (views - 1):
            print("Done")
            sys.exit(0)


visit()
