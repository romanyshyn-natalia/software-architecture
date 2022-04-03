# HW 1: Basic architecture of microservices

## Installation
To install from our github repository, you can do:
```bash
git clone https://github.com/romanyshyn-natalia/software-architecture.git
cd software-architecture
```

## Requirements
The following command installs all necessary packages:
```bash
pip install -r requirements.txt
```

### Usage
```bash
FLASK_APP=facade-service/facade-service.py flask run -p 8080
FLASK_APP=logging-service/logging-service.py flask run -p 8081
FLASK_APP=messages-service/messages-service.py flask run -p 8082
```