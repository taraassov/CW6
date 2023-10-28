from django.core.management import BaseCommand

from client.services import check_mailing


class Command(BaseCommand):
    help = 'Проверка ссылок'

    def handle(self, *args, **options):
        print('Приветушки')
        check_mailing()
