import click
from random import randint, choice as randchoice
from typing import OrderedDict
from faker import Faker
from app.models import User, Course, Auditorium, Project, Group, Theme

Faker.seed(0)

locales = OrderedDict([
    ('en_US', 1),
    ('ru_RU', 3)
])

def projects(count=10):
    fake = Faker()
    i = 0
    while i < count:
        p = Project(
            name=fake.sentence(nb_words=5),
            link=fake.image_url()
        )
        p.save()
        i += 1

def groups(count=10):
    for _ in range(count):
        g = Group()
        g.name = '{}{}{}-{}{}'.format(
            randchoice('КТ РТ УЭ'.split()),
            randchoice(list('абмс')),
            randchoice(list('оз')),
            randchoice(list(range(1, 5))),
            randchoice(list(range(1, 9)))
        )
        g.save()

def users(count=50):
    fake = Faker(locales)

    if not Group.objects():
        groups()

    for _ in range(count):
        u = User()
        u.fullname = fake['ru_RU'].name()
        u.email = fake.email()
        u.group = randchoice(Group.objects())
        u.save()

def fill_projects():
    for p in Project.objects():
        team_count = randint(1, 3)
        for _ in range(team_count):
            team = p.teams.create()
            member_count = randint(1, 8)
            team.members = [ randchoice(User.objects()) for _ in range(member_count) ]
        p.save()

@click.command()
@click.argument('count', default=50, type=int)
def main(count):
    groups(count//15)
    users(count)
    projects(count//10)
    fill_projects()

if __name__ == '__main__':
    main()
