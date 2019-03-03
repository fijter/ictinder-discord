FROM phusion/baseimage:0.11
MAINTAINER dave.defijter@iota.org
EXPOSE 4486

RUN add-apt-repository universe
RUN apt update
RUN apt -y install python3 python3-venv python3-pip supervisor

RUN mkdir -p /discordbot/src
COPY . /discordbot/src/
WORKDIR /discordbot/src
RUN python3 -m venv /discordbot/env
RUN /discordbot/env/bin/pip install -r /discordbot/src/requirements.txt
RUN cp /discordbot/src/conf/supervisor.conf /etc/supervisor/conf.d/ictinder.conf
RUN /discordbot/env/bin/python /discordbot/src/manage.py migrate --noinput

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

CMD service supervisor start && supervisorctl tail -f ictinder
