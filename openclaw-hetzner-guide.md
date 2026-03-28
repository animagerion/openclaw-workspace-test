# Guía Completa de Instalación de OpenClaw en VPS Hetzner

## Índice

1. [Introducción](#1-introducción)
2. [Requisitos previos](#2-requisitos-previos)
3. [Creación del VPS en Hetzner](#3-creación-del-vps-en-hetzner)
4. [Configuración inicial del VPS](#4-configuración-inicial-del-vps)
5. [Instalación de OpenClaw](#5-instalación-de-openclaw)
6. [Configuración de Telegram](#6-configuración-de-telegram)
7. [Configuración de MiniMax](#7-configuración-de-minimax)
8. [Configuración de Google Workspace](#8-configuración-de-google-workspace)
9. [Configuración de OpenClaw](#9-configuración-de-openclaw)
10. [Primeros pasos](#10-primeros-pasos)
11. [Mantenimiento](#11-mantenimiento)
12. [Resolución de problemas comunes](#12-resolución-de-problemas-comunes)

---

## 1. Introducción

### 1.1 ¿Qué es OpenClaw?

OpenClaw es una plataforma de agentes de inteligencia artificial de código abierto que te permite ejecutar un asistente personal completamente configurable en tu propio servidor. A diferencia de otros agentes que funcionan en la nube de terceros, OpenClaw se ejecuta en tu infraestructura, lo que significa:

- **Control total** sobre tus datos y conversaciones
- **Privacidad garantizada** — nada se almacena en servidores externos
- **Flexibilidad total** para personalizar plugins, integraciones y modelos
- **Coste predecible** — pagas solo tu servidor, sin sorpresas

### 1.2 ¿Por qué esta configuración?

Esta guía documenta una configuración probada y optimizada que combina las mejores herramientas disponibles:

| Componente | Elección | Motivo |
|------------|----------|--------|
| Servidor | **Hetzner VPS** | Excelente relación precio/rendimiento, servidores en Europa |
| Modelo IA | **MiniMax M2.7** | Potente, económico, contexto amplio |
| Mensajería | **Telegram** | Fiable, gratuito, API sencilla |
| Productividad | **Google Workspace** | Gmail, Calendar, Drive, Docs integrados |
| Plataforma | **OpenClaw** | Flexible, extensible, open source |

### 1.3 Coste aproximado mensual

| Servicio | Coste |
|----------|-------|
| VPS Hetzner CX11 (Ubuntu) | ~$5-10/mes |
| MiniMax (plan de uso) | $5-20/mes según uso |
| Telegram Bot | Gratuito |
| Google Workspace | Cuenta personal gratuita |
| **Total** | **~$10-30/mes** |

> **Nota:** El plan CX11 de Hetzner (~$5/mes) es suficiente para empezar. Si necesitas más potencia, el CX21 (~$10/mes) ofrece el doble de recursos.

---

## 2. Requisitos previos

Antes de comenzar, necesitas tener preparadas las siguientes cuentas y herramientas:

### 2.1 Cuenta en Hetzner Cloud

1. Ve a **[console.hetzner.cloud](https://console.hetzner.cloud)**
2. Regístrate con tu email y contraseña
3. Verifica tu cuenta (recibes un email de confirmación)
4. **Importante:** Añade un método de pago (tarjeta de crédito/débito o PayPal)
5. Añade un proyecto nuevo llamado "openclaw"

**Costes:** Solo se factura por los recursos que uses. Puedes cancelar en cualquier momento.

### 2.2 Cuenta en MiniMax

1. Visita **[platform.minimax.io](https://platform.minimax.io)**
2. Regístrate con Google o email
3. Accede al panel de control
4. En "Billing" → "Overview", revisa los planes disponibles
5. El **plan de pago por uso** es el más recomendable para empezar

**Coste típico:** ~$5-15/mes según el volumen de conversaciones.

### 2.3 Bot de Telegram

Necesitarás crear un bot de Telegram para comunicarte con tu agente:

1. Abre Telegram y busca **@BotFather**
2. Envía el comando `/newbot`
3. Sigue las instrucciones:
   - Nombre del bot (ej: "Mi Asistente IA")
   - Username del bot (ej: `miasistenteia_bot`) — debe terminar en `_bot`
4. BotFather te dará un **token API** — **guárdalo bien**, lo necesitarás más adelante

**Ejemplo del token recibido:**
```
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789
```

> ⚠️ **Advertencia:** Nunca compartas este token públicamente. Es la clave de acceso a tu bot.

### 2.4 Cuenta de Google

Necesitas una cuenta de Google para las integraciones de Workspace. Puede ser:

- Tu cuenta personal de Gmail (gratuita)
- Una cuenta de Google Workspace (de pago)

**Recomendación:** Usa una cuenta dedicada para el agente, separada de tu cuenta personal principal.

### 2.5 Herramientas necesarias en tu ordenador

| Herramienta | Propósito | Instalación |
|-------------|-----------|-------------|
| **Terminal** | Ejecutar comandos SSH | Ya viene con macOS/Linux; usa PowerShell en Windows |
| **SSH** | Conectar al VPS | macOS/Linux ya lo tienen; en Windows instala [OpenSSH](https://docs.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse) |
| **Git** | Control de versiones (opcional) | `sudo apt install git` en Ubuntu |

---

## 3. Creación del VPS en Hetzner

### 3.1 Acceder a la consola de Hetzner

1. Abre tu navegador y ve a **[console.hetzner.cloud](https://console.hetzner.cloud)**
2. Inicia sesión con tus credenciales
3. Verás el panel de control principal

### 3.2 Crear un nuevo proyecto

Si es la primera vez que usas Hetzner, ya tendrás un proyecto "Default". Te recomendamos crear uno específico:

1. Haz clic en **"New Project"**
2. Nombre: `openclaw` (o el nombre que prefieras)
3. Opcional: Añade una descripción
4. Haz clic en **"Create project"**

### 3.3 Crear el servidor (VPS)

1. Dentro de tu proyecto, haz clic en **"Add Server"**

2. **Selecciona la ubicación:**
   - Elige el datacenter más cercano a ti (por ejemplo, `Nuremberg (nbg1)` para España)
   - Todas las ubicaciones tienen buena latencia desde Europa

3. **Selecciona el sistema operativo:**
   - Elige **Ubuntu 22.04 LTS** (o 24.04 LTS si está disponible)
   - Ubuntu Server LTS es la opción más compatible y documentada

4. **Selecciona el tipo de servidor:**
   - **CX11** (1 vCPU, 2 GB RAM) — `$3.49/mes` — Recomendado para empezar
   - **CX21** (2 vCPU, 4 GB RAM) — `$5.99/mes` — Si necesitas más potencia

5. **Configura las opciones adicionales:**
   - ✅ **Enable backups** (opcional, ~20% del coste) — Recomendado
   - ❌ Private network (no necesario para esta configuración)
   - ✅ **Placement group** (opcional)

6. **Añade tu clave SSH:**
   - Si no tienes una, genera una nueva:
   
   ```bash
   # En tu ordenador local, genera una clave SSH
   ssh-keygen -t ed25519 -C "mi-openclaw-vps"
   
   # Copia la clave pública
   cat ~/.ssh/id_ed25519.pub
   ```
   
   - En Hetzner, haz clic en **"Add SSH Key"**
   - Dale un nombre (ej: "Mi portatil")
   - Pega la clave pública en el campo correspondiente

7. **Nombre del servidor:**
   - Escribe `openclaw` o el nombre que prefieras

8. **Crear el servidor:**
   - Haz clic en **"Create & Buy now"**
   - En segundos tendrás tu VPS funcionando

### 3.4 Anotar los datos del servidor

Una vez creado, anota esta información (la verás en el panel):

```
IP del servidor: 123.456.78.90
Nombre: openclaw
Estado: Running
```

> 📝 **Guarda estos datos:** La IP pública es lo que necesitarás para conectar por SSH.

---

## 4. Configuración inicial del VPS

### 4.1 Conectar al servidor por SSH

Abre tu terminal y conecta:

```bash
ssh root@123.456.78.90
```

(Reemplaza `123.456.78.90` con la IP de tu servidor)

La primera vez que te conectes, te preguntará si confías en la clave del servidor:

```
The authenticity of host '123.456.78.90' can't be established.
ECDSA key fingerprint is SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.
Are you sure you want to continue connecting (yes/no)?
```

Escribe `yes` y pulsa Enter.

### 4.2 Crear un usuario no-root (recomendado)

Nunca uses `root` directamente por seguridad. Crea un usuario con privilegios:

```bash
# Crear usuario (reemplaza "gerion" por el nombre que quieras)
adduser gerion

# Añadir al grupo sudo
usermod -aG sudo gerion

# Crear directorio .ssh para el usuario
mkdir -p /home/gerion/.ssh

# Copiar tu clave pública SSH al nuevo usuario
cp /root/.ssh/authorized_keys /home/gerion/.ssh/authorized_keys

# Asignar permisos correctos
chmod 700 /home/gerion/.ssh
chmod 644 /home/gerion/.ssh/authorized_keys
chown -R gerion:gerion /home/gerion/.ssh
```

### 4.3 Configurar SSH para mayor seguridad

Edita la configuración SSH:

```bash
nano /etc/ssh/sshd_config
```

Modifica o añade estas líneas:

```
Port 22                    # Puerto por defecto (puedes cambiarlo)
PermitRootLogin no         # NO permitir login como root
PasswordAuthentication no  # NO permitir login con contraseña
PubkeyAuthentication yes   # SÍ permitir login con clave SSH
MaxAuthTries 3             # Máximo 3 intentos fallidos
```

```bash
# Reiniciar el servicio SSH para aplicar cambios
systemctl restart sshd
```

> ⚠️ **Importante:** Antes de cerrar la sesión, verifica que puedes conectar con el nuevo usuario en otra terminal.

### 4.4 Configurar el firewall (UFW)

Ubuntu viene con UFW (Uncomplicated Firewall). Configúralo:

```bash
# Permitir SSH (si usas puerto 22)
ufw allow 22/tcp

# Permitir HTTP y HTTPS (para futuras webhooks)
ufw allow 80/tcp
ufw allow 443/tcp

# Habilitar el firewall
ufw enable

# Verificar estado
ufw status verbose
```

Deberías ver algo como:

```
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
443/tcp                    ALLOW       Anywhere
```

### 4.5 Actualizar el sistema

Siempre empieza actualizando todo:

```bash
apt update && apt upgrade -y
```

### 4.6 Instalar dependencias básicas

```bash
apt install -y curl wget git unzip zip
```

---

## 5. Instalación de OpenClaw

### 5.1 Método oficial de instalación

OpenClaw ofrece un script de instalación automático. Conéctate como tu usuario no-root y ejecuta:

```bash
# Conectar como usuario no-root
ssh gerion@123.456.78.90

# Instalar OpenClaw (comando oficial)
curl -fsSL https://raw.githubusercontent.com/stevenwardware/openclaw/main/install.sh | bash
```

Durante la instalación, el script puede pedirte:

- **Ubicación de instalación:** Pulsa Enter para aceptar la ubicación por defecto (`~/.openclaw`)
- **¿Iniciar el servicio?** Responde `yes`

### 5.2 Verificar la instalación

```bash
# Verificar que OpenClaw está instalado
openclaw --version

# Ver el estado del servicio
openclaw gateway status
```

Si el servicio está corriendo, deberías ver algo como:

```
✅ Gateway running on http://localhost:18789
```

### 5.3 Archivos de configuración principales

OpenClaw crea la siguiente estructura:

```
~/.openclaw/
├── config.yaml          # Configuración principal
├── plugins/             # Plugins instalados
├── skills/              # Skills personalizados
├── workspace/           # Directorio de trabajo
└── data/                # Datos y logs
```

---

## 6. Configuración de Telegram

### 6.1 Obtener el token de tu bot

Si no lo has hecho ya al crear el bot en el paso 2.3, aquí te recuerdo cómo recuperarlo:

1. Abre Telegram y busca **@BotFather**
2. Envía `/mybots`
3. Selecciona tu bot
4. Haz clic en **API Token** para ver/copiar tu token

El token tiene este formato:
```
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789
```

### 6.2 Configurar el webhook de Telegram

Para que tu bot reciba mensajes, necesitas configurar un webhook que apunte a tu servidor:

```bash
# Reemplaza TOKEN y IP con tus datos
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook" \
  -d "url=https://<TU_DOMINIO_O_IP>/webhook/telegram"
```

> 📝 **Nota:** Si no tienes un dominio, puedes usar la IP pública directamente, pero Telegram requiere HTTPS. Más adelante configuraremos esto con un certificado gratuito (Let's Encrypt) o un túnel reversed.

### 6.3 Alternativa: Usar ngrok para pruebas (sin dominio)

Si estás probando y no tienes dominio, usa ngrok para crear un túnel HTTPS:

```bash
# Instalar ngrok
curl -fsSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok

# Autenticar (necesitas cuenta gratuita en ngrok.com)
ngrok config add-authtoken <TU_TOKEN>

# Crear túnel HTTPS en el puerto de OpenClaw (por defecto 18789)
ngrok http 18789
```

Ngrok te dará una URL HTTPS como `https://xxxx-xx-xx.ngrok.io`. Usa esa URL para el webhook.

### 6.4 Configurar Telegram en OpenClaw

Edita el archivo `config.yaml`:

```bash
nano ~/.openclaw/config.yaml
```

Añade o modifica la sección de Telegram:

```yaml
channels:
  telegram:
    enabled: true
    botToken: "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789"
    webhookSecret: "mi_secreto_telegram_2024"  # Una cadena aleatoria
```

### 6.5 Probar el bot

Envía un mensaje a tu bot desde Telegram. Deberías recibir una respuesta automática confirmando que el webhook está funcionando.

---

## 7. Configuración de MiniMax

### 7.1 Alta en MiniMax

1. Ve a **[platform.minimax.io](https://platform.minimax.io)**
2. Regístrate o inicia sesión
3. Completa el proceso de verificación si es necesario

### 7.2 Obtener tu API Key

1. En el panel, ve a **"API Keys"** o **"Settings"** → **"API Keys"**
2. Haz clic en **"Create New API Key"**
3. Dale un nombre descriptivo (ej: "OpenClaw VPS")
4. **Copia y guarda la API key** — solo se muestra una vez

La API key tiene este formato:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

> ⚠️ **Advertencia:** Guarda esta clave en un lugar seguro. Si la pierdes, tendrás que crear otra.

### 7.3 Verificar el modelo disponible

En el panel de MiniMax, revisa:

1. **Models** — Revisa qué modelos tienes disponibles (generalmente MiniMax-Text-01 o similar)
2. **Usage** — Monitorea tu uso para evitar sorpresas en la factura
3. **Billing** — Configura alertas de gasto si es posible

### 7.4 Configurar MiniMax en OpenClaw

Edita el archivo `config.yaml`:

```bash
nano ~/.openclaw/config.yaml
```

Añade o modifica la sección de modelos:

```yaml
models:
  default: minimax
  providers:
    minimax:
      apiKey: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
      model: "MiniMax-Text-01"
      maxTokens: 8192
      temperature: 0.7
```

---

## 8. Configuración de Google Workspace

### 8.1 Instalar gogcli

**gogcli** es la herramienta de línea de comandos para Google Workspace. Instálala en tu VPS:

```bash
# Instalar con Homebrew (si tienes brew)
brew install steipete/tap/gogcli

# O descargar el binario directamente (Linux arm64)
curl -fsSL https://github.com/steipete/gogcli/releases/latest/download/gogcli-linux-arm64.tar.gz | tar -xz -C /usr/local/bin

# Verificar instalación
gog --version
```

### 8.2 Configurar autenticación de Google

Necesitas crear un proyecto en Google Cloud Console y obtener credenciales OAuth:

1. Ve a **[console.cloud.google.com](https://console.cloud.google.com)**
2. Selecciona o crea un nuevo proyecto
3. Ve a **APIs y servicios** → **Biblioteca**
4. Activa estas APIs:
   - Gmail API
   - Google Calendar API
   - Google Drive API
   - Google Docs API
   - Google Sheets API
   - People API

5. Ve a **APIs y servicios** → **Credenciales**
6. Haz clic en **Crear credenciales** → **ID de cliente OAuth 2.0**
7. Tipo de aplicación: **App de escritorio**
8. Descarga el archivo `client_secret.json`

### 8.3 Autenticar con gogcli

```bash
# Configurar credenciales
gog auth credentials /ruta/a/client_secret.json

# Añadir tu cuenta Google
gog auth add animagerion@gmail.com \
  --services gmail,calendar,drive,contacts,docs,sheets

# Verificar que está autenticado
gog auth list
```

### 8.4 Probar las integraciones

```bash
# Probar Gmail
gog gmail search "newer_than:1d" --max 5

# Probar Calendar
gog calendar events primary --from 2024-01-01 --to 2024-01-07
```

### 8.5 Configurar Google en OpenClaw

Edita el archivo `config.yaml`:

```yaml
plugins:
  google-workspace:
    enabled: true
    credentialsPath: "/home/gerion/.config/gog/credentials.json"
    account: "animagerion@gmail.com"
```

---

## 9. Configuración de OpenClaw

### 9.1 Estructura del archivo config.yaml

El archivo de configuración principal es `~/.openclaw/config.yaml`. Aquí tienes una configuración completa de ejemplo:

```yaml
# ============================================
# CONFIGURACIÓN PRINCIPAL DE OPENCLAW
# ============================================

# Nombre de tu agente
agent:
  name: "Gerion"
  owner: "Paduel"
  timezone: "Europe/Madrid"

# Modelos
models:
  default: minimax
  providers:
    minimax:
      apiKey: "TU_API_KEY_MINIMAX"
      model: "MiniMax-Text-01"
      maxTokens: 8192
      temperature: 0.7

# Canales de comunicación
channels:
  telegram:
    enabled: true
    botToken: "TU_TOKEN_TELEGRAM"
    webhookSecret: "tu_secreto_aleatorio"
    allowedUsers:
      - "tu_user_id_de_telegram"  # Tu ID de Telegram (obténlo de @userinfobot)

# Integraciones
plugins:
  google-workspace:
    enabled: true
    credentialsPath: "/home/gerion/.config/gog/credentials.json"
    account: "animagerion@gmail.com"

# Configuración del servidor
server:
  host: "0.0.0.0"
  port: 18789
  https:
    enabled: true
    certPath: "/etc/letsencrypt/fullchain.pem"
    keyPath: "/etc/letsencrypt/privkey.pem"

# Logging
logging:
  level: "info"
  file: "/home/gerion/.openclaw/logs/openclaw.log"
```

### 9.2 Obtener tu ID de Telegram

Para restringir el acceso a tu bot solo a ti:

1. Abre Telegram y busca **@userinfobot**
2. Envía `/start`
3. Te responderá con tu **Telegram ID** (un número largo como `123456789`)

### 9.3 Instalar un certificado SSL (Let's Encrypt)

Para que Telegram funcione con HTTPS:

```bash
# Instalar Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtener certificado (reemplaza con tu dominio o IP)
sudo certbot certonly --standalone -d tu-dominio.com

# Los certificados se guardan en:
# /etc/letsencrypt/live/tu-dominio.com/
```

### 9.4 Habilitar y reiniciar el servicio

```bash
# Habilitar inicio automático
sudo systemctl enable openclaw

# Reiniciar con la nueva configuración
sudo systemctl restart openclaw

# Ver logs
sudo journalctl -u openclaw -f
```

---

## 10. Primeros pasos

### 10.1 Comandos básicos de OpenClaw

```bash
# Ver estado del gateway
openclaw gateway status

# Iniciar el gateway
openclaw gateway start

# Detener el gateway
openclaw gateway stop

# Reiniciar el gateway
openclaw gateway restart

# Ver logs en tiempo real
openclaw logs -f

# Ver versión
openclaw --version
```

### 10.2 Usar el bot desde Telegram

Una vez configurado, abre Telegram y envía mensajes a tu bot:

| Comando | Descripción |
|---------|-------------|
| `/start` | Iniciar conversación |
| `/help` | Ver ayuda |
| `/status` | Estado del agente |
| `/memory` | Ver memorias guardadas |
| `/model` | Ver modelo en uso |

### 10.3 Tu primera interacción

Prueba con algo simple:

```
¡Hola! Preséntate brevemente.
```

Deberías recibir una respuesta de tu agente en segundos.

### 10.4 Configurar skills personalizados

Los skills extienden las capacidades de tu agente. Están en `~/.openclaw/skills/`:

```bash
# Ver skills disponibles
ls ~/.openclaw/skills/

# Instalar un skill (ejemplo)
openclaw skills install https://github.com/usuario/skill-repo
```

---

## 11. Mantenimiento

### 11.1 Actualizaciones de OpenClaw

```bash
# Actualizar OpenClaw a la última versión
openclaw update

# O manualmente
curl -fsSL https://raw.githubusercontent.com/stevenwardware/openclaw/main/install.sh | bash
```

### 11.2 Actualizaciones del sistema

```bash
# Actualizar todos los paquetes
sudo apt update && sudo apt upgrade -y

# Limpiar paquetes innecesarios
sudo apt autoremove -y
```

### 11.3 Backup de configuración

Es crucial hacer copias de seguridad periódicas:

```bash
# Crear directorio de backups
mkdir -p ~/backups

# Backup de configuración
tar -czvf ~/backups/openclaw-config-$(date +%Y%m%d).tar.gz \
  ~/.openclaw/config.yaml \
  ~/.openclaw/skills/ \
  ~/.config/gog/

# Backup de la base de datos de agentes (si existe)
tar -czvf ~/backups/openclaw-data-$(date +%Y%m%d).tar.gz \
  ~/.openclaw/data/
```

### 11.4 Restaurar desde backup

```bash
# Extraer configuración
tar -xzvf ~/backups/openclaw-config-20240101.tar.gz -C ~/

# Restaurar datos
tar -xzvf ~/backups/openclaw-data-20240101.tar.gz -C ~/
```

### 11.5 Monitorización básica

```bash
# Uso de recursos del servidor
htop

# Espacio en disco
df -h

# Uso de memoria
free -h

# Ver logs de OpenClaw
tail -f ~/.openclaw/logs/openclaw.log

# Ver logs del sistema
sudo journalctl -u openclaw -n 50
```

### 11.6 Automatizar backups con cron

Edita el crontab:

```bash
crontab -e
```

Añade esta línea para hacer backup diario a las 3 AM:

```
0 3 * * * tar -czvf /home/gerion/backups/openclaw-config-$(date +\%Y\%m\%d).tar.gz ~/.openclaw/config.yaml ~/.openclaw/skills/ ~/.config/gog/ 2>/dev/null
```

---

## 12. Resolución de problemas comunes

### 12.1 El bot de Telegram no responde

**Causas posibles y soluciones:**

1. **Webhook no configurado:**
   ```bash
   # Verificar webhook actual
   curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo
   ```

2. **El servicio no está corriendo:**
   ```bash
   openclaw gateway status
   sudo systemctl status openclaw
   ```

3. **Token incorrecto en config.yaml:**
   Verifica que el token en `config.yaml` coincide exactamente con el de BotFather.

### 12.2 Error "Connection refused" al conectar

**Solución:**
```bash
# Verificar que el puerto está abierto
sudo ufw status

# Abrir el puerto si es necesario
sudo ufw allow 18789/tcp

# Verificar que OpenClaw está escuchando
ss -tlnp | grep 18789
```

### 12.3 Error de autenticación con Google

**Solución:**
```bash
# Re-autenticar gogcli
gog auth list
# Si no aparece tu cuenta, vuelve a autenticar:
gog auth add animagerion@gmail.com --services gmail,calendar,drive,docs,sheets
```

### 12.4 MiniMax API returns 401 Unauthorized

**Causa:** La API key ha expirado o es incorrecta.

**Solución:**
1. Ve a [platform.minimax.io](https://platform.minimax.io)
2. Genera una nueva API key
3. Actualiza `config.yaml`
4. Reinicia el servicio

### 12.5 Alto consumo de memoria / servidor lento

**Solución:**
```bash
# Ver qué está consumiendo memoria
htop

# Reducir uso de OpenClaw
# En config.yaml, reduce maxTokens:
maxTokens: 4096  # en lugar de 8192
```

### 12.6 El servidor no arranca tras reiniciar

**Solución:**
```bash
# Verificar que está habilitado
sudo systemctl enable openclaw

# Arrancar manualmente
sudo systemctl start openclaw

# Ver errores
sudo journalctl -u openclaw -n 100
```

### 12.7 Problemas con ngrok (webhook caótico)

Si usas ngrok y el webhook deja de funcionar:

1. Cada vez que reinicies ngrok, obtienes una URL nueva
2. Actualiza el webhook con la nueva URL:
   ```bash
   curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook" -d "url=https://nueva-url.ngrok.io/webhook/telegram"
   ```

### 12.8 SSL Certificate expired

**Solución:**
```bash
# Renovar certificado Let's Encrypt
sudo certbot renew

# Reiniciar OpenClaw
sudo systemctl restart openclaw
```

---

## Apéndice: Quick Reference Card

### Comandos esenciales

| Acción | Comando |
|--------|---------|
| Conectar por SSH | `ssh gerion@123.456.78.90` |
| Estado de OpenClaw | `openclaw gateway status` |
| Reiniciar servicio | `sudo systemctl restart openclaw` |
| Ver logs | `tail -f ~/.openclaw/logs/openclaw.log` |
| Actualizar sistema | `sudo apt update && sudo apt upgrade -y` |
| Actualizar OpenClaw | `openclaw update` |
| Hacer backup | `tar -czvf backup.tar.gz ~/.openclaw/` |

### URLs importantes

| Servicio | URL |
|----------|-----|
| Panel Hetzner | [console.hetzner.cloud](https://console.hetzner.cloud) |
| MiniMax Platform | [platform.minimax.io](https://platform.minimax.io) |
| BotFather Telegram | [@BotFather](https://t.me/BotFather) |
| Google Cloud Console | [console.cloud.google.com](https://console.cloud.google.com) |
| Docs OpenClaw | [openclaw.io/docs](https://openclaw.io/docs) |

---

*Documento creado el 28 de marzo de 2026*
*Configuración: VPS Hetzner + Ubuntu + OpenClaw + MiniMax M2.7 + Telegram + Google Workspace*
