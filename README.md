# Proyecto de Aplicación Web para Monitoreo Medico Personal (MMP)

## Descripción del Proyecto

El proyecto consiste en el desarrollo de una aplicación web utilizando el lenguaje de programación Python y el framework Flask. La aplicación se enfoca en el monitoreo de la salud cardiovascular de los usuarios, haciendo uso de un sensor MAX30102 conectado a un Arduino para obtener mediciones de pulso cardiaco y SpO2 (saturación de oxígeno) en tiempo real. Estos datos son enviados al monitor serial de Arduino.

La aplicación web utiliza una base de datos PostgreSQL alojada en Railway para almacenar los datos de los usuarios. Entre los datos almacenados se encuentran los nombres, apellidos, número de teléfono, correo electrónico, edad, nombre de usuario y contraseña utilizados para el inicio de sesión en la aplicación. Además, se almacenan los valores de las mediciones correspondientes a cada usuario, así como la fecha y hora en que se realizaron.

Una vez registrados en la aplicación, los usuarios tienen la capacidad de realizar mediciones de pulso cardiaco y SpO2, y los resultados se almacenan en la base de datos asociados a su perfil. Cada vez que se realiza una medición, se envía automáticamente un mensaje al correo electrónico registrado por el usuario con los valores obtenidos.

La aplicación web cuenta con un panel de administración que permite a los administradores controlar los usuarios registrados. Desde este panel, los administradores pueden editar los datos de los usuarios, ver todas las mediciones realizadas por cada usuario y tienen la opción de descargar los datos en un archivo de Excel para su posterior análisis.

## Características principales

- Desarrollo de la aplicación web en Python utilizando el framework Flask.
- Utilización de PostgreSQL alojado en Railway para almacenar los datos de los usuarios y las mediciones.
- Integración con el sensor MAX30102 y Arduino para obtener mediciones de pulso cardiaco y SpO2.
- Registro de usuarios con almacenamiento de datos como nombres, apellidos, número de teléfono, correo electrónico, edad, nombre de usuario y contraseña.
- Almacenamiento de mediciones en la base de datos con los valores obtenidos, fecha y hora.
- Envío automático de mensajes por correo electrónico con los valores de las mediciones al correo electrónico registrado por el usuario.
- Panel de administración para controlar usuarios, editar datos y ver mediciones.
- Descarga de datos en formato de archivo Excel para su análisis.

## Tecnologías utilizadas

El proyecto utiliza las siguientes tecnologías:

- Lenguaje de programación: Python
- Framework de desarrollo web: Flask
- Base de datos: PostgreSQL (alojado en Railway)
- Interfaz de usuario: HTML, CSS, JavaScript
- Integración con Arduino: Comunicación serial
- Librerías adicionales: Flask-Mail, pandas, openpyxl

## Funcionalidades adicionales sugeridas

Además de las características principales descritas anteriormente, se sugieren las siguientes funcionalidades adicionales para mejorar el proyecto:

- Gráficas de visualización de las mediciones realizadas por cada usuario.
- Notificaciones en la interfaz web cuando se reciban nuevos valores de mediciones.
- Configuración de alarmas para valores fuera del rango normal de pulso cardiaco y SpO2.
- Generación de informes de salud con los datos de las mediciones para cada usuario.
- Análisis estadístico de los datos de mediciones para identificar patrones o tendencias.
- Integración con dispositivos móviles para facilitar el acceso a la aplicación y recibir notificaciones.


## Conexiones del Sensor MAX30102 al Arduino

El proyecto utiliza el sensor MAX30102 para obtener mediciones de pulso cardiaco y SpO2. A continuación, se describen las conexiones necesarias entre el sensor MAX30102 y el Arduino:

- Conexión SDA: Conecta el pin SDA del sensor MAX30102 al pin SDA del Arduino. Este pin se utiliza para la comunicación I2C entre el sensor y el Arduino.

- Conexión SCL: Conecta el pin SCL del sensor MAX30102 al pin SCL del Arduino. Este pin también se utiliza para la comunicación I2C entre el sensor y el Arduino.

- Conexión VCC: Conecta el pin VCC del sensor MAX30102 a una salida de 3.3V o 5V del Arduino, dependiendo de la configuración del sensor.

- Conexión GND: Conecta el pin GND del sensor MAX30102 al pin GND del Arduino para establecer la conexión a tierra.

![Conexiones Sensor MAX30102-Arduino1](<Diagrama de Conexiones.JPG>)

## Configuración de la Base de Datos

El proyecto utiliza una base de datos PostgreSQL para almacenar los datos de los usuarios y las mediciones. A continuación, se presentan las consultas SQL necesarias para la creación de las tablas en la base de datos:

```sql
CREATE TABLE registro_usuarios (
    id SERIAL PRIMARY KEY,
    nombres VARCHAR(50) NOT NULL,
    apellidos VARCHAR(50) NOT NULL,
    edad INTEGER NOT NULL,
    correo VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    usuario VARCHAR(20) UNIQUE NOT NULL,
    contraseña VARCHAR(200) NOT NULL
);

CREATE TABLE medicionespo2 (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES registro_usuarios (id),
    medicion_spo2 INTEGER NOT NULL,
    hora TIME NOT NULL,
    fecha DATE NOT NULL
);

CREATE TABLE medicionespul (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES registro_usuarios (id),
    medicion_spo2 INTEGER NOT NULL,
    hora TIME NOT NULL,
    fecha DATE NOT NULL
);
```

Estas consultas crean tres tablas en la base de datos:

1. La tabla `registro_usuarios` almacena los datos de los usuarios registrados, como nombres, apellidos, edad, correo electrónico, número de teléfono, nombre de usuario y contraseña.

2. La tabla `medicionespo2` almacena las mediciones de SpO2 (saturación de oxígeno) realizadas por cada usuario, junto con la hora y la fecha de la medición.

3. La tabla `medicionespul` almacena las mediciones de pulso cardiaco realizadas por cada usuario, junto con la hora y la fecha de la medición.

Estas tablas están relacionadas entre sí a través del campo `usuario_id`, que hace referencia al ID del usuario en la tabla `registro_usuarios`.

Es importante ejecutar estas consultas en la base de datos antes de utilizar la aplicación para asegurar que la estructura de la base de datos esté correctamente configurada.

## Acceso a Administrador.

USER_ADMIN = AdminAcceso
PASSWORD_ADMIN = AdministradorMMP

## Conclusiones

La aplicación web para el monitoreo de la salud cardiovascular ha sido desarrollada utilizando Python y el framework Flask. La integración con el sensor MAX30102 y Arduino permite obtener mediciones de pulso cardiaco y SpO2 en tiempo real. Los datos de los usuarios, así como las mediciones realizadas, se almacenan en una base de datos PostgreSQL alojada en Railway.

La aplicación proporciona una forma conveniente y accesible para que los usuarios realicen mediciones de su salud cardiovascular. Los resultados de las mediciones se presentan de manera clara y comprensible, y se envían automáticamente a los usuarios a través de correo electrónico.

El panel de administración permite a los administradores gestionar y controlar los usuarios registrados, así como ver y descargar los datos de las mediciones realizadas.

En general, este proyecto combina tecnologías modernas y técnicas de desarrollo web para crear una aplicación efectiva y útil en el ámbito del monitoreo de la salud cardiovascular.