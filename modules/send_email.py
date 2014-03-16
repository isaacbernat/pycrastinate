import smtplib
from email.mime.text import MIMEText


def send_email(config, data):
    config = config.get(__name__.split(".")[-1], {})
    sender = config["from"]
    to = config.get("to", [])
    cc = config.get("cc", [])
    bcc = config.get("bcc", [])

    def prepare_msg(msg):
        msg = MIMEText(msg)
        msg['Subject'] = config.get("subject",
                                    "Pycrastinate automated mail")
        msg['From'] = sender
        msg['To'] = ",".join(to)
        msg["Cc"] = ",".join(cc)
        return msg

    def prepare_smtp():
        smtp_name = config.get("smtp_name", "localhost")
        smtp_port = config.get("smtp_port", 587)
        server = smtplib.SMTP(smtp_name, smtp_port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        if config.get("username") and config.get("password"):
            server.login(config["username"], config["password"])
        return server

    server = prepare_smtp()
    data = list(data)
    yield data
    msg = prepare_msg("\n".join(data))
    server.sendmail(sender, to + cc + bcc, msg.as_string())
    server.quit()
