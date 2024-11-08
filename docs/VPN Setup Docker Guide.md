# VPN Setup Docker Guide


## 1. Let the Wrapper Handle it

Wrapper has an inbuild support for enabling Docker and Spinning the container. All you need to do is ensure that:

- VPN Login Credentials exist in environment variables [Guide](#setting-up-login-environment-variables)
- Docker Service is active [Guide](#enable-docker-service)

## 2. Using Makefile

- VPN Login Credentials exist in environment variables [Guide](#setting-up-login-environment-variables)
- Docker Service is active [Guide](#enable-docker-service)

Spin the Docker Container using:

```bash
source /etc/environment
make docker_run
```

The robot is connected to the IP `10.168.1.101:1448`. Ping the robot at:

```bash
ping 10.168.1.101
```

## 3. Manual Guide

### 1. Usage

1. **Install Docker locally**.
2. **Pull the image**:

   ```bash
   docker pull crpi-orhk6a4lutw1gb13.cn-hangzhou.personal.cr.aliyuncs.com/bestoray/pgyvpn
   ```

3. **Start the container**:

   ```bash
   docker run -d --device=/dev/net/tun --net=host --cap-add=NET_ADMIN --env PGY_USERNAME="xxx" --env PGY_PASSWORD="xxx" crpi-orhk6a4lutw1gb13.cn-hangzhou.personal.cr.aliyuncs.com/bestoray/pgyvpn
   ```

### 2. Usage Notes

1. The container must be started with the `--cap-add=NET_ADMIN` option; otherwise, the virtual network card will fail to be created, causing the network to malfunction.

2. The `USERNAME` option supports entering either the "Oray account" or "UID".

3. The image supports using Docker's `-v` option to utilize container volumes.

4. The image comes pre-installed with network debugging tools like `ping` and `ifconfig`, which makes it convenient for users to troubleshoot.

5. **Log file path**: `/var/log/oray`.

6. **Configuration file path**: `/etc/oray/pgyvpn`.

## Utils

### Setting Up Login Environment Variables
Setup the environment variables as follows:

Open `/etc/environment` as root user and add the following lines to it at bottom

```txt
# PGY Dandelion VPN Configuration
"export PGY_USERNAME="{username}"
"export PGY_PASSWORD="{password}"
```

Source the environment variables with:

```bash
source /etc/environment
```
### Enable Docker Service

Enable Docker Service As Follows:

```bash
systemctl start docker.service
```
