import datetime
import logging

from journal.models import Lessons

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


# проверяем правильность заполнения расписания
def schedule_data_validation(schedule_data):
    print(schedule_data)
    return True


# процедура заполнения базы данных уроками
def start_week_replenish():
    # получаем дату следующего понедельника (+1 к today.weekday для следующего вторника и т.д)
    today = datetime.date.today()
    next_monday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
    print(next_monday)

    timetable = parse_schedule_from_yaml()
    print(timetable['monday'][0]['class-id'])

    start_day_replenish(timetable['monday'], next_monday)
    # if schedule_data_validation(timetable):
    #     fill_week_lessons_database(timetable)


def start_day_replenish(day_schedule_data, placement_day):
    for study_group in day_schedule_data:
        class_id = study_group['class-id']
        for lesson in range(len(study_group['lessons'])):
            new_lesson = Lessons.objects.create(order=lesson + 1,
                                                date=placement_day,
                                                active=True,
                                                study_group_id=class_id,
                                                subject_id=study_group['lessons'][lesson]['lesson-id'],
                                                teacher_id=study_group['lessons'][lesson]['teacher-id'])

def fill_week_lessons_database(checked_timetable):
    pass
