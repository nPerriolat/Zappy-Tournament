##
## EPITECH PROJECT, 2024
## HEADER
## File description:
## HEADER
##

SRC	=	./src/main.py

NAME =	zappy_ai

$(NAME)	:
			cp $(SRC) ./zappy_ai

all: $(NAME)

clean:
		rm -rf zappy_ai

fclean:	clean

re:	fclean all

tests_run:
	pytest --cov=src/ tests/

.PHONY: all clean fclean re tests_run
