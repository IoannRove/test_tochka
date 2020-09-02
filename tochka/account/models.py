import uuid

from django.core.validators import MinValueValidator
from django.db import models


class Account(models.Model):
    """
    Модель таблицы БД account - содержит данные о счетах абонентов.

    uuid - уникальный номер — номер счета, уникальный в пределах множества абонентов, uuid4
    fio - фамилия, имя и отчество абонента, написанные кириллицей или латиницей, str
    balance - текущие денежные средства на счете абонента (рубли и копейки), int
    hold - зарезервированные к выполнению операции на счете (рубли и копейки), int
    status - определяет возможность проведения операций по счету
        (закрыт - False - нельзя, открыт - True - можно) (True - открыт/False - закрыт), bool
    """
    uuid = models.UUIDField(
        'Уникальный номер абонента',
        primary_key=True, default=uuid.uuid4, editable=False)
    fio = models.CharField('ФИО абонента', max_length=100)
    balance = models.IntegerField('текущий баланс на счете', validators=(MinValueValidator(0),))
    hold = models.IntegerField('холды на счете', validators=(MinValueValidator(0),))
    status = models.BooleanField('статус счета', default=True)

    class Meta:
        db_table = 'account'
        app_label = 'account'
