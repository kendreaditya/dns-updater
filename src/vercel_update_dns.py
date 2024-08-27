import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to get current public IP
def get_public_ip():
    return requests.get('https://api.ipify.org').text

# Function to get the current IP of the DNS record
def get_current_record_ip(vercel_token, domain, record_name, team_id):
    headers = {
        'Authorization': f'Bearer {vercel_token}',
        'Content-Type': 'application/json',
    }


    response = requests.get(f'https://vercel.com/api/v4/domains/{domain}/records?teamId={team_id}', headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch current DNS records. Status code: {response.status_code}")
        return None

    records = response.json()['records']
    existing_record = next((r for r in records if r['name'] == record_name and r['type'] == 'A'), None)
    
    return existing_record

# Function to update DNS record
def update_dns_record(ip, vercel_token, domain, record_name, team_id, record_id=None):
    headers = {
        'Authorization': f'Bearer {vercel_token}',
        'Content-Type': 'application/json',
    }

    if record_id:
        update_url = f'https://api.vercel.com/v1/domains/records/{record_id}?teamId={team_id}'
        update_data = {
            'value': ip,
            'ttl': 60
        }
        response = requests.patch(update_url, headers=headers, json=update_data)
        
        if response.status_code == 200:
            print(f"DNS record updated successfully. New IP: {ip}")
            return True

        print(f"Failed to update DNS record. Status code: {response.status_code}")
        print(response.text)
        return False
    
    print("Failed to find record_id")
    return False

# Main function
def main():
    vercel_token = os.getenv('VERCEL_TOKEN')
    domain = os.getenv('DOMAIN')
    record_name = os.getenv('RECORD_NAME')
    team_id = os.getenv('TEAM_ID')
    
    current_ip = get_public_ip()
    current_record = get_current_record_ip(vercel_token, domain, record_name, team_id)

    if current_record:
        record_id = current_record['id']
        record_ip = current_record['value']
        
        if current_ip != record_ip:
            update_dns_record(current_ip, vercel_token, domain, record_name, team_id, record_id)
        else:
            print(f"DNS record is already up to date. Current IP: {current_ip}")
    else:
        update_dns_record(current_ip, vercel_token, domain, record_name, team_id)

if __name__ == "__main__":
    main()
