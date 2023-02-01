from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Load data from csv files into database.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.ERROR('Not loaded'))
