# app2.py
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
from helpers import best_fit
def app():
    df = pd.read_csv('~/team_84/notebooks/20210111/final_merged_latest.csv', index_col = 0)
    '''
    # TEST ID 1  braken down by district size
    '''
    #Converting all the assessment columns back to  percentage columns for exceeded, nearly met, not met to show completion results as percentage of test taken
    df['Percentate Std Exceed'] =(df['Total Standard Exceeded']/df['Students Tested']*100).round(decimals=0)
    df['Percentage Std Met'] =(100*df['Total Standard Met']/df['Students Tested']).round(decimals=0)
    df['Percentage Std Nearly Met'] =(100*df['Total Standard Nearly Met']/df['Students Tested']).round(decimals=0)
    df['Percentage Std Not Met'] =(100*df['Total Standard Not Met']/df['Students Tested']).round(decimals=0)
    df['Percentage Std Met and Above'] =(100*df['Total Standard Met and Above']/df['Students Tested']).round(decimals=0)
    #Percentage was multiplied by the students tested information and not the total enrollment information.
    #Students tested in Math and Literacy can be the same students or different students, we don't have that information.
    #we are adding the results of both exams, this can cause a duplicate in value of students tested, I will separate both datasets

    df['Pass'] = df['Percentate Std Exceed'] + df['Percentage Std Met']
    df['Fail'] = df['Percentage Std Nearly Met'] + df['Percentage Std Not Met']
    # filtering based on total enrollment
    df = df[df['Total Enrollment'] != 0]
    df = df[df['Total Enrollment'] > 250]

    # need to filter out the 6 schools that have more students tested than enrolled

    # dataset containing school districts with over $20,000 revenue per student
    df_high_funding = df[(df['Revenue per student'] > 20_000)]

    # update the main dataset to not include schools with over 20k revenue per student nor zero revenue per student
    df = df[(df['Revenue per student'] < 20_000)]
    df = df[(df['Revenue per student'] != 0)]
    
    st.markdown('## Ethnicity breakdown in districts w/high funding')

    #plt.figure(figsize=(6, 4))
    sns.barplot(x='Count Enrollment per ethnicity',y='Agency Name',hue='Subgroup ID',data=df_high_funding)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt)

    # https://github.com/streamlit/streamlit/issues/638
    plt.figure() 

    st.markdown('## We are looking at the schools and were are they in the revenue/score comparison')

    plt.figure(figsize=(10, 4))
    sns.scatterplot(x='Revenue per student', y='Mean Scale Score', hue='Agency Name',data=df_high_funding)
    st.pyplot(plt)

    # https://github.com/streamlit/streamlit/issues/638
    plt.figure() 

    # def best_fit(X, Y):

    #     xbar = sum(X)/len(X)
    #     ybar = sum(Y)/len(Y)
    #     n = len(X) # or len(Y)

    #     numer = sum([xi*yi for xi,yi in zip(X, Y)]) - n * xbar * ybar
    #     denum = sum([xi**2 for xi in X]) - n * xbar**2

    #     b = numer / denum
    #     a = ybar - b * xbar

    #     #print('best fit line:\ny = {:.2f} + {:.2f}x'.format(a, b))

    #     return a, b
    a, b = best_fit(df_high_funding['Revenue per student'],df_high_funding['Mean Scale Score'])
    plt.scatter(df_high_funding['Revenue per student'],df_high_funding['Mean Scale Score'])
    yfit = [a + b * xi for xi in df_high_funding['Revenue per student']]
    plt.plot(df_high_funding['Revenue per student'], yfit)
    plt.title('Mean Scale Score relationship to Revenue for Highly funded districts')
    plt.xlabel('Revenue per Student')
    _=plt.ylabel('Mean Scale Score')
    st.pyplot(plt)


        ## Initial EDA


    '''
        The analysis was performed on Data from 2016-2017 school year.
        Data Analysis has been performed at the District level, were Mean scale scores are the mean of all schools in the district for all the grades.

        Test id 1 are the results for Literature and Arts.
        Test id 2 are the results for Mathematics 

        Data Sources:
                - Enrollment and Revenue data gathered from the Nacional Center for Education Statistics - table generator. https://nces.ed.gov/ccd/elsi/tableGenerator.aspx

               - Assessment data gathered from California assessment student performance and progress. 
        https://caaspp-elpac.cde.ca.gov/caaspp/ResearchFileList?ps=true&lstTestYear=2019&lstTestType=B&lstCounty=00&lstDistrict=00000&lstSchool=0000000


        Districts with higher than 20K revenue per student were outliers in our data and were filtered, a total of 9 districts.
    '''

    df = pd.read_csv('~/team_84/organized notebooks/final_economic_merged.csv', index_col = 0)
    # filtering based on total enrollment
    df = df[df['Total Enrollment'] != 0]
    df = df[df['Total Enrollment'] > 250]

    #Converting all the assessment columns back to  percentage columns for exceeded, nearly met, not met to show completion results as percentage of test taken
    df['Percentate Std Exceed'] =(df['Total Standard Exceeded']/df['Students Tested']*100).round(decimals=0)
    df['Percentage Std Met'] =(100*df['Total Standard Met']/df['Students Tested']).round(decimals=0)
    df['Percentage Std Nearly Met'] =(100*df['Total Standard Nearly Met']/df['Students Tested']).round(decimals=0)
    df['Percentage Std Not Met'] =(100*df['Total Standard Not Met']/df['Students Tested']).round(decimals=0)
    df['Percentage Std Met and Above'] =(100*df['Total Standard Met and Above']/df['Students Tested']).round(decimals=0)
    #Percentage was multiplied by the students tested information and not the total enrollment information.
    #Students tested in Math and Literacy can be the same students or different students, we don't have that information.
    #we are adding the results of both exams, this can cause a duplicate in value of students tested, I will separate both datasets

    df['Pass'] = df['Percentate Std Exceed'] + df['Percentage Std Met']
    df['Fail'] = df['Percentage Std Nearly Met'] + df['Percentage Std Not Met']

    # filtering based on total enrollment
    df = df[df['Total Enrollment'] != 0]
    df = df[df['Total Enrollment'] > 250]

    # need to filter out the 6 schools that have more students tested than enrolled
    # update the main dataset to not include schools with over 20k revenue per student nor zero revenue per student
    df = df[(df['Revenue per student'] < 20_000)]
    df = df[(df['Revenue per student'] != 0)]

    '''
    ## DATASET TEST ID 1
    '''

    list = ['1.0']
    test_Id1 = df[df['Test Id'].isin(list)]
    test_ID1 = test_Id1.drop(['Test Id', 'County Code', 'Total Tested At Entity Level', 
                   'Total Standard Met and Above', 'Total Revenue',
                  'Total Tested with Scores', 'Students with Scores', 'District Code'], axis=1)

    _ = plt.hist(test_ID1['Revenue per student'], density=False, bins=30)
    _ = plt.ylabel('Number of ocurrences')
    _ = plt.xlabel('Revenue')
    _ = plt.title("Revenue per Student")

    st.pyplot(plt)

    # https://github.com/streamlit/streamlit/issues/638
    plt.figure() 

    st.markdown('## PASS/FAIL Dataset - Test ID 1')

    # adding pass and fail columns 
    test_ID1['Pass'] = test_ID1['Total Standard Exceeded'] + test_ID1['Total Standard Met']
    test_ID1['Fail'] = test_ID1['Total Standard Nearly Met'] + test_ID1['Total Standard Not Met']

    # creating a new dataframe by copying
    pass_fail_df = test_ID1.copy()

    # dropping columns
    pass_fail_df = pass_fail_df.drop(['Total Standard Exceeded', 'Total Standard Met', 'Total Standard Nearly Met', 
                   'Total Standard Not Met', 'CAASPP Reported Enrollment', 'Count Enrollment per ethnicity'], axis=1)

    #rearranging columns
    pass_fail_df = pass_fail_df.reindex(columns=['Agency Name', 'Subgroup ID','Revenue per student', 
                                                 'Mean Scale Score', 'Students Tested',
                                                 'Pass', 'Fail'])

    #corr.style.background_gradient(cmap='coolwarm')
    # https://github.com/altair-viz/altair/pull/1945
    corrMatrix = pass_fail_df.corr().reset_index().melt('index')
    corrMatrix.columns = ['var1', 'var2', 'correlation']
    chart = alt.Chart(corrMatrix).mark_rect().encode(
        x=alt.X('var1', title=None),
        y=alt.Y('var2', title=None),
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


    #hour_to_filter = st.sidebar.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
    #st.sidebar.checkbox('Show raw data')
    school_district_size = st.sidebar.selectbox(
        "Filter by school distric size",
        ("Large", "Medium", "Small")
    )

    school_district_size_options = {"Large": 60000, "Medium": 30000, "Small": 10}
    # large title: ## Large districts: above 60,000 total enrollment
    st.markdown('# TEST ID 1 dataset broken down by district size')



    list1 = ['White', 'Black', 'Hispanic']

    # Step 2: filter based on the list above
    test_ID1 = test_ID1[test_ID1['Subgroup ID'].isin(list1)]

    # filtering based on total enrollment
    large_districts_ID1 = test_ID1[test_ID1['Total Enrollment'] < school_district_size_options[school_district_size]]

    # there are 2 school dsitricts with enrollment larger or equal to 100,000
    #large_districts_ID1['Agency Name'].unique()

    _ = plt.hist(large_districts_ID1['Mean Scale Score'], density=False, bins=200)
    st.pyplot(plt)