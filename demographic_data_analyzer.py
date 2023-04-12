import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df.groupby(df['race']).size()

    # What is the average age of men?
    average_age_men = round(df.groupby('sex').agg(avg_age = ('age', 'mean')).loc['Male'][0], 1)

    # What is the percentage of people who have a Bachelor's degree?
    total_bachelors = df.groupby(df['education']).size().loc['Bachelors']
    percentage_bachelors = round((total_bachelors*100)/df.shape[0], 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    lst = ['Bachelors', 'Masters', 'Doctorate']
    higher_education = df.groupby(['education', 'salary']).size().loc[lst]
    lower_education = df.groupby(['education', 'salary']).size().drop(lst)
    
    # with salary >50k
    higher_edu_rich = higher_education.loc[['Bachelors', 'Masters', 'Doctorate'], '>50K']
    total_higher_edu_rich = higher_edu_rich.sum()
    lower_edu_rich = lower_education.xs('>50K', level = 1, drop_level = False)
    total_lower_edu_rich = lower_edu_rich.sum()
    
    # percentage with salary >50K
    higher_education_rich = round((total_higher_edu_rich*100)/higher_education.sum(), 1)
    lower_education_rich = round((total_lower_edu_rich*100)/lower_education.sum(), 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df.groupby(['hours-per-week', 'salary']).size()[1].sum()
    min_hour_rich = df.groupby(['hours-per-week', 'salary']).size().xs('>50K', level = 1, drop_level = False).iloc[0]

    rich_percentage = (min_hour_rich*100)/num_min_workers

    # What country has the highest percentage of people that earn >50K?
    people_per_country = df.groupby('native-country').size()
    rich_per_country = df.groupby(['native-country', 'salary']).size().xs('>50K', level = 1, drop_level = False)

    highest_earning_country = (rich_per_country/people_per_country).idxmax()[0]
    highest_earning_country_percentage = round((rich_per_country/people_per_country).max()*100, 1)

    # Identify the most popular occupation for those who earn >50K in India.
    india = df[df['native-country'] == 'India']
    india_rich = india[india['salary'] == '>50K']
    
    top_IN_occupation = india_rich.groupby(['occupation', 'salary']).size().idxmax()[0]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
