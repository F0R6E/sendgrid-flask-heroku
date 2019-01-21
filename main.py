import os
import sendgrid
import os
from flask import Flask, request
from sendgrid.helpers.mail import *
import urllib2 as urllib

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

app = Flask(__name__)


@app.route("/", methods=["POST"])
def mail():
    if request.method == "POST":
        sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
        from_email = Email(os.environ["FROM_EMAIL"])
        to_email = Email(request.args.get('email'))
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
