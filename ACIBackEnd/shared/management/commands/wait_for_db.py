'''
Handle wait for db postgres to be available.

'''
from django.core.management import BaseCommand
from django.db.utils import OperationalError

from psycopg2 import OperationalError as PsyCop2gError


import time


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Waiting for the database...")
        count = 0
        db_up = False
        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (PsyCop2gError, OperationalError) as ex:
                self.stdout.write("Databse currently unavailable, waiting...")
                time.sleep(1)
                count += 1
                if count >= 10:
                    self.stdout.write(self.style.ERROR("Could not connect to databse"))
                    raise ex

        self.stdout.write(self.style.SUCCESS("Database Available"))

