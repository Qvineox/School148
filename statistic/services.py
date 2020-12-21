from django.utils import timezone

from accounts.models import Apprentices
from journal.models import Marks, Lessons


def get_apprentice_average_score(apprentice_id):
    all_marks = Marks.objects.filter(holder_id=apprentice_id).exclude(value=0)
    overall_score = 0
    count_score = 0

    for mark in all_marks:
        overall_score += mark.value * mark.weight
        count_score += mark.weight
    try:
        average_score = overall_score / count_score
    except ZeroDivisionError:
        return None
    else:
        return average_score


def get_teacher_average_score(teacher_id):
    all_marks = Marks.objects.filter(appraiser_id=teacher_id).exclude(value=0)
    overall_score = 0
    count_score = 0

    for mark in all_marks:
        overall_score += mark.value * mark.weight
        count_score += mark.weight
    try:
        average_score = overall_score / count_score
    except ZeroDivisionError:
        return None
    else:
        return average_score


def get_apprentice_attendance_score(apprentice_id, all_lessons=None):
    if not all_lessons:
        all_lessons = Lessons.objects.filter(
            study_group_id=Apprentices.objects.get(id=apprentice_id).study_group_id, date__lte=timezone.now()).count()
    non_attendance_count = Marks.objects.filter(holder_id=apprentice_id, value=0).count()
    print(non_attendance_count)
    try:
        attendance_score = (non_attendance_count / all_lessons) * 100
        print(attendance_score)
    except ZeroDivisionError:
        return None
    else:
        return 100 - attendance_score


def get_performance_score(apprentice_id):
    non_attended_lessons = get_apprentice_attendance_score(apprentice_id)
    all_lessons = Lessons.objects.filter(
        study_group_id=Apprentices.objects.get(id=apprentice_id).study_group_id).count()


def get_all_teacher_lessons(teacher_id):
    all_lessons = Lessons.objects.filter(teacher_id=teacher_id, date__lte=timezone.now()).count()
    return all_lessons


# возвращает grid со статистиками
def get_group_statistics(apprentices_list, study_group_id):
    apprentices_grid = [[], [], []]
    all_lessons = Lessons.objects.filter(study_group_id=study_group_id, date__lte=timezone.now()).count()

    for counter, item in enumerate(apprentices_list):
        item.__setattr__('stats',
                         (get_apprentice_attendance_score(item.id, all_lessons),
                          get_apprentice_average_score(item.id)))
        apprentices_grid[counter % 3].append(item)

    return apprentices_grid
