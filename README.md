# Calculadora Interactiva de Ganancias en Trading

Esta aplicación interactiva permite calcular ganancias potenciales al operar con instrumentos financieros como criptomonedas o acciones. Utiliza datos históricos de precios obtenidos de Yahoo Finance y considera parámetros personalizados como tarifas, impuestos y montos de inversión. La aplicación está construida con Python y Streamlit, proporcionando una interfaz gráfica intuitiva.

## ¿Cómo funciona?

1. **Entrada de parámetros:**
   - Introduce un ticker financiero (e.g., `BTC-USD`, `AAPL`).
   - Define el monto a invertir en dólares.
   - Especifica tarifas opcionales, como las de blockchain, y la tasa de impuestos.

2. **Procesamiento:**
   - Descarga datos históricos de precios (5 días, intervalos de 1 minuto).
   - Calcula los rangos extremos de precios según probabilidades específicas (10%, 20%, 30%).
   - Ajusta los cálculos para incluir tarifas de eToro (1% en compra y venta).

3. **Resultados:**
   - Visualiza precios históricos en gráficos interactivos.
   - Muestra las ganancias potenciales ajustadas por tarifas e impuestos.
   - Descarga los resultados en formato CSV.

## Requerimientos

Para utilizar esta aplicación, asegúrate de tener instalado Python 3.7 o superior y las siguientes bibliotecas:

- `numpy`
- `pandas`
- `yfinance`
- `matplotlib`
- `streamlit`

Instálalas con:
```bash
pip install numpy pandas yfinance matplotlib streamlit
