import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# CSV 파일 로드
df = pd.read_csv("yearly.csv")
df['date'] = pd.to_datetime(df['date'])
df['weekday'] = pd.Categorical(df['weekday'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)

prophet_df = pd.read_csv("prophet_decomposed.csv")
prophet_df['ds'] = pd.to_datetime(prophet_df['ds'])
prophet_df['weekday'] = prophet_df['ds'].dt.day_name()
prophet_df['weekday'] = pd.Categorical(prophet_df['weekday'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)

categories = df['category'].unique()

st.title("📊 네이버 쇼핑 인사이트 분석 대시보드")

# -------------------------
# 1. 요일별 클릭량 시각화
st.header("📅 요일별 클릭량 분석")
weekday_categories = st.multiselect("\[요일별] 카테고리를 선택하세요", categories, default=categories[:1], key="weekday")

col1, col2 = st.columns(2)
with col1:
    weekday_avg_all = df[df['category'].isin(weekday_categories)].groupby(['category', 'weekday'])['click_volume'].mean().reset_index()
    fig = px.line(weekday_avg_all, x='weekday', y='click_volume', color='category', title="요일별 평균 클릭량 (라인차트)")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    weekday_pivot = df.groupby(['category', 'weekday'])['click_volume'].mean().unstack()
    fig2 = px.imshow(
        weekday_pivot,
        labels=dict(x="요일", y="카테고리", color="평균 클릭량"),
        aspect="auto",
        title="요일별 클릭량 히트맵 (전체 카테고리)"
    )
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# 2. 월별 클릭량 시각화
st.header("📆 월별 클릭량 분석")
month_categories = st.multiselect("\[월별] 카테고리를 선택하세요", categories, default=categories[:1], key="month")

col3, col4 = st.columns(2)
with col3:
    month_avg_all = df[df['category'].isin(month_categories)].groupby(['category', 'month'])['click_volume'].mean().reset_index()
    fig3 = px.line(month_avg_all, x='month', y='click_volume', color='category', title="월별 평균 클릭량 (라인차트)")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    month_pivot = df.groupby(['category', 'month'])['click_volume'].mean().unstack()
    fig4 = px.imshow(
        month_pivot,
        labels=dict(x="월", y="카테고리", color="평균 클릭량"),
        aspect="auto",
        title="월별 클릭량 히트맵 (전체 카테고리)"
    )
    st.plotly_chart(fig4, use_container_width=True)

# -------------------------
# 3. Prophet 분해 시각화
st.header("🔍 Prophet 시계열 분해 결과")
prophet_categories = st.multiselect("\[Prophet] 카테고리를 선택하세요", categories, default=categories[:1], key="prophet")

prophet_filtered = prophet_df[prophet_df['category'].isin(prophet_categories)]

fig5 = px.line(prophet_filtered, x='ds', y='trend', color='category', title="Trend (추세)")
st.plotly_chart(fig5, use_container_width=True)

fig6 = px.line(prophet_filtered, x='ds', y='yearly', color='category', title="Yearly Seasonality (계절성)")
st.plotly_chart(fig6, use_container_width=True)

# 요일 기준 주기 시각화
weekly_avg = prophet_filtered.groupby(['category', 'weekday'])['weekly'].mean().reset_index()
fig7 = px.line(weekly_avg, x='weekday', y='weekly', color='category', title="Weekly Seasonality (주기)")
st.plotly_chart(fig7, use_container_width=True)

st.caption("데이터 출처: 네이버 데이터랩 쇼핑 인사이트")