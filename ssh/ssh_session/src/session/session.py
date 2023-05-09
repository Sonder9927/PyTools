from .ssh_connector import SSHConnector
import json


def session_connect(js: str) -> SSHConnector:
    with open(js) as f:
        hos = json.load(f)

    sc = SSHConnector(**hos)

    return sc
