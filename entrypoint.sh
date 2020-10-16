#!/bin/bash

python scripts/execute_migrations.py

[ -v ENVIRONMENT ] && export ENVIRONMENT=$ENVIRONMENT || export ENVIRONMENT=$OPENSHIFT_BUILD_REFERENCE

if [[ ${ENVIRONMENT} = 'LOCAL' ]]; then
#     while ! nc -zvw3 postgres 5432; do echo waiting for postgres; sleep 30; done;
#     echo "Postgres is up"

#     exec alembic upgrade head && uvicorn asgi:app --host 0.0.0.0 --port 5000  --log-level=debug
    exec uvicorn asgi:app --host 0.0.0.0 --port 5000  --log-level=debug
else
    exec uvicorn asgi:app --host 0.0.0.0 --port 5000
fi
