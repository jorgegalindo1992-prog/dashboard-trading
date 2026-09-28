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
# PESTAÑA INICIO: Cajón de Noticias Interactivo con Sub-Categorías
# ---------------------------------------------------------
with tab_inicio:
    st.subheader("Bienvenido al Panel Principal")
    st.write("Selecciona cualquiera de las pestañas superiores para ver el Estado del Bot o la Rotación de Mercado.")

    # Widget desplegado en la esquina inferior derecha (~10x10 cm -> 380x380 px)
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
            position: fixed;
            bottom: 10px;
            right: 10px;
            width: 360px;
            height: 360px;
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.6);
            overflow: hidden;
            z-index: 99999;
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
        /* Barra de Pestañas / Secciones */
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
            padding: 3px 8px;
            font-size: 10px;
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
            height: 270px;
            overflow: hidden;
            position: relative;
        }
        .scroll-content {
            position: absolute;
            width: 100%;
            animation: scrollUp 35s linear infinite;
        }
        .scroll-content:hover {
            animation-play-state: paused;
        }
        @keyframes scrollUp {
            0% { top: 100%; }
            100% { top: -220%; }
        }
        .news-item {
            padding: 8px 0;
            border-bottom: 1px dashed #21262d;
            font-size: 11px;
            line-height: 1.4;
            color: #e6edf3;
            cursor: pointer;
            transition: color 0.2s;
        }
        .news-item:hover {
            color: #00e676;
        }
        .news-time {
            font-size: 9px;
            color: #8b949e;
            margin-top: 2px;
        }
    </style>
    </head>
    <body>

    <div class="news-box">
        <div class="news-header">
            <span>📰 TITULARES EN VIVO</span>
            <span style="font-size: 9px; color: #8b949e; background: #21262d; padding: 2px 6px; border-radius: 4px;">ACTUALIZADO</span>
        </div>

        <!-- Secciones / Categorías -->
        <div class="category-bar">
            <button class="cat-btn active" onclick="changeCategory('petroleo', this)">🛢️ Petróleo</button>
            <button class="cat-btn" onclick="changeCategory('semiconductores', this)">💻 Semis</button>
            <button class="cat-btn" onclick="changeCategory('software', this)">⚙️ Software</button>
            <button class="cat-btn" onclick="changeCategory('bonos', this)">📜 Bonos</button>
        </div>

        <!-- Contenedor del desplazamiento -->
        <div class="scroll-container">
            <div class="scroll-content" id="newsContent">
                <!-- Se puebla mediante Javascript -->
            </div>
        </div>
    </div>

    <script>
        // Base de noticias organizadas por sector
        const newsData = {
            petroleo: [
                { title: "1. Petróleo WTI se estabiliza tras decisión de producción de la OPEP+.", time: "Hace 10 min" },
                { title: "2. Inventarios de crudo en EE.UU. caen más de lo esperado.", time: "Hace 25 min" },
                { title: "3. Conflicto en Oriente Medio eleva la prima de riesgo en el sector energético.", time: "Hace 45 min" },
                { title: "4. Refinerías globales aumentan margen de procesamiento en diésel.", time: "Hace 1 hora" },
                { title: "5. Demanda de combustible de aviación alcanza máximos estacionales.", time: "Hace 2 horas" },
                { title: "6. Chevron y Exxon reportan avance en proyectos offshore en Guyana.", time: "Hace 2 horas" },
                { title: "7. Gas Natural sube por previsiones de clima frío en EE.UU. y Europa.", time: "Hace 3 horas" },
                { title: "8. Exportaciones de crudo desde el Golfo de México marcan hito récord.", time: "Hace 4 horas" },
                { title: "9. Precios del Brent mantienen soporte en rango clave técnico.", time: "Hace 5 horas" },
                { title: "10. Inversores de energía reajustan coberturas mediante opciones PUT.", time: "Hace 6 horas" }
            ],
            semiconductores: [
                { title: "1. Nvidia anuncia nueva arquitectura de chips para centros de datos e IA.", time: "Hace 5 min" },
                { title: "2. TSMC incrementa capacidad de empaquetado avanzado para clientes clave.", time: "Hace 18 min" },
                { title: "3. AMD lanza nuevos procesadores optimizados para servidores enterprise.", time: "Hace 40 min" },
                { title: "4. ASML reporta sólido volumen de pedidos en sistemas EUV de litografía.", time: "Hace 1 hora" },
                { title: "5. Broadcom experimenta fuerte demanda en soluciones de red de alta velocidad.", time: "Hace 2 horas" },
                { title: "6. Intel acelera desarrollo en su nodo de fabricación 18A.", time: "Hace 3 horas" },
                { title: "7. Qualcomm amplia presencia en chips para la industria automotriz.", time: "Hace 3 horas" },
                { title: "8. Micron recibe impulso por alta demanda de memorias HBM3e.", time: "Hace 4 horas" },
                { title: "9. Índice de Semiconductores de Filadelfia (SOX) prueba máximos históricos.", time: "Hace 5 horas" },
                { title: "10. Cadencia y Synopsys suben ante mayor diseño de ASICs personalizados.", time: "Hace 6 horas" }
            ],
            software: [
                { title: "1. Microsoft integra nuevas funciones de IA Copilot en entorno Cloud.", time: "Hace 12 min" },
                { title: "2. Salesforce eleva sus perspectivas de ingresos anuales por suscripción.", time: "Hace 30 min" },
                { title: "3. Oracle muestra crecimiento acelerado en su infraestructura de nube.", time: "Hace 50 min" },
                { title: "4. Adobe expande herramientas creativas generativas para empresas.", time: "Hace 1 hora" },
                { title: "5. ServiceNow reporta expansión en contratos de automatización de procesos.", time: "Hace 2 horas" },
                { title: "6. CrowdStrike refuerza participación en seguridad en la nube multi-cloud.", time: "Hace 3 horas" },
                { title: "7. Palantir gana contrato federal clave para integración de datos e IA.", time: "Hace 4 horas" },
                { title: "8. Snowflake mejora estimaciones de consumo de plataforma de datos.", time: "Hace 4 horas" },
                { title: "9. Datadog registra incremento de clientes de gran escala en supervisión APM.", time: "Hace 5 horas" },
                { title: "10. MongoDB presenta mejoras de rendimiento en bases de datos vectoriales.", time: "Hace 6 horas" }
            ],
            bonos: [
                { title: "1. Rendimiento del Bono a 10 años retrocede tras datos de inflación.", time: "Hace 8 min" },
                { title: "2. Reserva Federal señala prudencia en próximas decisiones de tasas.", time: "Hace 20 min" },
                { title: "3. Subasta de bonos a 30 años registra fuerte demanda de compradores extranjeros.", time: "Hace 35 min" },
                { title: "4. Curva de rendimientos se empina a medida que se ajusta el tramo corto.", time: "Hace 1 hora" },
                { title: "5. Rendimiento a 2 años reacciona a cifras del mercado laboral en EE.UU.", time: "Hace 2 horas" },
                { title: "6. Deuda corporativa con grado de inversión mantiene diferenciales estrechos.", time: "Hace 3 horas" },
                { title: "7. El BCE evalúa ritmo de flexibilización monetaria para próximos trimestres.", time: "Hace 4 horas" },
                { title: "8. Bonos soberanos europeos (Bunds) cotizan con volatilidad contenida.", time: "Hace 5 horas" },
                { title: "9. Entradas de capital hacia Fondos Monetarios marcan máximos anuales.", time: "Hace 5 horas" },
                { title: "10. Expectativas de inflación a 5 años permanecen ancladas según datos del Fed.", time: "Hace 6 horas" }
            ]
        };

        // Función para cambiar de categoría y reescribir los titulares
        function changeCategory(catKey, btnElement) {
            // Actualizar botones
            const buttons = document.querySelectorAll('.cat-btn');
            buttons.forEach(btn => btn.classList.remove('active'));
            btnElement.classList.add('active');

            // Cargar datos
            const contentDiv = document.getElementById('newsContent');
            const items = newsData[catKey] || [];
            
            let html = '';
            items.forEach(item => {
                html += `
                    <div class="news-item">
                        <div>${item.title}</div>
                        <div class="news-time">${item.time}</div>
                    </div>
                `;
            });

            // Reiniciar animación al cambiar de pestaña
            contentDiv.style.animation = 'none';
            contentDiv.offsetHeight; // Refresco de DOM
            contentDiv.innerHTML = html;
            contentDiv.style.animation = 'scrollUp 35s linear infinite';
        }

        // Cargar categoría inicial (Petróleo)
        document.addEventListener('DOMContentLoaded', () => {
            const firstBtn = document.querySelector('.cat-btn');
            changeCategory('petroleo', firstBtn);
        });
    </script>

    </body>
    </html>
    """
    components.html(news_ticker_html, height=390)

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