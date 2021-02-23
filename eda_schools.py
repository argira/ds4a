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
    st.header("School Level EDA")
    st.markdown('''
        ### After more investigation and research, we decided to look at the assessment data at the school level. \n Also, we looked to evaluate where the money was spent and how that could impact scores as well. We looked for other factors, like Teacher-Student Ratio, Full-Time Equivalent Teachers.
        ''')

    df = data_prep_by_school()

    def disadvantaged_displot(df):
        
        st.subheader('Disadvantaged Students continued to underperformed on average in comparison to Not Disadvantaged students.')
        plt.figure(figsize=(10,8))
        sns.displot( x="Mean Scale Score", kind="kde", data=df, palette='plasma', hue='Disadvantaged', fill=True)
        #plt.title("Mean Scale Score per Disadvantaged category", fontsize=16)
        plt.xlabel('Mean Scale Score', fontsize=16)
        _ = plt.ylabel('Density', fontsize=16)
        st.pyplot(plt)


    def correlation_disadvantaged_expense_others(df):
        st.subheader('Correlation was negative to null to Revenue Sources or Expense Allocation at the School Level')
        plt.figure()
        kpi = st.selectbox(
            "Break down by",
            ("Correlation to Revenue Sources and other factors", "Correlation to Expense Allocation")
        )
        if kpi == "Correlation to Revenue Sources and other factors":
            st.subheader('Correlaiton of revenue sources Vs Scores and Pass Fail')
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
            width=alt.Step(40),
            height=alt.Step(40)
            )

            chart += chart.mark_text(size=15).encode(
                text=alt.Text('correlation', format=".2f"),
                color=alt.condition(
                    "datum.correlation > 0.1",
                    alt.value('white'),
                    alt.value('black')
                )
            )
            chart.height=600
            st.altair_chart(chart)
        else:
            st.subheader('Correlaiton of Expense Allocation and Scores')
            corr_columns = ['School Name', 'District Name', 'District Code_x','Full-Time Equivalent (FTE) Teachers', 
                'Pupil/Teacher Ratio',
                'Total Revenue (TOTALREV) per Pupil ',
                'Total Revenue - Local Sources (TLOCREV) per Pupil ',
                'Total Revenue - State Sources (TSTREV) per Pupil',
                'Total Revenue - Federal Sources (TFEDREV) per Pupil ',
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
              width=alt.Step(40),
              height=alt.Step(40)
              )

            chart += chart.mark_text(size=15).encode(
                    text=alt.Text('correlation', format=".2f"),
                    color=alt.condition(
                        "datum.correlation > 0.1",
                        alt.value('white'),
                        alt.value('black')
                    )
            )
            chart.height=600
            st.altair_chart(chart)


    def relationship_comparison(df):
        st.subheader('We reviewed the Mean Scale Scores Relationship to other Factors')
        revenue = st.selectbox(
            "Correlation to:",
            ("Revenue per Student by Ethnicity", "Joint Distribution by Economical Background", 'Total School Enrollment','Full-Time equivalent Teacher','Expenditures in Salary')
        )
        if revenue == "Revenue per Student by Ethnicity":
            st.markdown('''### Revenue per pupil at the school level continues to show a null to negative correlation to scores''')
            a, b = best_fit(df['Total Revenue (TOTALREV) per Pupil '],df['Mean Scale Score'])
            plt.figure(figsize=(15,6))
            sns.scatterplot(df['Total Revenue (TOTALREV) per Pupil '],df['Mean Scale Score'],
                hue=df['Subgroup ID'])
            yfit = [a + b * xi for xi in df['Total Revenue (TOTALREV) per Pupil ']]
            plt.plot(df['Total Revenue (TOTALREV) per Pupil '], yfit,color='green')
            plt.title('''Ethnicity performance doesn't  seem to vary based on Revenue per Student''', fontsize=18)
            plt.xlabel('Revenue per Student', fontsize=18)
            _=plt.ylabel('Mean Scale Score', fontsize=18)
            st.pyplot(plt)
            pearsonr_ci_details(df['Total Revenue (TOTALREV) per Pupil '],df['Mean Scale Score'])

        if revenue == 'Joint Distribution by Economical Background':
            _ = sns.jointplot(x='Total Revenue (TOTALREV) per Pupil ', y='Mean Scale Score', hue='Disadvantaged', data=df, kind="kde", palette='plasma')
            _.fig.set_size_inches(8,6)

            st.pyplot(plt)
        

        if revenue == 'Total School Enrollment':   
            st.markdown('''
                ### Scores Vs Total Enrollment of schools, show a positive relationship.
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

        if revenue == 'Full-Time equivalent Teacher':
            st.markdown('''
                ### FTE Teacher shows to have a positive impact in scores as well.
                ''')
            a, b = best_fit(df['Full-Time Equivalent (FTE) Teachers'],df['Mean Scale Score'])
            plt.figure(figsize=(15,8))
            sns.scatterplot('Full-Time Equivalent (FTE) Teachers','Mean Scale Score', hue='Disadvantaged',palette='YlGnBu', data=df)
            yfit = [a + b * xi for xi in df['Full-Time Equivalent (FTE) Teachers']]
            plt.plot(df['Full-Time Equivalent (FTE) Teachers'], yfit, color='red')
            plt.title('Mean Scale Score vs Full-Time Equivalent Teacher', fontsize=18)
            plt.xlabel('FTE TEachers', fontsize=18)
            _=plt.ylabel('Mean Scale Score', fontsize=18)
            st.pyplot(plt)
            pearsonr_ci_details(df['Full-Time Equivalent (FTE) Teachers'],df['Mean Scale Score'])
            st.subheader('Observation')
            st.markdown('''
                        ### We see that the distribution of FTE teachers is not different based on the economic background of students. Rather is in function of enrollment of students, it is unclear why Revenue per Student shows a negative or non correlation to  FTE teachers.
                        ''')
            st.subheader('Statistics for FTE teachers to Total revenue per student')
            pearsonr_ci_details(df['Full-Time Equivalent (FTE) Teachers'],df['Total Revenue (TOTALREV) per Pupil '])
            st.subheader('Statistics for FTE teachers to Total Expenditures per pupil')
            pearsonr_ci_details(df['Full-Time Equivalent (FTE) Teachers'],df['Total Expenditures (TOTALEXP) per Pupil '])

        if revenue == 'Expenditures in Salary':
            st.subheader('''Total Salary Expenditures didn't show relationship to Scores as well.''')
            a, b = best_fit(df['Total Current Expenditures - Salary (Z32) per Pupil '],df['Mean Scale Score'])
            plt.figure(figsize=(15,8))
            sns.scatterplot(df['Total Current Expenditures - Salary (Z32) per Pupil '],df['Mean Scale Score'], hue=df['Disadvantaged'],palette='plasma')
            yfit = [a + b * xi for xi in df['Total Current Expenditures - Salary (Z32) per Pupil ']]
            plt.plot(df['Total Current Expenditures - Salary (Z32) per Pupil '], yfit, color='red')
            plt.title('Mean Scale Score vs. Salary Expenditures per Disadvantaged category', fontsize=18)
            plt.xlabel('Total Current Salary Expenditures', fontsize=18)
            plt.ylabel('Mean Scale Score', fontsize=18)
            st.pyplot(plt)
            pearsonr_ci_details(df['Total Current Expenditures - Salary (Z32) per Pupil '],df['Mean Scale Score'])


    disadvantaged_displot(df)
    correlation_disadvantaged_expense_others(df)
    relationship_comparison(df)
    
