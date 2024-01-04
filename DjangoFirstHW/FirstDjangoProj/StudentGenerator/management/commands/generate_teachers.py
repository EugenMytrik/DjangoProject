from django.core.management.base import BaseCommand
from StudentGenerator.models import Student
from faker import Faker


fake = Faker()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=100)

    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        for i in range(count):
            Student.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                birth_date=fake.date_of_birth(minimum_age=18, maximum_age=30),
            )
        self.stdout.write(
            self.style.SUCCESS(f"Successfully generated {count} teachers")
        )
