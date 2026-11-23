import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

df_ratios=pd.read_csv("mcdonalds_ratios_transposed.csv", index_col=0)




st.title("Financial Dashboard")


selected_year = st.sidebar.selectbox("Select Year:", ["2021","2022","2023","2024"])

col1, col2, col3, col4,  = st.columns(4)
col5, col6, col7, col8 = st.columns(4)

col1.metric("Net Profit Margin %", f"{df_ratios.loc['Net Profit Margin %', selected_year]}%")
col2.metric("Current Ratio", df_ratios.loc['Current Ratio', selected_year])
col3.metric("ROA %", f"{df_ratios.loc['ROA %', selected_year]}%")
col4.metric("ROE %", f"{df_ratios.loc['ROE %', selected_year]}%")
col5.metric("Debt to Assets %", f"{df_ratios.loc['Debt to Assets %', selected_year]}%")
col6.metric("Debt to Equity %", f"{df_ratios.loc['Debt to Equity %', selected_year]}%")
col7.metric("Receivables Turnover", f"{df_ratios.loc['Receivables Turnover', selected_year]}x")
col8.metric("Inventory Turnover", f"{df_ratios.loc['Inventtory Turnover', selected_year]}x")

st.divider()

df_chart = df_ratios.T.reset_index().rename(columns={'index': 'Year'})

page = st.sidebar.radio(
    "Navigation",
    ["📊 Financial Ratios","📈 Horizontal Analysis","🍰 Vertical Analysis"]
    )

if page == "📊 Financial Ratios":
    c1, c2 = st.columns(2)
    fig_prof = px.line(df_chart, x='Year', y=['Opperating Margin %', 'Net Profit Margin %'], title="Profitability Margins Chart", markers=True)
    c1.plotly_chart(fig_prof, width='stretch')

    fig_liq = px.bar(df_chart, x='Year', y=['Current Ratio', 'Quick Ratio', 'Cash Ratio'], title="Liquidity Ratios Chart", barmode='group')
    c2.plotly_chart(fig_liq, width='stretch')

    c3, c4 = st.columns(2)
    fig_debt = px.bar(df_chart, x='Year', y='Debt to Assets %', title="Debt Chart")
    c3.plotly_chart(fig_debt, width='stretch')

    fig_eff = px.line(df_chart, x='Year', y=['Receivables Turnover', 'Inventtory Turnover'], title="Eff Chart", markers=True)
    c4.plotly_chart(fig_eff, width='stretch')

elif page == "📈 Horizontal Analysis":
    df_horizontal = pd.read_excel("mcdonalds_analysis.xlsx", sheet_name="Horizontal_Analysis") 

    df_horizontal.columns=df_horizontal.columns.astype(str)

    st.subheader("Year-over-Year Growth Analysis (YoY %)")

    df_melted = df_horizontal.melt(id_vars=['table', 'heading', 'subheading'], value_vars=['2022', '2023', '2024'], value_name='Growth %', var_name='year')

    selected_table = st.selectbox("Select Financial Statement:", df_melted['table'].unique())
    filtered_df = df_melted[df_melted['table'] == selected_table]
    pd.ExcelWriter(
            st.dataframe(filtered_df,width='stretch', hide_index=True)
        )
    
    key_items = ['operating_income', 'net_income', 'food_and_paper']

    df_plot = df_melted[df_melted['subheading'].isin(key_items)]

    hc = px.bar(df_plot, x='year', y='Growth %', title="Horizontal Analysis Chart", barmode='group', color='subheading')
    st.plotly_chart(hc, width='stretch')

elif page == "🍰 Vertical Analysis":
    df_inc_vert = pd.read_excel("mcdonalds_analysis.xlsx", sheet_name="Income_Vertical")
    df_bal_vert = pd.read_excel("mcdonalds_analysis.xlsx", sheet_name="Balance_Vertical")
    df_inc_vert.columns = df_inc_vert.columns.astype(str)
    df_bal_vert.columns = df_bal_vert.columns.astype(str)

    vc1, vc2 = st.columns(2)

    df_assets = df_bal_vert[df_bal_vert['table'] == 'assets']
    df_assets_pos = df_assets[df_assets[selected_year] > 0]

    assets_chart = px.pie(df_assets_pos, names='subheading', values=selected_year, hole=0.4, title=f"Assets Structure {selected_year}")
    vc1.plotly_chart(assets_chart,width='stretch')

    df_revenue_breakdown = df_inc_vert[df_inc_vert['table'] == 'revenue_breakdown']
    revenue_breakdown_chart = px.pie(df_revenue_breakdown, names='subheading', values=selected_year, hole=0.4, title=f"Revenue Breakdown Structure {selected_year}")
    vc2.plotly_chart(revenue_breakdown_chart,width='stretch')

    selected_statement = st.selectbox("Select Statement:",["Balance Sheet","Income Statement"])
    if selected_statement == "Balance Sheet":
        pd.ExcelWriter(
                st.dataframe(df_bal_vert ,width='stretch', hide_index=True)
            )
    elif selected_statement == "Income Statement":
         pd.ExcelWriter(
                st.dataframe(df_inc_vert ,width='stretch', hide_index=True)
              )