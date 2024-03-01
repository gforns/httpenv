FROM python:3.6
RUN apt-get update && apt-get install -y net-tools curl lsof dnsutils tcpdump bind9-utils jq telnet
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV PORT=80
ENV SSL=False
ENTRYPOINT ["python"]
CMD ["app.py"]
EXPOSE 80
