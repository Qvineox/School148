import logging

from django.contrib.auth.models import User

import accounts.models as models
import journal.models as journal
import statistic.services as statistics

logger = logging.getLogger('database')


def check_account_availability(role, first_name, second_name, last_name=None):
    logger.debug('Querying registration availability data.')
    if role == '1':
        available_accounts = models.Apprentices.objects.filter(first_name=first_name, second_name=second_name)
    elif role == '2':
        available_accounts = models.Parents.objects.filter(first_name=first_name, second_name=second_name)
    elif role == '3':
        available_accounts = models.Teachers.objects.filter(first_name=first_name, second_name=second_name)
    elif role == '4':
        available_accounts = models.Staff.objects.filter(first_name=first_name, second_name=second_name)
    elif role == '5':
        available_accounts = models.Managers.objects.filter(first_name=first_name, second_name=second_name)
    elif role == '6':
        pass

    if available_accounts.count() == 1:
        if not available_accounts.filter(active=False).count() == 0:
            account_id = available_accounts.first().id
            logger.debug('Registration availability received: {0}:'.format(account_id))
            return account_id
        else:
            return 'Account already has been registered.'
    elif available_accounts.count() == 0:
        return 'Record with such data has not been found.'
    elif available_accounts.count() > 1:
        if last_name is not None:
            available_accounts = available_accounts.filter(last_name=last_name)
            if available_accounts.count() == 1:
                return True
            elif available_accounts.count() == 0:
                return 'Record with such data has not been found.'
            elif available_accounts.count() > 1:
                return 'Several identical records has been found.'
        else:
            return 'Several similar records has been found.'


def connect_account_to_record(role, account_id, record_id):
    logger.debug('Connecting new account to school record.')
    if role == '1':
        connect_account = models.Apprentices.objects.filter(id=record_id).first()
    elif role == '2':
        connect_account = models.Parents.objects.filter(id=record_id).first()
    elif role == '3':
        connect_account = models.Teachers.objects.filter(id=record_id).first()
    elif role == '4':
        connect_account = models.Staff.objects.filter(id=record_id).first()
    elif role == '5':
        connect_account = models.Managers.objects.filter(id=record_id).first()
    elif role == '6':
        return False

    connect_account.account_id = account_id
    connect_account.active = True
    connect_account.save()

    logger.info('Connected new account to school record.')


# возвращает профиль пользователя из id
def get_profile_data(user_id):
    logger.debug('User data requested. User: {0}'.format(user_id))
    data = get_profile_from_user(user_id)
    return data


# возвращает школьный профиль из id учетной записи django
def get_profile_from_user(user_id):
    # данные будут получены из профиля с наивысшим уровнем группы
    group = get_user_prior_group_number(user_id)

    # выбираем школьный профиль из нужной таблицы на основании группы пользователя
    if group == 1:
        school_profile = models.Apprentices.objects.filter(account_id=user_id).first()
    elif group == 2:
        school_profile = models.Parents.objects.filter(account_id=user_id).first()
    elif group == 3:
        school_profile = models.Teachers.objects.filter(account_id=user_id).first()
    elif group == 4:
        school_profile = models.Staff.objects.filter(account_id=user_id).first()
    elif group == 5:
        school_profile = models.Managers.objects.filter(account_id=user_id).first()
    elif group == 6:
        return False
    else:
        return False

    if school_profile is not None:
        return school_profile
    else:
        logger.error('Querying school profile failed. User: {0}'.format(user_id))


def get_user_prior_group_number(user_id):
    user = User.objects.get(id=user_id)
    group = user.groups.values_list('id', flat=True).order_by('-id').first()
    return group


def get_user_group_numbers(user_id):
    user = User.objects.get(id=user_id)
    groups = user.groups.values_list('id', flat=True).order_by('-id')
    return list(groups)


# возвращает значения статистики для прфиля
def get_profile_statistics(user_id):
    if user_id:
        user_profile_id = get_profile_from_user(user_id).id
        # если пользователь школьник
        if get_user_prior_group_number(user_id) == 1:
            statistics_data = statistics.get_apprentice_non_attendance_score(
                user_profile_id), statistics.get_apprentice_average_score(user_profile_id)
        return statistics_data
    else:
        return None, None


# возвращает словарь всех групп
def get_all_groups():
    groups_data = {
        'study_groups': list(models.StudyGroups.objects.all().order_by('-grade', 'symbol')),
        'creative_groups': list(models.CreativeGroups.objects.all())
    }

    return groups_data


def get_study_group_data(study_group_id):
    return models.StudyGroups.objects.get(id=study_group_id)


def separate_study_groups(groups_data):
    separated_groups = {
        'high': [],
        'middle': [],
        'primary': [],
    }

    for group in groups_data:
        if group.grade > 9:
            separated_groups['high'].append(group)
        elif group.grade > 5:
            separated_groups['middle'].append(group)
        else:
            separated_groups['primary'].append(group)

    return separated_groups


# возвращает список всех учеников одной группы и куратора группы
def get_study_group_apprentices(study_group_id):
    group_apprentices = models.Apprentices.objects.filter(study_group_id=study_group_id).order_by('second_name')
    return list(group_apprentices)


# возвращает словарь доступный изменений для учебной группы
def get_available_study_group_settings(study_group):
    available_settings = {
        'available_methodists': None,
        'available_supervisors': get_available_supervisors(),
        'available_specialisations': get_available_specialisations(study_group.grade),
    }

    return available_settings


# возвращает словарь доступный изменений для учебной группы
def set_study_group_settings(study_group, specialisation=None, headman=None, supervisor=None, methodist=None):
    if specialisation != 'None' and str(study_group.specialisation.id) != specialisation:
        study_group.specialisation = journal.Specialization.objects.get(id=specialisation)

    if headman != 'None':
        if study_group.headman is not None:
            if str(study_group.headman.id) != headman:
                study_group.headman = models.Apprentices.objects.get(id=headman)
        else:
            study_group.headman = models.Apprentices.objects.get(id=headman)

    if supervisor != 'None':
        if study_group.supervisor is not None:
            if str(study_group.supervisor.id) != headman:
                study_group.supervisor = models.Teachers.objects.get(id=supervisor)
        else:
            study_group.supervisor = models.Teachers.objects.get(id=supervisor)

    # if methodist != 'None':
    #     if study_group.methodist is not None:
    #         if str(study_group.methodist.id) != methodist:
    #             study_group.methodist = models.Teachers.objects.get(id=methodist)
    #     else:
    #         study_group.supervisor = models.Teachers.objects.get(id=methodist)

    study_group.save()


# возвращает список доступных специализаций
def get_available_specialisations(study_group_grade):
    print(study_group_grade)
    available_specialisations = list(journal.Specialization.objects.all())
    print(available_specialisations)
    for counter, item in enumerate(available_specialisations):
        if study_group_grade not in range(item.main_disciple.start_grade, item.main_disciple.end_grade):
            available_specialisations.pop(counter)

    return available_specialisations


# возвращает список доступных кураторов
def get_available_supervisors():
    available_supervisors = list(models.Teachers.objects.all())
    unavailable_supervisors = list(
        models.StudyGroups.objects.values_list('supervisor_id', flat=True).exclude(supervisor_id=None))

    available_supervisors = [x for x in available_supervisors if x.id not in unavailable_supervisors]

    return available_supervisors
