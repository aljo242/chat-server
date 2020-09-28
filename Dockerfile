FROM python:3

ADD test1.py /
ADD test2.py /

ADD server.py /
ADD client.py /
ADD _common_.py /

CMD ["python", "./test1.py"]
CMD ["python", "./test2.py"]
