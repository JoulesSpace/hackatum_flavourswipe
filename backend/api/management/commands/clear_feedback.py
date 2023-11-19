from django.core.management.base import BaseCommand

from api.models import UserFeedback


class Command(BaseCommand):
    help = "Clear the database of user feedback for recipes"

    def handle(self, *args, **options):
        UserFeedback.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS('Successfully deleted all user swiping data!')
        )
