##
## NILS PERRIOLAT, 2024
## Zappy Tournament Script
## File description:
## Makefile
##

SRC		=	src/main.py

NAME	=	./zts

.PHONY: clean fclean re

all: $(NAME)

$(NAME):
	cp $(SRC) $(NAME)
	chmod 555 $(NAME)

clean:

fclean: clean
	rm -f $(NAME)

re: fclean all
