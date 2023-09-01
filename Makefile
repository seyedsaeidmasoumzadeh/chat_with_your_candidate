
NAME=chat_with_your_candidate
USER=$(shell id -u):$(shell id -g)

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

build:
	docker-compose build chat_with_your_candidate
	docker-compose build linter

format:
	docker-compose run --rm --user $(USER) linter black src/

bash:
	docker-compose run --rm --user $(USER) chat_with_your_candidate bash

# unfurtunatly, port binding is not supported for MAC OS in docker compose, this why we use docker rather than docker compose
run: 

	docker-compose run -p 7860:7860 --rm --user $(USER) chat_with_your_candidate gradio main.py
