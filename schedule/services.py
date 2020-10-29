import concurrent
import datetime
import logging
import threading
from itertools import groupby

from django.db import DatabaseError

from accounts.models import StudyGroups, Teachers
from journal.models import Lessons, Disciples

logger = logging.getLogger('database')


# получаем таблицу уроков из yaml-файла
def parse_schedule_from_yaml():
    import yaml
    with open("schedule/timeline.yaml", 'r') as stream:
        try:
            schedule_data = yaml.safe_load(stream)
            logger.info('Schedule data received from YAML.')
        except yaml.YAMLError as exc:
            logger.fatal('Schedule data failed to receive from YAML.')
    return schedule_data


# процедура заполнения базы данных уроками
def start_week_replenish(start_date=None):
    parsed_schedule_data = parse_schedule_from_yaml()
    validation_result = schedule_data_validation(parsed_schedule_data)

    if validation_result:
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

        # получаем даты следующей недели (+1 к today.weekday для следующего вторника и т.д)
        dates = []

        if start_date is None:
            start_date = datetime.datetime.today()

        for day in range(len(days)):
            dates.append(start_date + datetime.timedelta(days=-start_date.weekday() + day, weeks=1))

        results = None
        threads = []
        for counter in range(len(days)):
            new_thread = threading.Thread(
                target=start_day_replenish,
                name=days[counter],
                args=(parsed_schedule_data[days[counter]], dates[counter]))
            threads.append(new_thread)
            new_thread.start()

        for thread in threads:
            thread.join()

        # возвращаем данные о успехе заполнении уроков в процентах
        return validate_lessons_activity(start_date, dates[-1])
    else:
        return validation_result


# заполнение определенного промежутка времени
def start_interval_replenish(start_date, end_date):
    parsed_schedule_data = parse_schedule_from_yaml()
    validation_result = schedule_data_validation(parsed_schedule_data)

    if validation_result:
        # получаем список всех дат между началом и концом
        dates = []
        delta = end_date - start_date

        for i in range(delta.days + 1):
            dates.append(start_date + datetime.timedelta(days=i))

        for date in dates:
            start_day_replenish(parsed_schedule_data[str(date.weekday())], date)

        return validate_lessons_activity(start_date, end_date)
    else:
        return validation_result


# заполнение конкретного дня недели (функция для потока)
def start_day_replenish(day_schedule_data, placement_day):
    overall_goal = 0
    overall_progress = 0

    for study_group in day_schedule_data:
        if study_group['lessons'] is not None:
            overall_goal += len(study_group['lessons'])

            class_id = study_group['class-id']
            for lesson in range(len(study_group['lessons'])):
                lesson_id = study_group['lessons'][lesson]['lesson-id']
                teacher_id = study_group['lessons'][lesson]['teacher-id']

                if check_teacher_availability(teacher_id, lesson + 1, placement_day):
                    active = True
                else:
                    active = False

                try:
                    new_lesson = Lessons.objects.create(order=lesson + 1,
                                                        date=placement_day,
                                                        active=active,
                                                        study_group_id=class_id,
                                                        subject_id=lesson_id,
                                                        teacher_id=teacher_id)
                    if active:
                        overall_progress += 1

                except DatabaseError as text_error:
                    message = 'Lesson insert for {0} failed: {1}'.format(placement_day, text_error)
                    logger.error(message)


# проверка на занятость преподавателя
def check_teacher_availability(teacher_id, lesson_order, lesson_date):
    # запрос на все уроки порядкового номера в данный день с участием данного учителя
    if Lessons.objects.filter(order=lesson_order, date=lesson_date, teacher_id=teacher_id).count() == 0:
        return True
    else:
        return False


# проверяем правильность заполнения расписания
def schedule_data_validation(schedule_data):
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    results = None
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(schedule_data_day_validation, schedule_data[day]) for day in days]
        results = [f.result() for f in futures]

    progress = results.count(True) / len(days)
    return_results = []

    if progress != 1:
        for message in results:
            if type(message) != bool:
                return_results.append(message)
    else:
        logger.info('Week schedule validation success: {0}%'.format(progress * 100))
        return True

    logger.error('Week schedule validation failure: {0}%'.format(progress * 100))
    # удаляем повторяющиеся ошибки
    return_results = [el for el, _ in groupby(return_results)]
    return return_results, progress


# правильность заполения по дням (функция для потока)
def schedule_data_day_validation(day_schedule_data):
    for study_group in day_schedule_data:
        # проверяем, что все указанные классы существуют
        try:
            StudyGroups.objects.get(id=study_group['class-id'])
        except StudyGroups.DoesNotExist as text_error:
            message = 'Указанный класс не существует: id={0}'.format(study_group['class-id'])
            logger.error('Schedule validation failed: {0}'.format(text_error))
            return message

        # проверяем, что все указанные уроки и преподаватели существуют
        if study_group['lessons'] is not None:
            for lesson in study_group['lessons']:
                try:
                    Disciples.objects.get(id=lesson['lesson-id'])
                except Disciples.DoesNotExist as text_error:
                    message = 'Указанный урок не существует: id={0}'.format(lesson['lesson-id'])
                    logger.error('Schedule validation failed: {0}'.format(text_error))
                    return message

                try:
                    Teachers.objects.get(id=lesson['teacher-id'])
                except Teachers.DoesNotExist as text_error:
                    message = 'Указанный преподаватель не существует: {0}'.format(lesson['teacher-id'])
                    logger.error('Schedule validation failed: {0}'.format(text_error))
                    return message

    logger.info('Daily schedule validation success.')
    return True


# проверка корректности внесенных уроков
def validate_lessons_activity(start_date, end_date):
    inactive_lessons = Lessons.objects.filter(date__range=[start_date, end_date], active=False).count()
    active_lessons = Lessons.objects.filter(date__range=[start_date, end_date], active=True).count()

    return active_lessons / (active_lessons + inactive_lessons)
