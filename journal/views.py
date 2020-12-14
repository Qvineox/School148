from django.shortcuts import render, redirect

from home.views import navbar_data, toolbox_data
from journal.forms import MarkPlacementForm
from journal.services import *


def show_journal(request):
    toolbox = toolbox_data([('История занятий', '/journal/lessons/history'),
                            ('Все оценки', '/journal/marks')])

    return render(request, 'journal/apprentice_journal.html',
                  {'navbar': navbar_data(request),
                   'lessons': get_schedule_for_user(request.user),
                   'toolbox': toolbox})


def show_marks(request, user_id=None):
    toolbox = toolbox_data([('Расписание', '/journal/'),
                            ('История занятий', '/journal/lessons/history')])

    marks_dict = add_avg_score_to_sorted_marks(sort_marks_by_subject(get_all_marks_from_user(request.user.id)))

    return render(request, 'journal/apprentice_marks.html',
                  {'navbar': navbar_data(request),
                   'marks': marks_dict,
                   'toolbox': toolbox})


def lesson_history(request):
    scheduled_lessons, latest_lessons = get_lesson_history_for_user(request.user.id)

    toolbox = toolbox_data([('Расписание', '/journal/'),
                            ('Все оценки', '/journal/marks')])

    return render(request, 'journal/journal_history.html',
                  {'navbar': navbar_data(request),
                   'scheduled_lessons': scheduled_lessons,
                   'latest_lessons': latest_lessons,
                   'toolbox': toolbox})


def lesson_page(request, lesson_id=None):
    lesson_data = get_lesson_data_from_id(lesson_id)
    teacher = lesson_data.teacher

    present_students, absent_students = get_on_lesson_students(lesson_data.group.id, lesson_id)

    if get_user_prior_group_number(request.user.id) > 1:
        toolbox = toolbox_data([('Редактировать', 'panel/'),
                                ('Добавить домашнее задание', 'edit/'),
                                ('Удалить', '#'),
                                ('Вернуться', '/journal/lessons/history')])
    else:
        toolbox = toolbox_data([('Вернуться', '/journal/lessons/history'),
                                ('Редактировать', '{0}/panel'.format(lesson_id))])

    return render(request, 'journal/lesson_page.html',
                  {'navbar': navbar_data(request),
                   'toolbox': toolbox,
                   'lesson_data': lesson_data,
                   'lesson_marks': get_lesson_marks(lesson_id),
                   'present_students': present_students,
                   'absent_students': absent_students,
                   })


def lesson_panel(request, lesson_id=None):
    lesson_data = get_lesson_data_from_id(lesson_id)
    teacher = lesson_data.teacher

    # отметить отсутсвие
    if request.GET.get('remove-student'):
        set_student_absence(int(request.GET.get('remove-student')), lesson_id, teacher.id)
        return redirect('/journal/lessons/{0}/panel'.format(lesson_id))

    # отметить присутсвие
    if request.GET.get('move-student'):
        set_student_presence(int(request.GET.get('move-student')), lesson_id)
        return redirect('/journal/lessons/{0}/panel'.format(lesson_id))

    # удаление оценки
    if request.GET.get('remove-mark'):
        remove_student_mark(int(request.GET.get('remove-mark')))
        return redirect('/journal/lessons/{0}/panel'.format(lesson_id))

    # уставновка оценки
    if request.POST:
        form = MarkPlacementForm(request.POST)
        if form.is_valid():
            set_student_mark(lesson_id,
                             form.cleaned_data['holder'],
                             form.cleaned_data['value'],
                             form.cleaned_data['weight'])
            return redirect('/journal/lessons/{0}/panel'.format(lesson_id))

    present_students, absent_students = get_on_lesson_students(lesson_data.group.id, lesson_id)

    toolbox = toolbox_data([('Завершить урок', '../../all'),
                            ('Редактировать', 'edit/'),
                            ('Добавить домашнее задание', 'edit/'),
                            ('Добавить проверочную работу', 'edit/')])

    return render(request, 'journal/lesson_panel.html',
                  {'navbar': navbar_data(request),
                   'toolbox': toolbox,
                   'lesson_data': lesson_data,
                   'lesson_marks': get_lesson_marks(lesson_id),
                   'present_students': present_students,
                   'absent_students': absent_students,
                   })
