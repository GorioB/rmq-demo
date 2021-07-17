# rmq-demo
Python RMQ demo for Elvis

## How to use this

### 1. Install docker and docker compose

You need to be able to run `docker-compose` command on your command line

### 2. Start the server

```
git clone http://github.com/goriob/rmq-demo
cd rmq-demo
docker-compose up
```

Docker compose will start the app server listener, and rabbitmq service at the same time. Logs for all 3 services will show up in the terminal

### 3. Test the service by sending POST requests with a json body to `localhost:3000/publish`

You can use curl like this:

```curl -X post localhost:3000/publish -H "content-type: application/json" --data '{"hello": "world"}'```

You can also use a browser plugin such as [RESTer](https://addons.mozilla.org/en-US/firefox/addon/rester/) to make JSON post requests easier.

Note that none of this really depends on JSON, I just used it as force of habit.

### 4. See what's happening

There should be two observations in the background:

1. Your message is picked up by the listener with a log like this:

```
[+] Message Received: $b'{"hello": "world", "your_processed_data": {"hello": "world"}}'
```

2. Rabbitmq management interface will show activity

You can access rabbitmq management by going to `localhost:15672` and logging in with the username and password guest:guest, then clicking to queues.

### 5. Understand how this shit works

There's several layers to this:

1. [Rabbitmq](https://www.cloudamqp.com/blog/part1-rabbitmq-for-beginners-what-is-rabbitmq.html) provides a queue service. We publish messages to an exchange, and create queues which can listen to messages from the exchange.
2. We use a [Flask](https://flask.palletsprojects.com/en/2.0.x/) app to create an API endpoint that takes an input, processes it, and publishes it to the exchange
3. We create a listener app that binds a queue to the exchange to listen for incoming messages and display it for us
4. We use [docker and docker-compose](https://docs.docker.com/compose/gettingstarted/) to conveniently orchestrate all this.
  a. `Dockerfile`s to describe how to build a `Docker Image`
  b. `Docker Image`s are used to create `container`s, which hold and run our software
  c. `docker-compose` is used to facilitate running 3 docker images at the same time
5. All our data processing would happen in `app/process_data.py`. In this case I made a simple wrapper to demonstrate how it fits together.
6. `app/publish_result.py` holds all the code for connecting to rabbitmq and publishing our result to the exchange
