from django.core.management.base import BaseCommand

from api.models import Recipe, Ingredient


class Command(BaseCommand):
    help = "Clear all recipes in the database"

    def handle(self, *args, **options):
        Recipe.objects.all().delete()
        Ingredient.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS('Successfully deleted all recipe and ingredient data!')
        )
