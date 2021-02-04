import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as sm
#import warnings
import altair as alt
from load_data import data_prep_total_enrollment
from load_data import data_prep_assessment
from load_data import data_prep_final_merged
# pip uninstall protobuf python3-protobuf
# pip install --upgrade pip
# pip install --upgrade protobuf 
from scipy import stats
from helpers import pearsonr_ci

import streamlit as st
def app():
    st.title('Because Los Angeles is such a large district, we identified it as an outlier and we dropped it.')
    # https://medium.com/@u.praneel.nihar/building-multi-page-web-app-using-streamlit-7a40d55fa5b4
    # http://awesome-streamlit.org/https://news.ycombinator.com/item?id=21158487https://towardsdatascience.com/coding-ml-tools-like-you-code-ml-models-ddba3357eace
    # https://docs.streamlit.io/en/stable/caching.html
    df = data_prep_total_enrollment()
    df_assessment = data_prep_assessment()
    df_final_merged = data_prep_final_merged()
    
    def total_enrollment_total_revenue(df):
        size_distric = st.selectbox(
            "Filter by distric size",
            ("Non-LA districts", "General Districs", "Large Districs")
        )
        df_nonLosAngeles = df.drop(493, axis=0)
        df_general_districts = df_nonLosAngeles[df_nonLosAngeles['Total Enrollment']<10000]
        df_large_districts = df_nonLosAngeles[df_nonLosAngeles['Total Enrollment']>10000]

        size_districs_options = {"Non-LA districts": df_nonLosAngeles, "General Districs": df_general_districts, "Large Districs": df_large_districts}
        
        plt.figure()
        sns.scatterplot(x='Total Enrollment', y='Total Revenue',data=size_districs_options[size_distric], palette="plasma")
        plt.title('Total enrollment vs Total revenue')
        st.pyplot(plt)

    def mean_scale_score_by_ethnicity(df):
        plt.figure()
        sns.catplot(x="Subgroup ID", y="Mean Scale Score", hue="Test Id", kind="box", data=df, palette="plasma")
        plt.xticks(rotation=45, ha='right')
        _=plt.title('Mean Scale Score per ethnicity')
        st.pyplot(plt)
        st.text('We can see that Black and hispanic students have the lower scores')


    def revenue_scale_scores_scatterplot(df):
        st.markdown('## Our main question is: Does Revenue per student impact Student scores?')
        plt.figure()
        g = sns.FacetGrid(df, row='Subgroup ID', 
                  margin_titles=True, height=6, aspect=2, palette="plasma")
        g.map(sns.regplot,'Revenue per student', 'Mean Scale Score', marker="x")
        _=g.set(xlim=(3000, 20000), 
         ylim=(2300, 2700))
        _=g.add_legend()
        st.pyplot(plt)

    def correlation_table_revenue_scores_ethnicity(df):
        plt.figure()
        corr_cols=['District Code', 'Agency Name', 'Total Revenue',
       'Total Enrollment',
       'County Code', 'Test Id',
       'Total Tested At Entity Level', 'Total Tested with Scores',
       'CAASPP Reported Enrollment', 'Students Tested', 'Students with Scores',
       'Total Standard Exceeded', 'Total Standard Met',
       'Total Standard Met and Above', 'Total Standard Nearly Met',
       'Total Standard Not Met', 'Percentate Std Exceed', 'Percentage Std Met',
       'Percentage Std Nearly Met', 'Percentage Std Not Met',
       'Percentage Std Met and Above']
        df_corr= df.drop(columns= corr_cols)
        #corr=df_corr.corr()
        #corr.style.background_gradient(cmap='PiYG')
        #corr.style.background_gradient(cmap='coolwarm')
        # https://github.com/altair-viz/altair/pull/1945
        corrMatrix = df_corr.corr().reset_index().melt('index')
        corrMatrix.columns = ['Revenue per student', 'Count Enrollment per ethnicity', 'correlation']
        chart = alt.Chart(corrMatrix).mark_rect().encode(
            x=alt.X('Revenue per student', title=None),
            y=alt.Y('Count Enrollment per ethnicity', title=None),
            color=alt.Color('correlation', legend=None),
        ).properties(
            width=alt.Step(80),
            height=alt.Step(80)
        )

        chart += chart.mark_text(size=25).encode(
            text=alt.Text('correlation', format=".2f"),
            color=alt.condition(
                "datum.correlation > 0.1",
                alt.value('white'),
                alt.value('black')
            )
        )
        chart.height=800
        st.altair_chart(chart)

        r,p,lo,hi=pearsonr_ci(df['Revenue per student'],df['Mean Scale Score'])
        st.text('The correlation coefficient is value is ' + str(r))
        st.text('The P for 95% is ' + str(p))
        st.text('The lower point of the confident interval is ' + str(lo))
        st.text('The higher point of the confidence interval is ' + str(hi))
        st.markdown('''
        ### It seems that revenue per student has a negative correlation to Mean Scale score or students passing. As we noted on each of the different ethnicities it would seem the larger the revenue per student the lower test scores, which is not what we were expecting. We then looked into searching for other factors that might be driving scores to be low.
            ''')

    total_enrollment_total_revenue(df)
    mean_scale_score_by_ethnicity(df_assessment)
    revenue_scale_scores_scatterplot(df_final_merged)
    correlation_table_revenue_scores_ethnicity(df_final_merged)
