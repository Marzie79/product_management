FROM python:3.10.12-slim

RUN mkdir /product_management

WORKDIR /product_management

COPY . .

RUN pip install -r requirements/requirements.txt

EXPOSE 8000

CMD ["0.0.0.0:8000"]