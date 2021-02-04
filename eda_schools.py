import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as sm
import altair as alt
from load_data import data_prep_by_school
# pip uninstall protobuf python3-protobuf
# pip install --upgrade pip
# pip install --upgrade protobuf 
from scipy import stats
from helpers import best_fit
from helpers import pearsonr_ci_details

def app():
    st.markdown('''
        ### After more investigation and research, we decided to look at the assessment data at the school level instead of the district level. Also, we looked to evaluate where the money was spent and how that could impact scores as well. We looked for other factors, like Teacher-Student Ratio, FTE Teachers.
        ''')

    df = data_prep_by_school()

    def correlation_disadvantaged_expense_others(df):
        st.text('Correlaiton of revenue sources Vs Scores and Pass Fail')
        corr_columns = ['School Name', 'District Name', 'District Code_x',
               'Total Current Expenditures - Instruction (TCURINST) per Pupil ',
               'Total Current Expenditures - Support Services (TCURSSVC) per Pupil ',
               'Total Current Expenditures - Other El-Sec Programs (TCUROTH) per Pupil',
               'Total Current Expenditures - Salary (Z32) per Pupil ',
               'Total Current Expenditures - Benefits (Z34) per Pupil ',
               'Total Expenditures (TOTALEXP) per Pupil ',
               'Total Expenditures - Capital Outlay (TCAPOUT) per Pupil ',
               'Total Current Expenditures - Non El-Sec Programs (TNONELSE) per Pupil',
               'Total Current Expenditures (TCURELSC) per Pupil',
               'Instructional Expenditures (E13) per Pupil ', 'Subgroup ID','County Code', 'District Code_y',
               'School Code', 'Test Id',
               'Total Tested At Entity Level', 'Total Tested with Scores',
               'CAASPP Reported Enrollment', 'Students Tested', 'Students with Scores',
               'Total Standard Exceeded', 'Total Standard Met',
               'Total Standard Met and Above', 'Total Standard Nearly Met',
               'Total Standard Not Met', 'Disadvantaged', 'Zip Code','Percentate Std Exceed', 'Percentage Std Met',
               'Percentage Std Nearly Met', 'Percentage Std Not Met',
               'Percentage Std Met and Above']
        df_corr = df.drop(columns= corr_columns)
        corrMatrix = df_corr.corr().reset_index().melt('index')
        corrMatrix.columns = ['Total Enrollment', 'Full-Time Equivalent (FTE) Teachers', 'correlation']
        chart = alt.Chart(corrMatrix).mark_rect().encode(
            x=alt.X('Total Enrollment', title=None),
            y=alt.Y('Full-Time Equivalent (FTE) Teachers', title=None),
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

    def revenue_per_student_score_disadvantage(df):
        revenue = st.selectbox(
            "Revenue per pupil",
            (">= $8000 & < $12000", "> $12000")
        )
        if revenue == ">= $8000 & < $12000":
            df_revenue=df[(df['Total Revenue (TOTALREV) per Pupil ']>=8000) & (df['Total Revenue (TOTALREV) per Pupil ']<12000)]
        else:
            df_revenue=df[df['Total Revenue (TOTALREV) per Pupil ']>12000]

        a, b = best_fit(df_revenue['Total Revenue (TOTALREV) per Pupil '],df_revenue['Mean Scale Score'])
        plt.figure(figsize=(15,6))
        sns.scatterplot(df_revenue['Total Revenue (TOTALREV) per Pupil '],df_revenue['Mean Scale Score'],
                        hue=df_revenue['Disadvantaged'], palette='plasma')
        yfit = [a + b * xi for xi in df_revenue['Total Revenue (TOTALREV) per Pupil ']]
        plt.plot(df_revenue['Total Revenue (TOTALREV) per Pupil '], yfit,color='red')
        plt.title('Schools Schores Vs Revenue per pupil for California')
        plt.xlabel('Revenue per Student')
        _=plt.ylabel('Mean Scale Score')
        st.pyplot(plt)
        pearsonr_ci_details(df_revenue['Total Revenue (TOTALREV) per Pupil '],df_revenue['Mean Scale Score'])

    def total_enrollment_scores(df):
        st.markdown('''
            ### Compare scores with Total Enrollment of schools, on the correlation, there seems to be a positive correlation.
            ''')
        a, b = best_fit(df['Total Enrollment'],df['Mean Scale Score'])
        plt.figure(figsize=(10,6))
        sns.scatterplot(df['Total Enrollment'],df['Mean Scale Score'], hue=df['Disadvantaged'],palette='plasma')
        yfit = [a + b * xi for xi in df['Total Enrollment']]
        plt.plot(df['Total Enrollment'], yfit, color='red')
        plt.title('Schools Schores Vs School Enrollment per pupil for California')
        plt.xlabel('Total Enrollment')
        _=plt.ylabel('Mean Scale Score')
        st.pyplot(plt)
        pearsonr_ci_details(df['Total Enrollment'],df['Mean Scale Score'])

    def teacher_student_ratio(df):
        st.markdown('''
            ### Teacher/Student Ratio also showed a positive correlation.
            ''')
        df_ts=df[df['Pupil/Teacher Ratio']<30]
        a, b = best_fit(df_ts['Pupil/Teacher Ratio'],df_ts['Mean Scale Score'])
        plt.figure(figsize=(10,6))
        sns.scatterplot(df_ts['Pupil/Teacher Ratio'],df_ts['Mean Scale Score'], hue=df_ts['Disadvantaged'],palette='plasma')
        yfit = [a + b * xi for xi in df_ts['Pupil/Teacher Ratio']]
        plt.plot(df_ts['Pupil/Teacher Ratio'], yfit, color='red')
        plt.title('Schools Scores Vs School Teacher/Student Ratiofor California')
        plt.xlabel('Teacher Student Ratio')
        _=plt.ylabel('Mean Scale Score')
        st.pyplot(plt)
        pearsonr_ci_details(df['Pupil/Teacher Ratio'],df['Mean Scale Score'])

    correlation_disadvantaged_expense_others(df)
    revenue_per_student_score_disadvantage(df)
    total_enrollment_scores(df)
    teacher_student_ratio(df)
