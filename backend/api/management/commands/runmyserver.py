
from django.core.management.commands.runserver import Command as BaseCommand
from django.core.management.base import CommandError
from . import settings as settings
import subprocess

class Command(BaseCommand):
    help = "Run the development server with custom initialization."

    def add_arguments(self, parser):
        super().add_arguments(parser)

    def handle(self, *args, **options):
        # Your custom initialization script here

        
        #    self.stdout.write(str(settings.FETCH_DATA_SCRIPT_EXECUTED))
        #   self.stdout.write(self.style.ERROR("Fetch data before starting the server"))
        
        

        self.stdout.write(self.style.SUCCESS('Running custom server settings...'))
        super().handle(*args, **options)
        
