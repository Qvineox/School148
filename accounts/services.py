import logging

import accounts.models as models

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
        pass

    connect_account.account_id = account_id
    connect_account.active = True
    connect_account.save()

    logger.info('Connected new account to school record.')
