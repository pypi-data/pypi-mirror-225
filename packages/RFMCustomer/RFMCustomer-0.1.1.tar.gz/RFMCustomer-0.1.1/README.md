<div>
    <a href="https://www.linkedin.com/in/sebastianurdaneguibisalaya/">
        <img src="https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white">
    </a>
    <a href="https://medium.com/@sebasurdanegui">
        <img src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white">
    </a>
    <img src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white">
    <img src="https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white">
    <img src="https://img.shields.io/badge/jupyter-%23000000.svg?style=for-the-badge&logo=jupyter&logoColor=white">
    <img src="https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white">
<div>


# **Segmentación RFM** 📊🤓
El presente repositorio tiene como objetivo la creación y explicación del funcionamiento de la librería ***RFMSegmentation*** 📊 en Python que es capaz de recibir input de las transacciones comerciales de los clientes para retornar como output una segmentación RFM para la óptima toma de decisiones empresariales.

## **Teoría Segmentación RFM**
**RFM** (Recency, Frequency and Monetary). Básicamente, es un score para la segmentación de los consumidores enfocado en el análisis de la compra reciente, la frecuencia y el monto de la compra por parte del cliente. 🛒 **En líneas generales, su función es utilizar los patrones de consumo del cliente para identificar el segmento al cual pertenece 🧑‍🤝‍🧑**. 

**Contexto para el ejemplo:**

La empresa desea realizar una segmentación RFM y toma como fecha de corte el 14 de agosto de 2023.
Sebastian es cliente de SportShoes S.A.C. Él realizó su última compra el 8 de agosto de 2023. Desde que realizó la primera compra del producto de la empresa hasta la fecha de corte, Sebastian realizó 9 compras con un monto total de S/. 5,000.00. 

1. **Recency** 
   
   ¿Hace cuánto el cliente realizó su última compra?
   
   ***Ejemplo:*** Sebastian realizó su última compra hace 6 días.
2. **Frequency**
   
   ¿Cuál es la frecuencia de compra del cliente?

   ***Ejemplo:***  Sebastian tiene una cantidad de órdenes total de 9 veces.
3. **Monetary**
   
   ¿Cuánto dinero gastó el cliente en sus compras en el establecimiento?

   **Ejemplo:** Sebastian gastó en total S/. 5,000.00 en la compra de productos de la empresa SportShoes S.A.C. (En ocasiones, suele usarse el promedio de los montos de compra.)

## **Pasos para el uso de la librería RFMSegmentation**

1. Abrir un notebook en Google Colab (también puedes usar VSCode, Anaconda o cualquier IDE). <a href="https://colab.research.google.com/?hl=es">Clic aquí</a>
2. Luego de abrir el entorno de Google Colab, debemos inicializar el entorno e importar las librerías.
<div>
<img src="./img/img_connect.png">
</div>

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

<div>
<img src="./img/img2.png">
</div>

1. Después, debemos instalar la librería **RFMCustomer**
```python
pip install RFMCustomer==0.0.3
```
<div>
<img src="./img/img1.png">
</div>

### **¡Perfecto, podemos hacer uso de la librería!**





Debes renombrar las columnas que serán necesarias para el uso de la librería.
Debes identificar en las columnas del dataframe que hagan referencia a la identificación del consumidor, el día en que se ejecutó la venta del producto o el día en que se generó la fecha de orden, una columna de venta total (precio por cantidad) por registro, en el caso no se cuente la columna de venta total se debe generar una columna y, por último, elegir una columna que no tenga valores nulos, puede ser la columna de identificación del registro.

```python
data = data.rename(columns = {
    'Identificación del consumidor' : 'Customer ID',
    'Día en que se ejecutó la venta' : 'Date',
    'Venta Total' : 'Sales',
    'Identificación del registo' : 'Order ID'
})
```

```python
data["Order Date"] = pd.to_datetime(data["Order Date"]).dt.strftime("%Y%m%d")
data = data.rename(columns = {'Order Date':'Date'})
```

```python
rfm = Segmentation.RFM(data, '20190115', positions = [1,2,5,17])
Segmentation.RFMTable(rfm)
Segmentation.RFMAnalysis(rfm)
Segmentation.RFMFindClientsBySegment(rfm, "Hola")
```