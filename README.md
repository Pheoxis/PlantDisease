# PlantDisease

## Docker instruction

Install docker if you do not have it already.

The instruction:

1. Go to main directory
2. Run: `docker build -t name:version .` - name and version are only for you on your machine and they are asigned to the docker image, you can change only version or leave it like `name`, but then you can have a lot of dangling old images, then run `docker prune` once in a while.
3. Run: `docker run --rm -p 80:8000 name:version`
4. On `127.0.0.1:80` the server will be listening
