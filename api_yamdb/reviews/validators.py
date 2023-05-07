from django.utils import timezone


def year_validator(value):
    if value < 1900 or value > timezone.now().year:
        raise ValueError(f'{value} is not a correct year!')
