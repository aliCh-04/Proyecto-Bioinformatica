## Instrucciones para ejecutar el proyecto

1. Instalar Visual Studio y Python según sea necesario
https://visualstudio.microsoft.com/es/downloads/
https://www.python.org/downloads/

2. Clonar el proyecto
Abrir Visual Studio -> Hacer click en "Clonar un repositorio" -> Pegar el link del repositorio https://github.com/aliCh-04/Proyecto-Bioinformatica.git en "Ubicación del repositorio" y clonar

3. Abrir la terminal
Abrir el proyecto clonado -> Hacer click en "Ver" en la barra superior -> Hacer click en "Terminal" entre las opciones que aparecen

4. Ejectuar el ensamblador
Asegúrate de estar en la raíz del proyecto. Por ejemplo, "C:\Users\john\source\repos\Proyecto-Bioinformatica"

Desde ahí, compila el proyecto, por ejemplo con la combinación de teclas ctrl + shift + b. Esto debería crear la carpeta x64 en la raíz del proyecto con el ejecutable del ensamblador. 

Con los pasos anteriores hechos, ejecuta el comando "python python/experimentacion.py". Esto correrá tanto el ensamblador en c++ como el código en python para exportar y mostrar los resultados del ensamblado. Asegúrate de que la ruta al archivo "experimentacion.py" es la correcta. Si estás en la raíz del proyecto como se indicó antes, será la indica anteriormente en este párrafo. 

Una vez finalice la ejecución, los resultados estarán en la carpeta "resultados". 

## Detalles sobre la ejecución

En la rama master que es la que debería usarse para probar el proyecto, está ya el dataset completo pasado a fasta, con 5x de cobertura y 0.01 de error. 

El ensamblador se ejecuta para k = 51 y k = 61, y toma alrededor de 5 minutos (puede haber diferencias en función del sistema que lo ejecute). 

Los resultados, una vez finalizado, se guardarán en la carpeta "resultados". Estos resultados incluyen los archivos de contigs generados para cada k, imágenes con gráficas de las distintas métricas, y un archivo .csv con los resultados para cada k de todas las métricas. 
