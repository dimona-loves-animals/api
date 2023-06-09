FROM python:3.11.4-alpine3.18

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

ENTRYPOINT [ "uvicorn", "main:app" ]
CMD [ "--port", "80", "--host", "0.0.0.0" ]
