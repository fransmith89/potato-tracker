from djangae.contrib.gauth_datastore.models import GaeDatastoreUser
from django.test import Client, RequestFactory, TestCase

from tracker.site.models import Project, Ticket
from tracker.site.views import update_ticket_view


class TestMyTicketsView(TestCase):
    def setup(self):
        self.client = Client()

    def test_landing_page_loads(self):
        res = self.client.get('/')

        self.assertEqual(res.status_code, 200)


class TestUpdateTicketsView(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

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

        self.project = Project.objects.create(
            title="Teal Drill",
            modified="2015-05-13T13:36:44.764Z",
            created_by=self.user,
            created="2015-05-13T13:36:44.762Z",
            pk=5466084618534912
        )

        self.ticket = Ticket.objects.create(
            title="Teal Drill's first ticket",
            description="",
            project=self.project,
            created_by=self.user,
            pk=6466084618534912
        )

    def test_update_ticket_view_updates_tickets_values(self):
        new_title = 'A new title'
        new_description = 'A new description'
        form_data = {
            'title': new_title,
            'description': new_description,
            'assignees': [self.user.id]
        }
        ticket_update_url = '/projects/{}/tickets/{}/edit'.format(self.project.id, self.ticket.id)
        request = self.request_factory.post(ticket_update_url, data=form_data)
        request.user = self.user

        res = update_ticket_view(request, project_id=self.project.id, ticket_id=self.ticket.id)

        updated_ticket = Ticket.objects.get(id=self.ticket.id)
        self.assertEqual(new_title, updated_ticket.title)
        self.assertEqual(new_description, updated_ticket.description)
        self.assertEqual(self.user.id, updated_ticket.assignees.values()[0]['id'])

