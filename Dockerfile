# Adapted from:
# * https://docs.docker.com/compose/gettingstarted/
# * https://github.com/python-poetry/poetry/issues/1178#issuecomment-998549092

FROM python:3.9-alpine
WORKDIR /backend

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers

RUN pip install poetry
RUN poetry config virtualenvs.in-project true
ADD pyproject.toml poetry.lock /backend/
RUN poetry install --no-ansi

ADD .env /backend/
ADD app.py /backend/

# TODO: Use uswgi if this were a production image
EXPOSE 5000
CMD ["poetry", "run", "flask", "run"]
