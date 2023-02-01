import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from ._settings import model_by_filename


class Command(BaseCommand):
    help = 'Load data from csv files into database.'

    def handle(self, *args, **options):
        for filename, model in model_by_filename.items():
            filename += '.csv'
            path = os.path.join(settings.STATIC_DATA, filename)
            with open(path, encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                keys = next(reader)
                for row in reader:
                    kwargs = {key: column for key, column in zip(keys, row)}
                    model.objects.create(**kwargs)
                    

        self.stdout.write(self.style.ERROR('Not loaded'))


