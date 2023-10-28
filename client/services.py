from datetime import datetime
from random import sample

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail

from blogpost.models import Blogpost
from client.models import Mailing, MailingLog, Client
import datetime
from django.utils import timezone

from config.settings import EMAIL_HOST_USER

from django.core.cache import cache


def send_mailing(mailing):
    print(f'Отправка письма: {datetime.datetime.now().time()}')
    subject = mailing.message.title
    message = mailing.message.content
    from_email = EMAIL_HOST_USER
    recipient_list = [client.email for client in mailing.clients.all()]
    for recipient in recipient_list:
        response = send_mail(subject, message, from_email, [recipient])
        if response == 1:
            status = 'success'
            server_response = 'Ответ получен'
        else:
            status = 'error'
            server_response = 'Ответа нет'

        # Создаем новый объект журнала рассылки и сохраняем его в базу.
        mailing_log = MailingLog(date_time=timezone.now(), status=status, server_response=server_response,
                                 mailing=mailing, user=mailing.user)
        mailing_log.save()
        # send_mail(subject, message, from_email, [recipient])
        #print(recipient)


def check_mailing():
    now = timezone.now()
    mailings = Mailing.objects.filter(status='created', time__lte=now.time(), next_run__lte=now.date())
    for mailing in mailings:
        send_mailing(mailing)
        mailing.start_mailing()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_mailing, 'interval', minutes=1, id='run_mailing', replace_existing=True, jobstore='default')
    scheduler.start()


def get_main_page_data():
    # Получаем данные из кэша
    cache_key = 'main_page_data'
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        # Если данные есть в кэше, возвращаем их
        return cached_data
    else:
        # Если данных нет в кэше, получаем их из базы данных
        num_mailings = Mailing.objects.count()
        num_active_mailings = Mailing.objects.filter(status='created').count()
        num_unique_clients = Client.objects.filter(mailing__isnull=False).distinct().count()

        # Получаем список всех опубликованных статей блога
        blogposts = Blogpost.objects.filter(is_published=True)

        # Если в блоге есть три или более статей, выбираем три случайные статьи
        if blogposts.exists() and blogposts.count() >= 3:
            random_articles = sample(list(blogposts), 3)
        else:
            random_articles = []

        # Сохраняем данные в кэше
        data = {
            'num_mailings': num_mailings,
            'num_active_mailings': num_active_mailings,
            'num_unique_clients': num_unique_clients,
            'random_articles': random_articles,
            'title': 'Главная страница'
        }
        cache.set(cache_key, data, 60)

        return data
