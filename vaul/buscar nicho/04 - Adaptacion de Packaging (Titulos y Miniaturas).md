# 🎨 04 - Adaptación de Packaging (Títulos y Miniaturas)

El "Packaging" es el 80% del éxito en YouTube: la miniatura consigue la impresión y el título convierte la impresión en clic (CTR).

---

## 1. Psicología de la Miniatura (Thumbnail)
Las miniaturas de los videos virales comparten 4 patrones invariables:

1. **La Regla de los 3 Elementos:**  
   El cerebro humano solo procesa 3 elementos en la pantalla de un móvil en medio segundo:
   * Elemento 1: Un rostro o sujeto con emoción intensa (sorpresa, determinación, intriga).
   * Elemento 2: Un objeto central de alto contraste.
   * Elemento 3: Máximo 3 a 4 palabras grandes de texto (o una flecha/gráfico).
2. **Contraste de Colores:**  
   Fondos oscuros con toques de amarillo brillante, cian eléctrico o rojo intenso.
3. **Curiosity Gap (Brecha de Curiosidad):**  
   La miniatura plantea una pregunta visual que solo se responde al ver el video.

---

## 2. Fórmulas de Títulos con Alto CTR

| Fórmula | Ejemplo en Inglés | Adaptación para Canal Hispano |
| :--- | :--- | :--- |
| **Poder del Silencio** | *Become SO STRONG that your SILENCE COMMANDS RESPECT* | *Hazte tan fuerte que tu silencio imponga respeto (Enseñanza Estoica)* |
| **La Revelación Oculta** | *The 1 Habit that changed my life in 30 days* | *El único hábito silencioso que transformó mi mente en 30 días* |
| **La Advertencia** | *Stop doing this before sleeping (It ruins your brain)* | *Deja de hacer esto antes de dormir (Está dañando tu cerebro)* |
| **Biografía de Choque** | *The man who tricked the entire Roman Empire* | *El hombre que engañó a todo un imperio y nadie pudo detener* |

---

## 3. El Gancho de Retención de los Primeros 15 Segundos (*Hook*)
Para que el gráfico de retención de YouTube no caiga en picada en el segundo 30:
1. **Segundo 0 a 5:** Reafirmar inmediatamente la promesa del título (nunca decir *"Hola amigos bienvenidos a mi canal, suscríbanse"*).
2. **Segundo 5 a 10:** Plantear una consecuencia grave o un misterio irresistible.
3. **Segundo 10 a 15:** Entregar la hoja de ruta del video (*"En este video descubrirás los 3 principios que..."*).

---

## 4. El Laboratorio de Clonación de Miniatura (Thumbnail Cloner)
Para no empezar una miniatura desde cero ni arriesgar problemas de derechos de autor:
1. **Extracción en Alta Resolución (MaxResDefault):**  
   El sistema extrae el fotograma original en 1280x720 píxeles directamente de los servidores de Google (`https://i.ytimg.com/vi/{id}/maxresdefault.jpg`).
2. **Ingeniería Inversa Visual con IA (Midjourney v6 / Flux 1.0):**  
   Se genera un prompt fotográfico con iluminación de recorte (*rim lighting*), fondo oscuro en claroscuro y encuadre cinematográfico (`--ar 16:9 --style raw`).
3. **Plantilla de Fondo Limpio (*Clean Background*):**  
   Permite generar únicamente el escenario atmosférico para que el creador agregue su propio sujeto, estatua o fotografía en primer plano.
4. **Composición Rápida en Photopea / Photoshop:**  
   Montaje de texto en tipografía de alto peso (*Impact* o *Montserrat ExtraBold*), trazo exterior de 6px y resplandor suave para máxima legibilidad en teléfonos inteligentes.

---

## 5. Estudio Interactivo de Miniaturas con IA (ViralHunter Studio)
ViralHunter 2.0 integra un generador directo con modelo **FLUX.1-schnell** sin costo ni APIs de pago:
1. **Modificación por Instrucción de Texto:**
   * El usuario introduce qué cambiar (ej. *"Cambia al personaje por un busto romano en penumbras, iluminación dorada"*).
   * Puede usar chips predefinidos: Estoicismo, Pintura Histórica, Neurociencia 3D, Bóveda de Lujo, Fondo Limpio.
2. **Renderizado en Tiempo Real (1280x720):**
   * Genera el fotograma en relación 16:9 de alta fidelidad directamente en el navegador.
3. **Estampado de Texto Viral:**
   * Motor de canvas con tipografía Jakarta Sans/Impact, trazo negro exterior de 18px y colores de alto impacto (Amarillo, Rojo, Blanco, Cian).
4. **Almacenamiento Directo en Obsidian:**
   * Con 1 clic, la miniatura generada se descarga y se registra en `05 - Registro de Nichos y Canales Ganadores.md`.
5. **Ingeniería Inversa Visual con Visión Multimodal (Image-to-Prompt):**
   * El botón `👁️ Escanear con Visión IA` lee los píxeles reales de la miniatura seleccionada mediante el proxy local y extrae el prompt exacto de su composición, iluminación y sujeto.
   * Permite dos flujos: `🎯 Clonar Tal Cual (Fiel a la Original)` para verificar la réplica exacta, o `✨ Recrear con Modificaciones` editando el texto libremente.

---

## 6. Auditor de Empaquetado y 21 Fórmulas de Ganchos (youtube-agent-skill)
Se integraron las heurísticas clave del repositorio de Jake Schincariol:
1. **Linter de Empaquetado (`yt-package`):**
   * **Regla de no duplicación:** Penaliza si la miniatura repite palabras del título, forzando a que la miniatura aporte intriga complementaria en lugar de duplicar información.
   * **Simulador de Pantalla Móvil:** Previsualiza el título cortado a los ~40 caracteres para asegurar que el tema central no se pierda en teléfonos celulares.
   * **Límite de 3 Palabras:** Asegura que el texto en la miniatura sea ultra-legible a feed size.
2. **Sistema de 21 Ganchos con HookScore (`hooks.json` + `hookscore.py`):**
   * Genera 3 ganchos psicológicos (*Contrarian Flip*, *The Mistake*, *The Result*) evaluados en 5 propiedades: Especificidad, Apelación directa ('Tú'), Consecuencia/Riesgo, Curiosidad y Ritmo (15 segundos a 150wpm).
3. **Capítulos Automáticos de YouTube (`chapters.py`):**
   * Genera marcas de tiempo oficiales para la descripción del video iniciando en 00:00 y con separación mínima de 10 segundos.

---

## 7. Suite de Producción de Video Completo con IA
ViralHunter 2.0 integra un generador de prompts maestros de producción organizados por herramienta:
1. **InVideo AI / Fliki (Todo-en-Uno en 1 Clic):**
   * Prompt maestro que genera el video de 15-20 min con voz, B-roll, música de tensión y subtítulos amarillos.
2. **ChatGPT / Claude 3.5 Sonnet (Guión de 2,500 Palabras):**
   * Prompt estructurado con bucle abierto (*open loop* en minuto 3), marcas de retención `[SFX]`, pausas y cortes midroll.
3. **ElevenLabs (Voz Humana en Off):**
   * Ajustes de retención: Estabilidad 65%, Claridad 85%, Velocidad 145 wpm y voces recomendadas (Marcus / George / Adam).
4. **Runway Gen-3 / Kling AI / Luma (B-Roll Cinemático):**
   * 5 escenas desglosadas con movimientos de cámara (slow push-in, aerial drone, macro, low angle, epic pull-out).
