from pathlib import Path

from radiens.common.constants import (TIME_SPEC)
from datetime import datetime


def time_now():
    return datetime.now().strftime(TIME_SPEC)
