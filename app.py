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
# PESTAÑA INICIO: Cajón de Noticias con Macro, Links y Scroll
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
            width: 370px;
            height: 380px;
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
        /* Contenedor del desplazamiento y scroll manual */
        .scroll-container {
            height: 285px;
            overflow-y: hidden;
            position: relative;
        }
        .scroll-container:hover {
            overflow-y: auto;
        }
        /* Estilizado de la barra de scroll lateral */
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
            animation: scrollUp 45s linear infinite;
        }
        .scroll-container:hover .scroll-content {
            animation-play-state: paused;
            position: relative;
        }
        @keyframes scrollUp {
            0% { top: 100%; }
            100% { top: -300%; }
        }
        .news-item {
            padding: 8px 0;
            border-bottom: 1px dashed #21262d;
            font-size: 11px;
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
            <span style="font-size: 9px; color: #8b949e; background: #21262d; padding: 2px 6px; border-radius: 4px;">15 NOTICIAS</span>
        </div>

        <!-- Secciones / Categorías -->
        <div class="category-bar">
            <button class="cat-btn active" onclick="changeCategory('macro', this)">🌐 Macro</button>
            <button class="cat-btn" onclick="changeCategory('petroleo', this)">🛢️ Petróleo</button>
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
        // Base de datos de 15 noticias por sector con enlaces directos
        const newsData = {
            macro: [
                { title: "1. Nóminas No Agrícolas (NFP) superan expectativas al registrar 225k empleos en EE.UU.", time: "Hace 5 min", url: "https://www.marketwatch.com/economy" },
                { title: "2. Tasa de desempleo en EE.UU. se mantiene estable en 3.8% acorde a las proyecciones.", time: "Hace 15 min", url: "https://www.bloomberg.com/markets" },
                { title: "3. Confianza del Consumidor de la Univ. de Michigan sube a 79.4 puntos.", time: "Hace 30 min", url: "https://www.reuters.com/business" },
                { title: "4. Inflación CPI en EE.UU. muestra desaceleración mensual al situarse en 0.2%.", time: "Hace 45 min", url: "https://www.cnbc.com/economy" },
                { title: "5. Ventas al por menor en EE.UU. muestran resiliencia con un aumento del 0.6%.", time: "Hace 1 hora", url: "https://www.investors.com" },
                { title: "6. Solicitudes semanales de subsidio por desempleo caen a 210,000.", time: "Hace 1 hora", url: "https://www.marketwatch.com/economy" },
                { title: "7. Índice PMI manufacturero S&P Global vuelve a terreno de expansión en 50.3.", time: "Hace 2 horas", url: "https://www.bloomberg.com/markets" },
                { title: "8. El Índice de Precios del Consumo Personal (PCE) subyacente cumple objetivo anual.", time: "Hace 2 horas", url: "https://www.reuters.com/business" },
                { title: "9. PIB de EE.UU. registra un crecimiento anualizado revisado del 2.7%.", time: "Hace 3 horas", url: "https://www.cnbc.com/economy" },
                { title: "10. Costo del empleo (ECI) en EE.UU. crece moderadamente moderando presiones salariales.", time: "Hace 4 horas", url: "https://www.investors.com" },
                { title: "11. Encuesta JOLTs muestra 8.8 millones de puestos de trabajo vacantes en EE.UU.", time: "Hace 4 horas", url: "https://www.marketwatch.com/economy" },
                { title: "12. Déficit comercial de bienes en EE.UU. se reduce ante sólido incremento exportador.", time: "Hace 5 horas", url: "https://www.bloomberg.com/markets" },
                { title: "13. Inventarios mayoristas en EE.UU. aumentan levemente un 0.3% en el mes.", time: "Hace 5 horas", url: "https://www.reuters.com/business" },
                { title: "14. Construcción de viviendas unifamiliares en EE.UU. repunta ante menor tasa hipotecaria.", time: "Hace 6 horas", url: "https://www.cnbc.com/economy" },
                { title: "15. Crédito al consumo en EE.UU. se expande a ritmo saludable impulsado por tarjetas.", time: "Hace 6 horas", url: "https://www.investors.com" }
            ],
            petroleo: [
                { title: "1. Petróleo WTI cotiza firme en $82 tras decisión de recorte voluntario de la OPEP+.", time: "Hace 10 min", url: "https://www.reuters.com/business/energy" },
                { title: "2. Inventarios de crudo API caen en 3.2 millones de barriles en EE.UU.", time: "Hace 20 min", url: "https://www.bloomberg.com/energy" },
                { title: "3. Tensiones en rutas del Mar Rojo elevan costos de flete para petroleros.", time: "Hace 35 min", url: "https://www.cnbc.com/oil" },
                { title: "4. Refinerías de la Costa del Golfo operan al 92% de capacidad instalada.", time: "Hace 50 min", url: "https://www.marketwatch.com/investing/future/crude%20oil%20- %20wti" },
                { title: "5. Demanda de combustible de aviación alcanza máximos prepandemia.", time: "Hace 1 hora", url: "https://www.reuters.com/business/energy" },
                { title: "6. ExxonMobil y Chevron aceleran producción en la cuenca Permian.", time: "Hace 1 hora", url: "https://www.bloomberg.com/energy" },
                { title: "7. Gas Natural Henry Hub sube 4% ante ola de frío pronosticada en EE.UU.", time: "Hace 2 horas", url: "https://www.cnbc.com/oil" },
                { title: "8. Exportaciones de GNL de EE.UU. marcan récord mensual hacia Europa.", time: "Hace 3 horas", url: "https://www.marketwatch.com" },
                { title: "9. Margen de refinado de diésel (Crack Spread) se expande a $35.", time: "Hace 3 horas", url: "https://www.reuters.com/business/energy" },
                { title: "10. Conteo de plataformas petroleras de Baker Hughes sube en 3 unidades.", time: "Hace 4 horas", url: "https://www.bloomberg.com/energy" },
                { title: "11. Arabia Saudita eleva precio oficial de venta (OSP) para clientes asiáticos.", time: "Hace 4 horas", url: "https://www.cnbc.com/oil" },
                { title: "12. Guyana proyecta alcanzar 1.2 millones de barriles diarios en producción.", time: "Hace 5 horas", url: "https://www.marketwatch.com" },
                { title: "13. Inversores institucionales aumentan posiciones netas largas en crudo Brent.", time: "Hace 5 horas", url: "https://www.reuters.com/business/energy" },
                { title: "14. Brasil acelera perforación presal con nuevas plataformas FPSO.", time: "Hace 6 horas", url: "https://www.bloomberg.com/energy" },
                { title: "15. Precios de la gasolina en surtidor en EE.UU. se estabilizan en $3.45/galón.", time: "Hace 6 horas", url: "https://www.cnbc.com/oil" }
            ],
            semiconductores: [
                { title: "1. Nvidia presenta la arquitectura Blackwell para supercómputo e IA.", time: "Hace 8 min", url: "https://www.cnbc.com/technology" },
                { title: "2. TSMC reporta crecimiento del 16% en ingresos trimestrales impulsado por 3nm.", time: "Hace 22 min", url: "https://www.reuters.com/technology" },
                { title: "3. AMD anuncia disponibilidad de procesadores Instinct MI300X.", time: "Hace 40 min", url: "https://www.bloomberg.com/technology" },
                { title: "4. ASML recibe nuevos pedidos de litografía High-NA EUV por parte de clientes de chip.", time: "Hace 1 hora", url: "https://www.marketwatch.com" },
                { title: "5. Broadcom prevé $10 mil millones en ventas de chips aceleradores para IA.", time: "Hace 1 hora", url: "https://www.cnbc.com/technology" },
                { title: "6. Intel recibe subsidio de la ley CHIPS Act para expansión de fábricas en Ohio.", time: "Hace 2 horas", url: "https://www.reuters.com/technology" },
                { title: "7. Qualcomm introduce plataforma Snapdragon para computadoras personales con IA.", time: "Hace 2 horas", url: "https://www.bloomberg.com/technology" },
                { title: "8. Micron inicia producción en masa de memorias HBM3e para aceleradores.", time: "Hace 3 horas", url: "https://www.marketwatch.com" },
                { title: "9. Índice Semiconductor SOX marca nuevo máximo intradiario liderado por megacaps.", time: "Hace 3 horas", url: "https://www.cnbc.com/technology" },
                { title: "10. Arm Holdings eleva guía de ingresos por cobro de regalías en chips v9.", time: "Hace 4 horas", url: "https://www.reuters.com/technology" },
                { title: "11. Applied Materials lanza herramientas de deposición para empaquetado 3D.", time: "Hace 4 horas", url: "https://www.bloomberg.com/technology" },
                { title: "12. Lam Research se beneficia del repunte en equipos de memoria NAND y DRAM.", time: "Hace 5 horas", url: "https://www.marketwatch.com" },
                { title: "13. KLA Corp reporta alta utilización de inspección de obleas en nodos avanzados.", time: "Hace 5 horas", url: "https://www.cnbc.com/technology" },
                { title: "14. Synopsys completa integración de software de diseño asistido por IA.", time: "Hace 6 horas", url: "https://www.reuters.com/technology" },
                { title: "15. Texas Instruments proyecta recuperación gradual en chips analógicos e industriales.", time: "Hace 6 horas", url: "https://www.bloomberg.com/technology" }
            ],
            software: [
                { title: "1. Microsoft integra Copilot para seguridad en suite Microsoft 365 Enterprise.", time: "Hace 12 min", url: "https://www.cnbc.com/technology" },
                { title: "2. Salesforce reporta margen operativo récord de 32.5% en su último trimestre.", time: "Hace 25 min", url: "https://www.reuters.com/technology" },
                { title: "3. Oracle Cloud Infrastructure (OCI) firma alianza estratégica con OpenAI.", time: "Hace 45 min", url: "https://www.bloomberg.com/technology" },
                { title: "4. Adobe lanza modelos Firefly Video para edición audiovisual profesional.", time: "Hace 1 hora", url: "https://www.marketwatch.com" },
                { title: "5. ServiceNow supera estimaciones en suscripciones de automatización con IA.", time: "Hace 1 hora", url: "https://www.cnbc.com/technology" },
                { title: "6. CrowdStrike expande plataforma Falcon hacia protección de identidades en la nube.", time: "Hace 2 horas", url: "https://www.reuters.com/technology" },
                { title: "7. Palantir renueva contrato multimillonario con el Departamento de Defensa de EE.UU.", time: "Hace 2 horas", url: "https://www.bloomberg.com/technology" },
                { title: "8. Snowflake lanza Cortex para búsqueda y análisis de datos no estructurados.", time: "Hace 3 horas", url: "https://www.marketwatch.com" },
                { title: "9. Datadog registra crecimiento de dos dígitos en monitoreo de aplicaciones en nube.", time: "Hace 3 horas", url: "https://www.cnbc.com/technology" },
                { title: "10. MongoDB aumenta retención de clientes enterprise en su servicio Atlas.", time: "Hace 4 horas", url: "https://www.reuters.com/technology" },
                { title: "11. Intuit reporta fuerte adopción de herramientas financieras impulsadas por IA.", time: "Hace 4 horas", url: "https://www.bloomberg.com/technology" },
                { title: "12. Palo Alto Networks acelera estrategia de plataforma unificada de ciberseguridad.", time: "Hace 5 horas", url: "https://www.marketwatch.com" },
                { title: "13. Workday expande soluciones HCM para gestión de capital humano en empresas.", time: "Hace 5 horas", url: "https://www.cnbc.com/technology" },
                { title: "14. HubSpot incrementa suscriptores pagos en la plataforma de CRM para PyMEs.", time: "Hace 6 horas", url: "https://www.reuters.com/technology" },
                { title: "15. Atlassian fortalece herramientas Jira con asistentes conversacionales virtuales.", time: "Hace 6 horas", url: "https://www.bloomberg.com/technology" }
            ],
            bonos: [
                { title: "1. Rendimiento del Bono a 10 años de EE.UU. retrocede a 4.22% tras datos de empleo.", time: "Hace 8 min", url: "https://www.cnbc.com/bonds" },
                { title: "2. Tasa del Bono a 2 años reacciona a expectativas sobre recortes de la Reserva Federal.", time: "Hace 18 min", url: "https://www.bloomberg.com/markets/rates-bonds" },
                { title: "3. Tesoro de EE.UU. subasta $39,000 millones en bonos a 10 años con sólida demanda.", time: "Hace 35 min", url: "https://www.reuters.com/markets/rates-bonds" },
                { title: "4. Curva de rendimiento entre 2 y 10 años desinvierte su pendiente gradualmente.", time: "Hace 50 min", url: "https://www.marketwatch.com/investing/bond/tmubmusd10y" },
                { title: "5. Diferenciales de crédito High Yield (Gran Rentabilidad) se mantienen comprimidos.", time: "Hace 1 hora", url: "https://www.cnbc.com/bonds" },
                { title: "6. Bonos del Tesoro protegidos contra la inflación (TIPS) ven aumento de volumen.", time: "Hace 2 horas", url: "https://www.bloomberg.com/markets/rates-bonds" },
                { title: "7. El Banco Central Europeo (BCE) sugiere posible senda de recortes graduales.", time: "Hace 2 horas", url: "https://www.reuters.com/markets/rates-bonds" },
                { title: "8. Emisión de deuda corporativa de grado de inversión alcanza los $40 mil millones.", time: "Hace 3 horas", url: "https://www.marketwatch.com" },
                { title: "9. Entradas netas a fondos monetarios en EE.UU. superan los $6 billones totales.", time: "Hace 3 horas", url: "https://www.cnbc.com/bonds" },
                { title: "10. Rendimiento del Bund alemán a 10 años se cotiza estable en 2.35%.", time: "Hace 4 horas", url: "https://www.bloomberg.com/markets/rates-bonds" },
                { title: "11. Bonos soberanos de Japón JGB a 10 años suben tras señales del Banco de Japón.", time: "Hace 4 horas", url: "https://www.reuters.com/markets/rates-bonds" },
                { title: "12. Inversores extranjeros incrementan tenencias de deuda pública norteamericana.", time: "Hace 5 horas", url: "https://www.marketwatch.com" },
                { title: "13. Tasa SOFR (Secured Overnight Financing Rate) se mantiene en 5.31%.", time: "Hace 5 horas", url: "https://www.cnbc.com/bonds" },
                { title: "14. Bonos municipales en EE.UU. registran 4 semanas consecutivas de flujos positivos.", time: "Hace 6 horas", url: "https://www.bloomberg.com/markets/rates-bonds" },
                { title: "15. Expectativas de inflación breakeven a 5 años en EE.UU. permanecen en 2.25%.", time: "Hace 6 horas", url: "https://www.reuters.com/markets/rates-bonds" }
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
                        <a href="${item.url}" target="_blank" class="news-link">
                            ${item.title}
                        </a>
                        <div class="news-time">${item.time}</div>
                    </div>
                `;
            });

            // Reiniciar animación al cambiar de pestaña
            contentDiv.style.animation = 'none';
            contentDiv.offsetHeight; // Refresco de DOM
            contentDiv.innerHTML = html;
            contentDiv.style.animation = 'scrollUp 45s linear infinite';
        }

        // Cargar categoría inicial (Macro)
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
