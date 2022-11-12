FROM python:3.6
RUN apt-get update && apt-get install -y net-tools curl lsof dnsutils tcpdump bind9-utils jq
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV PORT=80
ENTRYPOINT ["python"]
CMD ["app.py"]
EXPOSE 80
