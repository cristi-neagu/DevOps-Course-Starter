FROM python:3.12-bookworm as base
RUN pip install poetry
WORKDIR /todo_app
COPY poetry.lock poetry.toml pyproject.toml /todo_app/
RUN poetry install

COPY todo_app todo_app

FROM base as production

EXPOSE 8000
ENTRYPOINT ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8000", "todo_app.app:create_app()"]

FROM base as development

EXPOSE 5000
ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]