import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="YouTube AI Dashboard", layout="wide")

st.title("🎬 YouTube Content Creation AI Dashboard")

uploaded_file = st.file_uploader("Upload your dataset", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df)

    st.divider()

    # QUESTION BOX
    st.subheader("💬 Ask Questions About the Dataset")

    question = st.text_input(
        "Example: views trend, category share, region comparison"
    )

    if question:

        q = question.lower()

        # AREA GRAPH
        if "views" in q:

            st.subheader("📈 Views Trend (Area Chart)")

            fig = px.area(
                df,
                x="video_id",
                y="views",
                color="category"
            )

            st.plotly_chart(fig, use_container_width=True)


        # 3D PIE CHART
        elif "category" in q:

            st.subheader("🥧 Category Distribution (3D Pie)")

            data = df["category"].value_counts()

            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=data.index,
                        values=data.values,
                        hole=0.2
                    )
                ]
            )

            fig.update_traces(
                textinfo="percent+label",
                marker=dict(colors=px.colors.qualitative.Bold)
            )

            st.plotly_chart(fig, use_container_width=True)


        # 100% STACKED LINE
        elif "region" in q:

            st.subheader("📊 Region Performance (100% Stacked Line)")

            region_data = df.groupby(["region", "category"]).size().unstack().fillna(0)

            region_data = region_data.div(region_data.sum(axis=1), axis=0)

            fig = px.line(
                region_data,
                x=region_data.index,
                y=region_data.columns
            )

            st.plotly_chart(fig, use_container_width=True)


        # LIKES AREA GRAPH
        elif "likes" in q:

            st.subheader("❤️ Likes Trend (Area Chart)")

            fig = px.area(
                df,
                x="video_id",
                y="likes",
                color="language"
            )

            st.plotly_chart(fig, use_container_width=True)


        else:

            st.warning(
                "Try asking: views, likes, category, region"
            )
            