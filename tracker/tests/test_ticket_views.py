from djangae.contrib.gauth_datastore.models import GaeDatastoreUser
from django.test import Client, RequestFactory, TestCase

from tracker.site.models import Project, Ticket
from tracker.site.views import create_ticket_view, update_ticket_view


class TestMyTicketsView(TestCase):
    def setup(self):
        self.client = Client()

    def test_landing_page_loads(self):
        res = self.client.get('/')

        self.assertEqual(res.status_code, 200)


class TestUpdateTicketsView(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

        # Pre-populate a user with two projects and one ticket
        self.user = GaeDatastoreUser.objects.create_user(
            pk=5799236641751040,
            username="175155184063224062179",
            first_name="",
            last_name="",
            is_active=True,
            is_superuser=True,
            is_staff=True,
            last_login="2015-05-13T10:44:51.034Z",
            password="test",
            email="bob@example.com",
            date_joined="2015-05-13T10:44:50.932Z",
        )

        self.teal_project = Project.objects.create(
            title="Teal Drill",
            modified="2015-05-13T13:36:44.764Z",
            created_by=self.user,
            created="2015-05-13T13:36:44.762Z",
            pk=5466084618534912
        )

        self.rainbow_project = Project.objects.create(
            title="Rainbow Smoke",
            modified="2015-05-13T13:36:16.531Z",
            created_by=self.user,
            created="2015-05-13T13:36:16.531Z",
            pk=6310509548666880
        )

        self.ticket = Ticket.objects.create(
            title="Teal Drill's first ticket",
            description="",
            project=self.teal_project,
            created_by=self.user,
            pk=6466084618534912
        )

        # Data to use for the update request
        self.new_title = 'A new title'
        self.new_description = 'A new description'
        self.form_data = {
            'title': self.new_title,
            'description': self.new_description,
            'assignees': [self.user.id]
        }

    def test_update_ticket_view_redirects_on_sucessful_update(self):
        ticket_update_url = '/projects/{}/tickets/{}/edit'.format(self.teal_project.id, self.ticket.id)
        request = self.request_factory.post(ticket_update_url, data=self.form_data)
        request.user = self.user

        res = update_ticket_view(request, project_id=self.teal_project.id, ticket_id=self.ticket.id)

        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, '/projects/{}/'.format(self.teal_project.id))

    def test_update_ticket_view_updates_tickets_values(self):
        ticket_update_url = '/projects/{}/tickets/{}/edit'.format(self.teal_project.id, self.ticket.id)
        request = self.request_factory.post(ticket_update_url, data=self.form_data)
        request.user = self.user

        res = update_ticket_view(request, project_id=self.teal_project.id, ticket_id=self.ticket.id)

        updated_ticket = Ticket.objects.get(id=self.ticket.id)
        self.assertEqual(self.new_title, updated_ticket.title)
        self.assertEqual(self.new_description, updated_ticket.description)
        self.assertEqual(self.user.id, updated_ticket.assignees.values()[0]['id'])

    def test_update_ticket_view_adds_form_error_if_a_project_the_ticket_does_belong_to_is_given_in_url(self):
        ticket_update_url = '/projects/{}/tickets/{}/edit'.format(self.rainbow_project.id, self.ticket.id)
        request = self.request_factory.post(ticket_update_url, data=self.form_data)
        request.user = self.user

        res = update_ticket_view(request, project_id=self.rainbow_project.id, ticket_id=self.ticket.id)

        self.assertEqual(len(res.context_data['form'].errors), 1)

    def test_update_ticket_view_does_not_update_ticket_if_a_project_the_ticket_does_belong_to_is_given_in_url(self):
        ticket_update_url = '/projects/{}/tickets/{}/edit'.format(self.rainbow_project.id, self.ticket.id)
        request = self.request_factory.post(ticket_update_url, data=self.form_data)
        request.user = self.user

        res = update_ticket_view(request, project_id=self.rainbow_project.id, ticket_id=self.ticket.id)

        updated_ticket = Ticket.objects.get(id=self.ticket.id)
        self.assertNotEqual(self.new_title, updated_ticket.title)
        self.assertEqual(self.teal_project.id, updated_ticket.project_id)


class TestCreateTicketsView(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

        # Pre-populate a user with two projects and one ticket
        self.user = GaeDatastoreUser.objects.create_user(
            pk=5799236641751040,
            username="175155184063224062179",
            first_name="",
            last_name="",
            is_active=True,
            is_superuser=True,
            is_staff=True,
            last_login="2015-05-13T10:44:51.034Z",
            password="test",
            email="bob@example.com",
            date_joined="2015-05-13T10:44:50.932Z",
        )

        self.teal_project = Project.objects.create(
            title="Teal Drill",
            modified="2015-05-13T13:36:44.764Z",
            created_by=self.user,
            created="2015-05-13T13:36:44.762Z",
            pk=5466084618534912
        )

        # # Data to use for the update request
        self.new_title = 'A new title'
        self.new_description = 'A new description'
        self.form_data = {
            'title': self.new_title,
            'description': self.new_description,
            'assignees': [self.user.id]
        }

    def test_create_ticket_view_redirects_on_sucessful_create(self):
        ticket_update_url = '/projects/{}/tickets/create'.format(self.teal_project.id)
        request = self.request_factory.post(ticket_update_url, data=self.form_data)
        request.user = self.user

        res = create_ticket_view(request, project_id=self.teal_project.id,)

        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, '/projects/{}/'.format(self.teal_project.id))

    def test_create_ticket_view_creates_ticket(self):
        ticket_update_url = '/projects/{}/tickets/create'.format(self.teal_project.id)
        request = self.request_factory.post(ticket_update_url, data=self.form_data)
        request.user = self.user

        res = create_ticket_view(request, project_id=self.teal_project.id,)

        new_ticket = Ticket.objects.all()[0]
        self.assertEqual(self.new_title, new_ticket.title)
        self.assertEqual(self.teal_project.id, new_ticket.project_id)
        self.assertEqual(self.user.id, new_ticket.assignees.values()[0]['id'])
