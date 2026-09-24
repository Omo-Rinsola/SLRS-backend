FROM python:3.12-slim

WORKDIR /code
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 git git-lfs && rm -rf /var/lib/apt/lists/*
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . .
RUN git lfs install && git lfs pull
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]