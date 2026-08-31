# Generador QR Pro

Generador de codigos QR profesionales con estilo, construido con Streamlit. Permite crear codigos QR personalizados con logos incrustados, diferentes tipos de contenido y disenio atractivo.

## Caracteristicas

- **4 tipos de QR:**
  - Texto plano
  - URL con validacion
  - WhatsApp (genera enlace `wa.me` directo)
  - WiFi (conexion automatica al escanear)
- **Logo personalizado:** Sube una imagen y se inserta automaticamente en el centro del QR con forma circular
- **Tamaño configurable:** Slider para ajustar entre 200 y 500 pixeles
- **Estilo visual:** Modulos redondeados y colores personalizables
- **Descarga directa:** Boton para descargar el QR como archivo PNG

## Requisitos

- Python 3.10 o superior
- pip

## Instalacion

```bash
# Clonar el repositorio
git clone https://github.com/TU_USUARIO/generador_QR_Streamlit.git
cd generador_QR_Streamlit

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

```bash
streamlit run qr_generator.py
```

La aplicacion se abrira en el navegador en `http://localhost:8501`.

### Tipos de QR

| Tipo | Descripcion |
|------|-------------|
| Texto plano | Cualquier texto libre |
| URL | Enlace web con validacion automatica |
| WhatsApp | Numero de telefono + mensaje opcional, genera enlace `wa.me` |
| WiFi | SSID, contraseña y tipo de encriptacion (WPA/WEP/abierta) |

## Estructura del proyecto

```
generador_QR_Streamlit/
├── qr_generator.py      # Aplicacion principal
├── requirements.txt     # Dependencias de Python
├── README.md            # Este archivo
└── .gitignore           # Archivos ignorados por Git
```

## Dependencias principales

| Paquete | Uso |
|---------|-----|
| `streamlit` | Framework web para la interfaz |
| `qrcode` | Generacion de codigos QR con estilos |
| `Pillow` | Manipulacion de imagenes y logos |

## Autor

**Sasinka Cristian**

## Version

1.0

## Licencia

Este proyecto es de uso libre.
