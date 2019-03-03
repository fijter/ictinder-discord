# IOTA Ictinder node bot

This Discord bot connects your Discord account to your Ict installation providing additional functionality through Discord.

## Requirements

To run this bot you need the following packages installed on your system:

 - Python 3.5+

## Installation

 - Install all python package dependancies (in a virtualenv by preference) with `pip install -r requirements.txt`
 - Add your discord keys and other configuration to the `.env` file (see .env.example to see the variable names to use)
 - Run `python manage.py run_bot` to start the bot as the active process
 - Optional: Run the run_bot command through supervisor so it auto restarts when needed
 - Optional: Run gunicorn with this Django app to expose a web interface/API

## Using Docker

This bot runs using Docker as well, expose port 4486 for allowing Ictinder to send you messages:

`docker build . -t ictinder -f Dockerfile`
`docker run -p 4486:4486 --network host ictinder`

## Features

This version of the NodeBot contains the following features

 - A basic bot that enables you to register your Discord account with the auto peering IXI
 - Interactive bot commands to remove and list your nodes
 - A basic API that allows the IXI to send you notification messages on Discord

