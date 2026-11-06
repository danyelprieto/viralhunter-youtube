# 📊 02 - Algoritmo Matemático de Outliers

Definición matemática de qué constituye un video viral en YouTube y cómo separar el éxito genuino del tema frente a la fama previa del canal.

---

## 1. ¿Qué es un Outlier?
Un **Outlier** (valor atípico) es un video cuyo rendimiento estadístico de reproducciones se sale drásticamente de la campana de Gauss habitual del canal que lo publicó.

---

## 2. La Fórmula Matemática de Viralidad

### Caso A: Ratio Vistas vs Suscriptores ($R_s$)
$$R_s = \frac{\text{Vistas del Video}}{\text{Suscriptores del Canal}}$$

* **$R_s < 0.2$ (Pobre):** El video apenas llegó al 20% de su propia base de suscriptores.
* **$0.2 \le R_s \le 1.0$ (Normal):** Rendimiento esperado para un canal consolidado.
* **$1.0 < R_s < 5.0$ (Bueno):** El video superó la cantidad de suscriptores; el algoritmo empezó a recomendarlo en la página de inicio (Browse Features).
* **$R_s \ge 5.0$ (OUTLIER VIRAL):** El video tiene 5 veces más vistas que los suscriptores.
* **$R_s \ge 20.0$ (MEGA OUTLIER):** El video detonó el algoritmo. El tema y la miniatura tienen un magnetismo universal.

### Caso B: Ratio Vistas vs Mediana de los Últimos 10 Videos ($R_m$)
$$R_m = \frac{\text{Vistas del Video}}{\text{Mediana}(\text{Vistas}_{v_1}, \dots, \text{Vistas}_{v_{10}})}$$

Esta fórmula es aún más precisa porque no se distorsiona si el canal tiene muchos suscriptores inactivos del pasado.

---

## 3. Ejemplo Práctico del Video de Adrián Sáenz
* **Canal analizado:** Canal automatizado en inglés de salud.
* **Suscriptores:** 45.000.
* **Vistas del video analizado:** 3.400.000 vistas.
* **Cálculo:**
  $$R_s = \frac{3.400.000}{45.000} \approx 75.5\times$$
* **Conclusión:** El video es un **Outlier de $75.5\times$**. La probabilidad de que ese mismo tema y packaging triunfen en español al adaptarlo es superior al 80%.
