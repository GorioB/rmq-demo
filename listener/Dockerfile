FROM python:3.9-alpine

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

EXPOSE 3000

# expects dev directory to be mounted to /app
# WILL NOT WORK on its own with no mounted directory
WORKDIR /app
CMD ["python", "-u", "listener.py"]
