import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Conversational AI Business Intelligence", layout="wide")

st.title("💬 Conversational AI for Instant Business Intelligence Dashboard")
st.markdown("Upload any business dataset and ask questions to get instant insights.")

uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df)

    st.divider()

    st.subheader("Ask Questions About Your Data")

    question = st.text_input(
        "Example: show sales trend, revenue distribution, category share, region comparison"
    )

    if question:

        q = question.lower()

        # Detect numeric columns
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        text_cols = df.select_dtypes(include="object").columns.tolist()

        chart_generated = False

        # Trend / Area Chart
        if "trend" in q or "over time" in q:

            if len(numeric_cols) > 0:

                col = numeric_cols[0]

                fig = px.area(
                    df,
                    y=col,
                    title=f"{col} Trend Analysis"
                )

                st.plotly_chart(fig, use_container_width=True)

                chart_generated = True


        # Distribution / Pie Chart
        if "distribution" in q or "share" in q:

            if len(text_cols) > 0:

                col = text_cols[0]

                data = df[col].value_counts().reset_index()
                data.columns = [col, "count"]

                fig = px.pie(
                    data,
                    names=col,
                    values="count",
                    title=f"{col} Distribution"
                )

                st.plotly_chart(fig, use_container_width=True)

                chart_generated = True


        # Comparison
        if "compare" in q or "comparison" in q:

            if len(text_cols) > 0 and len(numeric_cols) > 0:

                fig = px.line(
                    df,
                    x=text_cols[0],
                    y=numeric_cols[0],
                    title="Comparison Analysis"
                )

                st.plotly_chart(fig, use_container_width=True)

                chart_generated = True


        # Direct column detection
        for column in df.columns:

            if column.lower() in q:

                if pd.api.types.is_numeric_dtype(df[column]):

                    fig = px.area(
                        df,
                        y=column,
                        title=f"{column} Analysis"
                    )

                    st.plotly_chart(fig, use_container_width=True)

                else:

                    data = df[column].value_counts().reset_index()
                    data.columns = [column, "count"]

                    fig = px.pie(
                        data,
                        names=column,
                        values="count",
                        title=f"{column} Distribution"
                    )

                    st.plotly_chart(fig, use_container_width=True)

                chart_generated = True


        if not chart_generated:

            st.warning("Try asking about trends, distribution, or comparisons in your dataset.")