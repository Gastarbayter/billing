FROM python:3.8-slim

WORKDIR /usr/src/app

COPY Pipfile.lock Pipfile ./

COPY . .

RUN pip install -U pip setuptools pipenv \
    && pipenv lock -r --keep-outdated > requirements.txt \
    && pip install -r requirements.txt --retries=1 \
#    && pipenv install --system --deploy --ignore-pipfile --dev \
    && mkdir -p /usr/src/app/logs \
    && chmod -R 777 /usr/src/app/logs \
    && chmod +x ./entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]
