import os
import random
import smtplib
import string
import threading
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from COLORED import Colored as col
import sqlite3

def input_with_timeout(prompt, timeout):
    prompt = col(prompt)
    prompt.color_blue()
    prompt.color_underline()
    print(prompt, end=' ')

    result = [None]

    def get_input():
        result[0] = input()

    input_thread = threading.Thread(target=get_input)
    input_thread.start()
    input_thread.join(timeout)

    if input_thread.is_alive():
        return ""
    else:
        return result[0]


load_dotenv()
my_email = os.getenv('EM')
password = os.getenv('PAS')

temp_s = col('Enter email:')
temp_s.color_bg_white()
temp_s.color_black()
print(temp_s, end='')
usr_em = input(' ')
randomPass = ''.join(random.sample(string.digits + string.ascii_uppercase, 5))

# SQLite database
conn = sqlite3.connect('verification.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS verification
                  (email TEXT, password TEXT, time INTEGER)''')
cursor.execute("INSERT INTO verification VALUES (?, ?, ?)",
               (usr_em, randomPass, int(time.time())))
conn.commit()

connection = smtplib.SMTP("smtp.gmail.com", 587)
connection.starttls()
connection.login(user=my_email, password=password)

try:
    msg = MIMEMultipart("alternative")
    msg["From"] = my_email
    msg["To"] = usr_em
    msg["Subject"] = "Email Verification"

    text = f"Your password is: {randomPass}"
    html = """
    <html>
        <body>
            <h1>Password Email</h1>
            <p>Your password is: <strong>{randomPass}</strong></p>
        </body>
    </html>
    """.format(randomPass=randomPass)

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    msg.attach(part1)
    msg.attach(part2)

    connection.sendmail(from_addr=my_email, to_addrs=usr_em, msg=msg.as_string())
    temp_s = col("Email sent successfully!")
    temp_s.color_bg_green()
    print(temp_s)
except smtplib.SMTPException as e:
    temp_s = col("Error sending email:" + str(e))
    temp_s.color_bg_red()
    print(temp_s)
    exit()

temp_s = col("Please check your email for the password.")
temp_s.color_bg_yellow()
print(temp_s)

timeout = int(os.getenv('TIMEOUT'))
entered_code = input_with_timeout("Enter the code:", timeout)

# Retrieve data from the database
cursor.execute("SELECT password, time FROM verification WHERE email = ?", (usr_em,))
data = cursor.fetchone()
stored_password = data[0]
verification_time = data[1]

current_time = int(time.time())
time_difference = current_time - verification_time

if time_difference <= timeout:
    if entered_code == stored_password:
        temp_s = col("Code entered correctly!")
        temp_s.color_green()
        print(temp_s)
    else:
        temp_s = col("\n\nIncorrect code.")
        temp_s.color_red()
        print(temp_s)
else:
    temp_s = col("\n\nTimeout reached. The code has expired.")
    temp_s.color_red()
    print(temp_s)
cursor.execute("DELETE FROM verification WHERE email = ?", (usr_em,))
conn.commit()
connection.quit()
conn.close()
exit()
