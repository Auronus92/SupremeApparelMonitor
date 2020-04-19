import os
import sys
import time
import six
import pause
import ssl
import argparse
import logging.config
import smtplib
from selenium import webdriver
from dateutil import parser as date_parser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [PID %(process)d] [Thread %(thread)d] [%(levelname)s] [%(name)s] %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": [
            "console"
        ]
    }
})

LOGGER = logging.getLogger()

def run(driver, url):
    driver.maximize_window()
    gmail_user = "monitorbar97@gmail.com"
    gmail_password = "passsssssss"
    sent_from = gmail_user
    to = "email@emaul.com"
    email_text = "Le SNEAKERS SONO ONLINE\n" + url
    to = ['youremail@email.com']
    while True:
        try:
            LOGGER.info("Requesting page: " + url)
            driver.get(url)
        except TimeoutException:
            LOGGER.info("Page load timed out but continuing anyway")
        #res = check_exists_by_xpath("//a[@data-sold-out='false']")
        res = check_exists_by_xpath("//b[@class='button sold-out']")
        if res == False:
            LOGGER.info("INSTOCK")
            #SENDMAIL OR NOTIFY
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            context = ssl.create_default_context()
            server.starttls(context=context)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to, email_text)
            server.quit()
            LOGGER.info("Email sent")
            break
        else:
            LOGGER.info("SOLDOUT")
        time.sleep(10)
    driver.quit()


def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="https://www.supremenewyork.com/shop/shoes/ndrgpvxhm/cxypn34k5")
    parser.add_argument("--driver-type", default="firefox", choices=("firefox", "chrome"))
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()

    driver = None
    if args.driver_type == "firefox":
        options = webdriver.FirefoxOptions()
        if args.headless:
            options.add_argument("--headless")
        if sys.platform == "darwin":
            executable_path = "./bin/geckodriver_mac"
        elif "linux" in sys.platform:
            executable_path = "./bin/geckodriver_linux"
        else:
            raise Exception("Unsupported operating system. Please add your own Selenium driver for it.")
        driver = webdriver.Firefox(executable_path=executable_path, firefox_options=options, log_path=os.devnull)
    elif args.driver_type == "chrome":
        options = webdriver.ChromeOptions()
        if args.headless:
            options.add_argument("headless")
        if sys.platform == "darwin":
            executable_path = "./bin/chromedriver_mac"
        elif "linux" in sys.platform:
            executable_path = "./bin/chromedriver_linux"
        else:
            raise Exception("Unsupported operating system. Please add your own Selenium driver for it.")
        driver = webdriver.Chrome(executable_path=executable_path, chrome_options=options)

    run(driver=driver, url=args.url)
