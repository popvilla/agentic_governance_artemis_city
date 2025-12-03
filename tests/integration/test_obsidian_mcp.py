import unittest
import urllib.request
import urllib.error
import json
import os
import sys


class TestObsidianMCP(unittest.TestCase):
    BASE_URL = "http://localhost:3000"
    API_KEY = None

    @classmethod
    def setUpClass(cls):
        # Try to load config from .env
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
        print(f"Loading config from {env_path}")
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('MCP_API_KEY='):
                        cls.API_KEY = line.split('=', 1)[1]
                    elif line.startswith('PORT='):
                        cls.BASE_URL = f"http://localhost:{line.split('=', 1)[1]}"
        
        if not cls.API_KEY:
            print("Warning: MCP_API_KEY not found in .env, using default/hardcoded if any (or failing).")
            # Fail if no key found
            if not cls.API_KEY:
                 print("Error: Could not find MCP_API_KEY in .env")
                 # We might want to allow passing via env var too
                 cls.API_KEY = os.environ.get('MCP_API_KEY')

    def test_01_health_check(self):
        """Verify the server is up and running."""
        url = f"{self.BASE_URL}/health"
        print(f"Testing Health Check: {url}")
        try:
            with urllib.request.urlopen(url) as response:
                self.assertEqual(response.getcode(), 200)
                content = response.read().decode('utf-8')
                print(f"Health Check Response: {content}")
                self.assertIn("MCP Server is healthy", content)
        except urllib.error.URLError as e:
            self.fail(f"Health check failed. Is the server running? Error: {e}")

    def test_02_list_notes(self):
        """Verify authentication and listNotes endpoint."""
        if not self.API_KEY:
            self.fail("MCP_API_KEY is not set.")

        url = f"{self.BASE_URL}/api/listNotes"
        print(f"Testing List Notes: {url}")
        
        req = urllib.request.Request(url, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f"Bearer {self.API_KEY}")
        
        # Empty body for listNotes
        data = json.dumps({}).encode('utf-8')
        
        try:
            with urllib.request.urlopen(req, data=data) as response:
                self.assertEqual(response.getcode(), 200)
                response_data = json.loads(response.read().decode('utf-8'))
                print("List Notes Response (truncated):", str(response_data)[:200])
                
                self.assertTrue(response_data.get('success'), "Response should indicate success")
                # Data might be empty if vault is empty, but 'data' key should exist
                self.assertIn('data', response_data)
                
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8')
            print(f"HTTP Error Body: {body}")
            self.fail(f"HTTP Error: {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            self.fail(f"URL Error: {e}")

if __name__ == '__main__':
    unittest.main()
