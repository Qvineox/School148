import datetime
import logging

from django.db import DatabaseError
from django.utils import timezone

from accounts.models import Teachers, StudyGroups, Apprentices
from accounts.services import get_profile_from_user, get_study_group_apprentices
from journal.models import Lessons, Disciples, Marks, Homeworks

logger = logging.getLogger('database')


# возвращает всю информацию об уроках на определенный день для определенной учебной группы
def get_lessons_for_study_group(study_group_id, schedule_date):
    data = None
    return data


# возвращает недельное расписание для ученика
def get_schedule_for_student(user_id):
    student_group_id = get_profile_from_user(user_id).study_group_id
    date = datetime.date.today()
    start_week = date - datetime.timedelta(date.weekday())
    end_week = start_week + datetime.timedelta(6)
    this_week_lessons = Lessons.objects.filter(date__range=[start_week, end_week],
                                               study_group_id=student_group_id,
                                               )

    logger.info('Weekly schedule received for user: {0}'.format(user_id))
    return process_schedule_data_for_journal_view(this_week_lessons)


# возвращает недельное расписание для учителя
def get_schedule_for_teacher(user_id):
    teacher_id = get_profile_from_user(user_id).id
    date = datetime.date.today()
    start_week = date - datetime.timedelta(date.weekday())
    end_week = start_week + datetime.timedelta(6)
    this_week_lessons = Lessons.objects.filter(date__range=[start_week, end_week],
                                               teacher_id=teacher_id,
                                               )
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


# возвращает домашнее задание на этот урок
def get_lesson_homework(lesson_id):
    homeworks = Homeworks.objects.filter(placement_lesson_id=lesson_id)
    return homeworks


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


# установка домашнего задания
def set_homework(content, deadline, required, placement_lesson):
    Homeworks.objects.create(text=content,
                             required=required,
                             deadline_time=deadline,
                             author_id=placement_lesson.teacher.id,
                             placement_lesson_id=placement_lesson.id,
                             target_group_id=placement_lesson.group.id)


# возвращает список уроков школьника
def get_lesson_history_for_student(user_id):
    profile_data = get_profile_from_user(user_id)

    scheduled_lessons = []
    latest_lessons = []

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


# возвращает список уроков учителя
def get_lesson_history_for_teacher(user_id):
    profile_data = get_profile_from_user(user_id)

    scheduled_lessons = []
    latest_lessons = []

    current_date = timezone.now().date()
    time_point = current_date - datetime.timedelta(days=7)
    # получаем список всех уроков за определенный период времени назад
    lessons_queryset = Lessons.objects.filter(teacher=profile_data.id,
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
def get_all_marks_for_student(user_id):
    profile_data = get_profile_from_user(user_id)

    all_marks = Marks.objects.filter(holder_id=profile_data.id).exclude(value=0)
    return all_marks


# возвращает все оценки по всем предметам учителя
def get_all_marks_for_teacher(user_id):
    profile_data = get_profile_from_user(user_id)

    all_marks = Marks.objects.filter(appraiser_id=profile_data.id).exclude(value=0)
    return all_marks


# возвращает сортированный по предметам, классам и ученикам список оценок для учителя
def sort_all_marks_for_teacher(all_marks_queryset):
    disciples = []
    marks_by_disciples = []

    # сортировка по дисциплинам
    for mark in all_marks_queryset:
        if mark.lesson.subject in disciples:
            marks_by_disciples[disciples.index(mark.lesson.subject)].append(mark)
        else:
            disciples.append(mark.lesson.subject)
            marks_by_disciples.append([mark])

    disciples_result = []
    # объединение
    for position in range(len(disciples)):
        disciples_result.append((disciples[position], marks_by_disciples[position]))

    groups_result = []
    # сортировка по группам
    for disciple_tuple in disciples_result:
        groups = []
        marks_by_groups = []

        for mark in disciple_tuple[1]:
            if mark.holder.study_group in groups:
                marks_by_groups[groups.index(mark.holder.study_group)].append(mark)
            else:
                groups.append(mark.holder.study_group)
                marks_by_groups.append([mark])

        for i in range(len(groups)):
            groups_result.append((groups[i], marks_by_groups[i]))

    students_result = []
    # сортировка по ученикам
    for group_tuple in groups_result:
        students = []
        marks_by_students = []

        for mark in group_tuple[1]:
            if mark.holder in students:
                marks_by_students[students.index(mark.holder)].append(mark)
            else:
                students.append(mark.holder)
                marks_by_students.append([mark])

        for i in range(len(students)):
            students_result.append((students[i], marks_by_students[i]))

    result_by_groups = []
    print(students_result)
    # объединение студентов в группы
    for i in range(len(groups_result)):
        result_by_groups.append((groups_result[i][0], students_result))

    result = []
    # объединение группы в дисциплины
    for i in range(len(disciples_result)):
        result.append((disciples_result[i][0], result_by_groups))

    print(result)
    return result


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
