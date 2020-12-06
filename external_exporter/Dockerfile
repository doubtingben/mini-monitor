FROM python:3

ADD ./pip.requirements /tmp/pip.requirements

RUN python -m pip install -r /tmp/pip.requirements
ADD balance-logger.py /tmp/balance-logger.py
ENTRYPOINT ["python", "/tmp/balance-logger.py"]