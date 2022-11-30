![alt](https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Logo_de_la_Copa_Mundial_de_f%C3%BAtbol_2022.svg/320px-Logo_de_la_Copa_Mundial_de_f%C3%BAtbol_2022.svg.png)
# Qatar 2022 API
Proyecto del ramo La Web de Datos CC7220-1 Primavera 2022.

Este proyecto tiene por objetivo implementar una API para obtener información sobre el mundial de fútbol de la FIFA de Qatar 2022 usando el *endpoint* del servicio de consultas de Wikidata ([WDQS](https://query.wikidata.org/)).

## Dependencias
Para este proyecto se necesita contar con los siguientes paquetes: **flask** y **requests**. Para obtenerlos basta con ejecutar el siguiente comando en la consola:

```console
pip install -r requierements.txt
```
## Ejecución de API
Para ejecutar el *backend* del proyecto se debe ejecutar el siguiente comando en la consola:

```console
py app.py
```

El cual estará hosteado por defecto en **localhost** (http://127.0.0.1:5000)

## Usos
La API cuenta con los siguientes casos de uso para obtener distinta información:

- Participantes:
  ```console
  localhost:5000/qatar2022/participants
  ```
- Estadios:
  ```console
  localhost:5000/qatar2022/stadiums
  ```
- Grupos:
  ```console
  localhost:5000/qatar2022/groups
  ```
  - Información de grupo <X>:
  ```console
  localhost:5000/qatar2022/group/info/<X>
  ```
  - Resultados de grupo <X>:
  ```console
  localhost:5000/qatar2022/group/results/<X>
  ```
  **X debe ser un valor dentro de la siguiente lista: [A, B, C, D, E, F, G o H]**

---

![Alt text](https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Wikidata_Stamp_Rec_Dark.svg/200px-Wikidata_Stamp_Rec_Dark.svg.png "Powered by Wikidata")
