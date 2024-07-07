##
## EPITECH PROJECT, 2024
## B-YEP-400-LYN-4-1-zappy-alexandre.douard
## File description:
## Dockerfile
##

FROM debian:bookworm-20240513-slim

RUN mkdir /zappy
RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-suggests --no-install-recommends \
                        libsfml-dev=2.5.1+dfsg-2+b2 \
                        libboost1.81-all-dev=1.81.0-5+deb12u1 \
                        wget=1.21.3-1+b2 \
                        xz-utils=5.4.1-0.2 \
                        binutils=2.40-2 \
                        tmux=3.3a-3 \
    && wget http://ftp.debian.org/debian/pool/main/g/gcc-14/libstdc++6_14-20240330-1_amd64.deb -P /tmp \
    && cd /tmp \
    && ar -x libstdc++6_14-20240330-1_amd64.deb data.tar.xz \
    && cd / \
    && tar xf /tmp/data.tar.xz -C / \
    && apt remove -y wget xz-utils binutils \
    && apt autoremove -y \
    && apt clean \
    && rm -rf /var/lib/apt/lists/* /tmp/*

COPY ./binaries/zappy_ai /zappy
COPY ./binaries/zappy_server /zappy
COPY ./binaries/zappy_gui /zappy
COPY ./binaries/font.ttf /zappy
COPY ./binaries/*.sh /zappy

WORKDIR /zappy
ENTRYPOINT ["bash", "/zappy/start_all.sh"]
