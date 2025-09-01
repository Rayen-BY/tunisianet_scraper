Tunisianet Laptop Price Scraper

Description:
This Python project automatically tracks the price and stock status of a laptop on Tunisianet. It scrapes the product page using Selenium, saves historical prices and stock information to CSV and Excel files, and sends email notifications when:

The laptop goes out of stock.

The price drops compared to the previous recorded price.

The price increases or remains unchanged.

Features:

Headless Chrome support (works on servers or cloud platforms).

Automatic CSV and Excel updates with timestamped data.

Email notifications using environment variables for credentials.

Handles "page not found" errors gracefully.

Technologies used:

Python 3

Selenium

pandas

requests

smtplib

Setup:

Clone this repository.

Install dependencies:

pip install -r requirements.txt


Set environment variables for email credentials:

EMAIL_USER

EMAIL_PASS

Run the script:

python tunisianet_scraper.py


Note:
Ensure you have ChromeDriver installed and the path configured in the script.
