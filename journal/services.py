import datetime
import logging

from django.db import DatabaseError

from accounts.models import Teachers, StudyGroups
from accounts.services import get_profile_from_user, get_study_group_apprentices
from journal.models import Lessons, Disciples, Marks

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


class Lesson(object):
    pass


def process_schedule_data_for_journal_view(lessons_queryset):
    lessons = Lesson()

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
def get_lesson_info(lesson_object, full=False, students=False):
    lesson_teacher = Teachers.objects.get(id=lesson_object['teacher_id'])
    lesson_teacher_info = ("{0} {1}.{2}".format(lesson_teacher.second_name,
                                                lesson_teacher.first_name[0],
                                                lesson_teacher.last_name[0]))

    disciple = Disciples.objects.get(id=lesson_object['subject_id'])
    lesson_subject = disciple.title
    lesson_scheme = disciple.scheme
    lesson_auditory = lesson_object['auditory']

    if lesson_object['homework_id'] is not None:
        lesson_has_homework = True
    else:
        lesson_has_homework = False

    lesson_info = Lesson()
    setattr(lesson_info, 'subject', lesson_subject)
    setattr(lesson_info, 'id', lesson_object['id'])
    setattr(lesson_info, 'active', lesson_object['active'])
    setattr(lesson_info, 'scheme', lesson_scheme)
    setattr(lesson_info, 'teacher', lesson_teacher_info)

    if full:
        lesson_info.teacher = lesson_teacher
        setattr(lesson_info, 'auditory', lesson_auditory)
        setattr(lesson_info, 'has_homework', lesson_has_homework)
        setattr(lesson_info, 'order', lesson_object['order'])
        setattr(lesson_info, 'date', lesson_object['date'])

        setattr(lesson_info, 'group', StudyGroups.objects.get(id=lesson_object['study_group_id']))

        if students:
            present_students, absent_students = get_on_lesson_students(lesson_info)

            setattr(lesson_info, 'present_students', present_students)
            setattr(lesson_info, 'absent_students', absent_students)

    return lesson_info


def get_on_lesson_students(group_id, lesson_id):
    present_students = get_study_group_apprentices(group_id)

    absent_students_id = list(
        Marks.objects.filter(lesson_id=lesson_id, value=0).values_list('holder_id', flat=True))

    print(absent_students_id)
    absent_students = []

    for count, student in enumerate(present_students):
        if student.id in absent_students_id:
            absent_students.append(present_students.pop(count))

    return present_students, absent_students


# возвращает данные об уроке из id
def get_lesson_data_from_id(lesson_id, students=False):
    lesson = Lessons.objects.filter(id=lesson_id).values()[0]
    return get_lesson_info(lesson, full=True, students=students)


# отмечает отсутствие ученика на уроке
def set_student_absence(student_id, lesson_id, teacher_id):
    try:
        Marks.objects.create(holder_id=student_id, lesson_id=lesson_id, appraiser_id=teacher_id, value=0)
    except DatabaseError:
        pass


# отмечает присутствие ученика на уроке
def set_student_presence(student_id, lesson_id):
    try:
        Marks.objects.filter(holder_id=student_id, lesson_id=lesson_id, value=0).delete()
    except DatabaseError:
        pass
