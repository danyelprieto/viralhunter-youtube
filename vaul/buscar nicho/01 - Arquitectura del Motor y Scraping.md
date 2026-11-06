# ⚙️ 01 - Arquitectura del Motor y Scraping

Detalles técnicos sobre cómo la herramienta extrae información de YouTube sin bloqueos, sin pagar API keys y con alta velocidad.

---

## 1. El Problema de la API Oficial de YouTube (Google Cloud)
* La API oficial de YouTube (v3) impone una cuota estricta de **10.000 unidades gratuitas por día**.
* Una sola búsqueda (`search.list`) consume **100 unidades**.
* Eso significa que con la API oficial solo se podrían hacer 100 búsquedas al día antes de que Google empiece a cobrar o corte el servicio.

---

## 2. Nuestra Solución: Motor Híbrido (Scrapetube + YouTube Innertube)
En lugar de depender de cuotas limitadas de Google Cloud, implementamos un motor en Python basado en **Innertube / Scrapetube**:
* **Sin API Key requerida:** Utiliza los endpoints internos públicos que el propio reproductor web de YouTube usa.
* **Búsquedas Ilimitadas:** No hay límite de 100 búsquedas diarias.
* **Extracción de Metadatos Críticos:**
  * `videoId`: Identificador único del video.
  * `title`: Título exacto en el idioma original.
  * `thumbnails`: URL de la miniatura en máxima resolución (`maxresdefault.jpg` / `hqdefault.jpg`).
  * `viewCount`: Vistas exactas o formateadas.
  * `publishedTimeText`: Fecha relativa (ej. *"hace 2 semanas"*, *"hace 1 mes"*).
  * `channelTitle`: Nombre del creador.
  * `channelId`: Identificador del canal para consultar su volumen de suscriptores.

---

## 3. Flujo de Datos
```
Usuario ingresa Nicho ("Stoicism", "Biographies", etc.)
          │
          ▼
Motor Scrapetube (Query en YouTube)
          │
          ▼
Extracción de Videos + Filtro de Duración (> 20 min)
          │
          ▼
Cálculo de Outlier Multiplier (Vistas / Base del canal)
          │
          ▼
Ordenamiento descendente por Viralidad (ej. 45x, 22x, 10x)
          │
          ▼
Panel Frontend Interactivo (Tarjetas visuales oscuras)
          │
          ▼
Botón "Adaptar al Español" -> Títulos, Gancho de 15s y Prompt Miniatura
```
