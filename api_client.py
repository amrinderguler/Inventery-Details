import requests
import logging
from requests.exceptions import RequestException

# Configure logging
logger = logging.getLogger(__name__)

class HPEServerClient:
    """Client for HPE iLO RESTful API"""

    def __init__(self, hostname, username, password, use_https=False, use_token=False):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.use_token = use_token
        self.token = None
        protocol = "https" if use_https else "http"
        self.base_url = f"{protocol}://{hostname}"
        self.session = requests.Session()
        self.session.verify = False  

        # Set up authentication based on token or basic auth
        if self.use_token:
            self.login_with_token()
        else:
            self.session.auth = (username, password)

    def login_with_token(self):
        """Authenticate and store X-Auth-Token"""
        login_url = f"{self.base_url}/redfish/v1/Sessions"
        payload = {"UserName": self.username, "Password": self.password}
        headers = {"Content-Type": "application/json"}

        try:
            # Attempt to log in using token-based authentication
            logger.info(f"Logging in to {login_url} with token-based authentication")
            response = self.session.post(login_url, json=payload, headers=headers, timeout=30)
            logger.info(f"Token login response code: {response.status_code}")
            response.raise_for_status()

            self.token = response.headers.get("X-Auth-Token")
            if self.token:
                self.session.headers.update({"X-Auth-Token": self.token})
                logger.info(f"Token acquired: {self.token[:10]}...")  
            else:
                logger.error("Failed to get X-Auth-Token")

        
        except RequestException as e:
            logger.error(f"Token login failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status code: {e.response.status_code}")
                logger.error(f"Response text: {e.response.text}")

    def get_endpoint(self, endpoint):
        """Send GET request to API endpoint"""
        try:
            url = f"{self.base_url}{endpoint}"
            logger.info(f"Making request to URL: {url}")
            logger.info(f"Using auth: {'token' if self.use_token else self.username}")

            response = self.session.get(url, timeout=30)
            logger.info(f"Response status code: {response.status_code}")
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            logger.error(f"Error fetching {endpoint} from {self.hostname}: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status code: {e.response.status_code}")
                logger.error(f"Response text: {e.response.text}")
            return None

    def get_members(self, collection_endpoint):
        """Get all members from a collection endpoint"""
        try:
            collection = self.get_endpoint(collection_endpoint)
            if not collection or "Members" not in collection:
                return []

            members = []
            for member in collection.get("Members", []):
                if "@odata.id" in member:
                    member_data = self.get_endpoint(member["@odata.id"])
                    if member_data:
                        members.append(member_data)

            return members
        except Exception as e:
            logger.error(f"Error processing collection {collection_endpoint}: {str(e)}")
            return []
    
    def get_serial_number(self, system_data):
        """Extract serial number from system data"""
        if not system_data:
            return None
            
        return system_data.get("SerialNumber")
