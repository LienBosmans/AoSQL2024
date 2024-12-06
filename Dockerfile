FROM python:3.13

WORKDIR /

COPY python_packages.txt /Docker/
RUN pip3 install -r /Docker/python_packages.txt

WORKDIR /duckdb

ENTRYPOINT [ "bash" ]
