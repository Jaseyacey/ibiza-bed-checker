import requests
import config

def call_email_verify_function(email):
    api_key = config.api_key
    try:
        response = requests.post(
            "https://api.resend.com/emails",
            json={
                "from": "FixtureFix <onboarding@fixturefix.co.uk>",
                "to": "jbeedle@gmail.com",
                "subject": "New run email",
                "html": f"<p>New run email</strong><strong> <br/>BED</strong>",
            },
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        )

        # Check if the request was successful
        if response.status_code == 200:
            print("Email sent successfully!")
        else:
            print(f"Failed to send email. Status code: {response.status_code}, Response: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

email = "jbeedle@gmail.com"

call_email_verify_function( email)
