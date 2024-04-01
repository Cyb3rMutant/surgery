```bash
You need to Add a New Doctor and Give Access ?
And
if you are running with docker follow these steps:

1 - docker-compose up -d
2 - docker exec -it project-smartcare-1 bash
3 - python manage.py createsuperuser
4 - go through the super user creation steps
5 - in your browser signup as a doctor
6 - then go to 127.0.0.1:8000/admin
7 - login with the superuser you created earlier in step 4
8 - press on user
9 - choose the doctor you created
10 - look for active and tick it
11 - scroll down and save changes
12 - go to 127.0.0.1:8000/logout
13 - now you should be able to login as that doctor

```