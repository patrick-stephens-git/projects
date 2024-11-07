from emailDataVariables import email_data

## Email Sender / Receiver Variables:
list_of_receiver_email_addresses = ['receiver_email_address']

## Authentication for Email Sender:
email_username = 'your_email_address'
email_password = 'your_email_app_password' # The App Password needed after the Google update for Less Secure Apps: https://support.google.com/accounts/answer/6010255?hl=en&p=less-secure-apps&rd=1#zippy=%2Cif-less-secure-app-access-is-on-for-your-account%2Cupdate-your-app-or-operating-system%2Cuse-more-secure-apps%2Cuse-an-app-password

## Email Subject:
email_subject = 'email subject'

## Email Body:
email_body = """
<b>Email Header:</b><br>
Email Text1<br>
Email Text2<br>
<br>
<b>DataFrame:</b><br>
{0}<br>
<br>
""".format(email_data)