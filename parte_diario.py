import streamlit as st
import polars as pl
import gspread

# --- Configuración de la Página ---
# Usamos el layout ancho para que la tabla ocupe más espacio
st.set_page_config(layout="wide")

st.title("Reporte - Parte Diario (Método 1)")

# --- Configuración de Google Sheets ---
SERVICE_ACCOUNT_FILE = "dotacion-key.json"
GOOGLE_SHEET_IDENTIFIER = "DOTACION_GENERAL"
HOJA_CON_LA_TABLA = "Tabla dinámica 1"
# Rango exacto que quieres leer (incluyendo encabezados)
RANGO_A_LEER = "A2:D5" 

# --- CONEXIÓN GLOBAL A GOOGLE SHEETS ---
# (MOVIDA FUERA DE LA FUNCIÓN PARA SOLUCIONAR EL NameError)
try:
    gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
    sh = gc.open(GOOGLE_SHEET_IDENTIFIER)
except Exception as e:
    st.error(f"Error fatal al conectar con Google Sheets: {e}")
    # Detiene la app si no se puede conectar al inicio
    st.stop() 

# --- Cargar datos del rango ---
@st.cache_data(ttl=600) # Cachear por 10 minutos
def load_pivot_range(worksheet_name, range_name):
    """
    Se conecta a Google Sheets y lee solo el rango específico.
    AHORA USA LA CONEXIÓN GLOBAL 'sh'.
    """
    try:
        # Usa la variable global 'sh'
        worksheet = sh.worksheet(worksheet_name)
        
        # Leemos solo el rango específico
        data = worksheet.get_values(range_name)
        
        if not data:
            st.error(f"No se encontraron datos en el rango {range_name} de la hoja {worksheet_name}")
            return None
        
        # Convertir a Polars (la primera fila son los encabezados)
        df = pl.DataFrame(data[1:], schema=data[0], orient="row")
        return df

    except gspread.exceptions.WorksheetNotFound:
        st.error(f"Error: No se encontró la hoja llamada '{worksheet_name}'. Revisa el nombre.")
        return None
    except Exception as e:
        st.error(f"Ocurrió un error inesperado al cargar '{worksheet_name}': {e}")
        return None

# --- NUEVO: Botón de Recarga ---
if st.button("Recargar Datos"):
    # Limpia el caché de la función de carga
    load_pivot_range.clear()
    st.toast("Datos actualizados desde Google Sheets.", icon="🔄")

st.markdown("---")

# --- App ---
df_pivot = None
with st.spinner("Cargando datos desde Google Sheets..."):
    # Pasamos los argumentos a la función
    df_pivot = load_pivot_range(HOJA_CON_LA_TABLA, RANGO_A_LEER) 

if df_pivot is not None:
    st.header("Resumen de Escalafones")
    
    # Usamos 'width="stretch"' para que la tabla use todo el ancho disponible
    # y 'hide_index=True' para ocultar la columna de índices (0, 1, 2...)
    st.dataframe(df_pivot, hide_index=True, width='stretch')

# --- AÑADIR OTRA TABLA DINÁMICA AQUÍ ---
# Para agregar otra tabla, sigue los mismos pasos:
st.markdown("---")

# 1. Define la hoja y el rango
# (Asegúrate de cambiar estos nombres por los correctos)
HOJA_OTRA_TABLA = "Tabla dinámica 1" 
RANGO_OTRA_TABLA = "A8:D17"

# 2. Llama a la función de carga
# (Envuelto en try/except para que no falle si la hoja no existe)
try:
    df_2 = load_pivot_range(HOJA_OTRA_TABLA, RANGO_OTRA_TABLA)
    
    if df_2 is not None:
        # 4. Muéstrala
        st.header("OFICIALES")
        st.dataframe(df_2, hide_index=True, width='stretch')

except Exception as e:
    st.warning(f"No se pudo cargar la segunda tabla ({HOJA_OTRA_TABLA}): {e}")
# -----------------------------------------------

###############################################################################
# --- AÑADIR OTRA TABLA DINÁMICA AQUÍ ---
# Para agregar otra tabla, sigue los mismos pasos:
st.markdown("---")

# 1. Define la hoja y el rango
# (Asegúrate de cambiar estos nombres por los correctos)
HOJA_OTRA_TABLA = "Tabla dinámica 1" 
RANGO_SUBOFICIALES = "A8:D17"

# 2. Llama a la función de carga
# (Envuelto en try/except para que no falle si la hoja no existe)
try:
    df_2 = load_pivot_range(HOJA_OTRA_TABLA, RANGO_SUBOFICIALES)
    
    if df_2 is not None:
        # 4. Muéstrala
        st.header("SUBOFICIALES")
        st.dataframe(df_2, hide_index=True, width='stretch')

except Exception as e:
    st.warning(f"No se pudo cargar la segunda tabla ({HOJA_OTRA_TABLA}): {e}")
# -----------------------------------------------