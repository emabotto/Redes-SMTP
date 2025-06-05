# Despliegue en AWS EC2

## Requisitos Previos
1. Cuenta en AWS (puedes usar la capa gratuita)
2. Par de claves SSH generado en AWS
3. Docker y Docker Compose instalados en la instancia EC2

## Pasos para el Despliegue

### 1. Crear Instancia EC2
1. Ve a la consola de AWS
2. Lanza una nueva instancia EC2:
   - Ubuntu Server 20.04 LTS
   - t2.micro (capa gratuita)
   - Configurar grupo de seguridad con los siguientes puertos:
     - SSH (22)
     - HTTP (80)
     - HTTPS (443)
     - Aplicación web (5000)
     - MailHog Web UI (8025)
     - SMTP (1025)

### 2. Configurar la Instancia
1. Conéctate a tu instancia:
```bash
ssh -i tu-clave.pem ubuntu@tu-ip-publica
```

2. Instalar Docker:
```bash
# Actualizar sistema
sudo apt-get update

# Instalar dependencias
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Agregar clave GPG de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Agregar repositorio
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER
```

### 3. Configurar el Proyecto

1. Clonar el repositorio:
```bash
git clone <URL_DEL_REPOSITORIO>
cd <DIRECTORIO_DEL_PROYECTO>
```

2. Modificar docker-compose.yml para exponer los puertos correctamente:
```yaml
version: '3'

services:
  smtp:
    image: mailhog/mailhog
    ports:
      - "1025:1025"
      - "8025:8025"
    networks:
      - mail_network
    restart: always

  web:
    build: ./web
    ports:
      - "5000:5000"
    depends_on:
      - smtp
    networks:
      - mail_network
    environment:
      - SMTP_HOST=smtp
      - SMTP_PORT=1025
    restart: always

networks:
  mail_network:
    driver: bridge
```

3. Ejecutar el sistema:
```bash
docker-compose up -d --build
```

## Acceso al Sistema

Una vez desplegado, podrás acceder al sistema usando la IP pública de tu instancia EC2:

- Aplicación web: `http://tu-ip-publica:5000`
- Interfaz MailHog: `http://tu-ip-publica:8025`

## Configuración de Dominio (Opcional)

1. Registra un dominio en Route 53 o tu proveedor preferido
2. Configura los registros DNS para apuntar a tu IP pública
3. Configura SSL con Let's Encrypt:

```bash
# Instalar Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tudominio.com
```

## Consideraciones de Seguridad

1. Configura un firewall (UFW):
```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 5000
sudo ufw allow 8025
sudo ufw allow 1025
sudo ufw enable
```

2. Configura autenticación básica para MailHog:
```yaml
services:
  smtp:
    environment:
      - MH_AUTH_FILE=/etc/mailhog/.auth
    volumes:
      - ./mailhog/.auth:/etc/mailhog/.auth
```

3. Mantén el sistema actualizado:
```bash
sudo apt-get update
sudo apt-get upgrade
```

## Mantenimiento

1. Monitorear logs:
```bash
docker-compose logs -f
```

2. Reiniciar servicios:
```bash
docker-compose restart
```

3. Actualizar contenedores:
```bash
docker-compose pull
docker-compose up -d --build
```

## Respaldo de Correos (Opcional)

Para mantener un respaldo de los correos, puedes configurar un volumen persistente:

```yaml
services:
  smtp:
    volumes:
      - maildata:/maildir

volumes:
  maildata:
``` 