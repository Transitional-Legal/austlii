FROM python:3.10
WORKDIR /code
COPY ./backend/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./backend/src /code
CMD ["flask", "main", "--host", "0.0.0.0", "--port", "8000"]
