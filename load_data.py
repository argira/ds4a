import pandas as pd

def data_prep_total_enrollment():

    df = pd.read_csv('../organized notebooks/dashboard_total_enrollment.csv', index_col = 0)
    #We eliminate the office of education and department of education because they don't have students enrolled directly
    df = df.loc[df['Agency Name'].apply(lambda x: 'OFFICE OF EDUCATION' not in x)]
    df = df.loc[df['Agency Name'].apply(lambda x: 'DEPARTMENT OF EDUCATION' not in x)]


    #Eliminate total enrollment is 0 or total revenue per student is 0, and only take schools with higher than 250 students. 
    #Investigation showed no school should have more than 20,000 revenue per student.
    df=df[df['Total Enrollment']!=0]
    df=df[df['Total Enrollment']>250]
    df=df[df['Revenue per student']!=0]
    df=df[df['Revenue per student']<20000]
    return df

def data_prep_assessment():
    return pd.read_csv('../organized notebooks/dashboard_assessment.csv', index_col=0)

def data_prep_final_merged():
    df = pd.read_csv('../organized notebooks/dashboard_final_merged.csv')
    # dataset containing school districts with over $20,000 revenue per student - during our research
    # we found information that there are no schools in California with revenue higher than 20 K and we chose to separate
    #those schools.

    # update the main dataset to not include schools with over 20k revenue per student nor zero revenue per student
    df_new = df[(df['Revenue per student'] < 20_000)]
    df_new = df_new[(df_new['Revenue per student'] != 0)]
    return df_new

def data_prep_by_school():
    return pd.read_csv('../organized notebooks/dashboard_school_df.csv', index_col=0)
