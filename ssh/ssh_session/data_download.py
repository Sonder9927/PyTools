from src.session import session_connect
from pathlib import Path
import json


def is_data(f: str) -> bool:
    condition = [f.startswith("start"), f.endswith("end")]

    return True if any(condition) else False


def load_data(df: str, dt: str) -> None:
    sc = session_connect("param/host_key.json")
    sc.connect()

    files = sc.listdir(df)
    data = [f for f in files if is_data(f)]

    targets = [[df+"/"+d, dt+"/"+d] for d in data]
    for t in targets:
        sc.download(t[0], t[1])

    sc.close()


if __name__ == "__main__":
    load_data("cloud", "temp")

