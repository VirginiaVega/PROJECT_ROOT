
<img src="static\images\qualif1.png">

## Sitio web Blog
Este proyecto es una aplicación web que permite la creación, actualización y exploración de publicaciones, con funcionalidades adicionales como comentarios y calificaciones de usuarios.  
Forma parte de mi portafolio profesional y busca demostrar tanto conocimientos técnicos como de documentación de software.

## Tecnologías usadas

- **Lenguaje:** Python 3.12
- **Framework:** Django 
- **Base de Datos:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript
- **Control de versiones:** Git + GitHub


| <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" width="30"> | <img src="https://static.djangoproject.com/img/logos/django-logo-negative.png" width="60"> | <img src="https://upload.wikimedia.org/wikipedia/commons/2/29/Postgresql_elephant.svg" width="30"> | <img src="https://www.w3.org/html/logo/badge/html5-badge-h-solo.png" width="30"> | <img src="https://upload.wikimedia.org/wikipedia/commons/d/d5/CSS3_logo_and_wordmark.svg" width="30"> | <img src="https://upload.wikimedia.org/wikipedia/commons/9/99/Unofficial_JavaScript_logo_2.svg" width="30"> | <img src="https://upload.wikimedia.org/wikipedia/commons/0/03/Git_format.png" width="30"> | <img src="https://upload.wikimedia.org/wikipedia/commons/c/c2/GitHub_Invertocat_Logo.svg" width="30"> |


## Objetivos del proyecto
- Implementar operaciones CRUD para la gestión de publicaciones.
- Permitir a los usuarios comentar y puntuar cada publicación.
- Explorar publicaciones de manera eficiente.
- Mantener documentación clara y profesional (requerimientos, casos de uso, Product backlog y diagramas UML).

## Documentación disponible
- [Requerimientos](/docs/requerimientos.md)  
- [Modelo del dominio](/docs/modelo_dominio.md)  
- [Casos de uso](/docs/casos_uso.md)  
- [Product Backlog](/docs/backlog.md)  
- [Diagrama de clases](/docs/img/diagrama_clases.png)  

## Instalar y ejecutar Qualifs:

1.  Clonar el repositorio en la terminal de tu maquina local: 
 ```bash
   git clone https://github.com/VirginiaVega/PROJECT_ROOT.git
 ```

2. Crear un entorno virtual y activarlo: 
 ```bash
python -m venv venv
source venv/bin/activate   # En Linux/Mac
venv\Scripts\activate      # En Windows
 ```

3. Instalar las dependencias del proyecto:
 ```bash
pip install -r requirements.txt
 ```

4. Configurar las variables de entorno en un archivo .env (ejemplo de guia en .env.example): 
 ```bash
SECRET_KEY=tu_clave_django
DEBUG=True
DB_NAME=nombre_db
DB_USER=usuario
DB_PASSWORD=contraseña
DB_HOST=localhost
DB_PORT=5432
 ```

5. Crear la base de datos PostgreSQL local y ejecutar migraciones:
  ```bash
  python manage.py migrate
   ```

6. Iniciar el servidor de desarrollo:
  ```bash
python manage.py runserver
  ```

7. Acceder en el navegador.
  ```bash
http://127.0.0.1:8000/
  ```

---

⚠️ Nota: Este proyecto usa PostgreSQL como base de datos. Para ejecutarlo localmente, instalar PostgreSQL y crear una BD con las credenciales definidas en el archivo .env.

## Capturas de pantalla

## Autora
Virginia Vega - Analista de sistemas orientada al desarrollo web. 2025

📧 Contacto: virginiavegaok@gmail.com

🌐 LinkedIn: (https://www.linkedin.com/in/virginia-vega-254b45263/)
