from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase

from tracker.site.views import project_list_view
from tracker.tests import test_helpers


class TestProjectListView(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.user = test_helpers.create_bob_user()

    def test_get_projects_list_loads_when_user_not_logged_in(self):
        request = self.request_factory.get('/projects')
        request.user = AnonymousUser()

        res = project_list_view(request)

        self.assertEqual(res.status_code, 200)

    def test_get_projects_list_returns_projects_in_alphabetical_order_when_user_not_logged_in(self):
        teal_project = test_helpers.create_teal_project(self.user)
        rainbow_project = test_helpers.create_rainbow_project(self.user)
        user_assigned_ticket = test_helpers.create_project_ticket(
            teal_project,
            self.user,
            [self.user]
        )
        request = self.request_factory.get('/projects')
        request.user = AnonymousUser()

        res = project_list_view(request)

        self.assertEqual(len(res.context_data['projects']), 2)
        self.assertEqual(res.context_data['projects'][0].pk, rainbow_project.pk)

    def test_get_projects_list_loads_when_user_logged_in(self):
        request = self.request_factory.get('/projects')
        request.user = self.user

        res = project_list_view(request)

        self.assertEqual(res.status_code, 200)

    def test_get_projects_list_returns_projects_user_has_assigned_tickets_for_first_when_logged_in(self):
        teal_project = test_helpers.create_teal_project(self.user)
        rainbow_project = test_helpers.create_rainbow_project(self.user)
        user_assigned_ticket = test_helpers.create_project_ticket(
            teal_project,
            self.user,
            [self.user]
        )
        request = self.request_factory.get('/projects')
        request.user = self.user

        res = project_list_view(request)

        self.assertEqual(len(res.context_data['projects']), 2)
        self.assertEqual(res.context_data['projects'][0].pk, user_assigned_ticket.project_id)
