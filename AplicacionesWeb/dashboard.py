"""
Dashboar de RH
@author: Jessica Santizo Galicia

Ejecutar: streamlit run dashboard.py
"""

#Importación de bibliotecas
import pandas as pd
import plotly.express as px
import streamlit as st


col_titulo, col_logo = st.columns([4, 1], vertical_alignment="center")
with col_titulo:
#1. Código que contiene las instrucciones para el despliegue de un título y una breve descripción de la aplicación web.
    st.title("Dashboard de Recursos Humanos")
    st.markdown(
            """
            Esta aplicación permite explorar y analizar la información del
            personal de la empresa: desempeño, horas trabajadas, salario,
            satisfacción y ausentismo. 
            """
        )

#Dibuja una línea horizontal
st.divider()

#2. Código que permita desplegar el logotipo de la empresa en la aplicación web.
with col_logo:
    st.image("logoRH.png", width=250)

# Cargando dataset
def cargar_datos(ruta: str) -> pd.DataFrame:
    df = pd.read_csv(ruta, encoding="utf-8-sig")

    #Eliminación de espacios en blanco
    df["gender"] = df["gender"].str.strip()
    df["marital_status"] = df["marital_status"].str.strip()
    df["position"] = df["position"].str.strip()
 
    # Conversión de fechas (formato día/mes/año)
    df["birth_date"] = pd.to_datetime(df["birth_date"], format="%d/%m/%y", errors="coerce")
    df["hiring_date"] = pd.to_datetime(df["hiring_date"], format="%d/%m/%y", errors="coerce")
    df["last_performance_date"] = pd.to_datetime(
        df["last_performance_date"], format="%d/%m/%y", errors="coerce"
    )
 
    # Selección de columnas específicas
    columnas = [
        "name_employee",
        "birth_date",
        "age",
        "gender",
        "marital_status",
        "hiring_date",
        "position",
        "salary",
        "performance_score",
        "last_performance_date",
        "average_work_hours",
        "satisfaction_level",
        "absences",
    ]
    return df[columnas]
 
 
df = cargar_datos("Employee_data.csv")



#3. Código que permita desplegar un control para seleccionar el género del empleado.
generos_disponibles = sorted(df["gender"].dropna().unique())
generos_seleccionados = st.sidebar.multiselect(
    "Género",
    options=generos_disponibles,
    default=generos_disponibles,
)

#4. Código que permita desplegar un control para seleccionar un rango del puntaje de desempeño del empleado.
puntaje_min = int(df["performance_score"].min())
#puntaje_max = int(df["performance_score"].max())
puntaje_max = 5
rango = st.sidebar.slider(
    "Rango de puntaje de desempeño",
    min_value=puntaje_min,
    max_value=puntaje_max,
    value=(puntaje_min, puntaje_max),
    step=1,
)

#5. Código que permita desplegar un control para seleccionar el estado civil del empleado.
estados_civiles_disponibles = sorted(df["marital_status"].dropna().unique())
estados_civiles_seleccionados = st.sidebar.multiselect(
    "Estado civil",
    options=estados_civiles_disponibles,
    default=estados_civiles_disponibles,
)

df_filtrado = df[
    (df["gender"].isin(generos_seleccionados))
    & (df["performance_score"].between(rango[0], rango[1]))
    & (df["marital_status"].isin(estados_civiles_seleccionados))
]

if df_filtrado.empty:
    st.warning("No hay empleados que cumplan con los filtros seleccionados.")
    st.stop()

#6. Código que permita mostrar un gráfico en donde se visualice la distribución de los puntajes de desempeño.
st.subheader("Distribución de los puntajes de desempeño")
fig_desempeno = px.histogram(
    df_filtrado,
    x="performance_score",
    color="gender",
    barmode="group",
    labels={"performance_score": "Puntaje de desempeño", "count": "Número de empleados"},
)
fig_desempeno.update_layout(bargap=0.15, yaxis_title="Número de empleados")
st.plotly_chart(fig_desempeno, use_container_width=True, key="grafico_desempeno")

#7. Código que permita mostrar un gráfico en donde se visualice el promedio de horas trabajadas por el género del empleado.
st.subheader("Promedio de horas trabajadas por género")
horas_por_genero = df_filtrado.groupby("gender")["average_work_hours"].mean().reset_index()
fig_horas_genero = px.bar(
    horas_por_genero,
    x="gender",
    y="average_work_hours",
    color="gender",
    text_auto=".1f",
    labels={"gender": "Género", "average_work_hours": "Promedio de horas mensuales"},
)
st.plotly_chart(fig_horas_genero, use_container_width=True, key="grafico_horas_genero")

st.divider()
#8. Código que permita mostrar un gráfico en donde se visualice la edad de los empleados con respecto al salario de los mismos.
st.subheader("Edad de los empleados vs. salario")
fig_edad_salario = px.scatter(
    df_filtrado,
    x="age",
    y="salary",
    color="gender",
    hover_data=["name_employee", "position"],
    labels={"age": "Edad", "salary": "Salario"},
)
st.plotly_chart(fig_edad_salario, use_container_width=True, key="grafico_edad_salario")

st.divider()
#9. Código que permita mostrar un gráfico en donde se visualice la relación del promedio de horas trabajadas versus el puntaje de desempeño.
st.subheader("Promedio de horas trabajadas vs. puntaje de desempeño")
fig_horas_desempeno = px.scatter(
    df_filtrado,
    x="average_work_hours",
    y="performance_score",
    color="gender",
    hover_data=["name_employee", "position"],
    labels={
        "average_work_hours": "Promedio de horas mensuales",
        "performance_score": "Puntaje de desempeño",
    },
)
st.plotly_chart(fig_horas_desempeno, use_container_width=True, key="grafico_horas_desempeno")
st.divider()

#10. Código que permita desplegar una conclusión sobre el análisis mostrado en la aplicación web.
st.subheader("Conclusión del análisis")
correlacion = df_filtrado["average_work_hours"].corr(df_filtrado["performance_score"])
promedio_general_horas = df_filtrado["average_work_hours"].mean()
promedio_general_desempeno = df_filtrado["performance_score"].mean()

st.markdown(
    f"""
    Se analizaron 311 empleados, en donde se obtuvo que  el promedio de horas mensuales trabajadas es de 4395 horas y el puntaje de desempeño promedio es de 2.98 (tomando una escala de 1 a 5).
    La correlación entre las horas trabajadas y el puntaje de desempeño es de 0.09, esto signfica que no hay  una relación fuerte entre la cantidad de horas trabajadas y el desempeño. 
    Finalmente se pude concluir que otros factores (como satisfacción, estado civil, puesto) pueden influir más en los resultados"""
)