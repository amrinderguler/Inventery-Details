"""
Celery tasks for HPE Server Inventory
"""

from celery import Celery
from api_client import HPEServerClient
from db import save_server_data

# Configure Celery with Redis backend
app = Celery('hpe_server_inventory',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')

# Configure Celery
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@app.task
def fetch_server_data(hostname, username, password, use_https=False):
    """Fetch all server data and save to database
    
    Args:
        hostname (str): Server hostname or IP
        username (str): API username
        password (str): API password
        use_https (bool): Whether to use HTTPS (default: False)
        
    Returns:
        str: Server serial number
    """
    # Initialize API client
    client = HPEServerClient(hostname, username, password, use_https=use_https)
    
    # Get system data (main endpoint)
    system = client.get_endpoint("/redfish/v1/Systems/1/")
    if not system:
        raise ValueError(f"Could not connect to server: {hostname}")
    
    serial_number = system.get("SerialNumber")
    if not serial_number:
        raise ValueError("Could not determine server serial number")
    
    # Get data from collection endpoints
    processors = client.get_members("/redfish/v1/Systems/1/Processors/")
    memory = client.get_members("/redfish/v1/Systems/1/Memory/")
    storage = client.get_members("/redfish/v1/Systems/1/Storage/")
    ethernet = client.get_members("/redfish/v1/Systems/1/EthernetInterfaces/")
    
    # Get manager data
    manager = client.get_endpoint("/redfish/v1/Managers/1")
    
    # Get power data
    power = client.get_endpoint("/redfish/v1/Chassis/1/Power")
    
    # Get PCIe devices
    pcie = client.get_members("/redfish/v1/Systems/1/PCIeDevices")
    
    # Create server data document
    server_data = {
        "serial_number": serial_number,
        "hostname": hostname,
        "system": system,
        "processors": processors,
        "memory": memory,
        "storage": storage,
        "ethernet": ethernet,
        "power": power,
        "manager": manager,
        "pcie": pcie
    }
    
    # Save to database
    save_server_data(server_data)
    
    return serial_number

@app.task(bind=True)
def process_server_list(self):
    """Process all servers from the server list file"""
    from config import SERVER_LIST_FILE
    import csv
    
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Processing server list from {SERVER_LIST_FILE}")
    
    results = []
    
    try:
        with open(SERVER_LIST_FILE) as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    result = fetch_server_data.delay(
                        hostname=row['hostname'],
                        username=row['username'],
                        password=row['password'],
                        use_https=row.get('use_https', 'False').lower() == 'true'
                    )
                    results.append(result)
                except Exception as e:
                    logger.error(f"Failed to process {row['hostname']}: {str(e)}")
        
        return [result.get() for result in results]
    except FileNotFoundError:
        logger.error(f"Server list file not found: {SERVER_LIST_FILE}")
        raise