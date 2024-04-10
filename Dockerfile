FROM python:3.12-slim

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libffi-dev g++ \
    && rm -rf /var/lib/apt/lists

RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock* /code/
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi && apt-get purge -y --auto-remove gcc libffi-dev g++


COPY . /code

RUN python -m compileall .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
