import base64
import functions_framework
import requests
import json
import pymysql
from datetime import datetime
import os

# Fetch environment variables
DB_HOST = os.environ.get("DB_HOST") 
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
API_KEY = os.environ.get("API_KEY")
APP_IP   = os.environ.get("IP")

# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def hello_pubsub(cloud_event):
    decoded_data = base64.b64decode(cloud_event.data["message"]["data"]).decode("utf-8")
    data_dict = json.loads(decoded_data)
    
    # Print out the decoded data
    email = data_dict["email"]
    token = data_dict["token"]
    send_simple_message(email, token)

def send_simple_message(email, token):
    verification_link = f"http://{APP_IP}:3000/v1/user/verify/{token}"
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                padding: 20px;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #f9f9f9;
                border-radius: 10px;
                padding: 40px;
                text-align: center;
            }}
            h1 {{
                color: #333;
            }}
            p {{
                color: #666;
                margin-bottom: 20px;
            }}
            .btn {{
                display: inline-block;
                background-color: #007bff;
                color: #fff;
                text-decoration: none;
                padding: 10px 20px;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>User Verification</h1>
            <p>Welcome! To complete your registration, please click the button below:</p>
            <a class="btn" href="{verification_link}">Verify Account</a>
        </div>
    </body>
    </html>
    """
    
    try:
        response = requests.post(
            "https://api.mailgun.net/v3/abhinavpandey.tech/messages",
            auth=("api","API_key"),
            data={
                "from": "User Verification <mailgun@abhinavpandey.tech>",
                "to": [email],
                "subject": "User Verification",
                "html": html_content
            }
        )
        response.raise_for_status()
        print("Email sent successfully.")
        update_users_table(email)
    except Exception as e:
        print(f"Error sending email: {e}")

def update_users_table(email):
    connection = None
    try:
        # Connect to Cloud SQL using private IP
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            autocommit=True
        )

        print("Connection to Cloud SQL established successfully for updating users table.")

        with connection.cursor() as cursor:
            print("Executing SQL update query...")
            # Execute SQL update query
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = "UPDATE users SET emailSentAt = %s WHERE email = %s"
            cursor.execute(sql, (timestamp, email))
            print("SQL update query executed successfully.")
    except Exception as e:
        print(f"Error updating users table: {e}")
    finally:
        if connection:
            connection.close()
            print("Connection to Cloud SQL closed for updating users table.")
