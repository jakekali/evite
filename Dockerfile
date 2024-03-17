FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update
# expose the port
EXPOSE 8000 8888

RUN pip install --upgrade pip
# make a new virtual environment
RUN pip install virtualenv
RUN virtualenv venv
# activate the virtual environment
RUN . venv/bin/activate
# install the requirements
RUN pip install -r requirements.txt
COPY . /code/
RUN echo 'sleep'


