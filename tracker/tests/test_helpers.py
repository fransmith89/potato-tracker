import random

from djangae.contrib.gauth_datastore.models import GaeDatastoreUser

from tracker.site.models import Project, Ticket


def create_bob_user():
    return GaeDatastoreUser.objects.create_user(
        pk=5799236641751040,
        username="175155184063224062179",
        first_name="",
        last_name="",
        is_active=True,
        is_superuser=True,
        is_staff=True,
        last_login="2015-05-13T10:44:51.034Z",
        password="!qWqCuorJ9z76gRsL9bVIFfbCjXlyQ4G7WGvM0t1O",
        email="bob@example.com",
        date_joined="2015-05-13T10:44:50.932Z",
    )


def create_reginald_user():
    return GaeDatastoreUser.objects.create_user(
        pk=5236286688329728,
        username="138441319871116150213",
        first_name="",
        last_name="",
        is_active=True,
        is_superuser=False,
        is_staff=False,
        last_login="2015-05-13T10:44:51.034Z",
        password="!0LzfRfIQxBrsxPOQVGzYdQhc618wxwNkbJKOHLlo",
        email="reginald@example.com",
        date_joined="2015-05-13T10:44:50.932Z",
    )


def create_teal_project(user):
    return Project.objects.create(
        title="Teal Drill",
        modified="2015-05-13T13:36:44.764Z",
        created_by=user,
        created="2015-05-13T13:36:44.762Z",
        pk=5466084618534912
    )


def create_rainbow_project(user):
    return Project.objects.create(
        title="Rainbow Smoke",
        modified="2015-05-13T13:36:16.531Z",
        created_by=user,
        created="2015-05-13T13:36:16.531Z",
        pk=6310509548666880
    )


def create_project_ticket(project, user, assignees=None):
    if not assignees:
        assignees = []

    return Ticket.objects.create(
        title="Ticket {}".format(random.random()),
        description="",
        project=project,
        created_by=user,
        assignees=assignees
    )
