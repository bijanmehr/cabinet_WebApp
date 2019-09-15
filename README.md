# AILAB

website project for connecting and performing commands on a robot

commands gets from user and then pass to rospy for handling

## How to setup

after cloning cd to AILAB directory

first make sure you have python3 and pip3 in your system and rospy works in python3 as well

if you don't have rospy in python3 use this command

>> sudo apt-get install python3-yaml

>> sudo pip3 install rospkg catkin_pkg

then install requirements with this command:

>> pip3 install -r requirements.txt

after that you should make your database:

>> python3 manage.py makemigrations

>> python3 manage.py migrate

and after that you can create a super user with bellow command 

super user used for changing data base at address "/admin"

>> python manage.py createsuperuser

at the end you can collect your static files (optional)

>>python3 manage.py collectstatic

## RUN SERVER

first make sure that your ros core is running after that

just run server with command:

>> python3 manage.py runserver 0.0.0.0:8000 --noreload

