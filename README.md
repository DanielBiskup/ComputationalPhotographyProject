# ComputationalPhotographyProject

*   [Add your user](https://docs.docker.com/install/linux/linux-postinstall/) to the `docker` group to ensure, that you can run docker as non root
*   [check](https://unix.stackexchange.com/a/325972/40226) that your running X11 and not Wayland: `loginctl` to find your SESSION name (e.g. `2`) and run `loginctl show-session 2 -p Type`
