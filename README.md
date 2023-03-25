# Reto técnico Data Engineering



## General
|  |  |
|-----------------------|:--------------|
| **Fecha de Presentación** : |25/03/2023 |
| **Nombre de Webservice** :|	DailyForecast_MX|
|**Presentado Por** :|	Kevin Javier Guevara Ortiz|


## Observaciones

- Debido a que el webservice presenta intermitencia, se usa como backup de consulta el servicio FTP que también se encuentra expuesto para la extracción de los datos requeridos. La aplicación inteta traer los datos desde el webservice, en caso de no obtener resultado, procede a extraerlos desde el FTP.
- En la carpeta data se almacenara todos los resultados de la solución. Se crea estructura de datos según zona y fecha de procesamiento como path principales, y en el interior se almacena la información en formato .csv solicitada en cada uno de los puntos: municipios_average (Punto 2), merge (Punto 3), current (Punto 4)
- Todo el proyecto se ejecuta mediante el main.py, el cual se encarga de usar el DataService que tiene 3 objetos principales, dataextraction, dataprocess y datawriter. Estos 3 objetos se encargan de realizar las tareas correspondientes a cada etapa del pipeline y que se encuentran comentadas en cada uno de ellos.
- El log de la solución se guarda en la carpeta log que se encuentra en la raíz del proyecto y cuyo nombre es main.log.
- Para iniciar el proyecto se debe instalar dependencias mediante el comando "python -m pip install -r requirements.txt" y posteriormente ejecutar main.py. 
Si desean también se puede usar docker para la ejecución, usando los comandos expuestos a continuación:
 ```
  docker build -t forecastdata .
  docker run -d forecastdata
  ```
- Lo anterior construira la imagen y posteriormente la correra en modo detach, siempre y cuando se tenga docker instalado de manera local.
## Preguntas Adicionales

- [x] Mejoras
  - [x] Uso de BD para almacenamiento o bucket en Cloud
  - [x] Uso de Cloudwatch para la ejecución de tarea programada con lambdas
  - [x] Migración de aplicación a un webservices que sea desplegado en kubernetes, así la tarea programada se podría hacer mediante un llamado al webservice, evitando el monolito.
- [x] Trabajo en equipo
  - [x] Documentación de la solución en Confluence o herramientas similares para que los compañeros puedan ver y entender la solución.
  - [x] Uso de git para control de cambios. Uso de herramienta como Gitlab para Gestión de trabajos, despliegue continúo de la aplicación y configuración.
  - [x] Uso de entorno cloud combinado con Gitlab u otra herramienta que permita realizar CI/CD
