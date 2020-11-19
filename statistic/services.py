from accounts.models import Apprentices
from journal.models import Marks, Lessons


def get_apprentice_average_score(apprentice_id):
    all_marks = Marks.objects.filter(holder_id=apprentice_id).exclude(value=0)
    overall_score = 0
    for mark in all_marks:
        overall_score += mark.value * mark.weight

    try:
        average_score = overall_score / len(all_marks)
    except ZeroDivisionError:
        return None
    else:
        return average_score


def get_apprentice_non_attendance_score(apprentice_id):
    all_lessons = Lessons.objects.filter(
        study_group_id=Apprentices.objects.get(id=apprentice_id).study_group_id).count()
    non_attendance_count = Marks.objects.filter(holder_id=apprentice_id, value=0).count()

    try:
        attendance_score = non_attendance_count / all_lessons * 100
    except ZeroDivisionError:
        return 100
    else:
        return attendance_score


def get_performance_score(apprentice_id):
    non_attended_lessons = get_apprentice_non_attendance_score(apprentice_id)
    all_lessons = Lessons.objects.filter(
        study_group_id=Apprentices.objects.get(id=apprentice_id).study_group_id).count()
