# define the name of the virtual environment directory
VENV := .venv
VPN_IMAGE := crpi-orhk6a4lutw1gb13.cn-hangzhou.personal.cr.aliyuncs.com/bestoray/pgyvpn
VPN_CONTAINER := pgy_vpn

all: venv

setup: pyproject.toml
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -e .

dev: pyproject.toml
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -e .[dev]

venv: $(VENV)/bin/activate

run: venv
	./$(VENV)/bin/python3 src/robotComms/robotComms.py

clean:
	rm -rf $(VENV)
	rm -rf .ruff_cache
	rm -rf logs
	find . -type f -name '*.pyc' -delete
	find . -name '__pycache__' -ls -exec rm -rv {} +
	find . -name '*.egg-info' -ls -exec rm -rv {} +

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

.PHONY: all venv run clean setup dev docker_run 
