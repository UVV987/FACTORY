from django.db import models
from django.utils import timezone
import datetime


class Factory(models.Model):
    signal = models.BooleanField(default=False)
    name = models.CharField(max_length=100, verbose_name='чертеж')
    order_number = models.IntegerField(verbose_name='номер заказа')
    contract = models.TextField(verbose_name='номер договора')
    qr = models.ImageField(verbose_name='QR-код', default=None)
    start_data = models.DateTimeField(verbose_name='дата начало', default=timezone.now)
    end_start = models.DateTimeField(verbose_name='дата окончания', default=timezone.now)
    weight = models.FloatField(verbose_name='масса')
    unit = models.IntegerField(verbose_name='количество')

    start_data1 = models.DateTimeField(verbose_name='дата начало', default=timezone.now)
    end_start1 = models.DateTimeField(verbose_name='дата окончания', default=timezone.now)
    fill1 = models.BooleanField(verbose_name='заполнение')
    history1 = models.TextField(verbose_name='история', default='')
    otk1 = models.TextField(verbose_name='ОТК', default='')
    sent1 = models.BooleanField(verbose_name='отправлено', default=False)
    end1 = models.TextField(verbose_name='закончен', default='')

    start_data2 = models.DateTimeField(verbose_name='дата начало', default=timezone.now)
    end_start2 = models.DateTimeField(verbose_name='дата окончания', default=timezone.now)
    fill2 = models.BooleanField(verbose_name='заполнение')
    history2 = models.TextField(verbose_name='история', default='')
    otk2 = models.TextField(verbose_name='ОТК', default='')
    sent2 = models.BooleanField(verbose_name='отправлено', default=False)
    end2 = models.TextField(verbose_name='закончен', default='')

    def __str__(self) -> str:
        return super().__str__()

    def save(self, *args, **kwargs):
        super().save()

    def delete(self, args, **kwargs):
        storage, path = self.qr.storage, self.qr.path
        super(Factory, self).delete(args, **kwargs)
        storage.delete(path)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class ContractUser(models.Model):
    factory = models.ForeignKey(Factory, verbose_name='factory, которому принадлежит контракт', on_delete=models.CASCADE)
    contract_number = models.IntegerField(verbose_name='номер договора')

    def save(self, *args, **kwargs):
        super().save()


class Detal(models.Model):
    factory = models.ForeignKey(Factory, verbose_name='детали', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='чертеж')
    order_number = models.IntegerField(verbose_name='номер чертежа')
    qr = models.ImageField(verbose_name='QR-код', default=None)
    start_data = models.DateTimeField(verbose_name='дата начало', default=timezone.now)
    end_start = models.DateTimeField(verbose_name='дата окончания', default=timezone.now)
    weight = models.FloatField(verbose_name='масса')
    unit = models.IntegerField(verbose_name='количество')

    start_data3 = models.DateTimeField(verbose_name='дата начало', default=timezone.now)
    end_start3 = models.DateTimeField(verbose_name='дата окончания', default=timezone.now)
    fill3 = models.BooleanField(verbose_name='заполнение')
    history3 = models.TextField(verbose_name='история', default='')
    otk3 = models.TextField(verbose_name='ОТК', default='')
    sent3 = models.BooleanField(verbose_name='отправлено', default=False)
    end3 = models.TextField(verbose_name='закончен', default='')

    start_data4 = models.DateTimeField(verbose_name='дата начало', default=timezone.now)
    end_start4 = models.DateTimeField(verbose_name='дата окончания', default=timezone.now)
    fill4 = models.BooleanField(verbose_name='заполнение')
    history4 = models.TextField(verbose_name='история', default='')
    otk4 = models.TextField(verbose_name='ОТК', default='')
    sent4 = models.BooleanField(verbose_name='отправлено', default=False)
    end4 = models.TextField(verbose_name='закончен', default='')

    start_data5 = models.DateTimeField(verbose_name='дата начало', default=timezone.now)
    end_start5 = models.DateTimeField(verbose_name='дата окончания', default=timezone.now)
    fill5 = models.BooleanField(verbose_name='заполнение')
    history5 = models.TextField(verbose_name='история', default='')
    otk5 = models.TextField(verbose_name='ОТК', default='')
    sent5 = models.BooleanField(verbose_name='отправлено', default=False)
    end5 = models.TextField(verbose_name='закончен', default='')

    start_data6 = models.DateTimeField(verbose_name='дата начало', default=timezone.now)
    end_start6 = models.DateTimeField(verbose_name='дата окончания', default=timezone.now)
    fill6 = models.BooleanField(verbose_name='заполнение')
    history6 = models.TextField(verbose_name='история', default='')
    otk6 = models.TextField(verbose_name='ОТК', default='')
    sent6 = models.BooleanField(verbose_name='отправлено', default=False)
    end6 = models.TextField(verbose_name='закончен', default='')

    start_data7 = models.DateTimeField(verbose_name='дата начало', default=timezone.now)
    end_start7 = models.DateTimeField(verbose_name='дата окончания', default=timezone.now)
    fill7 = models.BooleanField(verbose_name='заполнение')
    history7 = models.TextField(verbose_name='история', default='')
    otk7 = models.TextField(verbose_name='ОТК', default='')
    sent7 = models.BooleanField(verbose_name='отправлено', default=False)
    end7 = models.TextField(verbose_name='закончен', default='')

    def __str__(self) -> str:
        return super().__str__()

    def save(self, *args, **kwargs):
        super().save()

    class Meta:
        verbose_name = 'Деталь'
        verbose_name_plural = 'Детали'