# define the name of the virtual environment directory
VENV := .venv
VPN_IMAGE := crpi-orhk6a4lutw1gb13.cn-hangzhou.personal.cr.aliyuncs.com/bestoray/pgyvpn
VPN_CONTAINER := pgy_vpn

ENTRY:=main.py

# Module Variables
MODULE:=robotComms

all: venv

init: 
	poetry shell

setup: pyproject.toml $(VENV)
	poetry install

run: $(VENV)
	./$(VENV)/bin/python3 $(ENTRY)

format:
	black $(MODULE)
	ruff check $(MODULE)

fix:
	ruff check $(MODULE) --unsafe-fixes --fix

clean:
	rm -rf $(VENV)
	rm -rf site
	find . -type f -name '*.pyc' -delete
	find . -name '__pycache__' -ls -exec rm -rv {} +
	find . -name '.ruff_cache' -ls -exec rm -rv {} +
	find . -name 'logs' -ls -exec rm -rv {} +
	find . -name 'dist' -ls -exec rm -rv {} +

docker_run:
	docker run -d \
		--name $(VPN_CONTAINER) \
		--device=/dev/net/tun \
		--net=host \
		--cap-add=NET_ADMIN \
		--cap-add=SYS_ADMIN \
		--env PGY_USERNAME=$(PGY_UNM) \
		--env PGY_PASSWORD=$(PGY_PWD) \
		$(VPN_IMAGE)

docker_clean:
	docker stop $(VPN_CONTAINER)
	docker rm $(VPN_CONTAINER)
	docker rmi $(VPN_IMAGE)

.PHONY: all init setup run format fix clean docker_run docker_clean 
