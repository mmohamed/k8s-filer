# Simple Filer


### 1. Local running

```bash
export UPLOAD_FOLDER=$(pwd)/uploads
# generate random file
head -c 1M </dev/urandom > myfile
# install and run
pipenv install
python main.py
# test
curl http://127.0.0.1:5000/filer/list
curl -X POST -F file=@myfile http://127.0.0.1:5000/filer
curl -X GET http://127.0.0.1:5000/filer-list
curl -o getfile http://127.0.0.1:5000/filer/myfile
curl -X DELETE http://127.0.0.1:5000/filer/myfile
```

### 2. Docker image building

```bash
# Building image
docker buildx build --push --platform linux/arm64,linux/arm/v7,linux/amd64 --tag medinvention/k8s-filer:dev .
```