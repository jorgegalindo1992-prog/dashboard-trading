import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILO NEÓN
# ---------------------------------------------------------
st.set_page_config(
    page_title="Trading Bot Dashboard",
    page_icon="🤖",
    layout="wide"
)

# Estilos CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0e14;
        color: #e6edf3;
    }
    button[data-baseweb="tab"] {
        color: #8b949e !important;
        background-color: transparent !important;
        font-weight: 600;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #00e676 !important;
        border-bottom-color: #00e676 !important;
    }
    div[data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.4);
    }
    div[data-testid="stMetricLabel"] {
        color: #8b949e !important;
        font-size: 0.85rem;
    }
    div[data-testid="stMetricValue"] {
        color: #00e676 !important;
        font-family: 'Courier New', monospace;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 BOT OPCIONES - DASHBOARD")

tab_bot, tab_mercado = st.tabs(["📊 ESTADO DEL BOT", "🌍 ROTACIÓN DE MERCADO"])

# ---------------------------------------------------------
# PESTAÑA 1: Estado del Bot
# ---------------------------------------------------------
with tab_bot:
    st.subheader("Resumen General de Operativa")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("GANANCIA DEL DÍA", "$ 18.430,00", "+ 8,72%")
    c2.metric("GANANCIA DEL MES", "$ 156.750,00", "+ 31,35%")
    c3.metric("GANANCIA TOTAL", "$ 278.940,00", "+ 55,78%")
    c4.metric("OPERACIONES HOY", "7", "5 ganadas / 2 perdidas")
    c5.metric("% ACIERTO (WINRATE)", "71.43%", "Alto rendimiento")
    
    st.info("💡 La conexión con la base de datos `trading.db` leerá automáticamente estos valores cuando tu bot ejecute operaciones.")

# ---------------------------------------------------------
# PESTAÑA 2: Rotación de Mercado + Matriz
# ---------------------------------------------------------
with tab_mercado:
    
    # --- SECCIÓN 1: FINVIZ MAPA DE CALOR S&P 500 ---
    st.markdown("### 🗺️ Mapa de Calor del Mercado EE.UU. (Finviz S&P 500)")
    
    col_btn, col_img = st.columns([1, 4])
    with col_btn:
        st.write("Visita la versión interactiva completa:")
        st.link_button("🔥 Abrir Finviz Map", "https://finviz.com/map.ashx?t=sec", type="primary")
    
    # Vista estática o integración mediante gráfico alternativo
    st.image("https://charts2.finviz.com/chart.ashx?t=SPY&ty=c&ta=0&p=d&s=l", caption="Vista de referencia S&P 500 (SPY)", width=600)

    st.markdown("---")

    # --- SECCIÓN 2: MATRIZ DE ESTILO (3x3) ---
    st.markdown("### 📊 US Equity Factors (1-Day Performance)")
    
    etfs_matriz = {
        'Large': {'Value': 'IVE', 'Core': 'IVV', 'Growth': 'IVW'},
        'Mid':   {'Value': 'IJJ', 'Core': 'IJH', 'Growth': 'IJK'},
        'Small': {'Value': 'IJS', 'Core': 'IJR', 'Growth': 'IJT'}
    }
    
    tickers_list = [etfs_matriz[r][c] for r in etfs_matriz for c in etfs_matriz[r]]
    
    try:
        data_matrix = yf.download(tickers_list, period='2d')['Close']
        cambio_pct = ((data_matrix.iloc[-1] - data_matrix.iloc[-2]) / data_matrix.iloc[-2]) * 100
        
        filas = ['Large', 'Mid', 'Small']
        columnas = ['Value', 'Core', 'Growth']
        
        matriz_valores = []
        matriz_texto = []
        
        for r in filas:
            v_fila = []
            t_fila = []
            for c in columnas:
                ticker = etfs_matriz[r][c]
                val = cambio_pct[ticker]
                v_fila.append(val)
                t_fila.append(f"{val:+.1f}%")
            matriz_valores.append(v_fila)
            matriz_texto.append(t_fila)

        fig_matrix = go.Figure(data=go.Heatmap(
            z=matriz_valores,
            x=columnas,
            y=filas,
            text=matriz_texto,
            texttemplate="%{text}",
            textfont={"size": 16, "color": "white", "family": "Arial Black"},
            colorscale=[
                [0.0, "#b71c1c"],   # Rojo oscuro
                [0.5, "#212121"],   # Fondo neutro
                [1.0, "#1b5e20"]    # Verde oscuro
            ],
            showscale=False
        ))

        fig_matrix.update_layout(
            template="plotly_dark",
            paper_bgcolor="#161b22",
            plot_bgcolor="#161b22",
            height=320,
            width=450,
            margin=dict(l=40, r=40, t=30, b=40)
        )
        
        st.plotly_chart(fig_matrix, use_container_width=False)
        
    except Exception as e:
        st.error(f"Error al calcular la matriz de factores: {e}")

    st.markdown("---")

    # --- SECCIÓN 3: TENDENCIA TEMPORAL VALUE vs GROWTH ---
    st.markdown("### 📈 Tendencia de Mediano Plazo")
    periodo = st.selectbox("Temporalidad del análisis", ["1mo", "3mo", "6mo", "1y"], index=1)
    
    try:
        datos = yf.download(["VUG", "VTV"], period=periodo)['Close']
        norm = (datos / datos.iloc[0]) * 100
        ratio = datos['VUG'] / datos['VTV']
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("##### Rendimiento Comparativo (%)")
            fig_comp = go.Figure()
            fig_comp.add_trace(go.Scatter(x=norm.index, y=norm['VUG'], name='Growth (VUG)', line=dict(color='#00e676', width=2)))
            fig_comp.add_trace(go.Scatter(x=norm.index, y=norm['VTV'], name='Value (VTV)', line=dict(color='#ff5252', width=2)))
            fig_comp.update_layout(
                template="plotly_dark",
                paper_bgcolor="#161b22",
                plot_bgcolor="#0b0e14",
                margin=dict(l=20, r=20, t=30, b=20),
                height=350
            )
            st.plotly_chart(fig_comp, use_container_width=True)
            
        with col_right:
            st.markdown("##### Ratio Growth / Value")
            fig_ratio = go.Figure()
            fig_ratio.add_trace(go.Scatter(x=ratio.index, y=ratio, name='Ratio (VUG/VTV)', line=dict(color='#00b0ff', width=2)))
            
            es_growth = ratio.iloc[-1] > ratio.iloc[0]
            texto_tendencia = " Tendencia hacia Growth" if es_growth else " Tendencia hacia Value"
            color_tendencia = "#00e676" if es_growth else "#ff5252"

            fig_ratio.update_layout(
                template="plotly_dark",
                paper_bgcolor="#161b22",
                plot_bgcolor="#0b0e14",
                margin=dict(l=20, r=20, t=30, b=20),
                height=350,
                annotations=[dict(
                    x=ratio.index[-1], 
                    y=ratio.iloc[-1],
                    text=texto_tendencia,
                    showarrow=True, 
                    arrowhead=1, 
                    arrowcolor=color_tendencia,
                    font=dict(color=color_tendencia, size=12)
                )]
            )
            st.plotly_chart(fig_ratio, use_container_width=True)

    except Exception as e:
        st.error(f"Error al obtener datos de rendimiento: {e}")