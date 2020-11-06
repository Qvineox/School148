from datetime import datetime, timedelta

from accounts.services import get_profile_from_user
from journal.models import Lessons
from journal.services import get_lesson_info


def get_homepage_lessons(user_id):
    study_group = get_profile_from_user(user_id).study_group_id

    if datetime.now().hour >= datetime.strptime('17', "%H").hour:
        return get_tomorrow_lessons(study_group)
    else:
        return get_today_lessons(study_group)


def get_today_lessons(study_group):
    return get_day_lessons(datetime.today(), study_group)


def get_tomorrow_lessons(study_group):
    return get_day_lessons(datetime.today() + timedelta(days=1), study_group)


class Object(object):
    pass


def get_day_lessons(date, study_group):
    lessons = []

    for lesson in Lessons.objects.filter(date=date, study_group_id=study_group).order_by('order').values():
        lessons.append(get_lesson_info(lesson, True))

    if date > datetime.today():
        pretext = "Завтра"
    else:
        pretext = "Сегодня"

    return lessons, pretext, date
