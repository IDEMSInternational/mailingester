import sys
from email.parser import BytesParser
from smtplib import SMTP


def send(host, port, mail):
    client = SMTP(host, port)

    with open(mail, "rb") as m:
        client.send_message(BytesParser().parse(m))

    client.quit()


if __name__ == "__main__":
    host, port, mail = sys.argv[1:4]
    send(host, port, mail)
