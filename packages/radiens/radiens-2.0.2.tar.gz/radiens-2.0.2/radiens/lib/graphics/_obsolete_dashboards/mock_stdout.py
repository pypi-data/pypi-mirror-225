import sys
import threading
import queue
import argparse
import queue
import time
from pathlib import Path
import numpy as np
import tempfile


def main(args):
    uid = 'dash_uid'
    mock_stdout = Path('./', uid+'.i')
    while True:
        args = input('radiens-py[drk] %')  # blocks until <enter>
        with open(mock_stdout, mode='w+') as f:
            f.seek(0)
            f.writelines(args)
        time.sleep(0.1)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
