# Proyecto: Carrito de Compras para Entradas de Conciertos 🎟️

Este proyecto es una tienda en línea desarrollada con Django que permite a los usuarios comprar entradas para conciertos. 

### Características principales:
- Explorar conciertos disponibles con detalles como fecha, ubicación y descripción.
- Comprar entradas para conciertos y descargar PDF de la compra.
- Gestionar conciertos y entradas desde un panel administrador.
- Gestionar usuaarios desde un panel administrador.

---

## Instalación 🚀

Sigue los pasos a continuación para configurar y ejecutar el proyecto en tu entorno local.

```bash
# 1. Clona el repositorio
git clone <URL-del-repositorio>
cd <nombre-del-repositorio>

# 2. Configura un entorno virtual
# En Linux/Mac:
python -m venv env
source env/bin/activate
# En Windows:
python -m venv env
env\Scripts\activate

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. Configura la base de datos
python manage.py makemigrations
python manage.py migrate

# 5. Crea un superusuario
python manage.py createsuperuser

# 6. Inicia el servidor
python manage.py runserver

# Accede al proyecto en tu navegador:
# http://127.0.0.1:8000
```
### Diagrama de Clases

```mermaid
classDiagram
    class Concierto {
        +Entero id
        +Cadena nombre
        +FechaHora fecha
        +Cadena ubicacion
        +Cadena descripcion
        +CampoImagen imagen
        +Cadena __str__()
    }

    class Entrada {
        +Entero id
        +Concierto concierto
        +Cadena numero_asiento
        +Usuario propietario
        +Decimal precio
        +Booleano esta_vendida
        +CampoArchivo archivo_pdf
        +Cadena __str__()
        +guardar(*args, **kwargs)
    }

    class CarritoDeCompras {
        +Entero id
        +Usuario usuario
        +MuchosAMuchos entradas
        +Cadena __str__()
    }

    class Transaccion {
        +Entero id
        +Entrada entrada
        +Usuario comprador
        +FechaHora fecha
        +Decimal monto
        +Cadena __str__()
    }

    class Usuario {
        <<de django.contrib.auth.models>>
    }

    Concierto "1" --> "*" Entrada : entradas
    Entrada "1" --> "1" Usuario : propietario
    CarritoDeCompras "1" --> "1" Usuario : usuario
    CarritoDeCompras "1" --> "*" Entrada : entradas
    Transaccion "1" --> "1" Entrada : entrada
    Transaccion "1" --> "1" Usuario : comprador
