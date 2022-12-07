# ETL - SPOTIPY
En este proyecto realizaremos un  **ETL** (Extract, Transform, Load) a los datos que se extraen de la **API de Spotify**, mediante **Spotipy** que nos permite programarlo en python.

## API SPOTIFY
Para obtener las credenciales de la API debemos ir a su [sitio web]([aquí](https://developer.spotify.com/dashboard/login)) y registrarnos, con esto obtendremos los siguientes datos:
  - CLIENT_ID
  - CLIENT_SECRET
  - SPOTIPY_REDIRECT_URI

## PIPENV
Recomiendo utilizar un entorno virtual para manejar nuestras dependencias, también se puede utiliza `venv` u otro que conozca.
Instalamos `pipenv`
```
pip install pipenv
```
Si desea instala la versión de python con la que quiere trabajar, en mi caso estaré trabajando con python 3.8
```
pipenv install --python 3.8
```
Corremos el entorno
```
pipenv shell
```
Instalamos las librerías necesarias
```
pipenv install spotipy
pipenv install python-decouple
pipenv install pandas
pipenv install sqlalchemy
pipenv install psycopg2
```
## EXTRACT
En esta fase **extraemos** los *datos crudos* de la API.

## TRANSFORM
Una vez obtenido los datos procedemos a **transformarlo**, es decir, aplicaremos ciertos filtros o restricciones, prepararemos un dataframe para luego cargarlo.

## LOAD
En esta etapa final realizaremos la **carga** a nuestro base de datos.

## DOCKER
La gran importancia de la utilización de contenedores es que nos permite trabajar un entorno que puede ser compartido a otras personas, además de tener todo estructurado con lo cual nos hará más fácil realizar mantenimiento a nuestro código.

La idea principal de este proyecto es tener contenedores para nuestro postgresql y pgadmin. Teneniendo estos contenedores podremos correr nuestro proyecto en otras máquinas sin problemas.

Hay dos formas de realizarlo, podemos crear cada contenedor con el `docker run ...`, es decir, creamos por separados los contenedores y tendremos que ejecutar cada uno de forma individual, esto podría traer un poco de complejidad en nuestro proyecto, debido a que debemos de correrlo individualmente, se vería así
```
docker run -d --name pg -p 5432:5432 -v date:/var/lib/postgresql/data -e POST...
docker run -d --name pgadmin -p 80:80 -e PGADMIN...
*otras imagenes*
```
Por este motivo, es mejor tener un orquestador de contenedores, en este caso usarmoes Docker Compose, que nos permite ejecutar los contenedores al mismo tiempo todo estará escrito en un archivo `docker-compose.yaml`.

### Docker compose
```yaml
version: "3.X" # 3.6, 3.7, ...
services:
  nombre_contenedor1:
    build: . # Construir la imagen que se encuentra en esta ruta, archivo dockerfile,
             # puede que no estén al mismo nivel, cambiar el . por su ruta.
    ports:
      - "0000:0000" # Puerto de ejemplo, port_anfitrion:port_contenedor
    links:
      nombre_contenedor2 # Aquí decimos que este contenedor tendrá acceso
                         # al nombre_contenedor1, va sin comillas.
  nombre_contenedor2:
    imagen: postgres
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_PASSWORD = postgres
      - POSTGRES_USER = postgres
      - POSTGRES_DB = db_spotipy
    volumes:
      - postgres-data: /var/lib/pgsql/data # Postgres guarda su datos en esta ruta
    # - mysql: /var/lib/mysql
    # - mongo: /data/db
volumes: # Esto nos permite crear un volumen en nuestra máquina anfitrión para almacenar
         # los datos y así no se pierdas en caso eliminamos el container
  postgres-data: # No va nada.
```
Lo ejecutamos con
```
docker compose up
```
