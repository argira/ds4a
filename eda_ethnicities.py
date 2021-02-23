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
from helpers import chi_squared_details

def app():
    st.header("Observations by Ethnicity")
    st.markdown('''
                    ### Looking at the slightly negative correlation between Revenue per student and Mean Scale Score. And also seeing a prevalence of low scores for Disadvantaged students. We wondered if schools with a majority of disadvantaged students might be getting higher revenue which would explain our initial findings.
                ''')

    df = data_prep_by_school()

    
    def revenue_distributed_disadvantaged(df):
        
        plt.figure(figsize=(12,6))
        sns.displot(df, x='Total Revenue (TOTALREV) per Pupil ', hue='Disadvantaged', kind="kde", palette='plasma',fill=True)
        plt.title("Economically Disadvantaged Students are getting more revenue than Not disadvantaged Students", fontsize=18)
        plt.xlabel('Revenue per Student', fontsize=18)
        plt.ylabel('Density', fontsize=18)
        st.pyplot(plt)

    def ethnicity_distribution(df):
        st.subheader('We also can see that the disfferent ethnicities fall within a different distribution, next we tested the differences between Means of the Ethnicities')
        plt.figure(figsize=(12,6))
        sns.displot(df, x='Mean Scale Score', hue='Subgroup ID', kind="kde", fill=True, palette='plasma')
        plt.title("Mean Scale Score difference between ethnicities", fontsize=18)
        plt.xlabel('Mean Scale Score', fontsize=18)
        _=plt.ylabel('Density', fontsize=18)
        st.pyplot(plt)

    cross=pd.crosstab(df['Subgroup ID'], df['Disadvantaged'])
    dis_ethnicity_prop = round(cross.div(cross.sum(axis=1), axis=0)*100,2)

    def observations_ethnicity(df):
        st.subheader('Black and American Indian/Alaska Native students show the lowest mean scale scores.')
        st.markdown('''
                ### We performed a pairwise ttest to see if the differences in mean scores for the different ethnicities were significantly different.
                ### Since Black, American Indian/Alaska Natives and Hispanics had the lowest scores but their populations are different. We also see that Hawaiian Nationals have a 100 percent disadvantage population with higher mean scores than the mentioned ethnnicities.
                ### The pairwise results tell us that the difference in mean between American Indian/Alaska Natives to Hawaiian Nationals, Blacks and Hispanics is not statistically significant. With these ethnicities having a high number of disadvantaged students.
                ### While Black studens do have a statistical difference to Hispanics which show different levels of not disadvantaged students.
                ''')
        plt.figure()
        sns.catplot(x="Subgroup ID", y="Mean Scale Score", kind="box", data=df, palette="plasma", height=6, aspect=2)
        plt.xticks(rotation=45, ha='right')
        _ = plt.xlabel('Ethnicity', fontsize=18)
        _ = plt.ylabel('Mean Scale Score', fontsize=18)
        st.pyplot(plt)


    def percent_ethnicities(df):
        st.subheader('Higher percentage of Disadvantaged students are present on lower performing ethnicities')
        plt.figure()
        plt_prop = dis_ethnicity_prop.plot(kind='bar', stacked = True, width = 1,colormap='Spectral')
        plt_prop.legend(bbox_to_anchor=(1,1), loc='upper left', ncol = 1)
        plt.xticks(rotation=60, ha='right')
        _ = plt.xlabel('Ethnicity', fontsize=18)
        _ = plt.ylabel("%", fontsize=18)
        st.pyplot(plt)
        chi_squared_details(cross)

        

        st.markdown('''
                ## Conclusion:

                ### Our results show that coming from an economically disadvantaged background is a better predictor of students' outcome than schools' revenue.
                ### Disadvantaged students underperform not disadvantaged students on both outcome measures, that are mean scale score and passing the standards.
                ### Schools receive higher revenue per disadvantaged students. 
                ### Outside research points out to changes that have been made in California in order to provide more resources to disadvantaged students, this can be why we see none to negative correlation between revenue per student and mean scale score. To understand the impact these changes have on disadvantaged students, we will require an evaluation through several years,  from the time the changes were implemented.  
                ### The next step would be the analysis of how this revenue has been spent, to see what kind of matter provides better outcomes. 
                ### On the small analysis we performed, Full-Time Elective Teachers had a positive correlation to scores, as well as "other Elementary-Secondary Education" expenses.
                ''')
    revenue_distributed_disadvantaged(df)
    ethnicity_distribution(df)
    observations_ethnicity(df)
    percent_ethnicities(df)