# ComputationalPhotographyProject

# With docker (Not working)
*   [Add your user](https://docs.docker.com/install/linux/linux-postinstall/) to the `docker` group to ensure, that you can run docker as non root
*   [check](https://unix.stackexchange.com/a/325972/40226) that your running X11 and not Wayland: `loginctl` to find your SESSION name (e.g. `2`) and run `loginctl show-session 2 -p Type`


# On Machine without docker
* Follow official instructions
* Install [`glibc`](https://community.citra-emu.org/t/glibc-2-27-not-found-required-by-citra/58776/2) required by `spinnakerView_QT` with `apt-get install libc6-amd64 libc6-dev libc6-dbg`

```bash
/usr/bin/SpinView_QT
/usr/bin/SpinView_QT: /lib/x86_64-linux-gnu/libm.so.6: version `GLIBC_2.27' not found (required by /usr/lib/libSpinnaker.so.1)
/usr/bin/SpinView_QT: /lib/x86_64-linux-gnu/libc.so.6: version `GLIBC_2.27' not found (required by /usr/lib/libSpinnaker.so.1)
```
