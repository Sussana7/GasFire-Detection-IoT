import os

class Config:
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("COM_MAIL")  # company's_email@gmail.com
    MAIL_PASSWORD = os.getenv("APP_PASS")  #  password or app password
    MAIL_DEFAULT_SENDER = os.getenv("DEF_SENDER")  
