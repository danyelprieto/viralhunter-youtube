"""
Servidor API REST y Servidor Web Local para ViralHunter
Puerto: 8500 | Sin dependencias externas pesadas | Integración con Obsidian
"""

import os
import sys
import json
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from fastapi import FastAPI, HTTPException, Body, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from core_engine import search_niche_outliers, get_niche_catalog, get_video_transcript
from ai_adapter import adapt_video_to_spanish

app = FastAPI(title="ViralHunter - YouTube Outlier Engine", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
DATA_DIR = os.path.join(BASE_DIR, "data")
FAVORITES_FILE = os.path.join(DATA_DIR, "favorites.json")
GENERATED_DIR = os.path.join(DATA_DIR, "generated_thumbnails")
OBSIDIAN_VAULT_FILES = [
    os.path.join(BASE_DIR, "baul_obsidian", "05 - Registro de Nichos y Canales Ganadores.md"),
    os.path.join(BASE_DIR, "vaul", "buscar nicho", "05 - Registro de Nichos y Canales Ganadores.md")
]

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(GENERATED_DIR, exist_ok=True)
if not os.path.exists(FAVORITES_FILE):
    with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

# --- ENDPOINTS API ---

@app.get("/api/niches")
def api_get_niches():
    """Devuelve el catálogo de nichos ganadores de alto RPM y baja saturación."""
    try:
        return get_niche_catalog()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search")
def api_search_niche(
    q: str = Query("the man who tricked history documentary", description="Palabra clave o consulta en inglés"),
    max_subs: int = Query(250000, description="Tope de suscriptores del canal (0 = sin límite)"),
    min_duration: float = Query(0.0, description="Duración mínima en minutos"),
    max_duration: float = Query(0.0, description="Duración máxima en minutos (0 = sin límite)"),
    min_views: int = Query(5000, description="Mínimo de visualizaciones"),
    max_views: int = Query(0, description="Máximo de visualizaciones (0 = sin límite)"),
    date_filter: str = Query("all", description="Filtro de fecha: 24h, 7d, 30d, 90d, 365d, all"),
    sort_by: str = Query("multiplier", description="Ordenamiento: multiplier, velocity, views, date"),
    limit: int = Query(40, description="Cantidad máxima de videos a inspeccionar")
):
    try:
        search_res = search_niche_outliers(
            keyword=q,
            max_subscribers=max_subs,
            min_duration_minutes=min_duration,
            max_duration_minutes=max_duration,
            min_views=min_views,
            max_views=max_views,
            date_filter=date_filter,
            sort_by=sort_by,
            limit=limit
        )
        return {
            "query": q,
            "count": search_res.get("count", 0),
            "relaxed_notice": search_res.get("relaxed_notice"),
            "filters": {
                "max_subscribers": max_subs,
                "min_duration_minutes": min_duration,
                "max_duration_minutes": max_duration,
                "min_views": min_views,
                "max_views": max_views,
                "date_filter": date_filter,
                "sort_by": sort_by
            },
            "results": search_res.get("results", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/transcript")
def api_get_transcript(video_id: str = Query(..., description="ID del video de YouTube")):
    """Obtiene la transcripción hablada completa del video."""
    res = get_video_transcript(video_id)
    return res

@app.post("/api/adapt")
def api_adapt_video(payload: dict = Body(...)):
    """Disección completa, clonación de miniatura y adaptación de empaquetado."""
    video = payload.get("video", {})
    if not video:
        raise HTTPException(status_code=400, detail="Faltan datos del video a adaptar.")
    adaptation = adapt_video_to_spanish(video)
    return adaptation

@app.get("/api/favorites")
def api_get_favorites():
    try:
        with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

@app.post("/api/favorites")
def api_save_favorite(payload: dict = Body(...)):
    video = payload.get("video", {})
    adaptation = payload.get("adaptation", None)
    if not video:
        raise HTTPException(status_code=400, detail="Datos de video incompletos.")

    # 1. Guardar en JSON local
    try:
        favs = []
        if os.path.exists(FAVORITES_FILE):
            with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
                favs = json.load(f)
        
        # Evitar duplicados por video_id
        if not any(f.get("video", {}).get("video_id") == video.get("video_id") for f in favs):
            entry = {
                "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "video": video,
                "adaptation": adaptation
            }
            favs.insert(0, entry)
            with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
                json.dump(favs, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[ERROR] Guardando favorito en JSON: {e}")

    # 2. Registrar automáticamente en la Bóveda de Obsidian
    try:
        title = video.get("title", "")
        channel = video.get("channel_name", "")
        multiplier = video.get("multiplier", 1.0)
        views = video.get("views_formatted", "")
        subs = video.get("subscribers_formatted", "")
        url = video.get("youtube_url", "")
        rpm = video.get("estimated_rpm_formatted", "$6.00 USD")
        earnings = video.get("estimated_earnings_formatted", "$0 USD")
        velocity = video.get("views_per_day_formatted", "")
        badge = video.get("badge", "OUTLIER")

        s_titles = adaptation.get("spanish_titles", ["Sin adaptar"]) if adaptation else ["Sin adaptar"]
        hook = adaptation.get("hook_15s", "No generado") if adaptation else "No generado"
        cloner = adaptation.get("thumbnail_cloner", {}) if adaptation else {}
        midjourney_prompt = cloner.get("midjourney_prompt", "No generado")
        thumb_text = cloner.get("hook_text", "")
        thumb_hd = video.get("maxres_thumbnail_url", "")

        md_block = f"""
### ⭐ [{badge}] {title}
* **Canal:** `{channel}` ({subs} subs)
* **Vistas Totales:** **{views}** | **Velocidad:** **{velocity}**
* **Multiplicador:** **{multiplier}x** | **RPM Estimado:** {rpm} | **Ganancias Est.:** **{earnings}**
* **Enlace YouTube:** [{url}]({url})
* **Miniatura HD Original:** [Ver Miniatura HD]({thumb_hd})

#### 🎯 Títulos Virales Adaptados al Español:
1. *{s_titles[0]}*
{f"2. *{s_titles[1]}*" if len(s_titles) > 1 else ""}
{f"3. *{s_titles[2]}*" if len(s_titles) > 2 else ""}

#### ⚡ Gancho de 15 Segundos (Hook Hablado):
> "{hook}"

#### 🎨 Laboratorio de Clonación de Miniatura:
* **Texto Sugerido:** `{thumb_text}`
* **Prompt para Midjourney / Flux:**
```text
{midjourney_prompt}
```

* **Fecha de Registro:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---
"""
        for vault_file in OBSIDIAN_VAULT_FILES:
            if os.path.exists(os.path.dirname(vault_file)):
                with open(vault_file, "a", encoding="utf-8") as f:
                    f.write(md_block)
    except Exception as e:
        print(f"[ERROR] Guardando en Obsidian: {e}")

    return {"status": "success", "message": "Video guardado exitosamente en tus Favoritos y en la Bóveda de Obsidian."}

@app.get("/api/thumbnail-proxy")
def api_thumbnail_proxy(video_id: str):
    """Descarga la miniatura de YouTube en el servidor y la devuelve en Base64 sin problemas de CORS."""
    import urllib.request
    import base64
    urls = [
        f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg",
        f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
    ]
    for u in urls:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=6) as resp:
                if resp.status == 200:
                    data = resp.read()
                    b64 = base64.b64encode(data).decode("utf-8")
                    return {
                        "status": "success",
                        "video_id": video_id,
                        "data_url": f"data:image/jpeg;base64,{b64}",
                        "content_type": "image/jpeg"
                    }
        except Exception:
            continue
    raise HTTPException(status_code=404, detail="No se pudo obtener la miniatura de YouTube.")

@app.post("/api/save-generated-thumbnail")
def api_save_generated_thumbnail(payload: dict = Body(...)):
    """Guarda la miniatura recreada con IA en disco y la enlaza en la Bóveda de Obsidian."""
    import base64
    video_id = payload.get("video_id", "unknown")
    image_base64 = payload.get("image_base64", "")
    prompt = payload.get("prompt", "")
    overlay_text = payload.get("overlay_text", "")
    title = payload.get("title", "Video")

    if not image_base64:
        raise HTTPException(status_code=400, detail="Faltan datos de la imagen.")

    try:
        # Limpiar encabezado base64 si viene con data:image/jpeg;base64,
        if "," in image_base64:
            image_base64 = image_base64.split(",")[1]

        image_bytes = base64.b64decode(image_base64)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"thumb_{video_id}_{timestamp}.jpg"
        file_path = os.path.join(GENERATED_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(image_bytes)

        # Registrar en Obsidian
        md_block = f"""
#### 🖼 Miniatura Recreada con IA ({datetime.now().strftime("%Y-%m-%d %H:%M")}):
* **Video:** {title} (`{video_id}`)
* **Texto Aplicado:** `{overlay_text}`
* **Prompt Utilizado:**
> {prompt}

* **Archivo Local:** `{file_path}`

---
"""
        for vault_file in OBSIDIAN_VAULT_FILES:
            if os.path.exists(os.path.dirname(vault_file)):
                with open(vault_file, "a", encoding="utf-8") as f:
                    f.write(md_block)

        return {
            "status": "success",
            "message": "Miniatura guardada en disco y registrada en Obsidian.",
            "filename": filename,
            "url": f"/thumbnails/{filename}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Servir Frontend y Miniaturas Generadas
if os.path.exists(GENERATED_DIR):
    app.mount("/thumbnails", StaticFiles(directory=GENERATED_DIR), name="thumbnails")

if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def serve_index():
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "ViralHunter API activa. Acceda a la interfaz frontend."}
