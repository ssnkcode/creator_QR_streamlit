import streamlit as st
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image, ImageDraw, ImageFilter
import io
import base64
import re

# Configuración de la página
st.set_page_config(
    page_title="Generador QR Pro",
    page_icon="🔲",
    layout="centered"
)

# Estilos CSS personalizados para un diseño minimalista
st.markdown("""
    <style>
        .stApp {
            max-width: 800px;
            margin: 0 auto;
        }
        .main-header {
            text-align: center;
            padding: 1rem 0;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            color: white;
            margin-bottom: 2rem;
        }
        .qr-container {
            display: flex;
            justify-content: center;
            margin: 1rem 0;
        }
        .stButton button {
            width: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: bold;
        }
        .download-btn {
            margin-top: 1rem;
        }
        .info-text {
            font-size: 0.9rem;
            color: #666;
            font-style: italic;
        }
    </style>
""", unsafe_allow_html=True)

def make_qr_circular(image, size):
    """Convierte una imagen a formato circular"""
    # Crear una máscara circular
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    
    # Aplicar la máscara a la imagen
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    circular_image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    circular_image.paste(image, (0, 0), mask)
    
    return circular_image

def generate_qr(data, logo_img=None, qr_size=280):
    """Genera el código QR con opción de logo"""
    # Crear el QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Crear imagen del QR con estilo
    img_qr = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=SolidFillColorMask(
            back_color=(255, 255, 255),
            front_color=(0, 0, 0)
        ),
        embeded_image_path=None
    )
    
    # Convertir a RGBA para trabajar con transparencia
    img_qr = img_qr.convert('RGBA')
    
    # Si hay logo, insertarlo en el centro
    if logo_img is not None:
        # Tamaño del logo (30% del QR)
        logo_size = int(img_qr.size[0] * 0.3)
        
        # Procesar el logo
        logo = Image.open(logo_img)
        
        # Redimensionar manteniendo relación de aspecto
        logo.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        # Crear fondo blanco para el logo
        logo_final = Image.new('RGBA', (logo_size, logo_size), (255, 255, 255, 255))
        
        # Posicionar el logo centrado
        x = (logo_size - logo.size[0]) // 2
        y = (logo_size - logo.size[1]) // 2
        logo_final.paste(logo, (x, y), logo if logo.mode == 'RGBA' else None)
        
        # Hacer el logo circular
        logo_final = make_qr_circular(logo_final, logo_size)
        
        # Posición para pegar en el QR
        pos = ((img_qr.size[0] - logo_size) // 2, (img_qr.size[1] - logo_size) // 2)
        
        # Pegar el logo en el QR
        img_qr.paste(logo_final, pos, logo_final)
    
    return img_qr

def is_valid_url(url):
    """Valida si una URL es válida"""
    pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return pattern.match(url) is not None

def get_credentials():
    """Devuelve usuario y contraseña desde st.secrets,
    con valores por defecto si no están configurados."""
    default_user = "usuario"
    default_pwd = "usuario321"
    try:
        user = st.secrets["login"]["usuario"]
        pwd = st.secrets["login"]["password"]
    except Exception:
        user = default_user
        pwd = default_pwd
    return user, pwd

def check_login():
    """Muestra el formulario de login y devuelve True si las credenciales son válidas."""
    st.markdown(
        '<div class="main-header"><h1>🔲 Generador QR Pro</h1>'
        '<p>Inicia sesión para continuar</p></div>',
        unsafe_allow_html=True
    )

    with st.container():
        st.markdown("### 🔐 Acceso restringido")
        st.markdown(
            "Esta aplicación requiere autenticación. Ingresa tus credenciales.",
            unsafe_allow_html=True
        )
        login_user = st.text_input("👤 Usuario:", key="login_user")
        login_pwd = st.text_input("🔑 Contraseña:", type="password", key="login_pwd")

        if st.button("🚀 Iniciar sesión", use_container_width=True):
            user, pwd = get_credentials()
            if login_user == user and login_pwd == pwd:
                st.session_state["autenticado"] = True
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")

    # Footer del login
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #666; font-size: 0.8rem;">'
        '© 2026 Todos los derechos reservados SSNKcode</p>',
        unsafe_allow_html=True
    )
    return False

def main():
    # Proteger la app con login
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False
    if not st.session_state["autenticado"]:
        check_login()
        return

    # Título principal
    st.markdown('<div class="main-header"><h1>🔲 Generador QR Pro</h1><p>Crea códigos QR profesionales con estilo</p></div>', unsafe_allow_html=True)
    
    # Sidebar para opciones
    with st.sidebar:
        st.markdown("### ⚙️ Configuración")
        qr_size = st.slider("Tamaño del QR", 200, 500, 280, step=20)
        st.markdown("---")
        st.markdown("### 📋 Tipos de QR")
        qr_type = st.radio(
            "Selecciona el tipo:",
            ["📝 Texto plano", "🌐 URL", "💬 WhatsApp", "📶 WiFi"],
            index=0
        )
        st.markdown("---")
        if st.button("🚪 Cerrar sesión"):
            st.session_state["autenticado"] = False
            st.rerun()
    
    # Área principal
    st.markdown("### 📝 Datos del código QR")
    
    # Entradas según el tipo seleccionado
    if qr_type == "📝 Texto plano":
        data = st.text_area("Escribe tu texto:", "¡Hola mundo!", height=100)
        st.caption("Ingresa cualquier texto que quieras codificar en el QR")
        
    elif qr_type == "🌐 URL":
        url = st.text_input("URL:", "https://www.ejemplo.com")
        if url and not is_valid_url(url):
            st.warning("⚠️ La URL no parece válida. Asegúrate de incluir http:// o https://")
        data = url
        
    elif qr_type == "💬 WhatsApp":
        col1, col2 = st.columns(2)
        with col1:
            phone = st.text_input("Número de teléfono:", "5491112345678")
        with col2:
            message = st.text_input("Mensaje (opcional):", "Hola, contacto desde el QR")
        if phone:
            clean_phone = re.sub(r'[^0-9]', '', phone)
            data = f"https://wa.me/{clean_phone}?text={message.replace(' ', '%20')}"
        else:
            data = ""
        st.caption("Formato: Código de país + número (ej: 5491112345678)")
        
    else:  # WiFi
        col1, col2 = st.columns(2)
        with col1:
            ssid = st.text_input("Nombre de la red (SSID):", "MiWiFi")
            password = st.text_input("Contraseña:", "contraseña123", type="password")
        with col2:
            encryption = st.selectbox("Tipo de seguridad:", ["WPA", "WEP", "nopass"])
            hidden = st.checkbox("Red oculta")
        data = f"WIFI:T:{encryption};S:{ssid};P:{password};{';H:true' if hidden else ''};"
        st.caption("Con esta opción, al escanear te conectarás automáticamente a la red")
    
    # Subida de imagen para el logo
    st.markdown("---")
    st.markdown("### 🖼️ Personalización")
    uploaded_file = st.file_uploader(
        "Sube una imagen o logo para el centro del QR (opcional)",
        type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
        help="La imagen se redimensionará automáticamente y se convertirá en circular"
    )
    
    # Botón para generar
    if st.button("🎯 Generar Código QR", use_container_width=True):
        if data:
            try:
                # Generar QR
                with st.spinner("Generando código QR..."):
                    if uploaded_file:
                        qr_img = generate_qr(data, uploaded_file, qr_size)
                    else:
                        qr_img = generate_qr(data, None, qr_size)
                
                # Mostrar el QR
                st.markdown("---")
                st.markdown("### ✅ Código QR generado")
                
                # Convertir a bytes para mostrar
                buf = io.BytesIO()
                qr_img.save(buf, format='PNG', quality=95)
                byte_im = buf.getvalue()
                
                # Mostrar imagen centrada
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(byte_im, use_container_width=True)
                
                # Botones de descarga
                col1, col2, col3 = st.columns(3)
                with col2:
                    st.download_button(
                        label="📥 Descargar QR",
                        data=byte_im,
                        file_name=f"codigo_qr.png",
                        mime="image/png",
                        use_container_width=True
                    )
                
                # Información adicional
                st.markdown("---")
                st.markdown(f"📌 **Tipo:** {qr_type}")
                st.markdown(f"📏 **Tamaño:** {qr_img.size[0]}x{qr_img.size[1]} píxeles")
                if uploaded_file:
                    st.markdown("✅ **Logo personalizado insertado** (circular y redimensionado automáticamente)")
                
            except Exception as e:
                st.error(f"❌ Error al generar el QR: {str(e)}")
        else:
            st.warning("⚠️ Por favor, ingresa los datos requeridos")
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #666; font-size: 0.8rem;">'
        '© 2026 Todos los derechos reservados SSNKcode</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

###############################
## Echo por Sasinka Cristian ##   
###############################