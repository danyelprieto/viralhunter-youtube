"""
Motor de Búsqueda, Filtrado Avanzado y Catálogo de Nichos de YouTube (ViralHunter Core)
Inspirado en la mecánica de Viralyt.ai (Adrián Sáenz & Eric)
Sin cuotas de API keys · Scraping concurrente y análisis en tiempo real
"""

import urllib.request
import re
import time
import socket
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any, Optional
import scrapetube
from youtube_transcript_api import YouTubeTranscriptApi

# Forzar timeout global estricto para evitar bloqueos en servidores en la nube
socket.setdefaulttimeout(3.0)

# Caché en memoria de suscriptores para no repetir requests al mismo canal.
# El valor es None cuando YouTube no dejó verificar el número: nunca
# inventar un número por defecto, porque eso falsifica el multiplicador.
CHANNEL_SUBS_CACHE: Dict[str, Optional[int]] = {}

# =========================================================================
# CATÁLOGO DE NICHOS GANADORES EN TENDENCIA (Alto RPM & Potencial Arbitraje)
# =========================================================================

NICHE_CATALOG = [
    {
        "id": "cronovidas_historia",
        "name": "Crónicas Ocultas y Biografías Oscuras (Cronovidas)",
        "category": "Historia y Documentales",
        "description": "Historias reales, enigmas históricos y personajes siniestros u olvidados. Altísima retención en videos de +20 minutos.",
        "rpm": 6.5,
        "rpm_range": "$5.00 - $8.50",
        "competition": "Baja",
        "saturation": "22%",
        "avg_multiplier": "18.5x",
        "opportunity_score": 96,
        "keywords": ["the man who tricked history", "forgotten historical figures documentary", "shocking ancient deception", "mysterious historical events"],
        "primary_query": "the man who tricked history documentary"
    },
    {
        "id": "estoicismo_psicologia",
        "name": "Estoicismo & Psicología Oscura del Silencio",
        "category": "Desarrollo Personal & Filosofía",
        "description": "Fórmulas de poder mental, autocontrol y leyes del silencio inspiradas en Marco Aurelio y Robert Greene.",
        "rpm": 7.2,
        "rpm_range": "$6.00 - $9.50",
        "competition": "Media",
        "saturation": "38%",
        "avg_multiplier": "21.0x",
        "opportunity_score": 94,
        "keywords": ["stoic rules of silence", "why quiet people are dangerous", "psychology of emotional control", "rules of stoicism in silence"],
        "primary_query": "stoic rules of silence"
    },
    {
        "id": "biohacking_sueno",
        "name": "Biohacking, Longevidad & Optimización del Sueño",
        "category": "Salud & Neurociencia",
        "description": "Ciencia del descanso profundo, reparación celular y hábitos nocturnos. Gran nicho anglosajón poco traducido al español.",
        "rpm": 9.5,
        "rpm_range": "$8.00 - $12.00",
        "competition": "Baja",
        "saturation": "19%",
        "avg_multiplier": "24.0x",
        "opportunity_score": 98,
        "keywords": ["habits that destroy deep sleep", "neuroscience sleep protocol", "brain repair habits before bed", "how to fix chronic fatigue"],
        "primary_query": "habits that destroy deep sleep protocol"
    },
    {
        "id": "ia_automatizacion",
        "name": "Inteligencia Artificial & Negocios Automatizados",
        "category": "Tecnología & Emprendimiento",
        "description": "Canales automatizados, herramientas de IA emergentes y modelos de monetización digital. Anunciantes corporativos de alto pago.",
        "rpm": 13.5,
        "rpm_range": "$10.00 - $17.00",
        "competition": "Media-Alta",
        "saturation": "48%",
        "avg_multiplier": "15.0x",
        "opportunity_score": 90,
        "keywords": ["ai tools nobody knows", "build faceless automated youtube", "ai business workflow 2026", "automated business software ai"],
        "primary_query": "ai tools nobody knows about automated"
    },
    {
        "id": "finanzas_arbitraje",
        "name": "Finanzas Personales, Deuda & Psicología del Dinero",
        "category": "Finanzas & Economía",
        "description": "El nicho rey en monetización publicitaria. Revelaciones sobre bancos, ahorro agresivo y mentalidad del 1%.",
        "rpm": 16.5,
        "rpm_range": "$12.00 - $22.00",
        "competition": "Alta",
        "saturation": "60%",
        "avg_multiplier": "14.2x",
        "opportunity_score": 88,
        "keywords": ["how banks keep you poor", "rules of money rich 1 percent", "habits keeping middle class poor", "financial traps to avoid"],
        "primary_query": "how banks keep people poor rules of money"
    },
    {
        "id": "misterios_arqueologia",
        "name": "Civilizaciones Perdidas & Enigmas Inexplicables",
        "category": "Misterio & Arqueología",
        "description": "Adicción pura a la curiosidad. Desata los multiplicadores virales más descomunales (>50x en canales de menos de 50k subs).",
        "rpm": 5.2,
        "rpm_range": "$4.00 - $7.00",
        "competition": "Baja",
        "saturation": "25%",
        "avg_multiplier": "27.5x",
        "opportunity_score": 95,
        "keywords": ["forbidden ancient structures discovery", "unexplained archaeological anomalies", "lost civilizations forgotten history", "deep ocean mysteries solved"],
        "primary_query": "forbidden ancient structures discovery documentary"
    },
    {
        "id": "crimen_interrogatorios",
        "name": "Psicología Criminal & Análisis de Interrogatorios",
        "category": "True Crime & Comportamiento",
        "description": "Análisis de mentiras, lenguaje corporal de sospechosos y casos policiales resueltos tras décadas de misterio.",
        "rpm": 4.8,
        "rpm_range": "$3.80 - $6.50",
        "competition": "Media",
        "saturation": "42%",
        "avg_multiplier": "19.5x",
        "opportunity_score": 91,
        "keywords": ["detective interrogation body language", "criminal confession caught in lie", "unsolved mystery solved after 30 years", "police interview psychology"],
        "primary_query": "detective interrogation psychology confession caught"
    },
    {
        "id": "estrategia_militar",
        "name": "Secretos Militares & Engaños Que Cambiaron Guerras",
        "category": "Estrategia & Tácticas",
        "description": "Operaciones encubiertas, tácticas de desinformación militar y armas secretas abandonadas. Audiencia masculina muy leal.",
        "rpm": 5.8,
        "rpm_range": "$4.50 - $7.50",
        "competition": "Muy Baja",
        "saturation": "16%",
        "avg_multiplier": "28.0x",
        "opportunity_score": 97,
        "keywords": ["military deception that tricked the enemy", "biggest blunders in military history", "secret military operations abandoned", "ingenious wartime tactics"],
        "primary_query": "ingenious military deception tactics history"
    }
]

def get_niche_catalog() -> List[Dict[str, Any]]:
    return NICHE_CATALOG

# =========================================================================
# PARSERS DE TEXTO Y DATOS DE YOUTUBE
# =========================================================================

def parse_views_text(text: str) -> int:
    if not text:
        return 0
    t = text.upper().replace("VIEWS", "").replace("VISTAS", "").replace("VISUALIZACIONES", "").strip()
    try:
        if "M" in t:
            num = float(t.replace("M", "").replace(",", ".").strip())
            return int(num * 1_000_000)
        elif "K" in t:
            num = float(t.replace("K", "").replace(",", ".").strip())
            return int(num * 1_000)
        else:
            clean = "".join(c for c in t if c.isdigit())
            return int(clean) if clean else 0
    except Exception:
        return 0

def parse_duration_text(text: str) -> float:
    if not text:
        return 0.0
    try:
        parts = text.strip().split(":")
        if len(parts) == 2:
            return int(parts[0]) + int(parts[1]) / 60.0
        elif len(parts) == 3:
            return int(parts[0]) * 60 + int(parts[1]) + int(parts[2]) / 60.0
    except Exception:
        pass
    return 0.0

def parse_published_to_days(text: str) -> int:
    """Convierte «3 weeks ago», «3w ago», «2mo ago», «8h ago»... a días.

    YouTube/scrapetube devuelve casi siempre la forma abreviada
    («3w ago», «2mo ago», «3d ago», «3y ago»), no la forma larga
    («3 weeks ago»). La versión anterior solo entendía la forma larga,
    así que casi todos los videos quedaban en 9999 y el filtro de fecha
    (30d, 90d...) nunca filtraba nada. Devuelve 9999 solo si el texto
    no se puede interpretar de ninguna forma.
    """
    if not text:
        return 9999
    t = text.lower().strip()
    # Quitar prefijos tipo "streamed", "premiered", "hace"
    t = re.sub(r'^(streamed|premiered|hace)\s+', '', t)
    m = re.search(r'(\d+(?:\.\d+)?)', t)
    if not m:
        return 9999
    num = float(m.group(1))

    # Orden importa: "mo" (meses) antes que "m" (minutos), "min" antes que "mo".
    if re.search(r'\b\d+(?:\.\d+)?\s*(months?|mos?|mo|meses?|mes)\b', t):
        return int(num * 30)
    if re.search(r'\b\d+(?:\.\d+)?\s*(years?|yrs?|y|años?|anos?)\b', t):
        return int(num * 365)
    if re.search(r'\b\d+(?:\.\d+)?\s*(weeks?|w|semanas?)\b', t):
        return int(num * 7)
    if re.search(r'\b\d+(?:\.\d+)?\s*(days?|d|días?|dias?)\b', t):
        return int(num)
    if re.search(r'\b\d+(?:\.\d+)?\s*(hours?|hrs?|h|horas?)\b', t):
        return 0
    if re.search(r'\b\d+(?:\.\d+)?\s*(minutes?|mins?|min|minutos?)\b', t):
        return 0
    if re.search(r'\b\d+(?:\.\d+)?\s*(seconds?|secs?|s|segundos?)\b', t):
        return 0
    return 9999

def parse_subs_string(text: str) -> Optional[int]:
    """Convierte «1.2M», «850K»... a número. Devuelve None si no se puede leer."""
    if not text:
        return None
    t = text.upper().replace("SUSCRIPTORES", "").replace("SUBSCRIBERS", "").replace("SUBS", "").strip()
    try:
        if "M" in t:
            num = float(t.replace("M", "").replace(",", ".").strip())
            return int(num * 1_000_000)
        elif "K" in t or "MIL" in t:
            clean_num = t.replace("MIL", "").replace("K", "").replace(",", ".").strip()
            num = float(clean_num)
            return int(num * 1_000)
        else:
            clean = "".join(c for c in t if c.isdigit())
            return int(clean) if clean else None
    except Exception:
        return None

def fetch_single_channel_subscribers(channel_handle_or_url: str) -> Optional[int]:
    """Extrae suscriptores reales de un canal forzando headers en inglés.

    Devuelve None cuando YouTube no deja leer el número (bloqueo,
    consentimiento, timeout o formato nuevo). Antes devolvía 15.000
    inventados, y ese número falso generaba todos los multiplicadores
    (390x, 265x...) que se vieron en la app. Nunca inventar un número:
    sin verificar no hay multiplicador. Se respeta el timeout de nube
    de Omar (2.5 s, 128 KB, cookie SOCS).
    """
    if not channel_handle_or_url:
        return None

    if channel_handle_or_url in CHANNEL_SUBS_CACHE:
        return CHANNEL_SUBS_CACHE[channel_handle_or_url]

    clean = channel_handle_or_url.strip()
    if clean.startswith("http"):
        url = clean
    elif clean.startswith("UC"):
        url = f"https://www.youtube.com/channel/{clean}"
    elif clean.startswith("/channel/"):
        url = f"https://www.youtube.com{clean}"
    elif clean.startswith("/@"):
        url = f"https://www.youtube.com{clean}"
    elif clean.startswith("@"):
        url = f"https://www.youtube.com/{clean}"
    else:
        url = f"https://www.youtube.com/{clean}"

    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': 'SOCS=CAESEwgDEgk2MTQ5Mjc4NjcaAmVuIAEaBgiA_LyaBg;'
        }
    )

    subs: Optional[int] = None
    try:
        with urllib.request.urlopen(req, timeout=2.5) as resp:
            # Leer solo los primeros 128 KB para no bloquear hilos en la nube
            html = resp.read(131072).decode('utf-8', errors='ignore')
            patterns = [
                r'([0-9\.,]+[KMBkmb]?)\s*(?:subscribers|suscriptores)',
                r'"subscriberCountText":\{"accessibility":\{"accessibilityData":\{"label":"([^"]+)"',
                r'"subscriberCount":"(\d+)"',
                r'subscriberCountText[^0-9]*([0-9\.,]+[KMBkmb]?)',
            ]
            for pat in patterns:
                m = re.search(pat, html, re.IGNORECASE)
                if m:
                    parsed = parse_subs_string(m.group(1))
                    if parsed is not None:
                        subs = parsed
                        break
    except Exception:
        subs = None

    CHANNEL_SUBS_CACHE[channel_handle_or_url] = subs
    return subs

def resolve_subscribers_in_parallel(channel_handles: List[str]) -> Dict[str, Optional[int]]:
    """Resuelve en paralelo los suscriptores de múltiples canales con ThreadPool acotado."""
    unique_handles = list(set(h for h in channel_handles if h))
    needed = [h for h in unique_handles if h not in CHANNEL_SUBS_CACHE][:8]
    
    if needed:
        with ThreadPoolExecutor(max_workers=min(len(needed), 4)) as executor:
            executor.map(fetch_single_channel_subscribers, needed)

    return {h: CHANNEL_SUBS_CACHE.get(h) for h in unique_handles}

def estimate_niche_rpm(keyword: str, title: str) -> float:
    combined = f"{keyword} {title}".lower()
    if any(k in combined for k in ["money", "bank", "wealth", "invest", "poor", "rich", "dollar", "finance", "dinero", "finanzas"]):
        return 16.50
    elif any(k in combined for k in ["ai", "tools", "business", "software", "code", "automate", "chatgpt"]):
        return 13.50
    elif any(k in combined for k in ["sleep", "brain", "health", "fatigue", "biohacking", "longevity", "sueño", "salud"]):
        return 9.50
    elif any(k in combined for k in ["stoic", "stoicism", "quiet", "silence", "psychology", "men", "mind"]):
        return 7.20
    elif any(k in combined for k in ["history", "empire", "tricked", "emperor", "war", "battle", "deception", "military"]):
        return 6.00
    elif any(k in combined for k in ["crime", "police", "interrogation", "detective", "murder", "unsolved"]):
        return 4.80
    elif any(k in combined for k in ["mystery", "ancient", "pyramid", "archaeology", "civilization"]):
        return 5.20
    else:
        return 4.50

# =========================================================================
# MOTOR DE BÚSQUEDA ELÁSTICO (Resuelve en < 2.5s y nunca queda en blanco)
# =========================================================================

def parse_raw_video_item(v: dict) -> Optional[dict]:
    """Extrae datos base de un video devuelto por scrapetube."""
    video_id = v.get("videoId")
    if not video_id:
        return None

    # Título
    title = ""
    if "title" in v and "runs" in v["title"] and len(v["title"]["runs"]) > 0:
        title = v["title"]["runs"][0].get("text", "")
    elif "title" in v and "simpleText" in v["title"]:
        title = v["title"].get("simpleText", "")

    # Duración
    length_text = ""
    if "lengthText" in v:
        length_text = v["lengthText"].get("simpleText", "")
    duration_min = parse_duration_text(length_text)

    # Vistas
    view_count_text = ""
    if "viewCountText" in v:
        view_count_text = v["viewCountText"].get("simpleText", "")
    elif "shortViewCountText" in v:
        view_count_text = v["shortViewCountText"].get("simpleText", "")
    views = parse_views_text(view_count_text)

    # Fecha
    published_text = ""
    if "publishedTimeText" in v:
        published_text = v["publishedTimeText"].get("simpleText", "")
    days_ago = parse_published_to_days(published_text)

    # Canal
    channel_name = "Canal"
    channel_handle = ""
    if "ownerText" in v and "runs" in v["ownerText"] and len(v["ownerText"]["runs"]) > 0:
        channel_name = v["ownerText"]["runs"][0].get("text", "Canal")
        endpoint = v["ownerText"]["runs"][0].get("navigationEndpoint", {})
        canonical = endpoint.get("browseEndpoint", {}).get("canonicalBaseUrl", "")
        browse_id = endpoint.get("browseEndpoint", {}).get("browseId", "")
        channel_handle = canonical if canonical else browse_id

    # Miniaturas
    hq_thumb = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
    maxres_thumb = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
    thumbnail_url = hq_thumb
    if "thumbnail" in v and "thumbnails" in v["thumbnail"] and len(v["thumbnail"]["thumbnails"]) > 0:
        thumbnail_url = v["thumbnail"]["thumbnails"][-1].get("url", hq_thumb)

    return {
        "video_id": video_id,
        "title": title,
        "thumbnail_url": thumbnail_url,
        "maxres_thumbnail_url": maxres_thumb,
        "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
        "views": views,
        "duration_min": duration_min,
        "duration_text": length_text or f"{round(duration_min)}m",
        "published_text": published_text or "Reciente",
        "days_ago": days_ago,
        "channel_name": channel_name,
        "channel_handle": channel_handle
    }

def search_niche_outliers(
    keyword: str,
    max_subscribers: int = 250000,
    min_duration_minutes: float = 0.0,
    max_duration_minutes: float = 0.0,
    min_views: int = 25000,
    max_views: int = 0,
    date_filter: str = "all",
    sort_by: str = "multiplier",
    limit: int = 40
) -> Dict[str, Any]:
    """
    Motor elástico de búsqueda:
    1. Escanea rápidamente hasta 45 videos de YouTube (tarda < 1.5s).
    2. Resuelve suscriptores de canales en paralelo.
    3. Si los filtros del usuario son tan extremos que dan 0 resultados,
       aplica un rescate inteligente para mostrar los mayores outliers reales del nicho.
    """
    max_days = {
        "24h": 1,
        "7d": 7,
        "30d": 30,
        "90d": 90,
        "365d": 365,
        "all": 999999
    }.get(date_filter, 999999)

    raw_candidates = []
    # Escaneamos los primeros 25 videos de YouTube para máxima velocidad (< 1 segundo)
    try:
        videos_gen = scrapetube.get_search(keyword, results_type="video")
        for i, v in enumerate(videos_gen):
            if i >= 25:
                break
            parsed = parse_raw_video_item(v)
            if parsed:
                raw_candidates.append(parsed)
    except Exception as e:
        print(f"[ERROR ENGINE] Error en scrapetube: {e}")

    if not raw_candidates:
        return {
            "query": keyword,
            "count": 0,
            "strict_count": 0,
            "is_relaxed": False,
            "relaxed_notice": None,
            "results": []
        }

    # Resolver suscriptores en paralelo para todos los canales únicos escaneados (tarda solo ~1.5 segundos con 12 hilos)
    needed_handles = list(set(c["channel_handle"] for c in raw_candidates if c.get("channel_handle")))
    subs_map = resolve_subscribers_in_parallel(needed_handles)

    # Construir lista completa con cálculos de multiplicadores.
    # Si los suscriptores no se pudieron verificar, NO hay multiplicador:
    # multiplier=None, badge "SIN VERIFICAR" y subscribers_formatted
    # "sin verificar". Mostrar un multiplicador inventado es peor que no
    # mostrar ninguno.
    enriched_videos = []
    for item in raw_candidates:
        ch_handle = item["channel_handle"]
        subs = subs_map.get(ch_handle)
        subs_verified = subs is not None and subs > 0
        views = item["views"]
        days_ago = item["days_ago"]

        if subs_verified:
            multiplier = round(views / subs, 1)
            if multiplier >= 20.0:
                badge = "🔥 MEGA OUTLIER"
                badge_class = "badge-mega"
            elif multiplier >= 5.0:
                badge = "⚡ VIRAL"
                badge_class = "badge-viral"
            elif multiplier >= 1.5:
                badge = "📈 TENDENCIA"
                badge_class = "badge-trend"
            else:
                badge = "⚪ REGULAR"
                badge_class = "badge-regular"
        else:
            multiplier = None
            badge = "❓ SIN VERIFICAR"
            badge_class = "badge-regular"

        # Velocidad solo si la fecha es conocida; con days_ago=9999 no se
        # puede calcular vistas/día y antes salía un número sin sentido.
        if days_ago is not None and days_ago < 9999:
            velocity_days = max(days_ago, 1)
            views_per_day = int(views / velocity_days)
            views_per_hour = round(views_per_day / 24.0, 1)
        else:
            views_per_day = 0
            views_per_hour = 0.0

        rpm = estimate_niche_rpm(keyword, item["title"])
        earnings = round((views / 1000.0) * rpm, 2)

        enriched_videos.append({
            **item,
            "views_formatted": f"{views:,}".replace(",", "."),
            "subscribers": subs if subs_verified else 0,
            "subscribers_formatted": f"{subs:,}".replace(",", ".") if subs_verified else "sin verificar",
            "subscribers_verified": subs_verified,
            "multiplier": multiplier,
            "badge": badge,
            "badge_class": badge_class,
            "views_per_day": views_per_day,
            "views_per_day_formatted": f"{views_per_day:,}".replace(",", "."),
            "views_per_hour": views_per_hour,
            "estimated_rpm": rpm,
            "estimated_rpm_formatted": f"${rpm:.2f} USD",
            "estimated_earnings": earnings,
            "estimated_earnings_formatted": f"${round(earnings):,} USD".replace(",", ".")
        })

    # INTENTO 1: Filtrado estricto con los parámetros pedidos por el usuario.
    # Un video solo pasa si CUMPLE el filtro: fecha desconocida (9999) no
    # pasa un filtro de fecha, y suscriptores sin verificar no pasan un
    # filtro de suscriptores, porque no se puede comprobar que lo cumpla.
    filtered = []
    for v in enriched_videos:
        # Duración
        if min_duration_minutes > 0 and v["duration_min"] < min_duration_minutes:
            continue
        if max_duration_minutes > 0 and v["duration_min"] > max_duration_minutes:
            continue
        # Vistas
        if min_views > 0 and v["views"] < min_views:
            continue
        if max_views > 0 and v["views"] > max_views:
            continue
        # Fecha
        if v["days_ago"] > max_days:
            continue
        # Suscriptores: solo cuentan los verificados
        if max_subscribers > 0 and (not v["subscribers_verified"] or v["subscribers"] > max_subscribers):
            continue

        filtered.append(v)

    strict_count = len(filtered)
    relaxed_notice = None
    is_relaxed = False

    # INTENTO 2: Si el filtro estricto dio 0 resultados, rescate explícito.
    # Antes el rescate se mezclaba con los resultados como si cumplieran
    # los filtros. Ahora queda marcado: strict_count=0, is_relaxed=True,
    # cada video lleva "relaxed": True y el aviso dice que NO cumplieron
    # los filtros y que hay que revisar fecha y duración de cada uno.
    if len(filtered) == 0:
        is_relaxed = True
        relaxed_notice = (
            f"💡 Ajuste Inteligente: 0 resultados cumplieron todos tus filtros "
            f"(fecha, vistas, duración y suscriptores verificados) en este nicho. "
            f"Se muestran videos de rescate de este tema, SIN aplicar esos filtros "
            f"— revisa la duración y la fecha de cada uno:"
        )
        for v in enriched_videos:
            if v["views"] >= 10000:
                rescued = dict(v)
                rescued["relaxed"] = True
                filtered.append(rescued)

        # Si aún no hay suficientes, mantener canales chicos verificados
        if len(filtered) == 0:
            filtered = [
                dict(v, relaxed=True) for v in enriched_videos
                if v["subscribers_verified"] and (max_subscribers == 0 or v["subscribers"] <= max_subscribers)
            ]

    # Ordenamiento: los multiplicadores sin verificar (None) van al final,
    # nunca arriba por un número inventado.
    if sort_by == "velocity":
        filtered.sort(key=lambda x: x["views_per_day"], reverse=True)
    elif sort_by == "views":
        filtered.sort(key=lambda x: x["views"], reverse=True)
    elif sort_by == "date":
        filtered.sort(key=lambda x: x["days_ago"], reverse=False)
    else:  # "multiplier"
        filtered.sort(key=lambda x: (x["multiplier"] is not None, x["multiplier"] or 0), reverse=True)

    return {
        "query": keyword,
        "count": len(filtered[:limit]),
        "strict_count": strict_count,
        "is_relaxed": is_relaxed,
        "relaxed_notice": relaxed_notice,
        "results": filtered[:limit]
    }

# =========================================================================
# EXTRACCIÓN DE TRANSCRIPCIÓN OFICIAL
# =========================================================================

def get_video_transcript(video_id: str) -> Dict[str, Any]:
    try:
        api = YouTubeTranscriptApi()
        transcript_data = api.fetch(video_id, languages=['en', 'es', 'en-US', 'es-419', 'en-GB'])
        
        full_text_lines = []
        timeline = []
        for item in transcript_data:
            text = item.text.strip()
            if text:
                full_text_lines.append(text)
                start_sec = int(item.start)
                minutes = start_sec // 60
                seconds = start_sec % 60
                timeline.append({
                    "time": f"{minutes:02d}:{seconds:02d}",
                    "seconds": start_sec,
                    "text": text
                })
        
        full_script = " ".join(full_text_lines)
        return {
            "status": "success",
            "video_id": video_id,
            "has_transcript": True,
            "total_snippets": len(timeline),
            "full_script": full_script,
            "timeline": timeline[:60]
        }
    except Exception as e:
        return {
            "status": "error",
            "video_id": video_id,
            "has_transcript": False,
            "error_msg": f"Este video no tiene subtítulos públicos activados: {str(e)}",
            "full_script": "No disponible para este video.",
            "timeline": []
        }
