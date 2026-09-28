import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import feedparser
import json
from datetime import datetime, timedelta, timezone
import time

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

# ---------------------------------------------------------
# EXTRACCIÓN DE NOTICIAS RECIENTES (MÁX. 10 DÍAS / 15 POR CATEGORÍA)
# ---------------------------------------------------------
@st.cache_data(ttl=300) # Se actualiza automáticamente cada 5 minutos
def fetch_live_news_es():
    # Parámetro when:10d limita la búsqueda en Google News a los últimos 10 días
    rss_urls = {
        "macro": "https://news.google.com/rss/search?q=economia+EEUU+inflacion+Reserva+Federal+when:10d&hl=es-419&gl=US&ceid=US:es-419",
        "petroleo": "https://news.google.com/rss/search?q=precio+petroleo+crudo+OPEP+when:10d&hl=es-419&gl=US&ceid=US:es-419",
        "semiconductores": "https://news.google.com/rss/search?q=semiconductores+Nvidia+TSMC+chips+when:10d&hl=es-419&gl=US&ceid=US:es-419",
        "software": "https://news.google.com/rss/search?q=acciones+software+inteligencia+artificial+nube+when:10d&hl=es-419&gl=US&ceid=US:es-419",
        "bonos": "https://news.google.com/rss/search?q=bonos+del+tesoro+EEUU+rendimiento+when:10d&hl=es-419&gl=US&ceid=US:es-419"
    }
    
    limite_fecha = datetime.now(timezone.utc) - timedelta(days=10)
    live_data = {}

    for cat, url in rss_urls.items():
        feed = feedparser.parse(url)
        items = []
        
        for entry in feed.entries:
            if len(items) >= 15: # Máximo 15 noticias por segmento
                break
                
            published_dt = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published_dt = datetime.fromtimestamp(time.mktime(entry.published_parsed), tz=timezone.utc)
            
            # Filtro adicional de seguridad para garantizar que no supere los 10 días
            if published_dt and published_dt < limite_fecha:
                continue
                
            items.append({
                "title": entry.title,
                "url": entry.link,
                "time": entry.published if hasattr(entry, 'published') else "Reciente"
            })
            
        live_data[cat] = items
    return live_data

# Carga noticias frescas en español
news_data_live = fetch_live_news_es()

# Navegación por pestañas principales
tab_inicio, tab_bot, tab_mercado = st.tabs([
    "🏠 INICIO", 
    "📊 ESTADO DEL BOT", 
    "🌍 ROTACIÓN DE MERCADO"
])

# ---------------------------------------------------------
# PESTAÑA INICIO: Distribución con Cajón Abajo a la Derecha
# ---------------------------------------------------------
with tab_inicio:
    col_izq, col_der = st.columns([1.2, 1])

    with col_izq:
        st.subheader("Bienvenido al Panel Principal")
        st.write("Selecciona cualquiera de las pestañas superiores para explorar el Estado del Bot o la Rotación de Mercado.")
        st.info("📌 Las noticias se actualizan automáticamente en tiempo real (máximo 10 días de antigüedad, 15 por categoría).")

    with col_der:
        # Espaciador vertical para empujar el cajón hacia la esquina inferior derecha
        st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
        
        news_data_json = json.dumps(news_data_live)

        news_ticker_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background-color: transparent;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                overflow: hidden;
            }}
            .news-box {{
                width: 100%;
                max-width: 450px;
                height: 400px;
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.6);
                overflow: hidden;
                padding: 12px;
                box-sizing: border-box;
                margin-left: auto; /* Alineación hacia la derecha extrema */
            }}
            .news-header {{
                font-size: 13px;
                font-weight: bold;
                color: #00e676;
                margin-bottom: 8px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            .category-bar {{
                display: flex;
                gap: 4px;
                border-bottom: 1px solid #30363d;
                padding-bottom: 6px;
                margin-bottom: 8px;
                overflow-x: auto;
                white-space: nowrap;
            }}
            .category-bar::-webkit-scrollbar {{
                height: 3px;
            }}
            .category-bar::-webkit-scrollbar-thumb {{
                background: #30363d;
                border-radius: 3px;
            }}
            .cat-btn {{
                background: #21262d;
                color: #8b949e;
                border: 1px solid #30363d;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 11px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
            }}
            .cat-btn:hover {{
                color: #e6edf3;
                border-color: #8b949e;
            }}
            .cat-btn.active {{
                background: #00e676;
                color: #0b0e14;
                border-color: #00e676;
            }}
            .scroll-container {{
                height: 305px;
                overflow-y: hidden;
                position: relative;
            }}
            .scroll-container:hover {{
                overflow-y: auto;
            }}
            .scroll-container::-webkit-scrollbar {{
                width: 5px;
            }}
            .scroll-container::-webkit-scrollbar-track {{
                background: #161b22;
            }}
            .scroll-container::-webkit-scrollbar-thumb {{
                background: #30363d;
                border-radius: 4px;
            }}
            .scroll-container::-webkit-scrollbar-thumb:hover {{
                background: #00e676;
            }}
            .scroll-content {{
                position: absolute;
                width: 95%;
                animation: scrollUp 65s linear infinite;
            }}
            .scroll-container:hover .scroll-content {{
                animation-play-state: paused;
                position: relative;
            }}
            @keyframes scrollUp {{
                0% {{ top: 100%; }}
                100% {{ top: -350%; }}
            }}
            .news-item {{
                padding: 10px 0;
                border-bottom: 1px dashed #21262d;
                font-size: 12px;
                line-height: 1.4;
            }}
            .news-link {{
                color: #e6edf3;
                text-decoration: none;
                display: block;
                transition: color 0.2s;
            }}
            .news-link:hover {{
                color: #00e676;
                text-decoration: underline;
            }}
            .news-time {{
                font-size: 10px;
                color: #8b949e;
                margin-top: 4px;
            }}
        </style>
        </head>
        <body>

        <div class="news-box">
            <div class="news-header">
                <span>📰 TITULARES EN VIVO</span>
                <span style="font-size: 9px; color: #8b949e; background: #21262d; padding: 2px 6px; border-radius: 4px;">MÁX 10 DÍAS</span>
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
            const newsData = {news_data_json};

            function changeCategory(catKey, btnElement) {{
                const buttons = document.querySelectorAll('.cat-btn');
                buttons.forEach(btn => btn.classList.remove('active'));
                if(btnElement) btnElement.classList.add('active');

                const contentDiv = document.getElementById('newsContent');
                const items = newsData[catKey] || [];
                
                let html = '';
                items.forEach((item, idx) => {{
                    html += `
                        <div class="news-item">
                            <a href="${{item.url}}" target="_blank" class="news-link">
                                ${{idx + 1}}. ${{item.title}}
                            </a>
                            <div class="news-time">🕒 ${{item.time}}</div>
                        </div>
                    `;
                }});

                contentDiv.style.animation = 'none';
                contentDiv.offsetHeight;
                contentDiv.innerHTML = html;
                contentDiv.style.animation = 'scrollUp 65s linear infinite';
            }}

            document.addEventListener('DOMContentLoaded', () => {{
                const firstBtn = document.querySelector('.cat-btn');
                changeCategory('macro', firstBtn);
            }});
        </script>

        </body>
        </html>
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
