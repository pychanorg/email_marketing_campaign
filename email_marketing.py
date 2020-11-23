import time
from datetime import datetime

from jinja2 import Template


def preprocess_email_template(email_template):
    """
    Preprocess email template by injecting "to/{{EMAIL}}"" pair

    Args:
        email_template (dict): json extract of email template
    """
    if 'to' not in email_template:
        email_template['to'] = "{{EMAIL}}"
    return email_template


def get_extra_custom_tags(tags=None):
    """
    Add extra tags by injecting "TODAY" tag

    {{TODAY}} tag is in "31 Dec 2020" format

    Args:
        tags (list): optional list of existing tags
    """
    if tags is None:
        tags = {}
    ts = time.time()
    ts_str = datetime.fromtimestamp(ts).strftime('%d %b %Y')
    tags['TODAY'] = ts_str

    return tags


def apply_tags(jinja_text, jinja_tags):
    """
    Apply jinja tags to jinja template text
    """
    template = Template(jinja_text)
    return template.render(jinja_tags)


def process_email_template(email_template, customers_details, extra_tags=None):
    """
    Apply customer tags from CSV to email template

    Args:
        email_template (dict): json extract of email template
        customers_details (list): list of customers details from csv file
    """
    customer_emails = []
    customers_errors = []

    if extra_tags is None:
        extra_tags = get_extra_custom_tags()

    for customer in customers_details:
        if 'EMAIL' not in customer or not customer['EMAIL']:
            # handle email error
            customers_errors.append(customer)
        else:

            # add any custom tags such as {{TODAY}} tags
            # NOTE: new 3.9 feature to perform union on dict
            customer = customer | extra_tags

            curr_template = email_template.copy()
            curr_template['to'] = apply_tags(
                curr_template.get('to', ""), customer)
            curr_template['subject'] = apply_tags(
                curr_template.get('subject', ""), customer)
            curr_template['body'] = apply_tags(
                curr_template.get('body', ""), customer)
            customer_emails.append(curr_template)

    return customer_emails, customers_errors
