# Parcial N° 4 para Tópicos avanzados en bases de datos 2022-2
### Bases de datos embebidas - NO SQL
Se debe desarrollar una aplicación que permita hacer uso de las operaciones CRUD a una base de datos SQLite a través de una interfaz de usuario.

[Requisitos para ejecutar la aplicación](https://github.com/Galhrrera/PescasArtesanales/blob/main/README.md#requisitos-para-ejecutar-la-aplicaci%C3%B3n)

[Preparación](https://github.com/Galhrrera/PescasArtesanales/blob/main/README.md#preparaci%C3%B3n)

[Ejecución de la aplicación](https://github.com/Galhrrera/PescasArtesanales/blob/main/README.md#ejecuci%C3%B3n-de-la-aplicaci%C3%B3n)

[Dominio del problema](https://github.com/Galhrrera/PescasArtesanales/blob/main/README.md#dominio-del-problema-pescas-artesanales)

[Explicación de la implementación](https://github.com/Galhrrera/PescasArtesanales/blob/main/README.md#explicaci%C3%B3n-de-la-implementaci%C3%B3n)

[Comentarios](https://github.com/Galhrrera/PescasArtesanales/blob/main/README.md#explicaci%C3%B3n-de-la-implementaci%C3%B3n)

## Requisitos para ejecutar la aplicación
- pip
- python 3 (El desarrollo se realizó en la versión 3.9.7)
- eel
- Google chrome

## Preparación
Antes de ejecutar la aplicación, es necesario verificar que cumple con os requisitos mencionados.

- Asegúrese de tener instalado el navegador google chrome. **eel** permite crear interfaces de usuario de manera sencilla con html, css y js, por lo cual es necesario tener un navegador que se encargue de interpretar la UI. Si no cuenta con google chrome instalado en su ordenador, es necesario descargarlo e instalarlo.
- Asegúrese de tener python instalado, preferiblemente en la versión recomendada (3.9.7). El teoría, debería funcionar sobre cualquier versión de python 3.10. Python es el lenguaje de programación con el que se ejecuta toda la lógica back-end de la solución. Si no cuenta con python instalado en su ordenador, es necesario descargarlo e instalarlo
- Asegúrese de tener pip instalado. pip será la herramienta con la cual se descargará e instalará el paquete **eel** de python, gracias al cual se logra realizar una conexión entre en back-end desarrollado en python y el front-end realizado con html, css y js.
- Asegúrese de tener instalado **eel**. eel es el paquete que permite la conexión entre el back-end desarrollado con python y el front-end desarrollado con html, css y js. Básicamente, se encarga de traducir los métodos o funciones de python a js.

### Nota
Una vez se asegure de tener instalado python, google chrome y pip, basta con ejecutar el siguiente comando para descargar e instalar pip:

`pip install eel`

## Ejecución de la aplicación
La aplicación se puede ejecutar directamente con python tras clonar este repositorio. Siga los siguientes pasos:

1. Clone este repositorio en su ordenador ingresando en la terminal el comando: `git clone https://github.com/Galhrrera/PescasArtesanales.git`
2. Ingrese a la carpeta del proyecto **PescasArtesanales**
3. En la terminal ejecute el archivo **main.py** utilizando python: `python.exe main.py`

Sí cumple con los requisitos mencionados, clonó correctamente el repositorio y no hubieron problemas, tras estos pasos se debería abrir la aplicación haciendo uso del motor de google chrome y debería poder ver algo como esto:

![Ventana inicial de la aplicación](https://github.com/Galhrrera/PescasArtesanales/blob/main/imgs/ventanaInicial.png)

A partir de este momento podrá navegar a través de las distintas opciones y, adicionalmente, podrá realizar las operaciones CRUD.


## Dominio del problema: Pescas artesanales

La Autoridad Nacional de Acuicultura y Pesca, AUNAP, quiere identificar cuales son las tendencias actuales en el manejo de la pesca artesanal en las principales cuencas hidrográficas del país, los métodos artesanales más comunes que se utilizan.

Las actividades de pesca tendrán los siguientes atributos:

- Consecutivo de la actividad
- Cuenca
- Método de la pesca
- Fecha de la actividad
- Peso del pescado obtenido en la actividad

### Diagrama entidad relación de la solución: 

![Diagrama entidad relación](https://github.com/Galhrrera/PescasArtesanales/blob/main/imgs/diagrama%20entidad%20relaci%C3%B3n.jpg)

## Explicación de la implementación

La solución, como se ha mencionado, fue desarrollada haciendo uso de Python, HTML, CSS y JavaScript.

- En la aplicación hay 3 opciones en el menú lateral izquierdo, las cuales hacen referencia cada una a una de las tablas u opciones disponibles: **pescas, métodos y cuencas**
- Cada una de las tablas cuenca con sus respectivas operaciones CRUD de la siguiente forma:
  - La apliación realiza un READ todo el tiempo, desde que se inicia la aplicación, cada vez que se actualiza o se carga la ventana y cada vez que hay cambios (las demás operaciones)
  - Cada tabla tiene habilitada la opción para crear un registro en su respectiva tabla. En el caso de las pescas, la aplicación mostrará todas las cuencas y métodos disponibles (lee la base de datos para cargar las opciones) y permite seleccionar la fecha e ingresar el peso de la pesca. En las demás tablas, se podrá ingresar el nombre según corresponda y desee.
  - Cada tabla tiene habilitada la opción de actualizar un registro. En cada caso se debe seleccionar la opción que desea actualizar y, adicionalmente, deberá indicar los datos que se actualizarán (en el caso de las pescas puede actualizar la cuenca, el método, la fecha y el peso; en el caso de las demás tablas, podrá ingresar un nuevo nombre para la cuenca o el método, según corresponda).
  - Cada tabla tiene habilitada la opción de eliminar un registro. En todos los casos, seleccione uno de los registros y elimínelo.
 - La lógica SQL (conexión a la base de datos, excepciones, select, update e insert to a la base de datos, entre otras) fue realizada 100% en python (ver main.py)
 - El frontend (UI) se realizó 100% con HTML, CSS y JS (ver /www)
 - **eel** es el traductor entre python y js. cada uno de los métodos declarados en python deben ser entonces expuestos utiizando la instrucción `@eel.expose` antes de la declaración de cada método.
 - Es mandatorio añadir dentro del cuerpo HTML la línea `<script type="text/javascript" src="/eel.js"></script>` para lograr la correcta traducción de los métodos de python a js y viceversa.
   - Como claración, el archivo *eel.js* no existe dentro del proyecto, sin embargo, **eel** se encarga de cargarlo implícito en el proyecto.
 
## Comentarios
- Existe un control de excepciones básico, como lo es la prohibición la creación y actualización de registros con valores seleccionados / ingresados nulos
- No es posible eliminar una cuenca o un método si está siendo usado en la tabla pescas por alguno de sus registros, debido a las *llaves*
- La aplicación NO es responsive, por lo que **recomienda usar la resolución por defecto (1920 x 1080)** para evitar disgustes visuales.
- Las tablas (gráficamente dentro de la aplicación) tienen una altura predeterminada y, en caso de tener muchos registros, se habilitará un scroll en cada tabla.

