##
## EPITECH PROJECT, 2024
## B-YEP-400-LYN-4-1-zappy-yohann.mangenot
## File description:
## Makefile
##

SRC		=	ai/main.py

NAME	=	./zappy_ai

.PHONY: clean fclean re

all: $(NAME)

$(NAME):
	cp $(SRC) $(NAME)
	chmod 555 $(NAME)

clean:

fclean: clean
	rm -f $(NAME)

re: fclean all
