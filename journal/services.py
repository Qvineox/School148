import datetime
import logging

from django.db import DatabaseError
from django.utils import timezone

from accounts.models import Teachers, StudyGroups, Apprentices
from accounts.services import get_profile_from_user, get_study_group_apprentices, get_user_prior_group_number
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
        end_week = start_week + datetime.timedelta(6)
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
        elif lesson['date'].weekday() == 6:
            continue

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
    setattr(lesson_info, 'date', lesson_object['date'])

    if full:
        lesson_info.teacher = lesson_teacher
        setattr(lesson_info, 'auditory', lesson_auditory)
        setattr(lesson_info, 'has_homework', lesson_has_homework)
        setattr(lesson_info, 'order', lesson_object['order'])

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

    absent_students = []

    for count, student in enumerate(present_students):
        if student.id in absent_students_id:
            absent_students.append(present_students.pop(count))

    return present_students, absent_students


# возвращает данные об уроке из id
def get_lesson_data_from_id(lesson_id, students=False):
    lesson = Lessons.objects.filter(id=lesson_id).values()[0]
    return get_lesson_info(lesson, full=True, students=students)


# возвращает все оценки этого урока
def get_lesson_marks(lesson_id):
    marks = Marks.objects.filter(lesson_id=lesson_id).exclude(value=0)
    return marks


# отмечает отсутствие ученика на уроке
def set_student_absence(student_id, lesson_id, teacher_id):
    try:
        Marks.objects.create(holder_id=student_id, lesson_id=lesson_id, appraiser_id=teacher_id, value=0, weight=None)
    except DatabaseError:
        pass


# отмечает присутствие ученика на уроке
def set_student_presence(student_id, lesson_id):
    try:
        Marks.objects.filter(holder_id=student_id, lesson_id=lesson_id, value=0).delete()
    except DatabaseError:
        pass


# устанавливает оценку ученику
def set_student_mark(lesson_id, student_id, value, weight, appraiser=None, comment=None):
    if appraiser is None:
        appraiser = Lessons.objects.get(id=lesson_id).teacher

    new_mark = Marks.objects.create(value=value,
                                    weight=weight,
                                    lesson=Lessons.objects.get(id=lesson_id),
                                    holder=Apprentices.objects.get(id=student_id),
                                    comment=comment,
                                    appraiser=appraiser)

    new_mark.save()


# удаляет оценку ученика
def remove_student_mark(mark_id):
    delete_mark = Marks.objects.get(id=mark_id)
    delete_mark.delete()


# возвращает список уроков пользователя
def get_lesson_history_for_user(user_id):
    user_group = get_user_prior_group_number(user_id)
    profile_data = get_profile_from_user(user_id)

    scheduled_lessons = []
    latest_lessons = []
    # archived_lessons = []

    # если пользователь - школьник
    if user_group == 1:
        current_date = timezone.now().date()
        time_point = current_date - datetime.timedelta(days=7)
        # получаем список всех уроков за определенный период времени назад
        lessons_queryset = Lessons.objects.filter(study_group_id=profile_data.study_group_id,
                                                  date__gt=time_point,
                                                  date__lte=current_date + datetime.timedelta(days=1))

        for lesson in lessons_queryset.order_by('date', 'order').values():
            new_lesson = get_lesson_info(lesson, full=False)
            if new_lesson.date >= current_date:
                scheduled_lessons.append(new_lesson)
            else:
                latest_lessons.append(new_lesson)

    return scheduled_lessons, latest_lessons


# возвращает все оценки пользователя
def get_all_marks_from_user(user_id):
    user_group = get_user_prior_group_number(user_id)
    profile_data = get_profile_from_user(user_id)

    # если пользователь - школьник
    if user_group == 1:
        all_marks = Marks.objects.filter(holder_id=profile_data.id).exclude(value=0)
        return all_marks
    else:
        return False


# распределение оценок по предметам
# возвращает словарь, где ключи - имена предметов, а значения - оценки
def sort_marks_by_subject(marks_queryset):
    user_marks = {}
    for mark in marks_queryset:
        mark_subject = mark.lesson.subject
        if mark_subject in user_marks.keys():
            user_marks[mark_subject].append(mark)
        else:
            user_marks.update({mark_subject: [mark]})

    return user_marks


def add_avg_score_to_sorted_marks(user_marks):
    for subject in user_marks:
        amount, count = 0, 0
        for mark in user_marks[subject]:
            amount += mark.value * mark.weight
            count += mark.weight

        avg_score = Lesson()
        setattr(avg_score, 'value', amount / count)
        setattr(avg_score, 'amount', amount)
        setattr(avg_score, 'count', count)

        user_marks[subject].append(avg_score)
    return user_marks
