# Calculadora Moderna - Python

Versión de la calculadora reimplementada en **Python** usando **tkinter** (librería estándar).

## Características

✅ Interfaz idéntica a la versión JavaScript  
✅ Operaciones matemáticas básicas (+, −, ×, ÷)  
✅ Funciones adicionales (%, ±, AC)  
✅ Diseño moderno con tema oscuro  
✅ Respuestas a errores (división por cero)  

## Requisitos

- Python 3.7+
- tkinter (incluido por defecto en la mayoría de instalaciones de Python)

## Cómo ejecutar

```bash
python calculator.py
```

O si tienes Python 3 instalado como `python3`:

```bash
python3 calculator.py
```

## API de Calculadora en Python

La API está en `calculator_api.py` usando Flask.

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Ejecutar la API

```bash
python calculator_api.py
```

La API quedará disponible en `http://localhost:5000`.

### Endpoint

- `POST /api/calc`
  - JSON body para operaciones binarias:
    - `action`: `add`, `subtract`, `multiply`, `divide`
    - `left`: número
    - `right`: número
  - JSON body para operaciones de valor único:
    - `action`: `percent`, `toggle-sign`
    - `value`: número

### Ejemplo de payload

```json
{
  "action": "add",
  "left": 5,
  "right": 3
}
```

### Ejemplo de respuesta

```json
{
  "result": 8
}
```

## Uso desde otra web

- `external_example.html` muestra un ejemplo que consume la API desde un navegador.
- Solo abre `external_example.html` en tu navegador y asegúrate de que la API esté corriendo en `http://localhost:5000`.

## Archivos

- **calculator.py** - La aplicación completa de la calculadora en Python con tkinter
- **calculator_api.py** - API REST para las operaciones de la calculadora
- **external_example.html** - Ejemplo de web que consume la API
- **app.js** - Lógica original en JavaScript adaptada a la API
- **index.html** - Interfaz web original
- **styles.css** - Estilos CSS originales
- **requirements.txt** - Dependencias para la API

## Diferencias con la versión JavaScript

La lógica de cálculo es idéntica, pero ahora la calculadora web puede pedir resultados a una API Python. La UI puede usar `POST /api/calc` para obtener respuestas desde el servidor.
