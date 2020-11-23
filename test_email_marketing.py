import unittest

from freezegun import freeze_time

from email_marketing import preprocess_email_template, \
    get_extra_custom_tags, \
    process_email_template, apply_tags


class TestPreprocessEmailTemplateFunctions(unittest.TestCase):
    def test_basic(self):
        email_template = {}
        actual = preprocess_email_template(email_template)
        expected = {'to': '{{EMAIL}}'}
        self.assertEqual(actual, expected)

        email_template = {'body': "Hi {{TITLE}} {{DUMMY}}"}
        actual = preprocess_email_template(email_template)
        expected = {'to': '{{EMAIL}}', 'body': "Hi {{TITLE}} {{DUMMY}}"}
        self.assertEqual(actual, expected)

    def test_no_override_to_key(self):
        email_template = {'to': '{{dummy}}'}
        actual = preprocess_email_template(email_template)
        expected = {'to': '{{dummy}}'}
        self.assertEqual(actual, expected)


class TestGetExtraCustomTags(unittest.TestCase):
    @freeze_time("2020-01-31")
    def test_basic_tags(self):
        actual = get_extra_custom_tags()
        expected = {'TODAY': '31 Jan 2020'}
        self.assertEqual(actual, expected)

        actual = get_extra_custom_tags({})
        expected = {'TODAY': '31 Jan 2020'}
        self.assertEqual(actual, expected)

    @freeze_time("2020-01-31")
    def test_add_more_tags(self):
        actual = get_extra_custom_tags({"COMPANY": "CORP"})
        expected = {'TODAY': '31 Jan 2020', "COMPANY": "CORP"}
        self.assertEqual(actual, expected)


class TestApplyTags(unittest.TestCase):
    def test_basic_tags(self):
        jinja_text = ""
        jinja_tags = {"TITLE": "example"}
        actual = apply_tags(jinja_text, jinja_tags)
        expected = ""
        self.assertEqual(actual, expected)

    def test_extra_text_tags(self):
        # jinja_text has extra tags that jinja_tags doesn't have
        jinja_text = "Hi {{TITLE}} {{FIRST_NAME}} {{LAST_NAME}},\nToday, {{TODAY}}, we would like to tell you that... Sincerely,\nThe Marketing Team"
        jinja_tags = {
            "TITLE": 'example title',
            "FIRST_NAME": "jon",
        }
        actual = apply_tags(jinja_text, jinja_tags)
        expected = "Hi example title jon ,\nToday, , we would like to tell you that... Sincerely,\nThe Marketing Team"
        self.assertEqual(actual, expected)

    def test_extra_jinja_tags(self):
        # test that template is correct if there  are extra jinja_tags tags
        jinja_text = "Hi {{TITLE}} {{FIRST_NAME}} {{LAST_NAME}},\nToday, {{TODAY}}, we would like to tell you that... Sincerely,\nThe Marketing Team"
        jinja_tags = {
            "TITLE": 'example title',
            "FIRST_NAME": "jon",
            "LAST_NAME": "smith",
            "TODAY": "01 Jan 2020",
            "EXTRA": "extra bonus",
        }
        actual = apply_tags(jinja_text, jinja_tags)
        expected = "Hi example title jon smith,\nToday, 01 Jan 2020, we would like to tell you that... Sincerely,\nThe Marketing Team"
        self.assertEqual(actual, expected)


class TestProcessEmailTemplate(unittest.TestCase):
    def test_empty_args(self):
        email_template = {}
        customers_details = []

        actual = process_email_template(email_template, customers_details)
        expected = [], []
        self.assertEqual(actual, expected)

    @freeze_time("2020-01-31")
    def test_basic(self):
        email_template = {
            "subject": "{{FIRST_NAME}}, a new product is being launched soon...",
            "body": "Hi {{TITLE}} {{FIRST_NAME}} {{LAST_NAME}},\nToday, {{TODAY}}, Good news",
            'to': "{{EMAIL}}",
        }
        customers_details = [
            {"TITLE": "Mr", "FIRST_NAME": "John", "EMAIL": "john@west"},
            {"TITLE": "Mr", "FIRST_NAME": "ANON", "EMAIL": ""},
        ]

        actual_emails, actual_errors = process_email_template(
            email_template, customers_details)
        expected_emails = [
            {
                "subject": "John, a new product is being launched soon...",
                "body": "Hi Mr John ,\nToday, 31 Jan 2020, Good news",
                'to': "john@west",
            }
        ]
        expected_errors = [
            {"TITLE": "Mr", "FIRST_NAME": "ANON", "EMAIL": ""}, ]

        self.assertEqual(actual_emails, expected_emails)
        self.assertEqual(actual_errors, expected_errors)
