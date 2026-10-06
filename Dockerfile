FROM python:3.12-slim

WORKDIR /code
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . .
RUN curl -L -o app/ml/vendor/pretrained/4426_model.pt "https://github.com/Omo-Rinsola/SLRS-backend/releases/download/v0.1.0-beta/4426_model.pt"
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]