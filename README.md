# HW 3: Microservices with Hazelcast Distributed Map

## Requirements
The following command installs all necessary packages:
```bash
pip install -r requirements.txt
```

### Usage
Run one instance of facade service, one of messaging and three of logging:
```bash
FLASK_APP=facade-service/facade-service.py flask run -p 8080
FLASK_APP=logging-service/logging-service.py flask run -p 8082
FLASK_APP=logging-service/logging-service.py flask run -p 8083
FLASK_APP=logging-service/logging-service.py flask run -p 8084
FLASK_APP=messages-service/messages-service.py flask run -p 8081
```

### Test
Execute the GET/POST requests from [Requests.http](https://github.com/romanyshyn-natalia/software-architecture/blob/micro_basics/facade-service/Requests.http) file.

## Results
We created three logging service instances and send 10 messages to facade service:
![](images/posting_to_facade.png)

Logging service 1 got such messages:
![](images/logging1.png)

Logging service 2 got such messages:
![](images/logging2.png)

Logging service 3 got such messages:
![](images/logging3.png)

Reading messages from facade:
![](images/reading.png)

Turning off few logging instances: (error are expected, because we choose logging service at random)
![](images/error.png)
