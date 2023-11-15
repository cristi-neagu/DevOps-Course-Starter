FROM python:3.12-bookworm as base
RUN pip install poetry
WORKDIR /todo_app
COPY poetry.lock poetry.toml pyproject.toml /todo_app/
RUN poetry install

EXPOSE 5000
COPY todo_app todo_app

ENTRYPOINT ["poetry", "run", "flask", "run", "-h", "0.0.0.0", "-p", "5000"]