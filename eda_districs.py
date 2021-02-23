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
from helpers import best_fit
# pip uninstall protobuf python3-protobuf
# pip install --upgrade pip
# pip install --upgrade protobuf 
from scipy import stats

def app():
    st.title('Economical Background')
    st.header('We went and got information on the economical background of students, and classified as Economically Disadvantaged and Not Economically Disadvantaged.')
    df = data_prep_final_merged()

    def ethnicity_scores_revenue(df):
        plt.figure()
        kpi = st.selectbox(
            "Break down by",
            ("Mean Scale Score", "Percentage of students that Pass")
        )
        if kpi == "Mean Scale Score":
            a, b = best_fit(df['Revenue per student'],df['Mean Scale Score'])
            plt.figure(figsize=(15,6))
            sns.scatterplot(df['Revenue per student'],df['Mean Scale Score'], hue=df['Disadvantaged'], palette='plasma')
            yfit = [a + b * xi for xi in df['Revenue per student']]
            plt.plot(df['Revenue per student'], yfit,color='green')
            plt.title('No Relationship between Mean Scale Score and Revenue per student', fontsize=16)
            plt.xlabel('Revenue per Student', fontsize=16)
            _=plt.ylabel('Mean Scale Score', fontsize=16)
            st.pyplot(plt)
            st.subheader('Observations')
            st.text('- Mean Scale Score vs Revenue per Student by disadvantaged category.')
            st.text('- The best fit line is almost flat indicating no noticeable \n relationship between the variables.')
            st.text('- There is an evident difference between the mean scale score \n for the disadvantaged category.')
            st.text('- Students in the disadvantaged category seems to clearly score \n lower than students in the not disadvantaged category')
            
        else:
            plt.figure(figsize=(15,6))
            sns.scatterplot(df['Revenue per student'],df['Pass'],hue=df['Disadvantaged'], palette='plasma')
            plt.axhline(y=40, color='g', linestyle='-')
            plt.title('Percentage of Pass vs. Revenue per student by Disadvantaged category', fontsize=16)
            plt.xlabel('Revenue per Student', fontsize=16)
            _=plt.ylabel('% Pass', fontsize=16)
            st.pyplot(plt)
            st.subheader('Observations')
            st.text('- Percentage of students who pass the standard vs revenue per student by disadvantaged category.')
            st.text('- A higher percentage of not disadvantaged students pass the standards.')
            st.text('- A lower percentage of disadvantaged students pass the standards.')
            st.text('- Consequently, a higher percentage of disadvantaged students fail the standards.')

    def scale_scores_per_student_by_disadvantaged(df):
        st.header("Comparing Mean Scale Scores")
        plt.figure()
        kpi = st.selectbox(
            "Break down by:",
            ("Economic Background", "Economic Background by Ethnicity")
        )
        if kpi == "Economic Background":
            plt.figure(figsize=(12,8))
            sns.catplot(x="Disadvantaged", y="Mean Scale Score", kind="box", data=df, palette='plasma')
            plt.xticks(rotation=45, ha='right')
            plt.title('Disadvantage students Mean Scores are lower in average', fontsize = 16)
            plt.xlabel('Disadvantaged', fontsize=16)
            _ = plt.ylabel('Mean Scale Score', fontsize=16)
            st.pyplot(plt)
            st.text('The p value is 9.17 e-293')   
        else:
            plt.figure(figsize=(12,8))
            sns.catplot(x="Subgroup ID", y="Mean Scale Score", 
                hue="Disadvantaged", 
                kind="box", data=df, palette='plasma') #plasma
            plt.xticks(rotation=45, ha='right')
            plt.title('Disadvanted Students Underperform Regardless of Ethnicity', fontsize=16)
            plt.xlabel('Ethnicity', fontsize=16)
            _ = plt.ylabel('Mean Scale Score', fontsize=16)
            st.pyplot(plt)

    def all_district_size_by_disadvantaged(df):
        st.header("% of Students Passing the standard is lower for Disadvantaged Students")
        plt.figure(figsize=(15,6))
        sns.lmplot(x="Revenue per student", y="Pass", hue="Disadvantaged", palette="plasma",
           col="Subgroup ID",
           data=df, col_wrap=4, height=5);
        st.pyplot(plt)
        st.subheader('Observations')
        st.text('- Revenue per student continues to show negative to no relationship for \n both disadvantaged and not disadvantaged category for most of the ethnicities.')
        
    def all_districts_by_sizes(df):
        st.markdown('''
            ### It was very clear that we had a large gap between disadvantaged and not disadvantaged students. Next we looked for patterns on the size of the district.
            ''')
        cut_labels = ['Smaller', 'Small', 'Medium', 'Large']
        # todo make this dynamic.
        cut_bins = [0, 10000, 30000, 60000,130000]
        df['district_enrollment'] = pd.cut(df['Total Enrollment'], bins=cut_bins, labels= cut_labels)
        plt.figure(figsize=(25, 10))
        sns.scatterplot(x='Revenue per student', y='Mean Scale Score', palette ='plasma', hue='district_enrollment', s=100, data=df)
        st.pyplot(plt)
        st.markdown('''
            ### The district size didn't show any patterns of revenue allocation. ''')

    ethnicity_scores_revenue(df)
    scale_scores_per_student_by_disadvantaged(df)
    all_district_size_by_disadvantaged(df)
    all_districts_by_sizes(df)