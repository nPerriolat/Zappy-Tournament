##
## EPITECH PROJECT, 2024
## B-YEP-400-LYN-4-1-zappy-paul.morilhat
## File description:
## Makefile
##

AI = ./ai

MAKE = make -s -C
MAKE_CLEAN = make -s clean -C
MAKE_FCLEAN = make -s fclean -C
MAKE_RE = make -s re -C

all: zappy_ai

zappy_ai:
	@$(MAKE) $(AI)

ai_clean:
	@$(MAKE_CLEAN) $(AI)

clean: ai_clean

ai_fclean:
	@$(MAKE_FCLEAN) $(AI)

fclean: ai_fclean

ai_re:
	@$(MAKE_RE) $(AI)

re: ai_re

.PHONY: re ai_re \
	fclean ai_fclean \
	clean ai_clean \
	all zappy_ai
