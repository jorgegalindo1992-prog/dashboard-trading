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
# PESTAÑA INICIO: Cajón de Noticias con Scroll y Filtros
# ---------------------------------------------------------
with tab_inicio:
    st.subheader("Bienvenido al Panel Principal")
    st.write("Selecciona cualquiera de las pestañas superiores para ver el Estado del Bot o la Rotación de Mercado.")

    news_ticker_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: transparent;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            overflow: hidden;
        }
        .news-box {
            width: 100%;
            max-width: 420px;
            height: 380px;
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.6);
            overflow: hidden;
            padding: 12px;
            box-sizing: border-box;
        }
        .news-header {
            font-size: 13px;
            font-weight: bold;
            color: #00e676;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .category-bar {
            display: flex;
            gap: 4px;
            border-bottom: 1px solid #30363d;
            padding-bottom: 6px;
            margin-bottom: 8px;
            overflow-x: auto;
            white-space: nowrap;
        }
        .category-bar::-webkit-scrollbar {
            height: 3px;
        }
        .category-bar::-webkit-scrollbar-thumb {
            background: #30363d;
            border-radius: 3px;
        }
        .cat-btn {
            background: #21262d;
            color: #8b949e;
            border: 1px solid #30363d;
            border-radius: 4px;
            padding: 4px 8px;
            font-size: 11px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .cat-btn:hover {
            color: #e6edf3;
            border-color: #8b949e;
        }
        .cat-btn.active {
            background: #00e676;
            color: #0b0e14;
            border-color: #00e676;
        }
        .scroll-container {
            height: 285px;
            overflow-y: hidden;
            position: relative;
        }
        .scroll-container:hover {
            overflow-y: auto;
        }
        .scroll-container::-webkit-scrollbar {
            width: 5px;
        }
        .scroll-container::-webkit-scrollbar-track {
            background: #161b22;
        }
        .scroll-container::-webkit-scrollbar-thumb {
            background: #30363d;
            border-radius: 4px;
        }
        .scroll-container::-webkit-scrollbar-thumb:hover {
            background: #00e676;
        }
        .scroll-content {
            position: absolute;
            width: 95%;
            animation: scrollUp 40s linear infinite;
        }
        .scroll-container:hover .scroll-content {
            animation-play-state: paused;
            position: relative;
        }
        @keyframes scrollUp {
            0% { top: 100%; }
            100% { top: -250%; }
        }
        .news-item {
            padding: 10px 0;
            border-bottom: 1px dashed #21262d;
            font-size: 12px;
            line-height: 1.4;
        }
        .news-link {
            color: #e6edf3;
            text-decoration: none;
            display: block;
            transition: color 0.2s;
        }
        .news-link:hover {
            color: #00e676;
            text-decoration: underline;
        }
        .news-time {
            font-size: 10px;
            color: #8b949e;
            margin-top: 4px;
        }
    </style>
    </head>
    <body>

    <div class="news-box">
        <div class="news-header">
            <span>📰 TITULARES EN VIVO</span>
            <span style="font-size: 9px; color: #8b949e; background: #21262d; padding: 2px 6px; border-radius: 4px;">ÚLTIMA HORA</span>
        </div>

        <div class="category-bar">
            <button class="cat-btn active" onclick="changeCategory('macro', this)">🌐 Macro</button>
            <button class="cat-btn" onclick="changeCategory('petroleo', this)">🛢️ Petróleo</button>
            <button class="cat-btn" onclick="changeCategory('semiconductores', this)">💻 Semis</button>
            <button class="cat-btn" onclick="changeCategory('software', this)">⚙️ Software</button>
            <button class="cat-btn" onclick="changeCategory('bonos', this)">📜 Bonos</button>
        </div>

        <div class="scroll-container">
            <div class="scroll-content" id="newsContent"></div>
        </div>
    </div>

    <script>
        const newsData = {
            macro: [
                { title: "1. Datos del IPC y PCE en EE.UU.: Expectativas de tasas de interés de la Reserva Federal.", time: "Hace 10 min", url: "https://www.cnbc.com/us-economy/" },
                { title: "2. Nóminas No Agrícolas (NFP) y datos de empleo en EE.UU.", time: "Hace 25 min", url: "https://www.reuters.com/business/us/" },
                { title: "3. Decisiones de política monetaria y discursos de Jerome Powell.", time: "Hace 40 min", url: "https://www.bloomberg.com/economics" },
                { title: "4. Indice de Confianza del Consumidor e indicadores manufactureros ISM.", time: "Hace 1 hora", url: "https://www.marketwatch.com/economy" }
            ],
            petroleo: [
                { title: "1. Precios del Petróleo WTI y Brent reaccionan a recortes de producción de la OPEP+.", time: "Hace 15 min", url: "https://www.reuters.com/business/energy/" },
                { title: "2. Informe semanal de inventarios de crudo de la EIA en Estados Unidos.", time: "Hace 35 min", url: "https://www.bloomberg.com/energy" },
                { title: "3. Tensiones geopolíticas en Medio Oriente y su impacto en la oferta energética.", time: "Hace 1 hora", url: "https://www.cnbc.com/oil/" }
            ],
            semiconductores: [
                { title: "1. Nvidia y el avance de chips para inteligencia artificial de nueva generación.", time: "Hace 12 min", url: "https://www.cnbc.com/technology/" },
                { title: "2. TSMC reporta ingresos y demanda en nodos de aceleradores de IA.", time: "Hace 30 min", url: "https://www.reuters.com/technology/" },
                { title: "3. AMD e Intel compiten por cuota de mercado en procesadores de centros de datos.", time: "Hace 50 min", url: "https://www.marketwatch.com/investing/stock/nvda" }
            ],
            software: [
                { title: "1. Microsoft integra nuevas funciones de IA Copilot en suites corporativas.", time: "Hace 20 min", url: "https://www.cnbc.com/software/" },
                { title: "2. Salesforce y Oracle muestran sólido crecimiento en ingresos por suscripción en la nube.", time: "Hace 45 min", url: "https://www.reuters.com/technology/" },
                { title: "3. Ciberseguridad: Palo Alto Networks y CrowdStrike registran alta demanda empresarial.", time: "Hace 1 hora", url: "https://www.bloomberg.com/technology" }
            ],
            bonos: [
                { title: "1. Rendimiento del Bono del Tesoro a 10 años (US10Y) ajusta posiciones.", time: "Hace 8 min", url: "https://www.cnbc.com/bonds/" },
                { title: "2. Curva de tipos entre bonos a 2 y 10 años muestra variaciones de diferencial.", time: "Hace 28 min", url: "https://www.bloomberg.com/markets/rates-bonds" },
                { title: "3. Subastas del Tesoro de EE.UU. registran demanda de inversores institucionales.", time: "Hace 55 min", url: "https://www.marketwatch.com/investing/bond/tmubmusd10y" }
            ]
        };

        function changeCategory(catKey, btnElement) {
            const buttons = document.querySelectorAll('.cat-btn');
            buttons.forEach(btn => btn.classList.remove('active'));
            btnElement.classList.add('active');

            const contentDiv = document.getElementById('newsContent');
            const items = newsData[catKey] || [];
            
            let html = '';
            items.forEach(item => {
                html += `
                    <div class="news-item">
                        <a href="${item.url}" target="_blank" class="news-link">
                            ${item.title}
                        </a>
                        <div class="news-time">🕒 ${item.time}</div>
                    </div>
                `;
            });

            contentDiv.style.animation = 'none';
            contentDiv.offsetHeight;
            contentDiv.innerHTML = html;
            contentDiv.style.animation = 'scrollUp 40s linear infinite';
        }

        document.addEventListener('DOMContentLoaded', () => {
            const firstBtn = document.querySelector('.cat-btn');
            changeCategory('macro', firstBtn);
        });
    </script>

    </body>
    </html>
    """
    components.html(news_ticker_html, height=400)

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
        df_download = yf.download(tickers_list, period='5d')['Close']
        df_download = df_download.dropna()
        
        last_two = df_download.tail(2)
        cambio_pct = ((last_two.iloc[-1] - last_two.iloc[-2]) / last_two.iloc[-2]) * 100
        
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
                [0.0, "#b71c1c"],
                [0.5, "#212121"],
                [1.0, "#1b5e20"]
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
        datos = yf.download(["VUG", "VTV"], period=periodo)['Close'].dropna()
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
