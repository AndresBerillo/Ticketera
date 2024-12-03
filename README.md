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
        +int id
        +String nombre
        +DateTime fecha
        +String ubicacion
        +String descripcion
        +ImageField  imagen
        +String __str__()
    }

    class Entrada {
        +int id
        +Concierto concierto
        +String numero_asiento
        +Usuario propietario
        +Decimal precio
        +Boolean esta_vendida
        +FileField archivo_pdf
        +String __str__()
        +guardar(*args, **kwargs)
    }

    class CarritoDeCompras {
        +Int id
        +Usuario usuario
        +MuchosAMuchos entradas
        +String __str__()
    }

    class Transaccion {
        +int id
        +Entrada entrada
        +Usuario comprador
        +DateTime fecha
        +Decimal monto
        +String __str__()
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
```

### Diagrama de Secuencia

```mermaid
sequenceDiagram
    participant Usuario
    participant Navegador
    participant ServidorDjango
    participant BaseDeDatos

    Usuario->>Navegador: Accede al sitio web
    Navegador->>ServidorDjango: Solicita la lista de conciertos (/concerts/)
    ServidorDjango->>BaseDeDatos: Obtiene los datos de los conciertos
    BaseDeDatos-->>ServidorDjango: Retorna los conciertos
    ServidorDjango-->>Navegador: Devuelve la lista de conciertos
    Navegador-->>Usuario: Muestra los conciertos disponibles

    Usuario->>Navegador: Selecciona un concierto y visualiza detalles
    Navegador->>ServidorDjango: Solicita detalles del concierto (/concert/<id>/)
    ServidorDjango->>BaseDeDatos: Obtiene los datos del concierto
    BaseDeDatos-->>ServidorDjango: Retorna los detalles del concierto
    ServidorDjango-->>Navegador: Devuelve los detalles del concierto
    Navegador-->>Usuario: Muestra los detalles del concierto

    Usuario->>Navegador: Agrega una entrada al carrito
    Navegador->>ServidorDjango: Solicita agregar la entrada al carrito (/cart/add/<id>/)
    ServidorDjango->>BaseDeDatos: Agrega la entrada al carrito del usuario
    BaseDeDatos-->>ServidorDjango: Confirma la operación
    ServidorDjango-->>Navegador: Actualiza el estado del carrito
    Navegador-->>Usuario: Muestra que la entrada fue añadida al carrito

    Usuario->>Navegador: Procede a la compra
    Navegador->>ServidorDjango: Solicita procesar el pago (/checkout/)
    ServidorDjango->>BaseDeDatos: Registra la transacción
    BaseDeDatos-->>ServidorDjango: Confirma la transacción
    ServidorDjango-->>Navegador: Confirma la compra
    Navegador-->>Usuario: Muestra confirmación de la compra

