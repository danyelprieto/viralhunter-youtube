"""
ViralPackaging & Hook Auditor
Inspirado en la ingeniería de packaging de youtube-agent-skill (Jake Schincariol)
Adaptado para canales en Español y flujos de trabajo de arbitraje de contenido.
"""

import re
from typing import Dict, Any, List

# Palabras de parada y filtros
STOP_WORDS_ES = {
    'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'de', 'del', 'para',
    'en', 'con', 'por', 'su', 'sus', 'tu', 'tus', 'y', 'o', 'que', 'como', 'por que',
    'este', 'esta', 'estos', 'estas', 'al', 'a', 'sobre', 'todo', 'todos'
}

VAGUE_WORDS_ES = {
    'increíble', 'increible', 'asombroso', 'loco', 'brutal', 'enorme', 'masivo',
    'definitivo', 'mejor', 'poderoso', 'secreto', 'revolucionario', 'perfecto', 'completo'
}

FILLER_WORDS_ES = {
    'básicamente', 'literalmente', 'bueno', 'hola', 'amigos', 'bienvenidos', 'hoy',
    'video', 'suscríbete', 'canal', 'dale like', 'comenta'
}

CONCRETE_REGEX = re.compile(
    r'\b(\d[\d,.]*\s?(%|k|m|x|s|m|h)?|\$\d|\d+\s?(segundo|minuto|hora|día|semana|mes|año)s?)\b', 
    re.I
)
YOU_REGEX = re.compile(r'\b(tú|tu|tus|te|ti|usted|contigo)\b', re.I)
STAKE_REGEX = re.compile(r'\b(perder|pierdes|arruina|destruye|grave|error|peligro|costo|riesgo|deja|nunca|muerte|fracaso|trampa|alerta)\b', re.I)
CURIOSITY_REGEX = re.compile(r'\b(por qué|cómo|qué|cuál|hasta|antes|pero|nadie|casi|excepto|razón|secreto|oculto|verdad|silencio)\b', re.I)


def audit_packaging(title: str, thumb_text: str = "") -> Dict[str, Any]:
    """
    Audita la dupla Título + Miniatura como UNA sola unidad:
    - Comprueba corte en móviles (~40 caracteres)
    - Comprueba duplicación de palabras entre título y miniatura
    - Verifica especificidad numérica y penaliza palabras vagas
    """
    t = title.strip()
    n = len(t)
    issues = []
    good = []
    
    # 1. Longitud de pantalla móvil y escritorio
    if n > 100:
        issues.append("Límite crítico: más de 100 caracteres se cortará en casi todas las plataformas.")
    elif n > 60:
        issues.append(f"{n} caracteres: la búsqueda de escritorio corta títulos a los 60 caracteres.")
    else:
        good.append(f"{n} caracteres: dentro del límite visual ideal de escritorio (menos de 60).")
        
    mobile_preview = t
    if n > 40:
        mobile_cut = t[:40].rsplit(" ", 1)[0]
        mobile_preview = mobile_cut + "..."
        issues.append(f'En el feed del móvil se verá como: "{mobile_preview}" (asegúrate de que el sujeto principal no quede cortado).')
    else:
        good.append(f"Perfecto para móviles: el título completo ({n} caracteres) cabe en la pantalla sin puntos suspensivos.")

    # 2. Mayúsculas excesivas
    caps = [w for w in t.split() if len(w) > 2 and w.isupper()]
    if len(caps) > 2:
        issues.append(f"{len(caps)} palabras en mayúsculas sostenidas: el algoritmo puede penalizarlo como spam/clickbait.")
    elif caps:
        good.append(f"{len(caps)} palabra en mayúsculas para énfasis estratégico.")

    # 3. Números y especificidad
    nums = re.findall(r'\d[\d,.]*%?', t)
    if nums:
        good.append(f"Contiene cifra concreta ({', '.join(nums[:2])}), lo cual eleva el CTR hasta un 30%.")
    else:
        issues.append("Sin cifra ni fecha específica (reemplazar una palabra por un número aumenta el clic).")

    # 4. Duplicación entre Título y Miniatura (Regla de oro de yt-package)
    if thumb_text:
        title_words = set(re.findall(r'[a-z0-9áéíóúüñ]+', t.lower())) - STOP_WORDS_ES
        thumb_words = set(re.findall(r'[a-z0-9áéíóúüñ]+', thumb_text.lower())) - STOP_WORDS_ES
        shared = title_words & thumb_words
        
        if shared:
            issues.append(
                f"La miniatura duplica palabras del título ({', '.join(sorted(shared))}). "
                "La miniatura debe aportar curiosidad complementaria, no repetir el título."
            )
        else:
            good.append("Excelente: la miniatura y el título usan palabras distintas, maximizando el área de impacto.")
            
        thumb_word_count = len(re.findall(r'[a-z0-9áéíóúüñ]+', thumb_text.lower()))
        if thumb_word_count > 4:
            issues.append(f"La miniatura tiene {thumb_word_count} palabras: en la pantalla del celular el máximo legible son 3 a 4 palabras.")
        else:
            good.append(f"Texto de miniatura conciso ({thumb_word_count} palabras), ideal para teléfonos móviles.")

    score = max(0, min(100, 100 - (len(issues) * 14) + (len(good) * 5)))
    rating = "EXCELENTE" if score >= 80 else "BUENO" if score >= 60 else "MEJORABLE"

    return {
        "title": t,
        "thumb_text": thumb_text,
        "chars": n,
        "score": score,
        "rating": rating,
        "mobile_preview": mobile_preview,
        "issues": issues,
        "good": good
    }


def score_spanish_hook(text: str) -> Dict[str, Any]:
    """
    Califica un gancho hablado de 15 segundos con los 5 pilares de hookscore.py:
    1. Especificidad (cifras vs generalizaciones)
    2. Apelación directa ('Tú')
    3. Riesgo / Costo / Stakes
    4. Curiosidad (pregunta abierta sin respuesta prematura)
    5. Brevedad (ritmo de habla para 15 segundos)
    """
    words = re.findall(r'[a-z0-9áéíóúüñ]+', text.lower())
    n_words = len(words)
    if n_words == 0:
        return {"verdict": 0, "band": "MEJORABLE", "parts": {}, "weakest": "Vacio"}
    
    # 1. Especificidad
    nums = len(CONCRETE_REGEX.findall(text))
    filler = sum(1 for w in words if w in FILLER_WORDS_ES)
    spec = max(0, min(100, 40 + (nums * 25) - (filler * 15)))
    
    # 2. Apelación directa
    n_you = len(YOU_REGEX.findall(text))
    first_you = 30 if any(w in YOU_REGEX.findall(' '.join(words[:6])) for w in words[:6]) else 0
    addr = max(0, min(100, 30 + (n_you * 15) + first_you))
    
    # 3. Consecuencia / Riesgo
    n_stake = len(STAKE_REGEX.findall(text))
    stakes = max(0, min(100, 30 + (n_stake * 25)))
    
    # 4. Curiosidad
    n_cur = len(CURIOSITY_REGEX.findall(text))
    q = 15 if text.strip().endswith('?') else 0
    curiosity = max(0, min(100, 30 + (n_cur * 20) + q))
    
    # 5. Brevedad (15-35 palabras para 15 segundos a 150wpm)
    if 15 <= n_words <= 35:
        brev = 100
    elif n_words < 15:
        brev = max(30, 100 - (15 - n_words) * 8)
    else:
        brev = max(20, 100 - (n_words - 35) * 5)
        
    vals = [spec, addr, stakes, curiosity, brev]
    verdict = round(0.6 * (sum(vals) / len(vals)) + 0.4 * min(vals))
    band = "FUERTE" if verdict >= 72 else "BUENO" if verdict >= 52 else "MEJORABLE"

    parts = {
        "Especificidad": spec,
        "Apelación Directa": addr,
        "Riesgo / Consecuencia": stakes,
        "Curiosidad": curiosity,
        "Ritmo (15s)": brev
    }
    weakest = min(parts, key=parts.get)

    return {
        "verdict": verdict,
        "band": band,
        "word_count": n_words,
        "parts": parts,
        "weakest": weakest
    }


def generate_proven_hooks(title: str, entity: str, category: str) -> List[Dict[str, Any]]:
    """
    Genera 3 opciones de ganchos usando las 21 fórmulas probadas de hooks.json:
    - Fórmula 1: Contrarian Flip (Rompe la creencia común)
    - Fórmula 2: The Mistake (El error que comete la mayoría)
    - Fórmula 3: The Statistic / Case Result (Dato concreto o caso de impacto)
    """
    e = entity or "este tema"
    
    # Hook 1: Contrarian Flip
    script_1 = (
        f"Casi todos creen que para dominar {e} necesitas años de esfuerzo o suerte. "
        f"Pero los registros demuestran exactamente lo contrario: cuando dejas de seguir a la masa, "
        f"tu mente cambia en menos de 7 días. Presta atención a esto."
    )
    score_1 = score_spanish_hook(script_1)
    
    # Hook 2: The Mistake
    script_2 = (
        f"Hay un error silencioso que estás cometiendo ahora mismo con {e} y que destruye tus resultados. "
        f"El 95% de las personas jamás se dan cuenta hasta que es demasiado tarde. "
        f"En este video te revelo cómo detenerlo hoy mismo."
    )
    score_2 = score_spanish_hook(script_2)

    # Hook 3: The Statistic / Case
    script_3 = (
        f"En la historia de {e}, un solo hombre logró lo que un ejército entero no pudo en 20 años. "
        f"Sin dinero y sin ayuda, utilizó una sola regla psicológica que hoy está a punto de cambiar tu perspectiva."
    )
    score_3 = score_spanish_hook(script_3)

    return [
        {
            "formula_name": "Contrarian Flip (El Giro Contraintuitivo)",
            "formula_id": "contrarian-flip",
            "script": script_1,
            "score": score_1["verdict"],
            "band": score_1["band"],
            "diagnostics": score_1
        },
        {
            "formula_name": "The Mistake (El Error Invisible)",
            "formula_id": "the-mistake",
            "script": script_2,
            "score": score_2["verdict"],
            "band": score_2["band"],
            "diagnostics": score_2
        },
        {
            "formula_name": "The Result / The Case (El Caso Histórico Imposible)",
            "formula_id": "someone-elses-result",
            "script": script_3,
            "score": score_3["verdict"],
            "band": score_3["band"],
            "diagnostics": score_3
        }
    ]


def generate_youtube_chapters_from_script(transcript_text: str, duration_sec: int = 1200) -> str:
    """
    Genera marcas de tiempo oficiales para la descripción de YouTube siguiendo las reglas de chapters.py:
    - Empieza en 00:00
    - Al menos 3 capítulos
    - Cada capítulo con al menos 10 segundos de separación
    """
    total_min = max(5, duration_sec // 60)
    
    c1 = "00:00 - Introducción & Gancho Psicológico"
    c2 = f"01:30 - El Error Común que Todos Cometen"
    c3 = f"04:45 - El Caso Real y los Registros Ocultos"
    c4 = f"09:15 - El Giro Contraintuitivo que Nadie Espera"
    c5 = f"14:00 - Las 3 Reglas para Aplicar en tu Vida"
    c6 = f"{total_min - 2:02d}:00 - Conclusión y Pregunta Clave"

    return "\n".join([c1, c2, c3, c4, c5, c6])


def build_video_production_suite(title: str, clean_entity: str, category: str, hook: str, outline: List[str]) -> Dict[str, Any]:
    """
    Construye los prompts maestros de producción para generar el video completo con las herramientas de IA líderes:
    1. InVideo AI / Fliki (Prompt todo-en-uno de video completo)
    2. ChatGPT / Claude 3.5 Sonnet (Prompt de guión largo de 2,500 palabras con retención)
    3. ElevenLabs (Configuración de voz y locución)
    4. Runway Gen-3 / Kling AI / Luma (Prompts cinemáticos escena por escena para B-roll)
    5. Directorio de herramientas recomendadas con enlaces directos
    """
    e = clean_entity or title
    
    # 1. Prompt Maestro para InVideo AI
    invideo_prompt = (
        f"Crea un video documental de YouTube de 15 minutos en español titulado: \"{title}\".\n"
        f"Nicho: {category}.\n"
        f"Ritmo: Cinemático, solemne, de alta retención.\n"
        f"Estilo visual: Documental de alta gama, planos de B-roll en claroscuro, reconstrucciones históricas con zoom 2.5D (efecto parallax), humo volumétrico tenue y relación 16:9.\n"
        f"Locución (Voz): Voz masculina profunda, autoritaria y reflexiva (estilo narrador de investigación), a 145 palabras por minuto.\n"
        f"Subtítulos: Grandes y llamativos en el centro de la pantalla, texto blanco con palabras clave en amarillo flúor (#FACC15) y trazo negro exterior.\n"
        f"Música de fondo: Chelo grave misterioso, pads atmosféricos oscuros y tambores de tensión progresiva.\n"
        f"REGLA OBLIGATORIA: Comenzar directamente en el segundo 00:00 con este gancho: \"{hook}\" sin decir jamás saludos, bienvenidas ni peticiones de likes.\n"
        f"Estructura narrativa:\n" + "\n".join(f"- {step}" for step in outline[:6])
    )

    # 2. Prompt Maestro para ChatGPT / Claude (Guión Completo de 2,500 palabras)
    script_prompt = (
        f"Actúa como el guionista principal de YouTube para canales de más de 1 millón de suscriptores (estilo Biografías Ocultas o Daily Stoic).\n"
        f"Tu objetivo es redactar el GUIÓN COMPLETO PALABRA POR PALABRA en español para un video de 15 a 20 minutos (~2,500 palabras) titulado: \"{title}\".\n\n"
        f"REGLAS ESTRICTAS DE RETENCIÓN DE YOUTUBE:\n"
        f"1. GANCHO (00:00 - 00:15): Empieza directamente con este texto exacto: \"{hook}\". Queda terminantemente prohibido decir 'Hola amigos bienvenidos a mi canal'. Confirma la promesa del título en la primera línea.\n"
        f"2. BUCLE ABIERTO (OPEN LOOP): En el minuto 03:00 plantea un misterio no resuelto ('Pero lo que los archivos revelaron después desafía toda lógica...') y no lo cierres hasta el minuto 13:00.\n"
        f"3. INDICACIONES DE PRODUCCIÓN: Intercala entre corchetes indicaciones para el editor: [Visual B-Roll: descripción de la toma cinematográfica], [SFX: Whoosh dramático, bajo ominoso], [Pausa dramática: 2 segundos].\n"
        f"4. RITMO CONVERSACIONAL: Frases concisas, cadencia magnética, sin tecnicismos aburridos ni relleno. Cada oración debe crear tensión para la siguiente.\n"
        f"5. MICRO-GANCHOS MIDROLL: En los minutos 05:30 y 11:30 añade un gancho de intriga justo antes del corte publicitario para que nadie abandone el video.\n\n"
        f"ESTRUCTURA DEL VIDEO:\n" + "\n".join(f"- {step}" for step in outline[:6]) + "\n\n"
        f"Comienza a escribir el guión palabra por palabra desde el segundo 00:00:"
    )

    # 3. Configuración de Locución para ElevenLabs
    elevenlabs_guide = {
        "voice_preset": "Marcus (Filosófica / Solemne) o George / Adam (Narrador Documental)",
        "stability": "65% (equilibrio perfecto entre naturalidad y dramatismo)",
        "similarity": "85% (máxima fidelidad tímbrica)",
        "style_exaggeration": "15% (subtle inflection sin sobreactuar)",
        "speed": "1.00 (145 palabras por minuto - ritmo óptimo de retención)",
        "notes": "Pega el texto del guión eliminando las indicaciones entre corchetes [Visual] y [SFX]. Deja saltos de línea para pausas naturales de 1 segundo."
    }

    # 4. Prompts de Escenas Cinemáticas para B-Roll (Runway Gen-3 / Kling AI / Luma Dream Machine)
    broll_scenes = [
        {
            "timestamp": "00:00 - 00:15 (Gancho)",
            "camera": "Slow cinematic push-in shot",
            "prompt": f"Cinematic slow push-in shot of {e}, intense dramatic shadows, high contrast rim lighting, dark atmospheric mist, 8k resolution, photorealistic, 16:9 ratio"
        },
        {
            "timestamp": "00:15 - 03:00 (Contexto)",
            "camera": "Wide atmospheric drone tracking shot",
            "prompt": f"Wide epic aerial drone tracking shot over an ancient mysterious environment representing {e}, dark ominous stormy sky, volumetric fog, cinematic lighting, 8k"
        },
        {
            "timestamp": "03:00 - 08:00 (El Suceso)",
            "camera": "Macro close-up with shallow depth of field",
            "prompt": f"Macro dramatic close up shot with shallow depth of field, detailed textures of historical artifacts or symbolic elements of {e}, golden candlelight, dark bokeh"
        },
        {
            "timestamp": "08:00 - 14:00 (El Giro)",
            "camera": "Low angle dramatic panning shot",
            "prompt": f"Dramatic low angle slow panning shot of a mysterious shadowy figure turning around, rim lighting, smoke floating, high tension, cinematic color grading"
        },
        {
            "timestamp": "14:00 - 20:00 (Conclusión)",
            "camera": "Slow pull-out epic wide shot",
            "prompt": f"Epic cinematic pull-out wide shot revealing the grand scale of {e}, solitary figure standing, sunset or dawn golden light cutting through darkness, 8k"
        }
    ]

    # 5. Directorio de herramientas recomendadas
    tools = [
        {
            "name": "InVideo AI",
            "url": "https://invideo.io",
            "role": "Video Completo con 1 Clic (Guión + Locución + Clips + Subtítulos)",
            "badge": "Recomendada Todo-en-Uno"
        },
        {
            "name": "ChatGPT / Claude 3.5 Sonnet",
            "url": "https://chatgpt.com",
            "role": "Redacción del Guión Maestro de 2,500 palabras",
            "badge": "Mejor Guionista IA"
        },
        {
            "name": "ElevenLabs",
            "url": "https://elevenlabs.io",
            "role": "Locución Hiperrealista Humana en Español",
            "badge": "Voz Número 1"
        },
        {
            "name": "CapCut",
            "url": "https://www.capcut.com",
            "role": "Montaje, efectos de sonido y subtítulos amarillos",
            "badge": "Editor Gratuito"
        },
        {
            "name": "Kling AI / Runway Gen-3",
            "url": "https://klingai.com",
            "role": "Generación de video B-Roll cinemático hiperrealista",
            "badge": "Video IA Cinemático"
        }
    ]

    return {
        "invideo_master_prompt": invideo_prompt,
        "script_master_prompt": script_prompt,
        "elevenlabs_guide": elevenlabs_guide,
        "broll_scenes": broll_scenes,
        "recommended_tools": tools
    }
