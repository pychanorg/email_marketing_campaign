import json
import io
import csv

from flask import Flask, render_template, request
from flask_mail import Mail, Message


from email_marketing import preprocess_email_template, \
    process_email_template


app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER'] = 'mailhog'
app.config['MAIL_PORT'] = 1025
mail = Mail(app)


@app.route('/', methods=['post', 'get'])
def send_email():
    message = ''
    if request.method == 'POST':
        success = False

        email_raw = request.form.get('template')
        customers_raw = request.form.get('customers')

        email_template_json = json.loads(email_raw)
        email_template_json = preprocess_email_template(email_template_json)

        customers_file_io = io.StringIO(customers_raw)
        customers_details = list(csv.DictReader(customers_file_io))

        customer_emails, customers_errors = process_email_template(
            email_template_json, customers_details)

        for customer_email in customer_emails:
            msg = Message(customer_email['subject'], sender=customer_email['from'], recipients=[
                          customer_email['to']])
            msg.body = customer_email['body']
            mail.send(msg)

            success = True

        if success:
            message = "Email submission to Mailhog is successful"
        else:
            message = "Email submission to Mailhog is not successful"

    return render_template('send_email.html', message=message)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
