FROM python:3.11
EXPOSE 5000
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
CMD ["flask", "run", "--host", "0.0.0.0"]