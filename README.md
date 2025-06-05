# Never-Broke-Again-
# 📊 Plataforma Integral de Análisis Financiero

Aplicación interactiva en Python y Streamlit para el análisis cuantitativo de portafolios multi-activo y activos individuales.  
Permite visualizar métricas, gráficos y retornos de los periodos recientes, así como descargar datos y reportes clave para trading, finanzas cuantitativas y experimentación académica.

> Desarrollado por **Juan Camilo Hernández Quintero** como base para investigaciones, proyectos académicos y tesis en finanzas cuantitativas.

---

## 🚀 Funcionalidades principales

- **Análisis de portafolios completos**: Selecciona entre portafolios temáticos (acciones, FX, cripto, índices, sectores, etc.) y obtén métricas agregadas, retornos, correlaciones, gráficas y features para IA.
- **Análisis individual de activos**: Analiza cualquier símbolo (acción, ETF, forex, cripto, índice) con métricas clave, indicadores técnicos y gráficos avanzados.
- **Enfoque en los datos recientes**: Visualización de los últimos 10 registros y cálculo del retorno total para el periodo seleccionado.
- **Descarga de archivos**: Exporta datos diarios, métricas resumen y gráficos en CSV/PNG.
- **Extracción de features para IA/trading algorítmico**: Exportación directa en CSV de features técnicos listos para modelos cuantitativos.

---

## ⚙️ Tecnologías utilizadas

- Python 3.8+
- Streamlit
- yfinance
- pandas, numpy, matplotlib

---

## 🏗️ Estructura de la aplicación

- **Tabs/Pestañas**: Elige entre análisis de portafolios o individual.
- **Inputs visuales**: Selección de portafolio, símbolo, fechas y ejecución con un click.
- **Resultados en pantalla**: Métricas, gráficos, correlaciones, features, y retornos recientes.
- **Descargas directas**: Datos, métricas y gráficos.

---

## 💡 Ejemplo de flujo de trabajo

1. Elige la pestaña “Análisis de Portafolio” o “Análisis Individual”.
2. Configura portafolio/símbolo y fechas de análisis.
3. Haz click en “Lanzar análisis”.
4. Visualiza:
    - Retornos y métricas de los últimos días.
    - Retorno total para el periodo seleccionado.
    - Métricas cuantitativas (volatilidad, Sharpe, drawdown, etc).
    - Gráficos de evolución y precio con indicadores técnicos.
    - Features avanzados para IA o backtesting.
5. Descarga tus archivos desde la misma app.
6. (Opcional) Los archivos se almacenan también localmente en carpetas por análisis.

---

## 🛠️ Instalación y ejecución

1. **Instala Python y dependencias:**
   ```bash
   pip install streamlit yfinance pandas numpy matplotlib
Guarda el archivo principal, por ejemplo:
plataforma_financiera_app.py

Ejecuta la app en tu terminal/cmd:

bash
Copy
Edit
streamlit run plataforma_financiera_app.py
Abre tu navegador en http://localhost:8501

🗺️ Roadmap (futuras extensiones)
Optimización de portafolios (Markowitz, Black-Litterman, etc).

Backtesting y simulación de estrategias.

Portafolios personalizados (tickers y pesos a medida).

Integración de más indicadores técnicos.

Dashboards y reportes en PDF.

Machine Learning y modelos de predicción.

Hosting multiusuario en la nube (Streamlit Cloud, AWS).

📃 Licencia
Desarrollado por Juan Camilo Hernández Quintero para uso académico y personal.
Abierto a la colaboración y extensión en investigación, docencia y prototipado.

📬 Contacto
¿Dudas, ideas o propuestas de colaboración?
jc-hernandez@javeriana.edu.co

🙏 Créditos y agradecimientos
Comunidad Python de análisis financiero y ciencia de datos.

Streamlit, yfinance, pandas, numpy, matplotlib.

Inspirado en recursos de QuantInsti y foros académicos de trading cuantitativo.

yaml
Copy
Edit

---

¿Quieres que agregue imágenes, ejemplos de outputs o algún apartado especial?  
¿Prefieres la estructura en inglés o con badges de GitHub?  
¡Solo dime!
