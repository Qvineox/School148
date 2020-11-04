import datetime
import logging

from accounts.models import Teachers
from accounts.services import get_profile_from_user
from journal.models import Lessons, Disciples

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


class Object(object):
    pass


def process_schedule_data_for_journal_view(lessons_queryset):
    lessons = Object()

    setattr(lessons, 'monday', [])
    setattr(lessons, 'tuesday', [])
    setattr(lessons, 'wednesday', [])
    setattr(lessons, 'thursday', [])
    setattr(lessons, 'friday', [])
    setattr(lessons, 'saturday', [])

    for lesson in lessons_queryset.order_by('date', 'order').values():
        if lesson['date'].weekday() == 0:
            lessons.monday.append(get_lesson_info(lesson))
        elif lesson['date'].weekday() == 1:
            lessons.tuesday.append(get_lesson_info(lesson))
        elif lesson['date'].weekday() == 2:
            lessons.wednesday.append(get_lesson_info(lesson))
        elif lesson['date'].weekday() == 3:
            lessons.thursday.append(get_lesson_info(lesson))
        elif lesson['date'].weekday() == 4:
            lessons.friday.append(get_lesson_info(lesson))
        elif lesson['date'].weekday() == 5:
            lessons.saturday.append(get_lesson_info(lesson))

    # не спрашивайте что это
    lessons.monday = lessons.monday + [None] * (8 - len(lessons.monday))
    lessons.tuesday = lessons.tuesday + [None] * (8 - len(lessons.tuesday))
    lessons.wednesday = lessons.wednesday + [None] * (8 - len(lessons.wednesday))
    lessons.thursday = lessons.thursday + [None] * (8 - len(lessons.thursday))
    lessons.friday = lessons.friday + [None] * (8 - len(lessons.friday))
    lessons.saturday = lessons.saturday + [None] * (8 - len(lessons.saturday))

    return lessons


# возвращает ифнормацию о уроке, по умолчанию возвращает краткую информацию
def get_lesson_info(lesson_object, full=False):
    lesson_teacher = Teachers.objects.get(id=lesson_object['teacher_id'])
    lesson_teacher_info = ("{0} {1}.{2}".format(lesson_teacher.second_name,
                                                lesson_teacher.first_name[0],
                                                lesson_teacher.last_name[0]))

    lesson_subject = Disciples.objects.get(id=lesson_object['subject_id']).title
    lesson_auditory = lesson_object['auditory']

    lesson_color = 'red'

    if lesson_object['homework_id'] is not None:
        lesson_has_homework = True
    else:
        lesson_has_homework = False

    lesson_info = Object()
    setattr(lesson_info, 'subject', lesson_subject)
    setattr(lesson_info, 'id', lesson_object['id'])
    setattr(lesson_info, 'active', lesson_object['active'])
    setattr(lesson_info, 'color', lesson_color)

    if full:
        setattr(lesson_info, 'teacher', lesson_teacher_info)
        setattr(lesson_info, 'auditory', lesson_auditory)
        setattr(lesson_info, 'has_homework', lesson_has_homework)

    return lesson_info
