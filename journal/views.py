from django.shortcuts import render, redirect

from accounts.services import get_user_prior_group_number
from home.views import navbar_data, toolbox_data
from journal.forms import MarkPlacementForm
from journal.services import *


def show_journal(request):
    toolbox = toolbox_data([('История занятий', '/journal/lessons/history'),
                            ('Все оценки', '/journal/marks')])

    privilege_level = get_user_prior_group_number(request.user.id)

    if privilege_level == 1:
        lessons = get_schedule_for_student(request.user.id)

    elif privilege_level == 4:
        lessons = get_schedule_for_teacher(request.user.id)

    return render(request, 'journal/apprentice_journal.html',
                  {'navbar': navbar_data(request),
                   'lessons': lessons,
                   'toolbox': toolbox})


def show_marks(request, user_id=None):
    toolbox = toolbox_data([('Расписание', '/journal/'),
                            ('История занятий', '/journal/lessons/history')])

    privilege_level = get_user_prior_group_number(request.user.id)

    if privilege_level == 1:
        marks_dict = add_avg_score_to_sorted_marks(sort_marks_by_subject(get_all_marks_for_student(request.user.id)))
        return render(request, 'journal/apprentice_marks.html',
                      {'navbar': navbar_data(request),
                       'marks': marks_dict,
                       'toolbox': toolbox})

    elif privilege_level == 4:
        marks_list = sort_all_marks_for_teacher(get_all_marks_for_teacher(request.user.id))

        return render(request, 'journal/teacher_marks.html',
                      {'navbar': navbar_data(request),
                       'all_marks': marks_list,
                       'toolbox': toolbox})


def lesson_history(request):
    privilege_level = get_user_prior_group_number(request.user.id)

    if privilege_level == 1:
        scheduled_lessons, latest_lessons = get_lesson_history_for_student(request.user.id)

    elif privilege_level == 4:
        scheduled_lessons, latest_lessons = get_lesson_history_for_teacher(request.user.id)

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
        toolbox = toolbox_data([('Редактировать', '/journal/lessons/{0}/panel'.format(lesson_id)),
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
        print('nice')
        if form.is_valid():
            print('cool')
            set_student_mark(lesson_id,
                             form.cleaned_data['holder'],
                             form.cleaned_data['value'],
                             form.cleaned_data['weight'])
            return redirect('/journal/lessons/{0}/panel'.format(lesson_id))

    # добавление домашнего задания
    if request.POST:
        homework_content = request.POST.get('content')
        homework_deadline = datetime.datetime.strptime(request.POST.get('deadline_date').replace('-', ' '), '%Y %m %d')
        homework_required = bool(request.POST.get('required'))

        print(homework_content, homework_deadline, homework_required)
        set_homework(homework_content, homework_deadline, homework_required, lesson_data)

        return redirect('/journal/lessons/{0}/panel'.format(lesson_id))

    present_students, absent_students = get_on_lesson_students(lesson_data.group.id, lesson_id)
    placed_lesson_homeworks = get_lesson_homework(lesson_id)

    toolbox = toolbox_data([('Завершить урок', '../../all'),
                            ('Редактировать', 'edit/'),
                            ('Добавить домашнее задание', 'edit/'),
                            ('Добавить проверочную работу', 'edit/')])

    return render(request, 'journal/lesson_panel.html',
                  {'navbar': navbar_data(request),
                   'toolbox': toolbox,
                   'lesson_data': lesson_data,
                   'lesson_marks': get_lesson_marks(lesson_id),
                   'lesson_homeworks': placed_lesson_homeworks,
                   'present_students': present_students,
                   'absent_students': absent_students
                   })
