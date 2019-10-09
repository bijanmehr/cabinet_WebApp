# Comprehensive Austism Screening System Web Application

website project for connecting and performing commands on a robot

commands gets from user and then pass to rospy for handling

## API
API documentation: https://documenter.getpostman.com/view/8126807/SVYjSMuw?version=latest

## How to setup


First make sure you have python3 and pip3 in your system and rospy works in python3 as well. if you don't have rospy in python3 use this command

>> sudo apt-get install python3-yaml

>> sudo pip3 install rospkg catkin_pkg

After cloning cd to the project directory install requirements with this command:

>> pip3 install -r requirements.txt

Next you should make your database:

>> python3 manage.py makemigrations

>> python3 manage.py migrate

And after that you can create a super user with bellow command 

>> python3 manage.py createsuperuser

Super user is used for changing database at address "/admin/"

In case you forgot your password you can create another superuser, or you can change the password with below command.

>> python3 manage.py changepassword [username]

## RUN SERVER

You can start django server by running below command. Before that, make sure roscore is up and running.

>> python3 manage.py runserver 0.0.0.0:8000 --noreload

## Admin Page

You can view, modify or add new instances of models by visiting /admin/ page. 

Some models are used for storing configuration. You can't create more than one instance of these models. 

### Durations

Each stage has a default duration. Values for durations can be modified at "/admin/website/duration/".

### Parrot Commands 

Parrot commands can be modified at "/admin/website/parrotcommand/". 

### Front-End Properties

Properties used at front-end can be modified at "/website/frontconfig/".
