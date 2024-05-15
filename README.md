
# TO-DO APP

# Deployed to DigitalOcean

### [DigitalOcean](https://lionfish-app-npi3c.ondigitalocean.app/docs#/)

---
# Getting started
---
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
# Prerequisites
This is a project written using Python and FAST API
1. Clone the repository
```
https://github.com/romedikc/to-do-app
```
2. Create the virtual enviroment
 ```
python3 -m venv venv
source venv/bin/activate
```
3. Install the requirements
```
pip install -r requirements.txt
```
4. Create a new PostgreSQL database

In your terminal:
```
psql postgres
CREATE DATABASE databasename
\c databasename
```
5. Generate a secret key
 ```
openssl rand -hex 32
 ```

6. Build the Docker Image
```
$ docker-compose --build 
```
7. Run the project
```
$ docker-compose up
```
