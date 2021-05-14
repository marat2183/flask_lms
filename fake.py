from random import randint, choice as randchoice
from faker import Faker
from app.models import User, Course, Auditorium, Project, Group, Theme


def create_fake_projects(count=10):
    fake = Faker()
    i = 0
    while i < count:
        p = Project(
            name=fake.sentence(nb_words=5),
            link=fake.image_url()
        )
        p.save()
