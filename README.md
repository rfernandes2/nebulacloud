# What is NebulaCloud
NebulaCloud is a website that allows you to manage files and folders within a user's primary folder. 
You can create, update, and delete folders, as well as preview photos.

This is an excellent solution for individuals with a home disk who want to use a personal NAS with a web interface.

The front-end is in another repository: https://github.com/j38moreira/nebulacloud-frontend

```
You can also find a script here to create users in the database. The website uses a token-based authentication system.
```

# Important notes:

* The OS must be a Linux system.
* The main folder is located at /srv/cloud/
  - Create a user folder here, for example, ricardo.
  - Then set the appropriate permissions:
```
chmod -R ricardo:ricardo /srv/cloud/ricardo
```

# How to Run
* Install requirements:
```
pip3 install -r requirements.txt
```
* Install any additional dependencies if prompted.

* Run the application:
```
python3 -m api.app
```
