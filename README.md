# 🚀 Epic SmartMatch: AI-Driven Mentor-Founder Engine

**MAD Fellowship Challenge 2026 | Track #1: Community Multiplier**

Este proyecto nace de la curiosidad por resolver el cuello de botella en el proceso de vinculación entre fundadores y mentores del EPIC Lab. En lugar de elegir una sola tecnología, decidí integrar un ecosistema completo para crear una experiencia sin fricciones, desde el primer contacto hasta el mensaje de vinculación.

## 🧠 El Proceso Creativo
Mi enfoque se basó en el **"Clear Thinking"** y la validación rápida:
1. **Ideación:** Empecé con una lluvia de ideas comparando chatbots, sitios web estáticos y modelos de IA existentes. 
2. **Curiosidad Técnica:** Me dio curiosidad saber qué pasaría si en lugar de elegir una, **juntaba las tres** para crear un ecosistema funcional.
3. **Validación:** Platiqué la idea con un colega para simplificar la UX. Concluimos que **Telegram** era el canal ideal para un MVP por su accesibilidad y baja barrera de entrada.
4. **El toque creativo:** Ideamos la integración de un **sticker NFC** físico en el Lab que, al ser escaneado, abre instantáneamente el bot de registro, eliminando cualquier fricción inicial.

## 🛠️ Tech Stack & Arquitectura
Aproveché el poder de la IA y herramientas *no-code/low-code* para construir una solución tangible en tiempo récord:

* **Captura:** Bot de Telegram conectado vía **Make.com**.
* **Procesamiento:** OpenAI API para extraer y estructurar datos de lenguaje natural.
* **Base de Datos:** Google Sheets como fuente única de verdad.
* **Algoritmo de Match:** Dashboard en **Streamlit (Python)** con una lógica de puntuación ponderada:
    * **Expertise (50%)**
    * **Industria (30%)**
    * **Etapa de la Startup (20%)**
    * *Factor Crítico:* Gestión de capacidad mensual del mentor.

## 📦 Entrega y Demo
- **Flujo de Automatización:** [https://us2.make.com/public/shared-scenario/g6olEaJyVAC/integration-telegram-bot
]
- **Base de Datos:** [https://docs.google.com/spreadsheets/d/1dgZJsbL-1UzGvvoME71ZKs1g0-LpccVz3sgkj3SuiEg/edit?usp=sharing
]

## 🚀 Cómo ejecutar el Dashboard
1. Clona este repositorio.
2. Instala las dependencias: `pip install -r requirements.txt`.
3. Ejecuta la app: `streamlit run app.py`.
