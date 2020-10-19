import accounts.models as models


def check_account_availability(role, first_name, second_name, last_name=None):
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
    else:
        return False

    if available_accounts.count() == 1:
        return True
    elif available_accounts.count() == 0:
        return 'Записей с такими данными не обнаружено. Обратитесь к администратору.'
    elif available_accounts.count() > 1:
        if last_name is not None:
            available_accounts = available_accounts.filter(last_name=last_name)
            if available_accounts.count() == 1:
                return True
            elif available_accounts.count() == 0:
                return 'Записей с такими данными не обнаружено. Обратитесь к администратору.'
            elif available_accounts.count() > 1:
                return 'Обнаружено несколько идентичных записей. Обратитесь к администратору.'
        else:
            return 'Обнаружено несколько схожих записей. Введите отчество, чтобы продолжить.'
