import os
import sys
import json
import urllib.request as urllib
from flask import Flask, request
import sendgrid
from sendgrid.helpers.mail import Email, Content, Substitution, Mail


SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

app = Flask(__name__)


@app.route("/", methods=["POST"])
def mailer():
    """Send welcome email."""
    if request.method == "POST":
        post_data = request.data
        data_dict = json.loads(post_data)
        print('data_dict = ', data_dict)
        sys.stdout.flush()
        sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
        from_email = Email(os.environ["FROM_EMAIL"])
        to_email = Email(data_dict['email'])
        mail = Mail(from_email, to_email)
        mail.template_id = os.environ["TEMPLATE_ID"]
        try:
            response = sg.client.mail.send.post(request_body=mail.get())
        except urllib.HTTPError as e:
            print(e.read())
            exit()
        print(response.status_code)
        print(response.body)
        print(response.headers)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
