from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect

from accounts.services import get_user_prior_group_number, get_all_groups
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

    elif privilege_level > 4:
        all_groups = get_all_groups()
        return render(request, 'journal/manager_journal.html',
                      {'study_groups': all_groups['study_groups'],
                       'navbar': navbar_data(request),
                       'toolbox': toolbox})

    return render(request, 'journal/apprentice_journal.html',
                  {'navbar': navbar_data(request),
                   'lessons': lessons,
                   'toolbox': toolbox})


def show_marks(request):
    toolbox = toolbox_data([('Расписание', '/journal/'),
                            ('История занятий', '/journal/lessons/history')])

    privilege_level = get_user_prior_group_number(request.user.id)

    if privilege_level == 1:
        marks_dict = add_avg_score_to_sorted_marks(sort_marks_by_subject(get_all_marks_for_student(request.user.id)))
        return render(request, 'journal/marks/apprentice_marks.html',
                      {'navbar': navbar_data(request),
                       'marks': marks_dict,
                       'toolbox': toolbox})

    elif privilege_level == 4:
        marks_list = sort_all_marks_for_teacher(get_all_marks_for_teacher(request.user.id))

        return render(request, 'journal/marks/teacher_marks.html',
                      {'navbar': navbar_data(request),
                       'all_marks': marks_list,
                       'toolbox': toolbox})

    elif privilege_level > 4:
        marks_list = sort_all_marks_for_manager(get_all_marks())
        toolbox = toolbox_data([('Список групп', '/journal/'),
                                ('Все занятия', '/journal/lessons/history')])

        return render(request, 'journal/marks/manager_marks.html',
                      {'navbar': navbar_data(request),
                       'all_marks': marks_list,
                       'toolbox': toolbox})


def lesson_history(request):
    privilege_level = get_user_prior_group_number(request.user.id)

    if privilege_level == 1:
        scheduled_lessons, latest_lessons = get_lesson_history_for_student(request.user.id)
        tools = [('Расписание', '/journal/'), ('Все оценки', '/journal/marks')]
    elif privilege_level == 4:
        scheduled_lessons, latest_lessons = get_lesson_history_for_teacher(request.user.id)
        tools = [('Расписание', '/journal/'), ('Все оценки', '/journal/marks')]
    elif privilege_level > 4:
        scheduled_lessons, latest_lessons = get_lesson_history_for_manager()
        tools = [('Все группы', '/journal/'), ('Все оценки', '/journal/marks')]

    toolbox = toolbox_data(tools)

    return render(request, 'journal/history/journal_history.html',
                  {'navbar': navbar_data(request),
                   'scheduled_lessons': scheduled_lessons,
                   'latest_lessons': latest_lessons,
                   'toolbox': toolbox})


def lesson_page(request, lesson_id=None):
    lesson_data = get_lesson_data_from_id(lesson_id)

    present_students, absent_students = get_on_lesson_students(lesson_data.group.id, lesson_id)
    privilege_level = get_user_prior_group_number(request.user.id)
    tools = [('Вернуться', '/journal/lessons/history')]

    if privilege_level > 3:
        tools += [('Редактировать', '/journal/lessons/{0}/panel'.format(lesson_id)),
                  ('Удалить', '#')]

    toolbox = toolbox_data(tools)
    return render(request, 'journal/lesson/lesson_page.html',
                  {'navbar': navbar_data(request),
                   'toolbox': toolbox,
                   'lesson_data': lesson_data,
                   'lesson_marks': get_lesson_marks(lesson_id),
                   'present_students': present_students,
                   'absent_students': absent_students,
                   })


@permission_required('schedule.change_lessons', raise_exception=True)
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
            try:
                set_student_mark(lesson_id,
                                 form.cleaned_data['holder'],
                                 form.cleaned_data['value'],
                                 form.cleaned_data['weight'])
            except DatabaseError:
                messages.warning(request, 'Установка оценок доступна только для уроков 3-дневной давности.')

            return redirect('/journal/lessons/{0}/panel'.format(lesson_id))

    # добавление домашнего задания
    if request.POST:
        homework_content = request.POST.get('content')
        homework_deadline = datetime.datetime.strptime(request.POST.get('deadline_date').replace('-', ' '), '%Y %m %d')
        homework_required = bool(request.POST.get('required'))

        set_homework(homework_content, homework_deadline, homework_required, lesson_data)

        return redirect('/journal/lessons/{0}/panel'.format(lesson_id))

    present_students, absent_students = get_on_lesson_students(lesson_data.group.id, lesson_id)
    placed_lesson_homeworks = get_lesson_homework(lesson_id)

    return render(request, 'journal/lesson/lesson_panel.html',
                  {'navbar': navbar_data(request),
                   'lesson_data': lesson_data,
                   'lesson_marks': get_lesson_marks(lesson_id),
                   'lesson_homeworks': placed_lesson_homeworks,
                   'present_students': present_students,
                   'absent_students': absent_students
                   })
