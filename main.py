import logging
import warnings
import urllib3
from datetime import datetime
from config import SERVER_LIST_FILE
from tasks import process_server_list

# Suppress InsecureRequestWarning when SSL verification is disabled
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"inventory_collection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    logger.info(f"Starting HPE Server Inventory Collection")
    logger.info(f"Using server list from: {SERVER_LIST_FILE}")
    
    # Trigger the Celery task to process all servers
    result = process_server_list.delay()
    logger.info(f"Process initiated with task ID: {result.id}")
    
    logger.info("Check Celery logs for task progress and completion")

if __name__ == "__main__":
    main()
