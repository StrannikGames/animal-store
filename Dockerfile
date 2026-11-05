FROM python:3.14-alpine
WORKDIR /animal_store
RUN pip install uv --no-cache-dir
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --no-cache --no-dev
COPY animal_store/ animal_store/
EXPOSE 8000
CMD [ "uv", "run", "--no-dev", "python", "-m", "animal_store.main" ]
