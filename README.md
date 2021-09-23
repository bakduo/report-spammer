Report Spam Django 3
=============================

# ROADMAP
- [ ] test
- [x] CRUD
- [x] rabbitmq
- [x] control workers
- [x] Frontend
- [ ] refactor
- [x] container
- [x] cluster

# Overview Task

La task de spam relacionado con la queue se encuentra desacoplada de Django entonces necesitamos poder iniciarla de la siguiente forma:

- 1 primero se inicia el worker.
- 2 se incia la tarea.

```
#inicia el worker:

celery -A messageadmin worker -l DEBUG

```

```
# se inicia la tarea

pipenv shell

from spammers.tasks import mqservice

run = mqservice.delay()

run.get()

```

Si queremos ver los resultados iniciamos django. 

```

python manage.py runserver


```


