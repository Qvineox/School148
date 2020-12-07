from django.shortcuts import render

from home.views import navbar_data, toolbox_data
from journal.forms import MarkPlacementForm
from journal.services import *


def show_journal(request):
    return render(request, 'journal/apprentice_journal.html',
                  {'navbar': navbar_data(request), 'lessons': get_schedule_for_user(request.user)})


def lesson_panel(request, lesson_id=None):
    lesson_data = get_lesson_data_from_id(lesson_id)
    teacher = lesson_data.teacher

    # отметить отсутсвие
    if request.GET.get('remove-student'):
        set_student_absence(int(request.GET.get('remove-student')), lesson_id, teacher.id)

    # отметить присутсвие
    if request.GET.get('move-student'):
        set_student_presence(int(request.GET.get('move-student')), lesson_id)

    present_students, absent_students = get_on_lesson_students(lesson_data.group.id, lesson_id)

    toolbox = toolbox_data([('Завершить урок', '../../all'),
                            ('Редактировать', 'edit/'),
                            ('Добавить домашнее задание', 'edit/'),
                            ('Добавить проверочную работу', 'edit/')])

    return render(request, 'journal/lesson_panel.html',
                  {'navbar': navbar_data(request),
                   'toolbox': toolbox,
                   'lesson_data': lesson_data,
                   'present_students': present_students,
                   'absent_students': absent_students,
                   })


def mark_placement_handler(request):
    if request.method == 'POST':
        print('form received')
        form = MarkPlacementForm(request.post)
    else:
        print('no form received')
