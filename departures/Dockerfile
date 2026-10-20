FROM python:3.13
WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY app.py ./
EXPOSE 8080
CMD ["uv", "run", "python", "app.py"]
