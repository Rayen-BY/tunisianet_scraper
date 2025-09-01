import requests
import os
import sys
import time
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from email.message import EmailMessage
import smtplib
import traceback

url = "https://www.tunisianet.com.tn/pc-portable-tunisie/84996-pc-portable-asus-vivobook-15-x1504va-i3-1315u-24-go-512-go-ssd-bleu.html"
try:
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        print("✅ page found")
    else:
        print(f"⚠️ Error {response.status_code} : page not found or server problem")
        exit()
except requests.exceptions.RequestException as e:
    print(f"❌ Unable to access the page : {e}")
    exit()
    
# Base path : sert à déterminer le chemin de base où se trouvent tes fichiers (CSV, XLSX)
if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(__file__)

csv_file = os.path.join(base_path, "tunisianet.csv")
prices_file = os.path.join(base_path, "prices.csv")
xlsx_file = os.path.join(base_path, "tunisianet.xlsx")

# Options Chrome (pour Render ou tout autre serveur sans interface graphique)
options = Options()
options.add_argument("--headless=new")       # exécution sans fenêtre
options.add_argument("--no-sandbox")         # obligatoire dans les conteneurs
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

# Utilisation de webdriver-manager pour installer automatiquement ChromeDriver
service = Service(ChromeDriverManager().install())

# Lance Chrome
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get(url)
    time.sleep(2)

    product_name = driver.find_element(By.TAG_NAME, "h1").text
    parent_div = driver.find_element(By.ID, "stock_availability")
    child = parent_div.find_element(By.CSS_SELECTOR, "span") 
    status = child.get_attribute("class")
    price_current = int(driver.find_element(By.CSS_SELECTOR, "span[itemprop='price']").get_attribute("content"))

    pd.Series([price_current]).to_csv(prices_file, mode="a", index=False, header=False)

    d = {"status": [status], "price": [price_current], "date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]}
    df = pd.DataFrame(d)

    if not os.path.isfile(csv_file):
        with open(csv_file, "w", encoding="utf-8") as f:
            f.write(product_name + "\n")
        df.to_csv(csv_file, mode="a", index=False, header=True, encoding="utf-8")
    else:
        df.to_csv(csv_file, mode="a", index=False, header=False, encoding="utf-8")

    comp = pd.read_csv(csv_file, skiprows=1)
    min_price = comp["price"].min()
    date_min_price = comp.loc[comp["price"] == min_price, "date"].values[0]
    print("prix maximum :", comp["price"].max())
    print("prix minimum :", min_price)
    print("date de prix minimum :", date_min_price)

    with open(csv_file, "a", encoding="utf-8") as f:
        f.write(f"date de plus petit prix :{date_min_price}\n")

    df_csv = pd.read_csv(csv_file, skiprows=1)
    filtered_df = df_csv[df_csv.iloc[:, 0].str.startswith("En")]
    filtered_df.to_excel(xlsx_file, index=False)

    try:
        with open(prices_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]

        email = os.getenv("email_user")
        password = os.getenv("email_pass")

        msg = EmailMessage()
        msg["From"] = email
        msg["To"] = email

        msg = None

        if status == "out-stock":
            msg = EmailMessage()
            msg["From"] = email
            msg["To"] = email
            msg["Subject"] = "Laptop Out of stock"
            msg.set_content(f"{product_name} is out of stock")
        elif len(lines) >= 2:
            if int(lines[-1]) < int(lines[-2]):
                msg = EmailMessage()
                msg["From"] = email
                msg["To"] = email
                msg["Subject"] = "Laptop price has dropped"
                msg.set_content(f"Laptop:\n{product_name}\nNew price: {price_current} DT")
            elif int(lines[-1]) > int(lines[-2]):
                msg = EmailMessage()
                msg["From"] = email
                msg["To"] = email
                msg["Subject"] = "Laptop price has increased"
                msg.set_content(f"Laptop:\n{product_name}\nNew price: {price_current} DT")
            else :
                msg = EmailMessage()
                msg["From"] = email
                msg["To"] = email
                msg["Subject"] = "Laptop price is unchanged."
                msg.set_content(f"Laptop:\n{product_name}\nprice: {price_current} DT")

        if msg:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(email, password)
                smtp.send_message(msg)
            print("Email sent successfully")

    finally:
        print("Script end")
        
except Exception as e:
    print(f"Error during scraping: {e}")
    
finally:
    driver.quit()
