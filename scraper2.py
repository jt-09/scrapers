from bs4 import BeautifulSoup
import requests
import smtplib
from email.message import EmailMessage
import csv
from datetime import datetime
import os

LOG_FILE = "price_history.csv"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# print(BASE_DIR)
LOG_FILE = os.path.join(BASE_DIR, "price_history.csv")

def log_price(title, url, price):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "title", "url", "price"])
        writer.writerow([datetime.now().isoformat(), title, url, price])



# List of (product URL, threshold price)
PRODUCTS = [
    ("https://www.amazon.com.au/dp/B0CD2V7T6N", 45.00),
    ("https://www.amazon.com.au/dp/B0CFRHV1MX", 50.00),
    ("https://www.amazon.com.au/dp/B08RHWX6G1", 45.00),
    ("https://www.amazon.com.au/dp/B0CH8ZWLKR", 50.00),
]
# Headers to mimic a real browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# print(soup.prettify())

# Email configuration
EMAIL_FROM = "jay.thakkar1427@gmail.com"
EMAIL_TO = "jay.thakkar1427@gmail.com"
EMAIL_PASS = "lwkj nhii howp yfan"  # Use app-specific password or low-privilege account


def get_price(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    # Product title
    title_tag = soup.find(id="productTitle")
    title = title_tag.get_text(strip=True) if title_tag else "No title found"

    # Price extraction
    price_tag = (
        soup.select_one("span.a-price span.a-offscreen") or
        soup.select_one("span.a-price-whole")
    )
    if not price_tag:
        raise Exception("Could not find price on page.")

    price_text = price_tag.get_text(strip=True).replace("$", "").replace(",", "")
    price = float(price_text)
    return title, price

def send_email(subject, body):
    msg = EmailMessage()
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_FROM, EMAIL_PASS)
        smtp.send_message(msg)

def check_all_prices():
    for url, threshold in PRODUCTS:
        try:
            title, current_price = get_price(url)
            print(f"{title} is currently ${current_price:.2f}")
            
            log_price(title,url,current_price)

            if current_price <= threshold:
                subject = f"Price Alert: {title} is ${current_price:.2f}"
                body = f"The price is now below ${threshold:.2f}.\n\n{title}\n{url}"
                send_email(subject, body)
                print("Email sent.\n")
            else:
                print("Above threshold.\n")

        except Exception as e:
            print(f"Error checking {url}: {e}\n")

if __name__ == "__main__":
    check_all_prices()