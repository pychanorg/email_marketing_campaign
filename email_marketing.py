import time
from datetime import datetime

from jinja2 import Template


def preprocess_email_template(email_template):
    if 'to' not in email_template:
        email_template['to'] = "{{EMAIL}}"
    return email_template


def preprocess_customers_details(customers_details):
    ts = time.time()
    ts_str = datetime.fromtimestamp(ts).strftime('%d %b %Y')
    for customer_detail in customers_details:
        customer_detail['TODAY'] = ts_str
    return customers_details


def apply_tags(jinja_text, jinja_tags):
    template = Template(jinja_text)
    return template.render(jinja_tags)


def process_email_template(email_template, customers_details):
    customer_emails = []
    customers_errors = []

    for customer in customers_details:
        if 'EMAIL' not in customer or not customer['EMAIL']:
            # handle email error
            customers_errors.append(customer)
        else:
            curr_template = email_template.copy()
            curr_template['to'] = apply_tags(curr_template['to'], customer)
            curr_template['subject'] = apply_tags(
                curr_template['subject'], customer)
            curr_template['body'] = apply_tags(curr_template['body'], customer)
            customer_emails.append(curr_template)

    return customer_emails, customers_errors
