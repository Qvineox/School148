from datetime import datetime, timedelta

from django.utils import timezone

from accounts.services import get_profile_from_user
from journal.models import Lessons, Homeworks, Marks
from journal.services import get_lesson_info


def get_student_homepage_lessons(study_group_id):
    if datetime.now().hour >= datetime.strptime('17', "%H").hour:
        return get_tomorrow_lessons(study_group_id)
    else:
        return get_today_lessons(study_group_id)


def get_teacher_homepage_lessons(teacher_id):
    lessons = []

    if datetime.now().hour >= datetime.strptime('17', "%H").hour:
        date = date = datetime.today() + timedelta(days=1)
        for lesson in Lessons.objects.filter(teacher_id=teacher_id, date=date).order_by('order').values():
            lessons.append(get_lesson_info(lesson, False))

        pretext = "Завтра"
    else:
        date = date = datetime.today()
        for lesson in Lessons.objects.filter(teacher_id=teacher_id, date=date).order_by('order').values():
            lessons.append(get_lesson_info(lesson, False))

        pretext = "Сегодня"

    return lessons, pretext, date


def get_student_homepage_homework(study_group_id, period=7):
    current_date = timezone.now()
    homeworks = Homeworks.objects.filter(target_group=study_group_id,
                                         deadline_time__range=(
                                             current_date, current_date + timedelta(days=period)))
    return homeworks


def get_teacher_homepage_homework(teacher_id, period=7):
    current_date = timezone.now()
    homeworks = Homeworks.objects.filter(author_id=teacher_id,
                                         deadline_time__range=(
                                             current_date, current_date + timedelta(days=period)))
    return homeworks


def get_student_homepage_marks(profile_id, period=7):
    marks = Marks.objects.filter(holder_id=profile_id,
                                 rating_date__gte=timezone.now() - timedelta(days=period)).order_by(
        'rating_date').exclude(value=0)
    return marks


def get_teacher_homepage_marks(teacher_id, period=7):
    marks = Marks.objects.filter(appraiser_id=teacher_id,
                                 rating_date__gte=timezone.now() - timedelta(days=period)).order_by(
        'rating_date').exclude(value=0)
    return marks


def get_today_lessons(study_group):
    return get_day_lessons(datetime.today(), study_group)


def get_tomorrow_lessons(study_group):
    return get_day_lessons(datetime.today() + timedelta(days=1), study_group)


class Object(object):
    pass


def get_day_lessons(date, study_group):
    lessons = []

    for lesson in Lessons.objects.filter(date=date, study_group_id=study_group).order_by('order').values():
        lessons.append(get_lesson_info(lesson, False))

    if date > datetime.today():
        pretext = "Завтра"
    else:
        pretext = "Сегодня"

    return lessons, pretext, date


def get_apprentice_home_data(user_id):
    apprentice_profile = get_profile_from_user(user_id)

    lessons, pretext, date = get_student_homepage_lessons(apprentice_profile.study_group_id)
    homeworks = get_student_homepage_homework(apprentice_profile.study_group_id, 14)
    marks = get_student_homepage_marks(apprentice_profile.id, 14)

    result = {
        'lessons': lessons,
        'pretext': pretext,
        'date': date,
        'homeworks': homeworks,
        'marks': marks
    }

    return result


def get_teacher_home_data(user_id):
    teacher_profile = get_profile_from_user(user_id)
    lessons, pretext, date = get_teacher_homepage_lessons(teacher_profile.id)
    homeworks = get_teacher_homepage_homework(teacher_profile.id, 7)
    marks = get_teacher_homepage_marks(teacher_profile.id, 7)

    result = {
        'lessons': lessons,
        'pretext': pretext,
        'date': date,
        'homeworks': homeworks,
        'marks': marks
    }

    return result
