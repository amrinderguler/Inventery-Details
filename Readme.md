#HPE Server Inventory Collector

A Dockerized application for collecting and storing HPE server inventory data using the iLO Redfish API.

##Features

- Collects comprehensive server inventory data via HPE iLO Redfish API
- Stores data in MongoDB for easy querying and analysis
- Uses Celery for asynchronous task processing
- Redis for task queue management
- Dockerized environment for easy deployment

##Prerequisites

- Docker and Docker Compose installed
- `.env` file with required configuration (Find attached with Mail)

##Quick Start

1. Clone this repository
2. Create a `.env` file .
3. Create a `server_list.csv` file with your server credentials.   #(Replace the `server_list.csv` with actual credentials file).
4. Run the application:

### Server List File

Create a CSV file with your server credentials (default: `server_list.csv`) in the below format:

```csv
hostname,username,password,use_https,use_token
ilo.example.com,admin,password123,true,true
192.168.1.100,operator,password456,false,false
```


1.Run to initialize the docker
```bash
docker-compose up --scale celery_worker=3  --build      #replace no of workers as per requirement
```
##TO initialize concurrency update docker-compose.yml in the celery_beat section.
#Eg. celery -A tasks beat --loglevel=info --concurrency=50   (replace with actual concurrency as per requirement).

##Services

The Docker Compose file sets up these services:

- **redis**: Redis server for Celery task queue
- **mongodb**: MongoDB database for storing inventory data
- **celery_worker**: Celery worker process
- **celery_beat**: Celery beat process for scheduled tasks


##Usage

###Collecting Data

Run the main script to collect data for all servers in your list



2.to check the state of docker
```bash
docker-compose ps
```
4.To stop the docker
```bash
docker-compose down
```



##Project Structure

```
├── api_client.py       # HPE iLO API client
├── config.py           # Configuration settings
├── db.py               # MongoDB operations
├── docker-compose.yml  # Docker configuration
├── main.py             # Main entry point
├── requirements.txt    # Python dependencies
├── server_list.csv     # Server credentials (example)
└── tasks.py            # Celery tasks
```

##Troubleshooting

- Check logs: `docker-compose logs`
- Verify services are running: `docker-compose ps`
- For SSL warnings: Ensure `use_https` is set correctly in your server list

