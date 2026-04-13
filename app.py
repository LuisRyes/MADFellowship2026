import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="EPIC SmartMatch", layout="wide")
st.title("🚀 EPIC SmartMatch: Mentor-Founder Engine")

# 2. Cargar las bases de datos (Movido arriba para que las métricas funcionen)
@st.cache_data(ttl=600)
def load_data():
    SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT58VUYzUkXGwo4HHPig4ETkghZwyoHnT7CYP_dZVa8UGDDyEHK0-4beJ7PMHyT_mZOvFaoybnCcx9l/pub?gid=0&single=true&output=csv"
    fundadores = pd.read_csv(SHEET_CSV_URL)
    # Asegúrate de que este archivo esté en la misma carpeta que tu script
    mentores = pd.read_csv("mentores.csv") 
    return fundadores, mentores

fundadores_df, mentores_df = load_data()
if fundadores_df.empty:
    st.info("👋 ¡Bienvenido! La base de datos está esperando su primer registro. "
            "Envía un mensaje a través del bot de Telegram para empezar.")
    st.stop() # Esto pausa la app de forma elegante hasta que haya datos

# 1.1 Métricas clave para el dashboard
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Fundadores", len(fundadores_df))
with col2:
    st.metric("Mentores Activos", len(mentores_df))
with col3:
    # Esto busca cualquier variante: "Tracción", "traccion", "Traccion", etc.
    traccion = len(fundadores_df[fundadores_df['Etapa_Startup'].str.contains('tracc', case=False, na=False)])
    st.metric("Startups en Tracción", traccion)

st.markdown("Algoritmo de recomendación ponderada para el ecosistema EPIC Lab.")

# 3. Interfaz del usuario
st.sidebar.header("Selecciona un Fundador")
opciones_fundadores = fundadores_df['Nombre_Completo'].tolist()
fundador_seleccionado = st.sidebar.selectbox("Fundador:", opciones_fundadores)

# Buscamos la fila sin forzar el .iloc[0] todavía
seleccion = fundadores_df[fundadores_df['Nombre_Completo'] == fundador_seleccionado]

# Verificamos si la búsqueda arrojó resultados
if not seleccion.empty:
    # Si existe, ahora sí extraemos la primera fila de forma segura
    datos_fundador = seleccion.iloc[0]
    
    st.subheader(f"Perfil: {datos_fundador['Nombre_Completo']}")
    st.write(f"**Industria:** {datos_fundador['Industria']} | **Etapa:** {datos_fundador['Etapa_Startup']}")
    st.write(f"**Necesidad Principal:** {datos_fundador['Necesidad_Principal']}")
    st.info(f"Contexto: {datos_fundador['Contexto_Breve']}")
else:
    # Si no hay match, mostramos un mensaje amigable en lugar de un error rojo
    st.warning("⚠️ No se encontraron datos para este fundador. Por favor, selecciona otro de la lista.")
    st.stop() # Esto evita que el resto del código (el motor de match) intente correr sin datos

# 4. Motor de Recomendación
if st.button("🔍 Encontrar Mentores Ideales"):
    resultados = []
    for index, mentor in mentores_df.iterrows():
        score = 0
        if str(datos_fundador['Necesidad_Principal']).strip() == str(mentor['Area_Expertise']).strip():
            score += 50
        if str(datos_fundador['Industria']).strip() == str(mentor['Industria_Experiencia']).strip():
            score += 30
        if str(datos_fundador['Etapa_Startup']) in str(mentor['Etapas_Preferencia']):
            score += 20

        if mentor['Capacidad_Mensual'] <= 0:
            score -= 100 
        elif mentor['Capacidad_Mensual'] <= 2:
            score -= 10  

        # Dentro del loop: for index, mentor in mentores_df.iterrows():
        resultados.append({
            'Mentor': mentor['Nombre_Completo'], # Cambiamos 'Nombre' por 'Nombre_Completo'
            'Match Score': score,
            'Expertise': mentor['Area_Expertise'],
            'Industria': mentor['Industria_Experiencia'],
            'Capacidad Restante': mentor['Capacidad_Mensual']
        })
        
    resultados_df = pd.DataFrame(resultados)
    resultados_df = resultados_df.sort_values(by='Match Score', ascending=False).head(3)
    
    st.success("¡Top 3 Mentores Encontrados!")
    
    for i, row in resultados_df.iterrows():
        with st.expander(f"⭐ {row['Mentor']} - Compatibilidad: {row['Match Score']}%"):
            st.write(f"**Área de Expertise:** {row['Expertise']}")
            st.write(f"**Industria:** {row['Industria']}")
            st.write(f"**Capacidad:** {row['Capacidad Restante']} al mes")
    
    st.markdown("---")
    st.subheader("🤖 Generador de Prompts para hacer el correo para el mentor y fundador")
    
    # Extraemos los datos del mejor match para alimentar los prompts
    mejor_mentor = resultados_df.iloc[0]
    nombre_f = datos_fundador['Nombre_Completo']
    industria_f = datos_fundador['Industria']
    etapa_f = datos_fundador['Etapa_Startup']
    necesidad_f = datos_fundador['Necesidad_Principal']
    contexto_f = datos_fundador['Contexto_Breve']
    nombre_m = mejor_mentor['Mentor']

    col_m, col_f = st.columns(2)

    with col_m:
        st.markdown(f"### 📧 Para el Mentor: **{nombre_m}**")
        prompt_mentor = f"""
Actúa como el Coordinador Estratégico del EPIC Lab ITAM. Tu misión es redactar una propuesta de mentoría.

DATOS DEL FUNDADOR:
- Nombre: {nombre_f}
- Industria: {industria_f}
- Etapa: {etapa_f}
- Necesidad: {necesidad_f}
- Contexto: {contexto_f}

INSTRUCCIONES:
1. Redacta un mensaje profesional para el mentor {nombre_m}.
2. Destaca que hemos seleccionado a {nombre_f} por su potencial en {industria_f}.
3. Resume el contexto de forma innovadora y explica que su expertise es clave para resolver la necesidad de: {necesidad_f}.
4. Cierre: Pregunta disponibilidad para una sesión de 45 min.
5. Tono: Ejecutivo y persuasivo.
        """
        st.code(prompt_mentor, language="markdown")

    with col_f:
        st.markdown(f"### 📱 Para el Fundador: **{nombre_f}**")
        prompt_fundador = f"""
Actúa como el Community Builder del EPIC Lab ITAM. Tu misión es avisarle a un fundador que tiene un match.

DATOS:
- Nombre: {nombre_f}
- Necesidad: {necesidad_f}
- Proyecto: {contexto_f}
- Mentor asignado: {nombre_m}

INSTRUCCIONES:
1. Redacta un mensaje entusiasta para {nombre_f}.
2. Confirma que tras analizar su proyecto de "{contexto_f}", le hemos asignado a {nombre_m} para ayudarle con su necesidad de {necesidad_f}.
3. Refuerza el valor de la red del EPIC Lab.
4. Tono: Amigable y motivador.
        """
        st.code(prompt_fundador, language="markdown")