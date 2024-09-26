#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
df = pd.read_excel(r'C:\Users\USER\Downloads\_Data Sets Reward_Program_Assignment_Input_v6 - TA.xlsx',sheet_name = 'Mentorship_Sessions')
print("Column names:", df.columns)


# In[11]:


# Initialize mentor points dictionary
mentor_points = {}

# Define the point allocation function
def allocate_points(group):
    print("Group:")
    print(group)
    points = 0
    session_number = len(group)
    job_info_completed = group['job_info_completed'].eq('Yes').any()
    print("Session Number:", session_number)
    print("Job Info Completed:", job_info_completed)
    if session_number >= 2 and job_info_completed:
        points += 500
    elif session_number >= 1 and job_info_completed:
        points += 250
    print("Points:", points)
    return points


grouped_df = df.groupby(['mentor_id', 'mentee_name'])
points_df = grouped_df.apply(allocate_points).reset_index()
points_df.columns = ['mentor_id', 'mentee_name', 'points']


mentor_points = {}

# Iterate through the points dataframe and allocate points to mentors
for index, row in points_df.iterrows():
    print("Row:")
    print(row)
    mentor_id = row['mentor_id']
    points = row['points']
    
    if mentor_id not in mentor_points:
        mentor_points[mentor_id] = 250 
    
    mentor_points[mentor_id] += points
    
    # Check if the mentor has conducted mentorship with 2 different mentees
    mentees = df[df['mentor_id'] == mentor_id]['mentee_name'].nunique()
    print("Mentees:", mentees)
    if mentees >= 2:
        mentor_points[mentor_id] += 1000  

# Export the mentor points dictionary to a CSV file
pd.DataFrame(list(mentor_points.items()), columns=['Mentor ID', 'Points Allocated']).to_csv('mentor_points.csv', index=False)

