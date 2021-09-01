from datetime import datetime, date, timedelta


class D:
    def __init__(self, *args):
        self.utcnow = datetime.utcnow()
        self.timedelta = 0
        self.date_format = "%Y-%m-%d"
        self.datetime_format = "%Y-%m-%d %H:%M:%S"

    @classmethod
    def datetime(cls, diff: int = 0) -> datetime:
        return cls().utcnow + timedelta(hours=diff)

    @classmethod
    def kstnow(cls) -> datetime:
        return cls.datetime(9)

    @classmethod
    def timestamp(cls):
        return str(cls.kstnow().strftime(cls().datetime_format))

    @classmethod
    def str2date(cls, str_date: str) -> date:
        return datetime.strptime(str_date, cls().date_format)
