from enum import Enum

MONITOR_HOOK_NAMES = ('healthchecks', 'cronitor', 'cronhub', 'pagerduty', 'ntfy')


class State(Enum):
    START = 1
    FINISH = 2
    FAIL = 3
    LOG = 4
