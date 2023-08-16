import enum


class SyncType(enum.IntEnum):
    All = 0
    Daily = 1
    Monthly = 2
    NoSync = 999
