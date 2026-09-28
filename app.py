import streamlit as st
import streamlit.components.v1 as components
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

# Navegación por pestañas principales
tab_inicio, tab_bot, tab_mercado = st.tabs([
    "🏠 INICIO", 
    "📊 ESTADO DEL BOT", 
    "🌍 ROTACIÓN DE MERCADO"
])

# ---------------------------------------------------------
# PESTAÑA INICIO: Solo Titulares animado en 10x10cm (inferior derecha)
# ---------------------------------------------------------
with tab_inicio:
    st.subheader("Bienvenido al Panel Principal")
    st.write("Selecciona cualquiera de las pestañas superiores para ver el Estado del Bot o la Rotación de Mercado.")

    # Widget desplegado en la esquina inferior derecha de 380x380 px (~10x10 cm)
    news_ticker_html = """
    <style>
        .news-box {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 380px;
            height: 380px;
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.6);
            overflow: hidden;
            z-index: 99999;
            padding: 12px;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        .news-header {
            font-size: 14px;
            font-weight: bold;
            color: #00e676;
            border-bottom: 1px solid #30363d;
            padding-bottom: 8px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .scroll-container {
            height: 320px;
            overflow: hidden;
            position: relative;
        }
        .scroll-content {
            position: absolute;
            width: 100%;
            animation: scrollUp 40s linear infinite;
        }
        .scroll-content:hover {
            animation-play-state: paused;
        }
        @keyframes scrollUp {
            0% { top: 100%; }
            100% { top: -180%; }
        }
        .news-item {
            padding: 8px 0;
            border-bottom: 1px dashed #21262d;
            font-size: 12px;
            line-height: 1.4;
        }
        .news-item a {
            color: #e6edf3;
            text-decoration: none;
            transition: color 0.2s;
        }
        .news-item a:hover {
            color: #00e676;
        }
    </style>

    <div class="news-box">
        <div class="news-header">
            <span>📰 ÚLTIMOS TITULARES</span>
            <span style="font-size: 10px; color: #8b949e;">EN VIVO</span>
        </div>
        <div class="scroll-container">
            <div class="scroll-content">
                <div class="news-item"><a href="https://www.tradingview.com/news/" target="_blank">1. La Reserva Federal mantiene tasas mientras evalúa inflación.</a></div>
                <div class="news-item"><a href="https://www.tradingview.com/news/" target="_blank">2. Nvidia registra un incremento en ingresos por IA.</a></div>
                <div class="news-item"><a href="https://www.tradingview.com/news/" target="_blank">3. El S&P 500 alcanza nuevos máximos tras resultados tecnológicos.</a></div>
                <div class="news-item"><a href="https://www.tradingview.com/news/" target="_blank">4. Petróleo WTI retrocede ante aumento de reservas comerciales.</a></div>
                <div class="news-item"><a href="https://www.tradingview.com/news/" target="_blank">5. Acciones de Apple muestran fortaleza tras demanda de nuevos dispositivos.</a></div>
                <div class="news-item"><a href="https://www.tradingview.com/news/" target="_blank">6. Rendimiento del Bono a 10 años cae ligeramente.</a></div>
                <div class="news-item"><a href="https://www.tradingview.com/news/" target="_blank">7. Amazon anuncia nuevas inversiones en centros de datos.</a></div>
                <div class="news-item"><a href="https://www.tradingview.com/news/" target="_blank">8. Sector financiero sube tras balances bancarios trimestrales.</a></div>
                <div class="news-item"><a href="https://www.tradingview.com/news/" target="_blank">9. Bitcoin se consolida en rangos clave de resistencia.</a></div>
                <div class="news-item"><a href="https://www.tradingview.com/news/" target="_blank">10. El mercado de opciones registra alta actividad en contratos CALL.</a></div>
                <div class="news-item"><a href="https://www.tradingview.com/news/" target="_blank">11. Meta Platforms acelera inversión en modelos abiertos de inteligencia artificial.</a></div>
                <div class="news-item"><a href="https://www.tradingview.com/news/" target="_blank">12. Dólar se estabiliza frente a principales divisas internacionales.</a></div>
                <div class="news-item"><a href="https://www.tradingview.com/news/" target="_blank">13. Empresas de Semiconductores muestran rebote técnico significativo.</a></div>
                <div class="news-item"><a href="https://www.tradingview.com/news/" target="_blank">14. Ventas minoristas en EE.UU. superan expectativas en el último trimestre.</a></div>
                <div class="news-item"><a href="https://www.tradingview.com/news/" target="_blank">15. Sector energía reacciona a decisiones operativas de la OPEP+.</a></div>
            </div>
        </div>
    </div>
    """
    components.html(news_ticker_html, height=420)

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
# PESTAÑA 2: Rotación de Mercado + TradingView Heatmap + Matriz
# ---------------------------------------------------------
with tab_mercado:
    
    # --- SECCIÓN 1: TRADINGVIEW MAPA DE CALOR S&P 500 ---
    st.markdown("### 🗺️ Mapa de Calor del Mercado EE.UU. (S&P 500)")
    
    tradingview_html = """
    <div style="width: 100%;">
        <div class="tradingview-widget-container" style="height: 500px; width: 100%;">
          <div class="tradingview-widget-container__widget" style="height: 500px; width: 100%;"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-stock-heatmap.js" async>
          {
          "exchanges": [],
          "dataSource": "SPX500",
          "grouping": "sector",
          "blockSize": "market_cap_basic",
          "blockColor": "change",
          "locale": "es",
          "symbolUrl": "",
          "colorTheme": "dark",
          "hasTopBar": true,
          "isDataSetEnabled": true,
          "isZoomEnabled": true,
          "hasSymbolTooltip": true,
          "width": "100%",
          "height": "500"
        }
          </script>
        </div>
    </div>
    """
    
    components.html(tradingview_html, height=530)

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