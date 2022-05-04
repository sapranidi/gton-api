FROM python:3.9

COPY api.py helpers.py requirements.txt /app/

WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3", "api.py" ]