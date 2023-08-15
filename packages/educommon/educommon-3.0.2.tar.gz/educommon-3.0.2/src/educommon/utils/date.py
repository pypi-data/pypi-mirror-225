"""Вспомогательные средства для работы с датами."""
import datetime
from collections import (
    namedtuple,
)
from typing import (
    Optional,
    Tuple,
    Union,
)

from dateutil import (
    rrule,
)
from django.conf import (
    settings,
)


# явно задаются имена дней, чтобы не возиться с настройками локали в питоне
MON_IDX = 0
TUE_IDX = 1
WED_IDX = 2
THU_IDX = 3
FRI_IDX = 4
SAT_IDX = 5
SUN_IDX = 6

WEEKDAYS = (
    (MON_IDX, 'Понедельник'),
    (TUE_IDX, 'Вторник'),
    (WED_IDX, 'Среда'),
    (THU_IDX, 'Четверг'),
    (FRI_IDX, 'Пятница'),
    (SAT_IDX, 'Суббота'),
    (SUN_IDX, 'Воскресенье')
)
WEEKDAYS_DICT = dict(WEEKDAYS)


def date_range_to_str(date_from, date_to, can_be_one_day_long=False):
    """
    Возвращает строку формата "с дд.мм.гггг [по дд.мм.гггг]",
    или дд.мм.гггг, если даты совпадают.

    Если указана только одна из дат то будет только
    "с ..." или "по ...", но если can_be_one_day_long=True,
    результат будет "дд.мм.гггг", для той даты, что указана.

    (<2001.01.01>, <2001.01.01>)         -> "01.01.2001"
    (<2001.01.01>, <2002.02.02>)         -> "с 01.01.2001 по 02.02.2002"
    (<2001.01.01>, None        )         -> "с 01.01.2001"
    (None,         <2002.02.02>)         -> "по 02.02.2002"
    (<2001.01.01>, None,       , True)   -> "01.01.2001"
    (None,         <2002.02.02>, True)   -> "02.02.2002"
    """
    def fmt(date):
        return date.strftime('%d.%m.%Y') if date else ''

    def validate_year(date):
        return (date if 1900 < date.year < 2100 else None) if date else None

    result = ''
    date_from = validate_year(date_from)
    date_to = validate_year(date_to)
    if date_from and date_to:
        assert date_from <= date_to
        if date_from == date_to:
            result = fmt(date_from)
        else:
            result = 'с %s по %s' % (fmt(date_from), fmt(date_to))
    else:
        if can_be_one_day_long:
            result = fmt(date_from or date_to or None)
        elif date_from:
            result = 'с %s' % fmt(date_from)
        elif date_to:
            result = 'по %s' % fmt(date_to)
    return result


def iter_days_between(date_from, date_to, odd_weeks_only=False):
    """
    Генератор дат в промежутке между указанными (включая границы).

    :param datetime.date: date_from - дата с
    :param datetime.date: date_to - дата по
    :param boolean: odd_weeks_only - только четные недели отн-но начала года

    :rtype: generator
    """
    if date_from > date_to:
        raise ValueError('date_from must be lower or equal date_to!')

    for dt in rrule.rrule(
        rrule.DAILY, dtstart=date_from, until=date_to
    ):
        if odd_weeks_only and dt.isocalendar()[1] % 2 != 0:
            # если требуются четные недели относительно начала года
            continue
        yield dt.date()


def get_week_start(date=None):
    """Возвращает дату первого дня недели (понедельника).

    :param date: Дата, определяющая неделю. Значение по умолчанию - текущая
        дата.
    :type date: datetime.date or None

    :rtype: datetime.date
    """
    if date is None:
        date = datetime.date.today()

    result = date - datetime.timedelta(days=date.weekday())

    return result


def get_week_end(date=None):
    """Возвращает дату последнего дня недели (воскресенья).

    :param date: Дата, определяющая неделю. Значение по умолчанию - текущая
        дата.
    :type date: datetime.date or None

    :rtype: datetime.date
    """
    if date is None:
        date = datetime.date.today()

    result = date + datetime.timedelta(days=SUN_IDX - date.weekday())

    return result


def get_week_dates(date=None):
    """Возвращает даты дней недели.

    :param date: Дата, определяющая неделю. Значение по умолчанию - текущая
        дата.
    :type date: datetime.date

    :rtype: dateutli.rrule.rrule
    """
    if date is None:
        date = datetime.date.today()

    monday = get_week_start(date)

    return (
        day.date()
        for day in rrule.rrule(rrule.DAILY, dtstart=monday,
                               count=len(WEEKDAYS))
    )


def get_weekdays_for_date(date=None, weekday_names=None):
    """Возвращает названия и даты дней недели.

    :param date: Дата, определяющая неделю. Значение по умолчанию - текущая
        дата.
    :type date: datetime.date or None

    :param weekday_names: Список или словарь наименований дней недели.
    :type weekday_names: dict, list

    :return: Кортеж из кортежей вида ('Название дня недели', дата).
    :rtype: tuple
    """
    weekday_names = weekday_names or WEEKDAYS_DICT

    return tuple(
        (weekday_names[day.weekday()], day)
        for day in get_week_dates(date)
    )


def get_today_min_datetime() -> datetime:
    """Возвращает дату/время начала текущих суток."""
    return datetime.datetime.combine(datetime.date.today(), datetime.time.min)


def get_today_max_datetime() -> datetime:
    """Возвращает дату/время окончания текущих суток."""
    return datetime.datetime.combine(datetime.date.today(), datetime.time.max)


def get_date_range_intersection(
    *date_ranges: Tuple[datetime.date, datetime.date]
) -> Union[Tuple[datetime.date, datetime.date], tuple]:
    """Возвращает минимальный внутренний диапазон дат из переданных диапазонов дат.

    В случае если диапазоны не пересекаются, возвращается пустой кортеж.
    """
    min_date = max((date_range[0] for date_range in date_ranges))
    max_date = min((date_range[1] for date_range in date_ranges))

    if min_date > max_date:
        date_range = ()
    else:
        date_range = min_date, max_date

    return date_range


def is_date_range_intersection(
    *date_ranges: Tuple[datetime.date, datetime.date]
) -> bool:
    """Возвращает признак того, что диапазоны дат пересекаются."""
    intersection = get_date_range_intersection(*date_ranges)

    return True if intersection else False


def date_to_str(
    date_: Optional[Union[datetime.date, datetime.datetime]],
    fmt: str = settings.DATE_FORMAT
) -> str:
    """Конвертирует дату в строку или возвращает '' если даты нет."""
    return date_.strftime(fmt) if date_ else ''


class Week(namedtuple('Week', ('year', 'week'))):
    """Работа с неделей."""

    @classmethod
    def withdate(cls, date):
        """Возвращает неделю, в которую входит дата."""
        return cls(*(date.isocalendar()[:2]))

    def day(self, number: int) -> datetime.date:
        """Возвращает дату дня недели.

        4 января должно попадать в первую неделю года и не важно на какой
        из дней недели приходится.
        Пример: если 4 января является воскресеньем, то это определенно 1-ая
        неделя года.
        """
        d = datetime.date(self.year, 1, 4)
        return d + datetime.timedelta(
            weeks=self.week - 1, days=-d.weekday() + number)

    def monday(self) -> datetime.date:
        """Дата понедельника."""
        return self.day(0)

    def sunday(self) -> datetime.date:
        """Дата воскресенья."""
        return self.day(6)

    def start_end_week(self) -> Tuple[datetime.date, datetime.date]:
        """Возвращает кортеж из даты начала и конца недели."""
        return self.day(0), self.day(6)

    def contains(self, day: datetime.date):
        """Проверяет попадание дня в текущую неделю."""
        return self.day(0) <= day < self.day(7)

    def year_week(self) -> Tuple[int, int]:
        """Возвращает кортеж (год, номер недели)."""
        return self.year, self.week

    def __repr__(self):  # noqa: D105
        return f'{self.__class__.__name__}({self.year}, {self.week})'
