import os, subprocess, random, time
import requests
from stem import Signal
from stem.control import Controller
from kozubenko.os import Parent
from kozubenko.print import print_dark_red, print_green, print_red


class Tor:
    TOR_EXE : str = os.path.join(Parent(__file__), 'tor.exe')
    TORRC   : str = os.path.join(Parent(__file__), 'torrc')

    def __init__(self):
        self._socks_port   : int = None 
        self._control_port : int = None
        self._process      : subprocess.Popen = None

        if not os.path.exists(Tor.TOR_EXE) or not os.path.exists(Tor.TORRC):
            raise Exception('Tor.exe/torrc required to instantiate Tor')
        
        with open(Tor.TORRC, 'r') as file:
            for line in file:
                key, value = (line.strip()).split(' ', 1)
                if(key == 'SocksPort' and value):
                    self._socks_port = int(value)
                if(key == 'ControlPort' and value):
                    self._control_port = int(value)

        if self._socks_port is None:
            raise Exception("To instantiate Tor(), must have line in torrc file: 'SocksPort 9050'")
        
        self._start()

    def test_request(self) -> str:
        """
        Routes a requests get method through tor's socks5h proxy, returns the public ip used in that request as a string
        """
        return requests.get(url='https://api.ipify.org', proxies=self.proxies_as_dict()).text

    def _start(self):
        if os.name == 'nt':
            Tor.kill_windows_tor_processes()
            self._process:subprocess.Popen = subprocess.Popen(
                [Tor.TOR_EXE, '-f', Tor.TORRC],
                creationflags=subprocess.CREATE_NO_WINDOW,                # flag is windows only, fyi
            )
            print_green(f'Tor started.')      
        else:
            raise Exception('os not supported')
        
    def proxies_as_dict(self) -> dict[str, str]:
        """
        {
            'http': 'socks5h://{username}:password@127.0.0.1:{self._socks_port}',
            'https': 'socks5h://{username}:password@127.0.0.1:{self._socks_port}'
        }
        
        Example use: `requests.get(url, proxies=tor.proxies_as_dict())`
        """
        proxy = self.proxy()
        return {
            'http': proxy,
            'https': proxy
        }
        
    def proxy(self) -> str:
        """
        returns a proxy string, e.g: `socks5h://{random_username}:password@127.0.0.1:{self._socks_port}`\n
        note: tor.exe uses: 9050, tor-browser uses: 9150. (nebulous) claims of "better success" with 9150
        """
        username = str(random.randint(10000, 99999))
        # return f'socks5h://@127.0.0.1:{self._socks_port}'
        return f'socks5h://{username}:password@127.0.0.1:{self._socks_port}'

    def stop(self):
        if(self._process):
            self._process.terminate()
            print_green('Tor stopped.')


    def request_new_identity(self):
        """
        **Call Requirements: "ControlPort 9051" line in torrc file.**
        \nRate limited at ~10 seconds.
        \nRebuilds circuit to get a new public ip, assuming you're routing the traffic through a socks5 proxy
        """
        if(self._control_port is None):
            raise RuntimeError("Tor().new_identity(), requires line in torrc file: 'ControlPort 9051'")
        
        try:
            with Controller.from_port(port=self._control_port) as control:
                control.authenticate()
                control.signal(Signal.NEWNYM)
        except Exception as e:
            raise Exception(f'Failed to get new identity: {e}')
        
        time.sleep(.5)
        
    def kill_windows_tor_processes():
        result = subprocess.run(
            ['tasklist', '/FI', 'IMAGENAME eq tor.exe'],        # list, filter, for 'tor.exe'
            capture_output=True,                                # capture stdout/stderr
            text=True                                           # result should be str, not byte obj
        )

        if "tor.exe" in result.stdout:
            print_red('Tor.kill_windows_tor_processes() tor.exe process(es) found. Killing...')
            result = subprocess.run(['taskkill', '/F', '/IM', 'tor.exe'], capture_output=True)
            if(result.returncode == 0):
                print_red('Tor.kill_windows_tor_processes(): Success')
            else:
                print_dark_red(f'Tor.kill_windows_tor_processes(): result.returncode: {result.returncode}')

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.stop()


# def selenium_firefox_test():
    # with Tor() as tor:
    #     profile = webdriver.FirefoxProfile()
    #     profile.set_preference("network.proxy.type", 1)
    #     profile.set_preference("network.proxy.socks", "127.0.0.1")
    #     profile.set_preference("network.proxy.socks_port", 9050)
    #     profile.set_preference("network.proxy.socks_remote_dns", True)
    #     profile.set_preference("browser.cache.disk.enable", False)
    #     profile.set_preference("browser.cache.memory.enable", False)

    #     options = Options()
    #     options.profile = profile
    #     # options.headless = True

    #     driver = webdriver.Firefox(options=options)

    #     URLS = [
    #         'https://check.torproject.org/',
    #         'https://check.torproject.org/',
    #         'https://api.ipify.org',
    #         'https://icanhazip.com',
    #         'https://check.torproject.org/',
    #         'https://check.torproject.org/',
    #         'https://ifconfig.me',
    #         'https://check.torproject.org/',
    #         'https://check.torproject.org/',
    #         'https://icanhazip.com',
    #         'https://check.torproject.org/',
    #         'https://check.torproject.org/'
    #     ]

    #     for i in range(URLS.__len__()):
    #         driver.get(URLS[i])
    #         time.sleep(10)
    #         driver.get('https://www.google.com/')
    #         time.sleep(2)

    #     driver.quit()