import subprocess
import warnings
import requests


class Color:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

    def __init__(self, color: str):
        self.color: str = color.upper()

    def __call__(self, text: str) -> None:
        colored_text = f"{self.__getattribute__(self.color)}{text}{self.RESET}"
        print(colored_text)


class Library(str):
    @staticmethod
    def info(text):
        Color('BLUE')(text)

    @staticmethod
    def warn(text):
        Color('RED')(text)

    def _network(self):
        self.warn('Failed to get information')

    def _not_installed(self):
        self.warn('The library is not installed')

    def _version(self):
        self.warn('Couldn\'t find the library version')

    @property
    def local_version(self) -> str:
        try:
            result = subprocess.check_output(["pip", "show", self]).decode("utf-8")
            lines = result.split("\n")
            for line in lines:
                if line.startswith("Version:"):
                    return line.split(":")[1].strip()
            self._version()
        except subprocess.CalledProcessError:
            self._not_installed()

    @property
    def latest_version(self):
        try:
            response = requests.get(f"https://pypi.org/pypi/{self}/json")
            data = response.json()
            latest_version = data["info"]["version"]
            return latest_version
        except requests.RequestException:
            self._network()


class LibraryChecker(Library):
    def __call__(self):
        self.info(
            f'CVAL-LIB: Package versioning begins...\n'
            'To disable this option, set CVAL_CHECK_VERSION_DISABLED.'
        )
        latest = self.latest_version
        local = self.local_version
        if latest != local and None not in (latest, local, ):
            self.warn(
                    f'Please update the package "{self}" to the version {latest}'
                    f'to avoid errors.'
                )
        self.info(f'Everything is fine! Installed cval-lib version is {local}.')
