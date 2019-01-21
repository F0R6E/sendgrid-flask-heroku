import os
import sys
import json
import urllib.request as urllib
from flask import Flask, request, make_response
import sendgrid
from sendgrid.helpers.mail import Email, Content, Substitution, Mail


SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

app = Flask(__name__)


@app.route("/", methods=["POST"])
def mailer():
    """Send welcome email."""
    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
    if request.method == "POST":
        post_data = request.data
        data_dict = json.loads(post_data)
        print('data_dict = ', data_dict)
        sys.stdout.flush()
        subscribers = data_dict['subscribers']
        for subscriber in subscribers:
            to_email = Email(subscriber['email'])
            from_email = Email(os.environ["FROM_EMAIL"])
            print("subscriber['email'] = ", subscriber['email'])
            sys.stdout.flush()
            mail = Mail(from_email, to_email)
            mail.template_id = os.environ["TEMPLATE_ID"]
            try:
                response = sg.client.mail.send.post(request_body=mail.get())
                return make_response(response.json(), 200)
            except urllib.HTTPError as e:
                print(e.read())
                sys.stdout.flush()
                print(response.status_code)
                sys.stdout.flush()
                print(response.body)
                sys.stdout.flush()
                print(response.headers)
                sys.stdout.flush()
                return make_response(e.read(), 500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
