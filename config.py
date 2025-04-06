import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB Configuration

MONGO_URI = str(os.getenv("MONGO_URI"))
MONGO_DB = str(os.getenv("MONGO_DB"))


# Celery Configuration
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# HPE Server API Endpoints
API_ENDPOINTS = {
    "system": "/redfish/v1/Systems/1/",
    "processors": "/redfish/v1/Systems/1/Processors/",
    "memory": "/redfish/v1/Systems/1/Memory/",
    "storage": "/redfish/v1/Systems/1/Storage/",
    "ethernet": "/redfish/v1/Systems/1/EthernetInterfaces/",
    "power": "/redfish/v1/Chassis/1/Power/",
    "manager": "/redfish/v1/Managers/1/",
    "pcie": "/redfish/v1/Systems/1/PCIeDevices/"
}

# Server list file (CSV with columns: hostname,username,password)
SERVER_LIST_FILE = os.getenv("SERVER_LIST_FILE", "server_list.csv")