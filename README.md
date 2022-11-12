# HTTPenv: Service that prints environment on http

Simple Python flask server that exposes request information and environment vars as http service

- https://hub.docker.com/r/gforns/httpenv
- https://github.com/gforns/httpenv


3 routes are available:

- `/anything` - Reports request information (like the  Kenneth Reitz httpbin.org project)
- `/env` - Reports environment variables from container
- `/all` - Reports request information and environment variables

In addition, some troubleshooting tools have been installed like: `curl`, `jq`, `nslookup`, `dig`, `tcpdump`, `netstat`, `lsof`, `tcpdump`.


## Run in Docker

```
docker run -p 10080:80 -e MY_VAR="Hello" gforns/httpenv
```
You can access environment variables with `curl`
```
curl --silent  localhost:10080/all | jq .env.MY_VAR
"Hello"
```


## Run in Kubernetes

You can run a `pod` and `service`

```
kubectl run myservice --image=gforns/httpenv --expose=true --port=80 --env=MY_VAR=Hello
```

You can use same image to troublehsoot connectivity executing a `bash `shell:

```
kubectl run --rm -it --image=gforns/httpenv --command bash bash
root@bash:/app#
root@bash:/app# curl myservice.default.svc.cluster.local/anything
{
  "headers": {
    "Host": "myservice.default.svc.cluster.local",
    "User-Agent": "curl/7.74.0",
    "Accept": "*/*"
  },
  "args": {},
  "form": {},
  "json": null,
  "method": "GET",
  "origin": null,
  "url": "http://myservice.default.svc.cluster.local/anything"
}
```

### Kubernetes manifest

```
apiVersion: v1
kind: Service
metadata:
  name: myservice
  namespace: default
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
  selector:
    run: myservice
---
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: myservice
  name: myservice
  namespace: default
spec:
  containers:
  - env:
    - name: MY_VAR
      value: Hello
    image: gforns/httpenv
    name: myservice
    ports:
    - containerPort: 80
    resources: {}
```


## Kubernetes downward API
This image let's expose information from the K8s downward API:
https://kubernetes.io/docs/concepts/workloads/pods/downward-api/

```
apiVersion: v1
kind: Service
metadata:
  name: myservice
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
  selector:
    run: myservice
---
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: myservice
  name: myservice
spec:
  containers:
  - env:
    - name: MY_NAME
      valueFrom:
        fieldRef:
          fieldPath: metadata.name
    - name: MY_NAMESPACE
      valueFrom:
        fieldRef:
          fieldPath: metadata.namespace
    image: gforns/httpenv
    name: myservice
    ports:
    - containerPort: 80
    resources: {}
```




