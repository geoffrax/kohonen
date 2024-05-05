FROM python:3.11-alpine

COPY . /

RUN pip install -r ./requirements.txt

EXPOSE 5000

CMD [ "python", "/kohonen.py" ]