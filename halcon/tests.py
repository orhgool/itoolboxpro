from django.test import TestCase

class DlFromWebsIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('halcon:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No urls are available.")
        self.assertQuerysetEqual(response.context['ultimos_boxes'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('halcon:index'))
        self.assertQuerysetEqual(
            response.context['ultimos_boxes'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['ultimos_boxes'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
