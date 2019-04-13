from django.test import TestCase
from django.urls import reverse, resolve
from django.utils import translation
from .views import index, thesis


class IndexTests(TestCase):
    fixtures = ['qualityland_election_2020']

    def setUp(self):
        translation.activate('de')
        self.response_de = self.client.get(reverse('index'))
        translation.activate('en')
        self.response_en = self.client.get(reverse('index'))

    def test_index_view_status_code(self):
        self.assertEquals(self.response_de.status_code, 200)
        self.assertEquals(self.response_en.status_code, 200)

    def test_index_url_resolves_index_view(self):
        translation.activate('de')
        view_de = resolve('/de/')
        translation.activate('en')
        view_en = resolve('/en/')
        self.assertEquals(view_de.func, index)
        self.assertEquals(view_en.func, index)

    def test_index_view_contains_link_to_first_survey_page(self):
        self.assertContains(self.response_de, 'href="1"')
        self.assertContains(self.response_en, 'href="1"')


class ThesesTests(TestCase):
    fixtures = ['qualityland_election_2020']

    def setUp(self):
        translation.activate('de')
        self.response_de = self.client.get(
            reverse('theses', kwargs={'thesis_id': 1}))
        translation.activate('en')
        self.response_en = self.client.get(
            reverse('theses', kwargs={'thesis_id': 1}))

    def test_theses_view_status_code(self):
        self.assertEquals(self.response_de.status_code, 200)
        self.assertEquals(self.response_en.status_code, 200)

    def test_thesis_url_resolves_thesis_view(self):
        translation.activate('de')
        view_de = resolve('/de/1/')
        translation.activate('en')
        view_en = resolve('/en/1/')
        self.assertEquals(view_de.func, thesis)
        self.assertEquals(view_en.func, thesis)

    def test_first_thesis_view_contains_link_to_all_answers(self):
        self.assertContains(self.response_de, 'href="/de/1/1/"')
        self.assertContains(self.response_de, 'href="/de/1/2/"')
        self.assertContains(self.response_de, 'href="/de/1/3/"')
        self.assertContains(self.response_en, 'href="/en/1/1/"')
        self.assertContains(self.response_en, 'href="/en/1/2/"')
        self.assertContains(self.response_en, 'href="/en/1/3/"')
