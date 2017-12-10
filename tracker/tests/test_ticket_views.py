from django.contrib.auth.models import AnonymousUser
from django.test import Client, RequestFactory, TestCase

from tracker.site.models import Ticket
from tracker.site.views import create_ticket_view, my_tickets_view, update_ticket_view
from tracker.tests import test_helpers


class TestMyTicketsViewIncludingMiddleWare(TestCase):
    def setup(self):
        self.client = Client()

    def test_landing_page_loads_when_user_not_logged_in(self):
        res = self.client.get('/')

        self.assertEqual(res.status_code, 200)


class TestMyTicketsView(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_landing_page_loads_when_user_not_logged_in(self):
        request = self.request_factory.get('/')
        request.user = AnonymousUser()

        res = my_tickets_view(request)

        self.assertEqual(res.status_code, 200)

    def test_my_ticket_view_loads_when_user_logged_in(self):
        request = self.request_factory.get('/')
        request.user = test_helpers.create_bob_user()

        res = my_tickets_view(request)

        self.assertEqual(res.status_code, 200)

    def test_my_ticket_view_returns_users_tickets(self):
        bob_user = test_helpers.create_bob_user()
        reginald_user = test_helpers.create_reginald_user()
        teal_project = test_helpers.create_teal_project(bob_user)
        bob_assigned_ticket = test_helpers.create_project_ticket(teal_project, bob_user, [bob_user, reginald_user])
        non_bob_assigned_ticket = test_helpers.create_project_ticket(teal_project, reginald_user, [reginald_user])
        request = self.request_factory.get('/')
        request.user = bob_user

        res = my_tickets_view(request)

        self.assertEqual(len(res.context_data['tickets']), 1)
        self.assertEqual(res.context_data['tickets'][0].id, bob_assigned_ticket.id)


class TestUpdateTicketsView(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

        # Pre-populate a user with two projects and one ticket
        self.user = test_helpers.create_bob_user()
        self.teal_project = test_helpers.create_teal_project(self.user)
        self.rainbow_project = test_helpers.create_rainbow_project(self.user)
        self.ticket = test_helpers.create_project_ticket(self.teal_project, self.user)

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

        # Pre-populate a user with a project
        self.user = test_helpers.create_bob_user()
        self.teal_project = test_helpers.create_teal_project(self.user)

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
