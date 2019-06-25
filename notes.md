[FLIR SDK](https://flir.app.boxcn.net/v/SpinnakerSDK)

[multi_pyspin - A simple multi camera library using PySpin](https://github.com/justinblaber/multi_pyspin)

# Dockerfile:
https://docs.docker.com/get-started/part2/
http://phase2.github.io/devtools/common-tasks/ssh-into-a-container/


```bash
docker exec -it <container name> <command>

# Build a Dockerfile (generates an image) with name `myApp`:
docker build --tag=myapp:v1 .

# List existing images:
docker image ls

# Run docker image:
docker run --interactive myapp:v1
```

[Name your own containers](https://stackoverflow.com/questions/25230812/when-to-use-dockers-container-name) with `--name` when you use `docker run`.

## Running GUI application in a docker container
https://medium.com/@SaravSun/running-gui-applications-inside-docker-containers-83d65c0db110
