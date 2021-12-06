import my_private_date
import smtplib

class NotificationManager:
    def send_emails(self, emails, message, google_flight_link):
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.ehlo()
            connection.starttls()
            connection.ehlo()
            connection.login(my_private_date.MY_EMAIL, my_private_date.MY_PASSWORD)
            for email in emails:
                connection.sendmail(
                    from_addr=my_private_date.MY_EMAIL,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}\n{google_flight_link}".encode('utf-8')
                )