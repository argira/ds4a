import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as sm
import altair as alt
from load_data import data_prep_total_enrollment
from load_data import data_prep_assessment
#import warnings
# pip uninstall protobuf python3-protobuf
# pip install --upgrade pip
# pip install --upgrade protobuf 

# app1.py
import streamlit as st
def app():
    st.title('''Variables affecting students' success (K-12) in California''')

    st.markdown('''
    
    Hypotheses:
        1 - Revenue per student is positively correlated with students’ outcome.
        2 - Racial minority students outperform in schools with higher revenue per student.

    Data Analysis was performed on for California School Districts, for the school year 2016-2017. The variables we used are Mean scale scores, which is the mean of all schools in the district for all the grades.

    * Test id 1 are the results for Literature and Arts.
    * Test id 2 are the results for Mathematics 
    Revenue per student, which is the revenue schools receive from local, state and federal sources divided by the students enrolled in the district.
    Enrollment per ethnicity, were we gathered 7 different ethnicities data.

    Data Sources:
      * Enrollment and Revenue data gathered from the Nacional Center for Education Statistics - table generator. https://nces.ed.gov/ccd/elsi/tableGenerator.aspx

      * Assessment data gathered from California assessment student performance and progress. https://caaspp-elpac.cde.ca.gov/caaspp/ResearchFileList?ps=true&lstTestYear=2019&lstTestType=B&lstCounty=00&lstDistrict=00000&lstSchool=0000000

    ''')

    df = data_prep_total_enrollment()
    df_assessment = data_prep_assessment()
    # df_nonLosAngeles = df.drop(493, axis=0)
    # df_general_districts = df_nonLosAngeles[df_nonLosAngeles['Total Enrollment']<10000]
    # df_large_districts = df_nonLosAngeles[df_nonLosAngeles['Total Enrollment']>10000]

    def histogram_revenue_per_student(df):
        plt.figure(figsize=(8,6))
        sns.displot( x="Revenue per student",kind="kde",  data=df, palette='plasma', fill=True)
        plt.title('Revenue per student averages $9409', fontsize = 16)

        # Adding labels
        _ = plt.xlabel('Revenue per student', fontsize=16)
        _ = plt.ylabel('Density', fontsize=16)

        st.pyplot(plt)

    def enrollment_per_ethnicity(df):
        DFfinMelt = pd.melt(df, id_vars=['District Code', 'Agency Name', 'Total Enrollment', 'Total Revenue', 'Revenue per student'], 
        value_vars=['Black', 'Hispanic', 'White', 'Asian or Asian/Pacific Islander','American Indian/Alaska Native', 'Hawaiian Nat./Pacific Isl.','Two or More Races'])
        DFfinMelt.columns = ['District Code', 'Agency Name', 'Total Enrollment', 'Total Revenue','Revenue per student', 'Subgroup ID', 'Count Enrollment per ethnicity']
        pivot_df = DFfinMelt.pivot_table(values='Count Enrollment per ethnicity',index='Subgroup ID', aggfunc=np.sum).reset_index()
        pivot_df.columns = ['Ethnicity', 'Total Enrollment']
        pivot_df['Percent']=pivot_df['Total Enrollment']/(pivot_df['Total Enrollment'].sum())*100
        #pivot_df.style.format({'Total Enrollment': "{:,.0f}"})#,'Percent':"{:.0%}"})#,'Percent Not Disadvantaged':"{:.2%}"})
        y = list(pivot_df['Percent'])
        #Seaborn Horizontal barplot
        #sns.set_style("whitegrid")
        ax = plt.subplots(figsize=(10,6))
        ax = sns.barplot(x="Total Enrollment", y='Ethnicity', data=pivot_df, ci=None ,orient='h', palette="plasma" )
        ax.set_title("California is a minority- majority State with Hispanics representing 50% of the population" , fontsize = 16)
        ax.set_xlabel ("Enrollment", fontsize = 16)
        ax.set_ylabel ("Ethnicity", fontsize = 16)
        for i, v in enumerate(pivot_df['Percent']):
            ax.text(v, i + .25,"%.2f%%"%(v), color='darkblue')
        st.pyplot(plt)

    def histogram_scale_scores(df):
        plt.figure(figsize=(6,4))
        sns.displot( x="Mean Scale Score",kind="kde",  data=df, palette='plasma', fill=True)
        plt.title('Mean Scale Scores average 2520 points', fontsize = 16)
        st.pyplot(plt)

    def barplot_percentage_students_pass_fail(df):
        plt.figure(figsize=(6,4))
        status = st.selectbox(
            "Filter by status",
            ("Pass", "Fail")
        )
        status_options = {"Pass": 'Percent of Students that Pass the Standard', "Fail": 'Percent of Students that Fail the Standard'}
        sns.catplot(x="Subgroup ID", y=status, kind="box", data=df, palette="plasma")
        plt.xticks(rotation=45, ha='right')
        _=plt.title(status_options[status])
        _=plt.xlabel ('Ethnicity', fontsize = 16)
        st.pyplot(plt)


    histogram_revenue_per_student(df)
    plt.figure()
    enrollment_per_ethnicity(df)
    plt.figure()
    histogram_scale_scores(df_assessment)
    plt.figure()
    barplot_percentage_students_pass_fail(df_assessment)

