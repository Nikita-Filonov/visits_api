# Visits API

Настройка проекта
---

1. Перед настройков проекта необходимо установить Docker + docker-compose. Как это сделать описано тут:

    - Установить [Docker](https://docs.docker.com/desktop/windows/install/)
      для Windows
    - Установить [docker-compose](https://docs.docker.com/compose/install/) для Windows

2. Теперь необходимо склонировать проект в локальный репозиторий

```shell
cd <some_folder>
git clone https://github.com/<github_username>/visits_api.git
cd visits_api
```

3. После того как проект склонирован мы можем запустить его. Для этого выполним команду

```shell
docker-compose up
```

Данная команда начнет скачивание образов и сборку контейнеров. После завершения выполнения билда вы консоли будет такой
лог

```shell
visits_api_server_1   | INFO:     Will watch for changes in these directories: ['/code']
visits_api_server_1   | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
visits_api_server_1   | INFO:     Started reloader process [1] using statreload
visits_api_server_1   | INFO:     Started server process [8]
visits_api_server_1   | INFO:     Waiting for application startup.
visits_api_server_1   | INFO:     Application startup complete.
```

Это означает, что наш сервер успешно запушен на 8000-м порту.

Для проверки того, что все запущено перейдем в бразуер по ссылке http://localhost:8000/docs. Мы должны увидеть страницу
Swagger

4. Для корректной работы бизнес логики нужно применить миграции и выполнить начальный сидинг.

Получим список запущенных контейнеров

```shell
docker ps
```

В консоли будет примерно такой лог

```shell
CONTAINER ID   IMAGE                          COMMAND                  CREATED         STATUS          PORTS                                                        NAMES
5e6adad8eb12   visits_api_visits_api_server   "uvicorn main:app --…"   7 days ago      Up 3 minutes    0.0.0.0:8000->8000/tcp, :::8000->8000/tcp                    visits_api_visits_ap
i_server_1
f22f00952168   postgres:latest                "docker-entrypoint.s…"   7 days ago      Up 3 minutes    0.0.0.0:5432->5432/tcp, :::5432->5432/tcp                    visits_api_visits_ap
i_db_1
dcc5bc7bde81   dpage/pgadmin4                 "/entrypoint.sh"         7 days ago      Up 3 minutes    80/tcp, 443/tcp, 0.0.0.0:5454->5454/tcp, :::5454->5454/tcp   visits_api_visits_ap
i_pgadmin_1
3a77221280ef   ws_chat_chat                   "python server.py"       17 months ago   Up 15 minutes   0.0.0.0:6789->6789/tcp, :::6789->6789/tcp                    web_socket_chat
```

В данном случае мы видим название образа `visits_api_visits_api_server` и id контейнера, в данном примере
это `5e6adad8eb12`

После того, как мы получили id контейнера, мы можем попасть внутрь контейнера и выполнить миграции и сидинг. Для этого
выполним команды

```shell
docker exec -it <your_container_id_here> /bin/bash
```

После у вас откроета `bash` консоль внутри контейнера. Чтобы проверить, что вы находитесь именно в нужном контейнере,
выполните команду

```shell
ls
```

Вы должны увидеть такой лог

```shell
root@5e6adad8eb12:/code# ls
Dockerfile  Procfile   __pycache__  database.py         groups   migrations  pairs        requirements.txt  seeders      static     users  venv
LICENSE     README.md  alembic.ini  docker-compose.yml  main.py  models      permissions  roles             settings.py  templates  utils
```

Теперь применим миграции. Для этгот тут же выполним команду

```shell
alembic upgrade head
```

И выполним начальный сидинг. Для этого нужно выполнить 3 команды

```shell
python -m seeders.roles
python -m seeders.permissions
python -m seeders.users
```

После чего будут созданны Roles, UserRoles, Permissions, RolePermissions, Users, Tokens
