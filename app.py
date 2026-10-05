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

# Estilos CSS Neón / Dark Mode
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
# EXTRACCIÓN Y ORDENAMIENTO CRONOLÓGICO DE NOTICIAS
# ---------------------------------------------------------
@st.cache_data(ttl=300)
def fetch_live_news_es():
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
        temp_items = []
        
        for entry in feed.entries:
            published_dt = None
            timestamp_sort = 0
            
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                timestamp_sort = time.mktime(entry.published_parsed)
                published_dt = datetime.fromtimestamp(timestamp_sort, tz=timezone.utc)
            
            if published_dt and published_dt < limite_fecha:
                continue
                
            temp_items.append({
                "title": entry.title,
                "url": entry.link,
                "time": entry.published if hasattr(entry, 'published') else "Reciente",
                "timestamp": timestamp_sort
            })
            
        temp_items.sort(key=lambda x: x["timestamp"], reverse=True)
        live_data[cat] = temp_items[:15]
        
    return live_data

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
        st.info("📌 Las noticias se actualizan automáticamente en vivo (ordenadas de la más reciente a la más antigua, máx. 10 días).")

    with col_der:
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
                margin-left: auto;
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
                <span style="font-size: 9px; color: #8b949e; background: #21262d; padding: 2px 6px; border-radius: 4px;">RECIENTES PRIMERO</span>
            </div>

            <div class="category-bar">
                <button class="cat-btn active" onclick="changeCategory('macro', this)">🌐 Macro</button>
                <button class="cat-btn" onclick="changeCategory('petroleo', this)">🛢️️ Petróleo</button>
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
# PESTAÑA 1: Estado del Bot (Alta Frecuencia - GGAL Opciones)
# ---------------------------------------------------------
with tab_bot:
    st.subheader("⚡ Resumen Operativo de Alta Frecuencia (Opciones GGAL)")
    
    # --- FILA 1: RENDIMIENTO ACUMULADO POR TEMPORALIDAD ---
    st.markdown("##### 💵 Ganancias y Pérdidas Netas (PnL)")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("PNL HOY", "$ 42.850,00", "+ 6,42%")
    m2.metric("PNL ESTA SEMANA", "$ 185.300,00", "+ 14,20%")
    m3.metric("PNL ESTE MES", "$ 620.400,00", "+ 32,80%")
    m4.metric("PNL HISTÓRICO", "$ 1.840.500,00", "+ 94,15%")
    m5.metric("COMISIONES HOY", "$ 8.120,00", "Broker + BYMA")

    st.markdown("---")

    # --- FILA 2: EFICIENCIA DE ESTRATEGIA (SCALPING 20s) ---
    st.markdown("##### 🎯 Eficiencia & Métricas de Ejecución (Ciclo <= 20s)")
    e1, e2, e3, e4, e5 = st.columns(5)
    e1.metric("OPERACIONES HOY", "84 trades", "61 G / 23 P")
    e2.metric("WIN RATE", "72,62%", "Objetivo > 65%")
    e3.metric("DURACIÓN PROMEDIO", "14,8 seg", "Target <= 20s")
    e4.metric("PROFIT FACTOR", "1,58", "Saludable")
    e5.metric("SLIPPAGE PROMEDIO", "0,12%", "Normal")

    st.markdown("---")

    # --- FILA 3: RIESGO & LATENCIA API ---
    st.markdown("##### 🛡️ Gestión de Riesgo & Conexión Broker")
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("EFECTIVIDAD ZIG-ZAG", "81,2%", "% Confirmación 20s")
    r2.metric("MAX DRAWDOWN HOY", "-$ 14.200,00", "- 1,85%")
    r3.metric("LATENCIA API / ORDEN", "165 ms", "Matriz / API OK")
    r4.metric("RACHA MÁXIMA GANADORA", "9 trades", "Consecutivos")

    st.markdown("---")

    # --- SECCIÓN GRÁFICA Y REGISTRO EN TIEMPO REAL ---
    col_chart, col_table = st.columns([1.3, 1])

    with col_chart:
        st.markdown("##### 📈 Curva de Equity Intradía (Evolución $)")
        
        # Simulación de curva de patrimonio acumulado trade por trade
        trades_sim = list(range(1, 26))
        pnl_acumulado = [0, 1200, 2400, 1800, 3100, 4500, 4100, 5800, 7200, 6900, 
                         8500, 10200, 12100, 11500, 13800, 15400, 18200, 17500, 19800, 
                         22400, 26100, 25300, 28900, 34200, 42850]

        fig_equity = go.Figure()
        fig_equity.add_trace(go.Scatter(
            x=trades_sim, 
            y=pnl_acumulado,
            mode='lines+markers',
            name='Capital ($)',
            line=dict(color='#00e676', width=2),
            fill='tozeroy',
            fillcolor='rgba(0, 230, 118, 0.08)'
        ))
        
        fig_equity.update_layout(
            template="plotly_dark",
            paper_bgcolor="#161b22",
            plot_bgcolor="#0b0e14",
            margin=dict(l=20, r=20, t=20, b=20),
            height=320,
            xaxis_title="Número de Trade",
            yaxis_title="Ganancia Acumulada ($)"
        )
        st.plotly_chart(fig_equity, use_container_width=True)

    with col_table:
        st.markdown("##### 📋 Últimas Operaciones Ejecutadas")
        
        # Tabla simulada de operaciones en tiempo real
        df_trades = pd.DataFrame({
            "Hora": ["15:42:10", "15:41:48", "15:41:25", "15:40:50", "15:40:12"],
            "Especie": ["GFGC6000AB", "GFGC6000AB", "GFGP5800AB", "GFGC6000AB", "GFGC6000AB"],
            "Tipo": ["CALL", "CALL", "PUT", "CALL", "CALL"],
            "Duración": ["12s", "18s", "15s", "11s", "19s"],
            "Resultado": ["+$ 1.850", "+$ 2.400", "-$ 920", "+$ 1.150", "+$ 3.100"]
        })
        
        st.dataframe(df_trades, use_container_width=True, hide_index=True)

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
