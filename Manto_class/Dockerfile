FROM python:3.9.16

COPY . /mydir

WORKDIR /mydir

# Run는 최대한 줄여야 함
RUN  python -m pip install --upgrade pip \
    && pip install -r requirements.txt

CMD ["uwsgi","uwsgi.ini"]