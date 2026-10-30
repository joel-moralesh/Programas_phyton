import numpy as np
import plotly.graph_objects as go
import streamlit as st


# =========================================================
# 1. CONFIGURACIÓN GENERAL
# =========================================================

st.set_page_config(
    page_title="Laboratorio Matemático 3D",
    page_icon="📐",
    layout="wide"
)


# =========================================================
# 2. DISEÑO DE LA APLICACIÓN
# =========================================================

st.markdown(
    """
    <style>
        .stApp {
            background-color: #f5f8fc;
        }

        h1, h2, h3 {
            color: #12345a;
        }

        [data-testid="stSidebar"] {
            background-color: #eaf1fa;
        }

        div.stButton > button {
            background-color: #1769aa;
            color: white;
            border-radius: 8px;
            border: none;
            font-weight: bold;
        }

        div.stButton > button:hover {
            background-color: #0d4778;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 3. ENCABEZADO
# =========================================================

st.title("Laboratorio Matemático 3D")

st.markdown(
    """
    Aplicación interactiva para explorar curvas y superficies
    tridimensionales mediante parámetros matemáticos.
    """
)

st.divider()


# =========================================================
# 4. OPCIONES DISPONIBLES
# =========================================================

TIPOS_GRAFICOS = [
    "Circunferencia 3D",
    "Elipse 3D",
    "Esfera",
    "Elipsoide",
    "Toroide",
    "Cilindro",
    "Cono",
    "Paraboloide",
    "Silla de montar",
    "Hélice"
]

COLORES = [
    "blue",
    "red",
    "green",
    "orange",
    "purple",
    "black",
    "magenta",
    "cyan",
    "gold"
]

PALETAS = [
    "Viridis",
    "Plasma",
    "Inferno",
    "Magma",
    "Cividis",
    "Turbo",
    "Blues",
    "Rainbow"
]


# =========================================================
# 5. PANEL DE CONFIGURACIÓN
# =========================================================

with st.sidebar:

    st.header("Configuración")

    tipo = st.selectbox(
        "Selecciona el tipo de gráfico",
        TIPOS_GRAFICOS
    )

    st.subheader("Parámetros matemáticos")

    a = st.number_input(
        "Escala X (a)",
        min_value=0.1,
        max_value=20.0,
        value=2.0,
        step=0.1
    )

    b = st.number_input(
        "Escala Y (b)",
        min_value=0.1,
        max_value=20.0,
        value=1.5,
        step=0.1
    )

    c = st.number_input(
        "Escala Z / altura (c)",
        min_value=0.1,
        max_value=20.0,
        value=2.0,
        step=0.1
    )

    r = st.number_input(
        "Radio menor del toroide (r)",
        min_value=0.1,
        max_value=10.0,
        value=0.6,
        step=0.1
    )

    vueltas = st.number_input(
        "Vueltas de la hélice",
        min_value=0.5,
        max_value=20.0,
        value=3.0,
        step=0.5
    )

    resolucion = st.slider(
        "Resolución del gráfico",
        min_value=20,
        max_value=200,
        value=70,
        step=10
    )

    color = st.selectbox(
        "Color de las curvas",
        COLORES
    )

    paleta = st.selectbox(
        "Paleta de las superficies",
        PALETAS
    )

    opacidad = st.slider(
        "Opacidad de la superficie",
        min_value=0.1,
        max_value=1.0,
        value=0.85,
        step=0.05
    )

    st.caption(
        "Los gráficos se actualizan al modificar los parámetros."
    )


# =========================================================
# 6. GENERACIÓN DE LOS GRÁFICOS
# =========================================================

def crear_grafico():

    fig = go.Figure()

    n = resolucion

    # Parámetros angulares
    u = np.linspace(0, 2 * np.pi, n)
    v = np.linspace(0, np.pi, n)

    U, V = np.meshgrid(u, v)

    # -----------------------------------------------------
    # Función para dibujar superficies
    # -----------------------------------------------------

    def agregar_superficie(X, Y, Z):

        fig.add_trace(
            go.Surface(
                x=X,
                y=Y,
                z=Z,
                colorscale=paleta,
                opacity=opacidad,
                showscale=True,
                colorbar=dict(
                    title="Escala"
                )
            )
        )

    # -----------------------------------------------------
    # Función para dibujar curvas
    # -----------------------------------------------------

    def agregar_curva(X, Y, Z):

        fig.add_trace(
            go.Scatter3d(
                x=X,
                y=Y,
                z=Z,
                mode="lines",
                line=dict(
                    color=color,
                    width=6
                )
            )
        )

    # =====================================================
    # GRÁFICO 1: CIRCUNFERENCIA 3D
    # =====================================================

    if tipo == "Circunferencia 3D":

        t = np.linspace(0, 2 * np.pi, n * 3)

        X = a * np.cos(t)
        Y = a * np.sin(t)
        Z = 0.4 * c * np.sin(2 * t)

        agregar_curva(X, Y, Z)

    # =====================================================
    # GRÁFICO 2: ELIPSE 3D
    # =====================================================

    elif tipo == "Elipse 3D":

        t = np.linspace(0, 2 * np.pi, n * 3)

        X = a * np.cos(t)
        Y = b * np.sin(t)
        Z = 0.5 * c * np.sin(t)

        agregar_curva(X, Y, Z)

    # =====================================================
    # GRÁFICO 3: ESFERA
    # =====================================================

    elif tipo == "Esfera":

        X = a * np.cos(U) * np.sin(V)
        Y = a * np.sin(U) * np.sin(V)
        Z = a * np.cos(V)

        agregar_superficie(X, Y, Z)

    # =====================================================
    # GRÁFICO 4: ELIPSOIDE
    # =====================================================

    elif tipo == "Elipsoide":

        X = a * np.cos(U) * np.sin(V)
        Y = b * np.sin(U) * np.sin(V)
        Z = c * np.cos(V)

        agregar_superficie(X, Y, Z)

    # =====================================================
    # GRÁFICO 5: TOROIDE
    # =====================================================

    elif tipo == "Toroide":

        X = (a + r * np.cos(V)) * np.cos(U)
        Y = (a + r * np.cos(V)) * np.sin(U)
        Z = r * np.sin(V)

        agregar_superficie(X, Y, Z)

    # =====================================================
    # GRÁFICO 6: CILINDRO
    # =====================================================

    elif tipo == "Cilindro":

        theta = np.linspace(0, 2 * np.pi, n)
        altura = np.linspace(-c, c, n)

        T, Z = np.meshgrid(theta, altura)

        X = a * np.cos(T)
        Y = a * np.sin(T)

        agregar_superficie(X, Y, Z)

    # =====================================================
    # GRÁFICO 7: CONO
    # =====================================================

    elif tipo == "Cono":

        theta = np.linspace(0, 2 * np.pi, n)
        altura = np.linspace(0, c, n)

        T, Z = np.meshgrid(theta, altura)

        radio = a * (1 - Z / c)

        X = radio * np.cos(T)
        Y = radio * np.sin(T)

        agregar_superficie(X, Y, Z)

    # =====================================================
    # GRÁFICO 8: PARABOLOIDE
    # =====================================================

    elif tipo == "Paraboloide":

        x = np.linspace(-a, a, n)
        y = np.linspace(-b, b, n)

        X, Y = np.meshgrid(x, y)

        Z = c * (
            (X / a) ** 2 +
            (Y / b) ** 2
        )

        agregar_superficie(X, Y, Z)

    # =====================================================
    # GRÁFICO 9: SILLA DE MONTAR
    # =====================================================

    elif tipo == "Silla de montar":

        x = np.linspace(-a, a, n)
        y = np.linspace(-b, b, n)

        X, Y = np.meshgrid(x, y)

        Z = c * (
            (X / a) ** 2 -
            (Y / b) ** 2
        )

        agregar_superficie(X, Y, Z)

    # =====================================================
    # GRÁFICO 10: HÉLICE
    # =====================================================

    elif tipo == "Hélice":

        t = np.linspace(
            0,
            2 * np.pi * vueltas,
            n * 10
        )

        X = a * np.cos(t)
        Y = b * np.sin(t)
        Z = c * t / (2 * np.pi)

        agregar_curva(X, Y, Z)

    # =====================================================
    # 7. CONFIGURACIÓN DE LOS EJES Y LA VISTA
    # =====================================================

    fig.update_layout(
        title=dict(
            text=tipo,
            x=0.5,
            xanchor="center"
        ),

        scene=dict(
            xaxis_title="Eje X",
            yaxis_title="Eje Y",
            zaxis_title="Eje Z",
            aspectmode="data",
            bgcolor="#f5f8fc"
        ),

        paper_bgcolor="#ffffff",

        font=dict(
            color="#12345a",
            size=12
        ),

        margin=dict(
            l=0,
            r=0,
            t=60,
            b=0
        ),

        height=650
    )

    return fig


# =========================================================
# 8. MOSTRAR EL GRÁFICO
# =========================================================

try:

    figura = crear_grafico()

    st.plotly_chart(
        figura,
        use_container_width=True,
        config={
            "displaylogo": False,
            "responsive": True,
            "scrollZoom": True
        }
    )

except Exception as error:

    st.error(
        f"No se pudo generar el gráfico: {error}"
    )


# =========================================================
# 9. INFORMACIÓN MATEMÁTICA
# =========================================================

FORMULAS = {

    "Circunferencia 3D":
        "x = a cos(t), y = a sin(t), z = 0.4c sin(2t)",

    "Elipse 3D":
        "x = a cos(t), y = b sin(t), z = 0.5c sin(t)",

    "Esfera":
        "x = a cos(u) sin(v), y = a sin(u) sin(v), z = a cos(v)",

    "Elipsoide":
        "x = a cos(u) sin(v), y = b sin(u) sin(v), z = c cos(v)",

    "Toroide":
        "x = (a + r cos(v)) cos(u), "
        "y = (a + r cos(v)) sin(u), z = r sin(v)",

    "Cilindro":
        "x = a cos(t), y = a sin(t), -c <= z <= c",

    "Cono":
        "radio(z) = a(1 - z/c), 0 <= z <= c",

    "Paraboloide":
        "z = c[(x/a)^2 + (y/b)^2]",

    "Silla de montar":
        "z = c[(x/a)^2 - (y/b)^2]",

    "Hélice":
        "x = a cos(t), y = b sin(t), z = ct/(2*pi)"
}


# =========================================================
# 10. PANEL DE INFORMACIÓN
# =========================================================

st.divider()

st.subheader("Información del modelo matemático")

st.write(
    f"**Gráfico seleccionado:** {tipo}"
)

st.latex(
    FORMULAS[tipo]
)

st.markdown(
    """
    **Instrucciones de uso**

    - Utiliza el panel lateral para cambiar el tipo de gráfico.
    - Modifica los parámetros matemáticos para observar los cambios.
    - Gira el gráfico arrastrando con el ratón.
    - Acerca o aleja la vista con la rueda del ratón.
    - Cambia los colores y la resolución desde la configuración.
    """
)

st.caption(
    "Laboratorio Matemático 3D | Python, NumPy, Plotly y Streamlit"
)
