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
    st.title('We went and got information on the economical background of students, and classified as Economically Disadvantaged and Not Economically Disadvantaged.')
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
            plt.title('Mean Scale Scores Vs Revenue per student for California')
            plt.xlabel('Revenue per Student')
            _=plt.ylabel('Mean Scale Score')
            st.pyplot(plt)
        else:
            plt.figure(figsize=(15,6))
            sns.scatterplot(df['Revenue per student'],df['Pass'],hue=df['Disadvantaged'], palette='plasma')
            plt.axhline(y=40, color='g', linestyle='-')
            plt.title('Percentage of students that Pass the Standard Vs Revenue per student for California')
            plt.xlabel('Revenue per Student')
            _=plt.ylabel('Percentage of students that pass the standard')
            st.pyplot(plt)

    def scale_scores_per_student_by_disadvantaged(df):
        plt.figure(figsize=(15,6))
        sns.catplot(x="Subgroup ID", y="Mean Scale Score", hue="Disadvantaged", kind="box", data=df, palette="plasma")
        plt.xticks(rotation=45, ha='right')
        _=plt.title('Mean Scale Score per ethnicity - Disadvantaged vs Not Disadvantged')
        st.pyplot(plt)

    def all_district_size_by_disadvantaged(df):
        plt.figure(figsize=(15,6))
        sns.lmplot(x="Revenue per student", y="Pass", hue="Disadvantaged", palette="plasma",
           col="Subgroup ID",
           data=df, col_wrap=4, height=5);
        st.pyplot(plt)

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
        plt.show()

    ethnicity_scores_revenue(df)
    scale_scores_per_student_by_disadvantaged(df)
    all_district_size_by_disadvantaged(df)
    all_districts_by_sizes(df)