FROM python

WORKDIR /code

COPY . /code/

RUN apt-get -y update

RUN apt-get install -y binutils libproj-dev gdal-bin python-gdal python3-gdal

RUN pip install -U pip

RUN pip install -r requirements.txt

#RUN apt-get install -y python-dev postgresql-server-dev-all


EXPOSE 8000