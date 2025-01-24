# sistema de laudos
sistema de laudos para mercaderia y hojalata

## requerimientos
- git
- visual studio code
- python
- postgresql
- msodbcsql (instalar el driver para conectar con sql-server)

## instalacion

### primer uso

1. crear carpeta local donde ubicar el proyecto

2. ejecutar el siguiente comando:

        git clone https://github.com/laureano934/laudos.git

3. configurar git si fuera necesario:

- configurar un nombre de usuario

        git config --global user.name “nombre_ejemplo”

- configurar un email

        git config --global user.email “email_ejemplo”

- colorear las lineas para facilitar la lectura

        git config --global color.ui auto

4. conceder acceso a github a traves del navegador

5. instaslar la extension "python" en visual studio code

6. antes de empezar a hacer cambios, crear un rama para no trabajar en la principal; ejemplos de nombre podrian incluir:

        desarrollo
        prueba_de_caracteristica
        rutas
        login
        etc...

### usos posteriores

8. para retomar el trabajo, actualizar cambios de los demas
        
        git pull

7. para ver todas las ramas

        git branch -a

9. restaurar la base de datos en caso de que hubiera una version nueva,
la misma se encuentra en la carpeta db en dos versiones;

        custom o backup de posgresql, el archivo no lleva extension
        plain o sql, el archivo termina en extension sql

## comandos y uso de git

- listar ramas

        git branch

- crear una nueva rama con un nombre que describa lo que vamos a hacer

        git branch "mi_nueva_rama"

- cambiar de rama

        git checkout "rama_destino"

- integrar cambios

        git merge "rama_origen"

- mostrar el historial de commits

        git log

- mostrar el estado actual de los archivos modificados
        
        git status

- agregar un archivo al proximo commit

        git add "archivo"

- quitar archivo de "add" sin perder modificaciones
        
        git reset "archivo"

- diferencias no agregadas con "add"
        
        git diff

- diferencias con "add" pero sin commit

        git diff --staged

- hacer commit

        git commit -m “mensaje que describa lo que acabamos de hacer en tiempo presente”

- descargar todas ramas de un repositorio

        git fetch "repo"

- integrar una rama remota en la rama actual local para actualizarla
        
        git merge "rama remota"

- subir commits locales a un repositorio remoto

        git push "repo_remoto"

- descargar e integrar cualquier commit desde la rama remota seguida 

        git pull

### Asignacion de tareas para desarrollo

Se trabajara horizontalmente, realizando para cada seccion la vista, el controlador y el modelo.
Recordar que antes que nada hay que chequear que el usuario este logueado y tenga autorizacion para estar en cada seccion.

#### laureano

        index
        login
        base
        mercaderia
        extracto
        insumos
        ubicaciones

#### luciano

        accesos
        ayuda
        sugerencias
        despachos
        vencimientos

#### silvio

        bloqueados
        motivos_bloqueo
        hojalata
        permisos
        usuarios
