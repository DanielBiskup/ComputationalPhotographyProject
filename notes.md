[FLIR SDK](https://flir.app.boxcn.net/v/SpinnakerSDK)

[multi_pyspin - A simple multi camera library using PySpin](https://github.com/justinblaber/multi_pyspin)

# Dockerfile:
https://docs.docker.com/get-started/part2/
http://phase2.github.io/devtools/common-tasks/ssh-into-a-container/


```bash
# Build a Dockerfile (generates an image) with name `myApp`:
docker build --tag=myapp:v1 .

# List existing images:
docker image ls

# Run docker image:
docker run myapp:v1

# Run docker image with interactive tty and bash:
docker run --interactive --tty myapp:v1 bash
```

[Name your own containers](https://stackoverflow.com/questions/25230812/when-to-use-dockers-container-name) with `--name` when you use `docker run`.

## Running GUI application in a docker container
https://medium.com/@SaravSun/running-gui-applications-inside-docker-containers-83d65c0db110

Flags to run docker with:

  * share the Host’s XServer with the Container by creating a volume `--volume="$HOME/.Xauthority:/root/.Xauthority:rw"`
  * share the Host’s DISPLAY environment variable to the Container `--env="DISPLAY"`
  * run container with host network driver with `--net=host`
