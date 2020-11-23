import sys
import os
import json
from pathlib import Path
from datetime import datetime
import time
import csv


from email_marketing import preprocess_email_template, \
    preprocess_customers_details, \
    process_email_template


def create_email_files(email_template_filename, customers_filename,
                       output_email_dir, errors_filename):
    with open(email_template_filename, 'r') as f:
        email_template = json.load(f)
    with open(customers_filename, 'r') as f:
        customers_details = list(csv.DictReader(f))

    email_template = preprocess_email_template(email_template)
    customers_details = preprocess_customers_details(customers_details)

    customer_emails, customers_errors = process_email_template(
        email_template, customers_details)

    if customer_emails:
        # write customers templates to output directory
        ts = time.time()
        ts_str = datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')
        for i, customer_email in enumerate(customer_emails):
            output_filename = '{}_{}.json'.format(ts_str, i)
            output_filepath = os.path.join(output_email_dir, output_filename)
            with open(output_filepath, 'w') as f:
                f.write(json.dumps(customer_email))

    if customers_errors:
        # handle errors in customers csv files
        with open(errors_filename, 'w') as f:
            fieldnames = customers_errors[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for error in customers_errors:
                writer.writerow(error)


def main():
    usage = """Generate marketing emails to customers

Example usage:
python send_email.py /path/to/email_template.json /path/to/customers.csv \
/path/to/output_emails/ /path/to/errors.csv"""

    if len(sys.argv) != 5:
        print(usage)
        sys.exit(1)

    email_template_filename = sys.argv[1]
    customers_filename = sys.argv[2]
    output_email_dir = sys.argv[3]
    errors_filename = sys.argv[4]

    # perform basic error checking of input files/dir from supplied args
    arg_files_has_errors = False
    if not Path(email_template_filename).is_file():
        error_msg = "email template json file is invalid or not found: {}"
        print(error_msg.format(email_template_filename))
        arg_files_has_errors = True
    if not Path(customers_filename).is_file():
        error_msg = "Customers csv template file is invalid or not found: {}"
        print(error_msg.format(customers_filename))
        arg_files_has_errors = True
    if not Path(output_email_dir).is_dir():
        error_msg = "Output email directory is invalid or not found: {}"
        print(error_msg.format(output_email_dir))
        arg_files_has_errors = True

    if arg_files_has_errors:
        sys.exit(1)

    create_email_files(email_template_filename,
                       customers_filename, output_email_dir, errors_filename)


if __name__ == "__main__":
    main()
