# ViralHunter 2.0 🚀
### Motor de Outliers de YouTube, Adaptación al Español y Estudio de Miniaturas con IA

Herramienta completa para encontrar videos atípicos (*outliers*) en canales pequeños, desglosar su empaquetado viral (títulos, miniaturas, ganchos), y adaptarlos para canales en español.

---

## 🌟 Características Principales
1. **Buscador de Outliers en Tiempo Real:** Scraping multihilo sin cuotas de API de Google. Calcula multiplicador de vistas/suscriptores, velocidad diaria y estimación de RPM.
2. **Estudio de Miniaturas con IA (Puter.js + FLUX.1):** 
   - Ingeniería inversa del prompt visual original.
   - Edición guiada por texto ("cambiar fondo", "añadir flecha", etc.).
   - Tipografía viral superpuesta con trazo pronunciado y sombra.
3. **Auditor de Empaquetado & Ganchos Virales:**
   - Inspirado en las fórmulas de `youtube-agent-skill`.
   - 3 fórmulas de gancho probadas (*Contrarian Flip*, *The Mistake*, *The Result*) con calificación matemática **HookScore (0-100)**.
   - Linter de títulos con corte móvil (~40 caracteres).
4. **Suite de Producción de Video:**
   - Prompt maestro para InVideo AI.
   - Guión completo de retención (+2.500 palabras) para ChatGPT / Claude.
   - Guía de voz para ElevenLabs y 5 tomas de cámara B-roll para Runway / Kling.
5. **Integración con Baúl de Obsidian:** Registro automático de nichos, canales ganadores y miniaturas generadas.

---

## 💻 Ejecución Local

```bash
cd backend
python -m uvicorn server:app --host 0.0.0.0 --port 8500
```
Abre en tu navegador:
- PC: `http://localhost:8500`
- Celular (mismo Wi-Fi): `http://<TU_IP_LOCAL>:8500`

---

## ☁️ Despliegue en la Nube (Render.com Gratis)

1. Conecta este repositorio en [Render.com](https://render.com).
2. **Build Command:** `pip install -r requirements.txt`
3. **Start Command:** `uvicorn backend.server:app --host 0.0.0.0 --port $PORT`
