# What is NebulaCloud
NebulaCloud is a website that allows you to manage files and folders inside a primary folder of a user. 
You can delete, update, create folders and see photos with the front-end.

This a good solution for a person that wants to use a personal NAS with a website.

The front-end is on another repository: https://github.com/j38moreira/nebulacloud-frontend

```
You also have a script here to create users on the database. The website uses token system to auth
```

# Important notes:

* The OS must be a Linux system.
* The main folder is on /srv/cloud/
  - Here you create your user folder for example ricardo.
  - Then give permissions
```
chmod -R ricardo:ricardo /srv/cloud/ricardo
```

# To Run
* install requirements:
```
pip3 install -r requirements.txt
```
```
python3 -m api.app
```

* Install if necessary other dependecies that can be asked

