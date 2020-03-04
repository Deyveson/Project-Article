FROM python:3.8

WORKDIR /usr/src/app/ws-img

EXPOSE 5555

RUN pip install pipenv

ENTRYPOINT pipenv install --system && \ 
           PROFILE=develop python ws-img.py 
