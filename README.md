# 💶 Gestor de Gastos Estudiantil (CRUD)

Aplicación de consola interactiva diseñada para registrar, gestionar y analizar gastos personales de forma organizada, visual y mensual. Permite realizar operaciones CRUD completas, visualizar datos en ventanas gráficas independientes, recibir alertas de presupuesto en tiempo real y exportar informes detallados, todo ello manteniendo un flujo no bloqueante y una arquitectura modular.

## 📦 Librería Externa Utilizada y Finalidad
El proyecto utiliza **dos librerías externas instaladas mediante `pip`**, con un rol central en la experiencia y funcionalidad de la aplicación:

- **`matplotlib`**: Librería profesional de visualización de datos. Se encarga de generar gráficos de barras interactivos que muestran la distribución de gastos por categoría. El gráfico se abre en una ventana nativa del sistema para permitir su análisis detallado sin saturar la terminal.
- **`colorama`**: Librería de formato de terminal multiplataforma. Se utiliza para aplicar colores y estilos a los mensajes de la consola, diferenciando visualmente operaciones exitosas, errores, validaciones y alertas de déficit presupuestario.

*(Nota: `tkinter` también se utiliza para renderizar la tabla de gastos en ventana interactiva, pero forma parte de la librería estándar de Python y no requiere instalación externa).*

## 🛠️ Instrucciones para Instalar las Dependencias
1. Abre una terminal o consola dentro de la carpeta raíz del proyecto.
2. Asegúrate de tener Python 3.9 o superior instalado (`python --version`).
3. Ejecuta el siguiente comando para instalar las librerías externas listadas en `librerias.txt`:

   ```bash
   pip install -r librerias.txt
   ```

## ▶️ Instrucciones para Ejecutar la Aplicación
Una vez instaladas las dependencias, inicia el programa con:

```bash
python principal.py
```
La aplicación arrancará en modo interactivo. Para finalizar la ejecución de forma segura, selecciona la opción 9. 🚪 Salir desde el menú o pulsa Ctrl+C.

## 📖 Descripción General del Funcionamiento
El gestor organiza los gastos por mes y año, guardando toda la información de forma persistente en archivos JSON locales. Al iniciar, solicita o carga automáticamente el presupuesto configurado para el mes actual, evitando peticiones repetitivas en futuras sesiones.

### 🔄 Flujo de Uso y Opciones
1. 📋 Ver lista completa: Abre una ventana interactiva con tkinter que muestra todos los registros en formato tabla. Incluye ordenación y un indicador superior con el estado financiero del mes actual (presupuesto, gastado y restante o déficit).
2. ➕ Registrar nuevo gasto: Solicita cantidad del gasto, categoría, descripción y fecha. Valida cada entrada y tras guardarlo, muestra automáticamente una alerta con el estado del presupuesto.
3. ✏️ Editar gasto existente: Muestra la tabla de gastos, pide el ID y permite modificar una cantidad de gasto, categoría, fecha o descripción. Aplica las mismas validaciones y actualiza el estado financiero.
4. 🗑️ Eliminar gasto: Muestra la tabla, solicita el ID y pide confirmación (s/n) antes de borrar. Tras la eliminación, recalcula los gastos y muestra la cantidad del presupuesto y si queda margen o si hay déficit.
5. 📊 Resumen + Gráfico visual: Genera un informe mensual y abre automáticamente un gráfico de barras con matplotlib para visualizar la distribución por categoría.
6. 💾 Exportar resumen a TXT: Guarda el informe mensual en un archivo .txt dentro de la carpeta reportes/ que se puede consultar o imprimir.
7. 📅 Filtrar por mes/año: Permite consultar gastos de cualquier mes histórico o futuro introduciendo el formato YYYY-MM. Carga o solicita el presupuesto asociado a ese periodo.
8. 💰 Configurar/Cambiar presupuesto: Permite actualizar el límite mensual de presupuesto de cualquier mes.
9. 🚪 Salir: Cierra la aplicación.
