# Tunisianet Price Tracker

Python script to track the price and availability of a laptop on Tunisianet, and send an email if the price changes or if the product is out of stock.

## Features

- Checks if the page exists
- Retrieves product name, price, and status (in stock / out of stock)
- Updates `prices.csv` and `tunisianet.csv`
- Exports data to Excel
- Sends an email if the price increases, decreases, or the product goes out of stock

## Requirements

- Python 3.11+
- Chrome and ChromeDriver
- Python libraries:
  - pandas
  - selenium
  - openpyxl
  - requests

## Environment Variables (Security)

To secure your credentials, **never put them directly in the code**.  
Set the following environment variables before running the script:

- `EMAIL_USER` : your Gmail address  
- `EMAIL_PASS` : Gmail app password (never use your main Gmail password)

### Example on Linux / macOS

```bash
export EMAIL_USER="your_email@gmail.com"
export EMAIL_PASS="your_app_password"
python3 tunisianet.py
