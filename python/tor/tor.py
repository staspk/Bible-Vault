import os, subprocess, random
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
                    self._socks_port = value
                if(key == 'ControlPort' and value):
                    self._control_port = value

        if self._socks_port is None:
            raise Exception("To instantiate Tor(), must have line in torrc file: 'SocksPort 9050'")
        
        self._start()

    def _start(self):
        if os.name == 'nt':
            Tor.kill_windows_tor_processes()
            self._process:subprocess.Popen = subprocess.Popen(
                [Tor.TOR_EXE, '-f', Tor.TORRC],
                creationflags=subprocess.CREATE_NO_WINDOW,                # flag is windows only, fyi
            )
            print_green(f'Tor started. {type(self._process)}')      
        else:
            raise Exception('os not supported')
        
    def proxy(self) -> str:
        """
        returns a proxy string, e.g: 'socks5h://{random_username}:password@127.0.0.1:{self._socks_port}'\n
        note: tor.exe uses: 9050, tor-browser uses: 9150. (nebulous) claims of "better success" with 9150
        """
        username = str(random.randint(10000, 99999))
        return f'socks5h://{username}:password@127.0.0.1:{self._socks_port}'

    def stop(self):
        if(self._process):
            self._process.terminate()
            exit_code = self._process.wait()
            if(exit_code == 0):
                print_green('Tor.stop(): Success')
            else:
                print_red(f'Tor.stop(): Failure. exit_code: {exit_code}')


    def new_identity(self):
        if(self._control_port is None):
            raise RuntimeError("Tor().new_identity(), requires line in torrc file: 'ControlPort 9051'")
        
        try:
            with Controller.from_port(port=self._control_port) as control:
                control.authenticate()
                control.signal(Signal.NEWNYM)
        except Exception as e:
            raise Exception(f'Failed to get new identity: {e}')
        
    def kill_windows_tor_processes():
        result = subprocess.run(
            ['tasklist', '/FI', 'IMAGENAME eq tor.exe'],        # list, filter, for 'tor.exe'
            capture_output=True,                                # capture stdout/stderr
            text=True                                           # result should be str, not byte obj
        )

        if "tor.exe" in result.stdout:
            print_red('Tor.kill_windows_tor_processes() tor.exe process(es) found.')
            result = subprocess.run(['taskkill', '/F', '/IM', 'tor.exe'], capture_output=True)
            if(result.returncode == 0):
                print_red('Tor.kill_windows_tor_processes(): Success')
            else:
                print_dark_red(f'Tor.kill_windows_tor_processes(): result.returncode: {result.returncode}')