import requests
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Cloudflare API credentials
API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN")
ZONE_ID = os.environ.get("CLOUDFLARE_ZONE_ID")
RECORD_NAME = os.environ.get('RECORD_NAME')
DOMAIN = os.environ.get('DOMAIN')

# Cloudflare API endpoint
BASE_URL = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

log_file = '/var/log/dns_updater.log'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()  # This will log to stdout
    ]
)

# Function to get current public IP
def get_public_ip():
    logging.info("Fetching public IP")
    try:
        ip = requests.get('https://api.ipify.org').text
        logging.info(f"Public IP fetched: {ip}")
        return ip
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching public IP: {e}")
        raise

def get_dns_record():
    logging.info(f"Fetching DNS record for {RECORD_NAME}.{DOMAIN}")
    try:
        response = requests.get(BASE_URL, headers=headers, params={"name": f"{RECORD_NAME}.{DOMAIN}"})
        response.raise_for_status()
        records = response.json()["result"]
        if records:
            logging.info(f"DNS record found: {records[0]}")
            return records[0]
        else:
            logging.warning(f"No DNS record found for {RECORD_NAME}.{DOMAIN}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching DNS record: {e}")
        raise

def update_dns_record(record_id, new_ip, record_type):
    logging.info(f"Updating DNS record {record_id} with new IP {new_ip}")
    url = f"{BASE_URL}/{record_id}"
    data = {
        "type": record_type,
        "name": RECORD_NAME,
        "content": new_ip,
        "ttl": 1,
        "proxied": False
    }
    try:
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        logging.info(f"DNS record updated successfully: {result['result']['content']}")
        return result
    except requests.exceptions.RequestException as e:
        logging.error(f"Error updating DNS record: {e}")
        raise

def main():
    logging.info("Starting DNS update process")
    try:
        record = get_dns_record()
        current_ip = get_public_ip()
        if record:
            if record["content"] != current_ip:
                result = update_dns_record(record["id"], current_ip, record["type"])
                logging.info(f"DNS record updated: {result['result']['content']} from {record['content']}")
            else:
                logging.info(f"DNS record already up to date: {record['content']}")
        else:
            logging.warning(f"No DNS record found for {RECORD_NAME}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    logging.info("DNS update process completed")

if __name__ == "__main__":
    main()
