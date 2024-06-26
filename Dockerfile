FROM python:3
ENV DONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code/

CMD ["uvicorn", "services.main:app", "--host=0.0.0.0", "--reload"]