FROM python:3.5
ADD config.toml config.toml
ADD python_cmd.sh python_cmd.sh
ADD main.py main.py
ADD package package
RUN cd package; pip3 install git+https://github.com/deeso/top-sites-check.git

#RUN pip install git+https://github.office.opendns.com/adpridge/fiery-snap.git

CMD [ "sh", "python_cmd.sh" ]

EXPOSE 10006/tcp
