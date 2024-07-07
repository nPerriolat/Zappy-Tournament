##
## EPITECH PROJECT, 2022
## undefined
## File description:
## Makefile
##

SRC =	$(wildcard src/*.py) \
		$(wildcard src/**/*.py)

NAME = zappy_ai

FLAGS_PY = --onefile --clean --name $(NAME)

$(NAME):
		pyinstaller $(FLAGS_PY) $(SRC)
		cp dist/$(NAME) ./
		cp $(NAME) ../

all: $(NAME)

clean:
		$(RM) -r ./build/
		$(RM) -r ./dist/
		$(RM) -r ./src/__pycache__/
		$(RM) ./zappy_ai.spec

fclean: clean
		$(RM) 	$(NAME)
		$(RM) ../$(NAME)

re: fclean all

.PHONY: all clean fclean re
