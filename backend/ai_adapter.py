"""
Módulo de Adaptación, Clonación de Empaquetado e Ingeniería Inversa de Miniaturas
(ViralHunter Thumbnail & Video Reverse-Engineering Engine)
"""

import re
from typing import Dict, Any
from packaging_auditor import audit_packaging, generate_proven_hooks, generate_youtube_chapters_from_script, build_video_production_suite

def clean_title_for_entity(title: str) -> str:
    """Elimina ruido de clickbait para aislar la entidad temática central."""
    noise = [
        r'^\d+\s+', r'how to', r'why you should', r'the secret of', r'the truth about',
        r'what happens when', r'this is why', r'why', r'how', r'stop doing this',
        r'never do this', r'the man who', r'the reason', r'explained', r'documentary',
        r'\(.*?\)', r'\[.*?\]'
    ]
    t = title
    for p in noise:
        t = re.sub(p, '', t, flags=re.IGNORECASE)
    t = re.sub(r'[^\w\s]', '', t)
    return t.strip() or title

def adapt_video_to_spanish(video: Dict[str, Any]) -> Dict[str, Any]:
    """
    Desglosa el empaquetado completo del video:
    - Clonación y recreación de miniatura (Midjourney, Flux, Photopea)
    - 3 títulos en español de alto CTR
    - Gancho de 15 segundos para el guión
    - Escaleta de retención para video largo de 20 minutos
    - Estrategia de monetización y pausas publicitarias
    """
    title_orig = video.get("title", "")
    channel = video.get("channel_name", "")
    multiplier = video.get("multiplier", 1.0)
    views = video.get("views_formatted", "")
    video_id = video.get("video_id", "")
    rpm = video.get("estimated_rpm", 6.5)
    earnings = video.get("estimated_earnings_formatted", "$0 USD")

    t_lower = title_orig.lower()
    clean_entity = clean_title_for_entity(title_orig)
    
    # 1. IDENTIFICACIÓN DE NICHO Y SÍNTESIS VISUAL PRECISA
    if any(k in t_lower for k in ["stoic", "silence", "quiet", "alone", "men", "strong", "mind", "discipline", "marcus", "seneca", "epictetus"]):
        category = "Estoicismo & Psicología del Silencio"
        formula = "El Poder de la Contención y el Dominio Emocional"
        titles = [
            f"Hazte Tan Fuerte Que Tu Silencio Imponga Respeto (La Regla Oculta)",
            f"Por Qué Las Personas Inteligentes Hablan Poco y Observan Todo",
            f"La Razón Psicológica Por La Que El Silencio Destruye a Quien Te Ataca"
        ]
        hook = (
            "En la antigua Roma, los hombres más temidos jamás levantaban la voz ni respondían a una ofensa. "
            "Sabían un secreto que hoy casi todos han olvidado: cuando hablas, regalas tu poder; pero cuando callas, "
            "obligas a los demás a revelar sus debilidades. En los próximos minutos entenderás por qué tu silencio "
            "puede convertirse en tu arma más letal."
        )
        thumb_text = "CALLA Y OBSERVA"
        thumb_subject = f"intense dramatic close-up portrait of a weathered Roman philosopher ({clean_entity}), stoic emotional gravity, piercing gaze"
        thumb_bg = "dark atmospheric ancient Roman marble hall, stone pillars, subtle volumetric smoke"
        thumb_colors = "Fondo carbón profundo (#0B0F19), luz de recorte cenital fría (#60A5FA), texto amarillo flúor (#FACC15)"
        thumb_lighting = "dramatic chiaroscuro Rembrandt lighting, golden and cold steel rim light cutting through darkness"
        thumb_style = "hyperrealistic 8k cinematic photograph, Hasselblad camera, ultra-sharp detail"
        thumb_direction = (
            "1. Colocar al filósofo o busto en el tercio derecho mirando fijamente al espectador.\n"
            "2. Aplicar sombra pesada en el lado opuesto del rostro (iluminación Rembrandt).\n"
            "3. En el tercio izquierdo, colocar el texto 'CALLA Y OBSERVA' en amarillo flúor con trazo negro grueso."
        )

    elif any(k in t_lower for k in ["history", "empire", "war", "battle", "rome", "king", "queen", "emperor", "general", "tricked", "napoleon", "caesar", "alexander", "army", "conquer", "deception"]):
        category = "Biografías Ocultas & Crónicas Históricas"
        formula = "El Engaño Histórico y el Personaje Imposible"
        titles = [
            f"El Hombre Que Engañó a Todo Un Imperio y Nadie Pudo Detener",
            f"El Error Histórico De 5 Minutos Que Destruyó el Reino Más Poderoso",
            f"La Verdad Silenciada Sobre el Personaje Más Peligroso de la Historia"
        ]
        hook = (
            "Durante más de doscientos años, los libros de historia ocultaron lo que ocurrió realmente en esa habitación. "
            "Un solo hombre, sin ejército ni dinero, puso de rodillas a la dinastía más poderosa del mundo utilizando únicamente "
            "una mentira calculada. Lo que estás a punto de escuchar no te lo enseñaron en la escuela."
        )
        thumb_text = "EL GRAN ENGAÑO"
        thumb_subject = f"epic cinematic portrait of an imposing historical ruler or commander representing ({clean_entity}), intense cunning gaze, detailed period garments or battle armor"
        thumb_bg = "dark candlelit war room or moody battlefield with smoke, burning embers, dramatic atmosphere"
        thumb_colors = "Fondo rojo carmesí oscuro y negro (#180A0A), fuego dorado (#F59E0B), texto blanco con borde negro"
        thumb_lighting = "dramatic firelight and candlelight, deep Renaissance shadows, rim lighting"
        thumb_style = "cinematic historical oil painting style blended with 8k photorealism"
        thumb_direction = (
            "1. Fondo con silueta de palacio o mapa antiguo en tonos oscuros cálidos.\n"
            "2. Sujeto en el centro o tercio lateral mirando fijamente a la cámara con expresión calculadora.\n"
            "3. Texto 'EL GRAN ENGAÑO' en blanco nítido con trazo negro grueso de 18px para móviles."
        )

    elif any(k in t_lower for k in ["sleep", "brain", "body", "health", "habit", "food", "eat", "fatigue", "longevity", "heart", "dopamine", "fasting"]):
        category = "Salud, Longevidad & Biohacking"
        formula = "La Advertencia de Consecuencia Inmediata en Tu Cuerpo"
        titles = [
            f"Deja de Hacer Esto Antes de Dormir (Está Destruyendo Tu Cerebro)",
            f"El Hábito Silencioso Que Arruina Tu Energía a Diario y Nadie te Advierte",
            f"Los 3 Alimentos Que Creías Sanos Pero Inflaman Tu Sistema al Instante"
        ]
        hook = (
            "Si cada mañana te despiertas con el cuerpo pesado y la mente nublada a pesar de haber dormido ocho horas, no es casualidad. "
            "Hay un hábito casi invisible que repites todas las noches en tu habitación y que está engañando a tu sistema nervioso, "
            "bloqueando la reparación profunda de tus células. Presta mucha atención a esto."
        )
        thumb_text = "DEJA DE HACERLO"
        thumb_subject = f"hyper-detailed 3D anatomical visualization of human brain and neural pathways ({clean_entity}), glowing biological stress synapses"
        thumb_bg = "minimalist dark medical laboratory, deep black vignette, neural network bokeh"
        thumb_colors = "Fondo azul eléctrico ultra oscuro (#030712), zonas de alarma en rojo fuego (#EF4444), flecha amarilla neón (#FACC15)"
        thumb_lighting = "contrasting bio-luminescence, warning red alert glow paired with cool electric cyan"
        thumb_style = "hyper-realistic 3D Octane render, medical macro photography, 8k resolution"
        thumb_direction = (
            "1. Modelo 3D del órgano en el centro derecho con brillo interno.\n"
            "2. Flecha amarilla neón apuntando al área crítica o elemento detonante.\n"
            "3. Texto 'DEJA DE HACERLO' en rojo o amarillo en el costado izquierdo superior."
        )

    elif any(k in t_lower for k in ["money", "rich", "poor", "dollar", "wealth", "invest", "bank", "financial", "crypto", "bitcoin", "millionaire", "business"]):
        category = "Finanzas, Riqueza & Psicología del Dinero"
        formula = "La Regla de la Minoría vs la Trampa de las Masas"
        titles = [
            f"La Regla del 1% Que Mantiene al 99% en la Pobreza Sin Saberlo",
            f"Cómo Duplicar Tu Capacidad Financiera Sin Cambiar Tu Estilo de Vida",
            f"Las 3 Trampas del Sistema Que Te Hacen Pobre Aunque Ganes Más Dinero"
        ]
        hook = (
            "La mayoría de las personas creen que ganar más dinero resolverá sus problemas financieros, pero las estadísticas "
            "demuestran exactamente lo contrario. Los verdaderos creadores de riqueza no juegan bajo las reglas del banco ni del salario; "
            "aplican un principio contraintuitivo que mantiene su patrimonio blindado."
        )
        thumb_text = "LA TRAMPA OCULTA"
        thumb_subject = f"striking minimalist concept of extreme wealth and power ({clean_entity}), stark contrast of success vs destruction, sleek luxury aesthetics"
        thumb_bg = "dark modern luxury bank vault corridor with moody floor reflections, clean deep black shadows"
        thumb_colors = "Fondo negro mate (#09090B), verde esmeralda neón (#10B981) o rojo advertencia (#DC2626)"
        thumb_lighting = "dramatic architectural strip lighting, golden hour highlights, high contrast"
        thumb_style = "cinematic commercial photography, sleek 8k resolution, minimalist luxury"
        thumb_direction = (
            "1. Símbolo de pérdida o trampa visual en el tercio derecho.\n"
            "2. Texto 'LA TRAMPA OCULTA' en mayúsculas tipografía bold blanca.\n"
            "3. Alto contraste para que resalte en el feed principal de YouTube."
        )

    elif any(k in t_lower for k in ["ai", "tech", "robot", "future", "computer", "quantum", "space", "nvidia", "hacker", "matrix", "code"]):
        category = "Tecnología, IA & Futuro"
        formula = "La Disrupción Tecnológica Inminente"
        titles = [
            f"Lo Que Esta Tecnología Hará en los Próximos 12 Meses Te Va a Asustar",
            f"Por Qué el 90% de los Trabajos Cambiarán Por Completo (La Verdad Silenciada)",
            f"El Avance Oculto Que Nadie Está Discutiendo y Cambiará el Mundo"
        ]
        hook = (
            "Mientras todos miran los avances superficiales, en los laboratorios más herméticos del mundo acaba de ocurrir "
            "algo que cambia las reglas del juego para siempre. Si entiendes esto hoy, estarás 5 años por delante de la mayoría."
        )
        thumb_text = "EL FUTURO LLEGÓ"
        thumb_subject = f"futuristic glowing microprocessor or cybernetic interface representing ({clean_entity}), intricate glowing circuits"
        thumb_bg = "dark high-tech server room with glowing fiber optic cables and atmospheric haze"
        thumb_colors = "Fondo negro espacial (#05050A), neón cian láser (#00F5FF) y púrpura eléctrico (#A855F7)"
        thumb_lighting = "cyberpunk volumetric neon cyan and electric violet glow"
        thumb_style = "ultra sharp 8k macro photography, futuristic concept art, cinematic depth"
        thumb_direction = (
            "1. Elemento tecnológico central iluminado con resplandor neón.\n"
            "2. Texto 'EL FUTURO LLEGÓ' en cian brillante o blanco.\n"
            "3. Fondo oscuro y limpio para máximo impacto en dispositivos móviles."
        )

    else:
        category = "Misterios, Enigmas & Curiosidades Humanas"
        formula = "La Pregunta Sin Respuesta Evidente"
        titles = [
            f"¿Por Qué Nadie Habla De Esto? La Verdad Que Pocos Quieren Ver",
            f"El Fenómeno Oculto Que Explica Por Qué Casi Todos Cometen Este Error",
            f"Lo Que Descubrieron Tras Años de Silencio y Cambió Todo Por Completo"
        ]
        hook = (
            "Parece una simple casualidad hasta que analizas los patrones con detenimiento. Lo que estás a punto de ver "
            "desafía todas las explicaciones oficiales y fue ignorado durante décadas por una razón muy concreta."
        )
        thumb_text = "NADIE LO VIO"
        thumb_subject = f"cinematic dramatic focal subject capturing the essence of ({clean_entity}), intense psychological tension and curiosity"
        thumb_bg = "atmospheric moody cinematic environment with heavy fog and deep depth of field"
        thumb_colors = "Fondo azul medianoche (#020617), luz cian (#06B6D4) y texto blanco de alto impacto"
        thumb_lighting = "dramatic high-contrast rim lighting, cinematic color grading, studio illumination"
        thumb_style = "photorealistic 8k cinematic shot, clean composition, National Geographic documentary lighting"
        thumb_direction = (
            "1. Elemento intrigante o sujeto iluminado en el centro o tercio lateral.\n"
            "2. Alto contraste lumínico para guiar el ojo del espectador de inmediato.\n"
            "3. Texto 'NADIE LO VIO' en la esquina opuesta con borde negro sólido."
        )

    # Construcción de prompts para Midjourney y FLUX.1
    thumb_prompt = f"{thumb_subject}, {thumb_bg}, {thumb_lighting}, {thumb_style}, clean composition, 16:9 aspect ratio --ar 16:9 --style raw"
    thumb_bg_prompt = f"{thumb_bg}, {thumb_lighting}, {thumb_style}, empty central copy space for main subject, 16:9 aspect ratio --ar 16:9"

    # Escaleta minuto a minuto (20 minutos para maximizar RPM con múltiples midrolls)
    outline = [
        "⏱ 00:00 - 00:15 | EL GANCHO PSICOLÓGICO: Retener al 70%+ de la audiencia planteando la premisa extrema.",
        "⏱ 00:15 - 03:00 | EL CONTEXTO Y LA AMENAZA: Por qué este tema te afecta directamente a ti hoy.",
        "⏱ 03:00 - 08:00 | CASO REAL O ANÉCDOTA HISTÓRICA: El ejemplo indiscutible que demuestra la teoría.",
        "⏱ 08:00 - 14:00 | EL GIRO CONTRAINTUITIVO (1ra Pausa Midroll): La explicación de por qué lo que todos creen está mal.",
        "⏱ 14:00 - 18:00 | LAS LEYES O PASOS PRÁCTICOS (2da Pausa Midroll): Las reglas aplicables que el espectador debe recordar.",
        "⏱ 18:00 - 20:00 | CONCLUSIÓN MEMORABLE & CTA: Cierre con frase de impacto y recomendación del siguiente video."
    ]

    # Auditoría de empaquetado (Linter título + miniatura de yt-package)
    packaging_audit = audit_packaging(titles[0] if titles else title_orig, thumb_text)

    # 3 Ganchos probados de 15 segundos con fórmulas de hooks.json
    proven_hooks = generate_proven_hooks(title_orig, clean_entity, category)

    # Capítulos con marcas de tiempo para YouTube (chapters.py)
    youtube_chapters = generate_youtube_chapters_from_script(title_orig, 1200)

    # Suite de producción completa de video (InVideo AI, ChatGPT/Claude, ElevenLabs, Runway/Kling)
    video_production = build_video_production_suite(
        title=titles[0] if titles else title_orig,
        clean_entity=clean_entity,
        category=category,
        hook=hook,
        outline=outline
    )

    return {
        "category": category,
        "psychological_formula": formula,
        "original_video": {
            "title": title_orig,
            "channel": channel,
            "views": views,
            "multiplier": multiplier,
            "video_id": video_id,
            "thumbnail_hd": f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg",
            "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
            "estimated_rpm": f"${rpm:.2f} USD",
            "estimated_earnings": earnings
        },
        "spanish_titles": titles,
        "packaging_audit": packaging_audit,
        "hook_15s": hook,
        "proven_hooks": proven_hooks,
        "youtube_chapters": youtube_chapters,
        "video_production": video_production,
        "thumbnail_cloner": {
            "hook_text": thumb_text,
            "subject": thumb_subject,
            "color_palette": thumb_colors,
            "midjourney_prompt": thumb_prompt,
            "background_prompt": thumb_bg_prompt,
            "art_direction": thumb_direction,
            "photopea_editor_url": "https://www.photopea.com"
        },
        "outline_20min": outline,
        "monetization_strategy": (
            f"Con un video de 20 minutos en este nicho ({category}) y un RPM estimado de ${rpm:.2f} USD, "
            f"puedes colocar hasta 3 pausas publicitarias (minuto 4, minuto 9 y minuto 15), multiplicando por 2.5x los ingresos habituales de un video corto."
        )
    }
