This project aims at creating a fully autonomous data engineer. Much of a data engineer's job contains tedious and repetitive tasks. The goal of this project is to automatically create data pipelines for importing data into a cloud data warehouse using an autonomous AI Agent.

The long-term goal is to have a collection of integration patterns and agent available that can be combined to automatically generate, manage, and maintain data pipelines.

Get started:
1- clone this repo
2- set .env file and set your GPT-4 API key
`` 
cp .env.template .env
``

3- install requirements.txt
``
pip install -r requirements.txt
``

4- generate code
``
python dep_generator.py 
``
