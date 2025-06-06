# Sistema de Correo SMTP con Docker

Este proyecto implementa un sistema de correo SMTP usando Flask y MailHog, todo containerizado con Docker.

## Requisitos Previos

1. **Docker Desktop**
   - Windows: [Descargar Docker Desktop para Windows](https://www.docker.com/products/docker-desktop/)
   - Mac: [Descargar Docker Desktop para Mac](https://www.docker.com/products/docker-desktop/)
   - Linux: [Instrucciones de instalación para Linux](https://docs.docker.com/desktop/install/linux-install/)

2. **Git** (opcional, para clonar el repositorio)
   - [Descargar Git](https://git-scm.com/downloads)

## Instalación

1. Clona o descarga este repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   ```
   O simplemente descarga y descomprime el ZIP del proyecto.

2. Abre una terminal y navega hasta el directorio del proyecto:
   ```bash
   cd ruta/al/proyecto
   ```

3. Asegúrate de que Docker Desktop esté ejecutándose.

## Ejecución

1. En la terminal, ejecuta:
   ```bash
   docker-compose up --build
   ```

2. Espera a que los contenedores se construyan y se inicien. El proceso está completo cuando veas mensajes indicando que los servicios están listos.

## Uso del Sistema

### Para enviar correos:
1. Abre tu navegador y ve a:
   ```
   http://localhost:5000
   ```
2. Llena el formulario con:
   - Correo del destinatario
   - Asunto
   - Contenido del mensaje
3. Haz clic en "Enviar Correo"

### Para ver los correos enviados:
1. Abre tu navegador y ve a:
   ```
   http://localhost:8025
   ```
2. Aquí podrás ver todos los correos enviados a través del sistema

## Detener el Sistema

1. En la terminal donde está ejecutándose, presiona:
   ```
   Ctrl + C
   ```

2. Para eliminar los contenedores (opcional):
   ```bash
   docker-compose down
   ```

## Puertos Utilizados

- **5000**: Aplicación web (formulario de envío)
- **1025**: Servidor SMTP (MailHog)
- **8025**: Interfaz web de MailHog (para ver los correos)

## Solución de Problemas

1. **Error "port is already allocated"**
   - Significa que los puertos 5000, 1025 o 8025 están en uso
   - Cierra otras aplicaciones que puedan estar usando estos puertos
   - O modifica los puertos en el archivo `docker-compose.yml`

2. **Docker Desktop no está ejecutándose**
   - Asegúrate de que Docker Desktop esté instalado y en ejecución
   - Verifica el ícono de Docker en la barra de tareas

3. **No se pueden enviar correos**
   - Verifica que ambos contenedores estén ejecutándose
   - Revisa los logs en la terminal
   - Asegúrate de que el formulario esté completo correctamente

## Notas Adicionales

- Este es un sistema de desarrollo/pruebas, no está diseñado para uso en producción
- Todos los correos son capturados por MailHog y no se envían a destinatarios reales
- Los correos se pierden cuando se detienen los contenedores

## Tecnologías Utilizadas

- Docker y Docker Compose
- Python con Flask
- MailHog
- Bootstrap para la interfaz de usuario #   R e d e s - S M T P  
 