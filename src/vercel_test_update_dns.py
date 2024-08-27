import os
import unittest
from time import sleep
from dotenv import load_dotenv

from vercel_update_dns import get_public_ip, get_current_record_ip, update_dns_record

# Load environment variables
load_dotenv()
vercel_token = os.getenv('VERCEL_TOKEN')
domain = os.getenv('DOMAIN')
record_name = os.getenv('RECORD_NAME')
team_id = os.getenv("TEAM_ID")

class TestDNSUpdater(unittest.TestCase):
    def test_record_ip(self):
        dummy_ip = "111.11.111.111"
        
        current_record = get_current_record_ip(vercel_token, domain, record_name, team_id)

        if not current_record:
            return self.assertFalse(False, msg=f"Failed to find record: {record_name}")

        record_id = current_record['id']
            
        successful_update = update_dns_record(dummy_ip, vercel_token, domain, record_name, team_id, record_id)

        if not successful_update:
            return self.assertFalse(False, msg=f"Failed to update record: {record_name}")
        
        sleep(60)

        current_record = get_current_record_ip(vercel_token, domain, record_name, team_id)

        if not current_record:
            return self.assertFalse(False, msg=f"Failed to find record after dummy ip change ({record_name})")

        record_ip = current_record['value']
        self.assertEqual(dummy_ip, record_ip)

if __name__ == '__main__':
    unittest.main()