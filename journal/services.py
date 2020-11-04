import datetime
import logging

from accounts.services import get_profile_from_user
from journal.models import Lessons

logger = logging.getLogger('database')


# возвращает всю информацию об уроках на определенный день для определенной учебной группы
def get_lessons_for_study_group(study_group_id, schedule_date):
    data = None
    return data


# возвращает недельное расписание
def get_schedule_for_user(user):
    this_week_lessons = None

    # если пользователь школьник
    if user.groups.values_list('id', flat=True).order_by('-id').first() == 1:
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)
        this_week_lessons = Lessons.objects.filter(date__range=[start_week, end_week],
                                                   study_group_id=get_profile_from_user(user.id).study_group_id,
                                                   )

    logger.info('Weekly schedule received for user: {0}'.format(user.id))
    return process_schedule_data_for_journal_view(this_week_lessons)


def process_schedule_data_for_journal_view(lessons_queryset):
    lessons_dict = {
        '0': [],
        '1': [],
        '2': [],
        '3': [],
        '4': [],
        '5': [],
        '6': []
    }

    for lesson in lessons_queryset.order_by('date', 'order').values():
        lessons_dict[str(lesson['date'].weekday())].append(
            (lesson['active'],
             lesson['subject_id'],
             lesson['homework_id'],
             lesson['teacher_id'],
             lesson['auditory'],
             lesson['id'],
             ))

    return lessons_dict
