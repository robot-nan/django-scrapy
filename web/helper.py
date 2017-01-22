from django.utils import timezone


def make_aware_timezone(date, format=None):
    if isinstance(date, str) or isinstance(date, unicode):
        naive_datatime = timezone.datetime.strptime(date, format)
        res = timezone.make_aware(naive_datatime, timezone.get_current_timezone())
    else:
        res = timezone.make_aware(date, timezone.get_current_timezone())
    return res