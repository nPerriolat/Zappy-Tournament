##
## EPITECH PROJECT, 2023
## B-YEP-400-LYN-4-1-zappy-alexandre.douard
## File description:
## Makefile
##

NAME	=	zappy_ai
TESTLOCATION	=	./tests/
VENV_LOCATION	=	./.venv
VENV_REQUIREMENTS_LOCATION	=	./requirements.txt

ifeq ($(shell uname -s), Windows_NT)
	BIN_NAME	=	$(NAME).exe
else
	BIN_NAME	=	$(NAME)
endif

all: ${VENV_LOCATION}
	. ${VENV_LOCATION}/bin/activate; PYTHONOPTIMIZE=2 pyinstaller --onefile $(NAME) -n $(BIN_NAME)
	cp dist/$(BIN_NAME) ./binaries

${VENV_LOCATION}: ${VENV_LOCATION}/touchfile

${VENV_LOCATION}/touchfile: ${VENV_REQUIREMENTS_LOCATION}
	test -d ${VENV_LOCATION} || python3 -m venv ${VENV_LOCATION}
	. ${VENV_LOCATION}/bin/activate; pip3 install -Ur ${VENV_REQUIREMENTS_LOCATION}
	touch ${VENV_LOCATION}/touchfile

tests_run:  ${VENV_LOCATION}
	. ${VENV_LOCATION}/bin/activate; pytest -vv $(TESTLOCATION)

tests_cov:  ${VENV_LOCATION}
	. ${VENV_LOCATION}/bin/activate; coverage run -m pytest $(TESTLOCATION)
	. ${VENV_LOCATION}/bin/activate; coverage report -m

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

fclean: clean
	rm -rf dist/
	rm -rf ./.venv/

re:
	@$(MAKE) fclean
	@$(MAKE) all

.PHONY: all tests_run tests_cov clean fclean re
