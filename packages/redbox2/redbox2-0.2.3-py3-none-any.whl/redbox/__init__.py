import tomli
from redbox.box import EmailBox

with open("pyproject.toml", "rb") as f:
    pyproject = tomli.load(f)

__version__ = pyproject["tool"]["poetry"]["name"]

gmail = EmailBox(
    host="imap.gmail.com",
    port=993,
)

outlook = EmailBox(
    host="outlook.office365.com",
    port=993,
)
