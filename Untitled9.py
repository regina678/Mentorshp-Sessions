#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pandas as pd
df = pd.read_excel(r'C:\Users\USER\Downloads\_Data Sets Reward_Program_Assignment_Input_v6 - TA.xlsx',sheet_name = 'Mentorship_Sessions')
print("Column names:", df.columns)


# In[17]:


print(df.columns)


# In[18]:


# Now we can use sessions_df
sessions_df = df

# Ensure the column names match the updated list
corrected_columns = ['mentee_id', 'mentor_id', 'Mentor_Name', 'mentee_name', 'session_number', 'Session_Duration_Min', 'job_info_completed', 'Session_Date']
if not set(corrected_columns).issubset(set(sessions_df.columns)):
    print("Warning: Some columns may not match the expected names. Please review and adjust accordingly.")
else:
    print("Column names match the expected list.")

def get_unique_mentees(mentor_id, sessions):
    return set(sessions.loc[sessions['mentor_id'] == mentor_id, 'mentee_id'])

def check_session_duration(duration):
    return duration >= 30

def check_job_info_completion(job_info):
    return job_info == 'COMPLETE'

def allocate_points(sessions_df):
    mentor_points = defaultdict(int)
    session_data = defaultdict(lambda: defaultdict(list))

    # Initialize base points
    mentor_points.update({m: 250 for m in sessions_df['mentor_id'].unique()})

    # Count unique mentor-mentee pairs
    unique_pairs = set(zip(sessions_df['mentor_id'], sessions_df['mentee_id']))

    # Iterate through sessions
    for _, row in sessions_df.iterrows():
        mentor_id, mentee_id, duration, job_info = row['mentor_id'], row['mentee_id'], row['Session_Duration_Min'], row['job_info_completed']

        # Update session data
        session_data[mentor_id][mentee_id].append(duration)
        session_data[mentor_id][mentee_id].append(job_info)

        # Check for mentorship relationships
        if len(session_data[mentor_id]) >= 2:
            mentees = get_unique_mentees(mentor_id, sessions_df)
            if len(mentees) == 2:
                mentor_points[mentor_id] += 1000

        # Calculate points for current session
        if check_session_duration(duration) and check_job_info_completion(job_info):
            max_points = min(len(session_data[mentor_id][mentee_id]), 2) * 500
            mentor_points[mentor_id] += min(max_points, 250)

    return mentor_points

# Allocate points
allocated_points = allocate_points(sessions_df)

# Create a report
print("Point Allocation Report:")
print("------------------------")
print(f"Total Mentors Signed Up: {len(set(sessions_df['mentor_id']))}")
print(f"Total Mentor-Mentee Relationships: {len(set(zip(sessions_df['mentor_id'], sessions_df['mentee_id'])))}")

print("\nTop Earning Mentors:")
for mentor_id, points in sorted(allocated_points.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"Mentor {mentor_id}: {points} points")

print("\nMentors who earned maximum points:")
max_points_earned = False
for mentor_id, points in allocated_points.items():
    if points == 1000:
        print(f"Mentor {mentor_id}: {points} points")
        max_points_earned = True

if not max_points_earned:
    print("\nNote: No mentors earned the maximum of 1000 points.")

# Save results to a new CSV file
results_df = pd.DataFrame(list(allocated_points.items()), columns=['Mentor_ID', 'Allocated_Points'])
results_df.to_csv('allocated_points_results.csv', index=False)

print("\nResults saved to 'allocated_points_results.csv'")


# In[ ]:





# In[ ]:




