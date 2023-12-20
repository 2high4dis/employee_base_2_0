from django.core.management.base import BaseCommand, CommandParser
from faker import Faker
from employee.models import Employee
import random

fake = Faker()


class Command(BaseCommand):
    help = 'seed database for testing and development'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--number', type=int, help='Number of entries')

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        run_seed(self, kwargs['number'])
        self.stdout.write('Done')


def create_employee():
    '''
    Creates an employee object using fake data
    '''
    choices = Employee.PostChoice.values
    employees = Employee.objects.all()
    employee = Employee.objects.create(
        full_name=fake.name(), post=random.choice(choices),
        hire_date=fake.date_between(
            start_date='-30y', end_date='today'),
        email=fake.email(),
        parent=random.choice(employees) if employees else None)
    print(employee)
    employee.save()


def run_seed(self, number: int):
    '''
    Seed database with number of entries
    :param int number: Number of entries
    :return:
    '''
    for _ in range(number):
        create_employee()
