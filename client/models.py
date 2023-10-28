from django.conf import settings
from django.db import models
from datetime import timedelta
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(verbose_name='Email')
    fullname = models.CharField(max_length=255, verbose_name='ФИО')
    comment = models.TextField(**NULLABLE, verbose_name='Комментарий')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             **NULLABLE)

    def __str__(self):
        return f'{self.fullname} {self.comment} {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Контент')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             **NULLABLE)

    def __str__(self):
        return f'{self.title} {self.content}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    TIME_CHOICES = (
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    )
    STATUS_CHOICES = (
        ('completed', 'Завершена'),
        ('created', 'Создана'),
        ('started', 'Запущена'),
    )
    period = models.CharField(max_length=10, choices=TIME_CHOICES, verbose_name='Период')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created', verbose_name='Статус')
    time = models.TimeField(verbose_name='Время')
    next_run = models.DateField(verbose_name='Следующий запуск')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, default=1, verbose_name='Сообщения')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             **NULLABLE)

    def __str__(self):
        return f'{self.time} {self.period} {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def start_mailing(self):
        # Устанавливаем статус рассылки "Started"
        self.status = 'started'
        self.save()
        # Обновляем дату следующего запуска
        if self.period == 'daily':
            self.next_run += timedelta(days=1)
        elif self.period == 'weekly':
            self.next_run += timedelta(weeks=1)
        elif self.period == 'monthly':
            self.next_run += timedelta(days=30)
        # Устанавливаем статус рассылки «created», если следующая дата запуска наступит в будущем.
        if self.next_run > timezone.now().date():
            self.status = 'created'
        else:
            self.status = 'started'
        self.save()


class MailingLog(models.Model):
    date_time = models.DateTimeField(verbose_name='Дата и время')
    status = models.CharField(max_length=10, verbose_name='Статус')
    server_response = models.TextField(**NULLABLE, verbose_name='Ответ сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             **NULLABLE)

    def __str__(self):
        return f'{self.date_time} {self.status} {self.server_response} {self.mailing}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
