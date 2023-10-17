FROM python:3.9

ENV PYTHONUNBUFFERED=1

WORKDIR /purrfect_pix

COPY ../requirements.txt /purrfect_pix/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /purrfect_pix/src

WORKDIR /purrfect_pix/src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
