#https://colab.research.google.com/notebooks
'''
good!
'''
# data=pd.read_clipboard()      # use data frome buffer (ctrl+c)

import pandas as pd
import numpy as np

students_performance = pd.read_csv("/Users/nikitasulimenko/Desktop/Prog/Python/Sample/StudentsPerformance.csv")
# simple print coloms and cortege
students_performance.iloc[0:5, [0,1,2]]

students_performance_with_indexes = students_performance.iloc[[0,3,5,6]]        # 0, 3, 5, 6 corteges
students_performance_with_indexes.index = ["first", "second", "third", "fourth"]

#students_performance_with_indexes
students_performance_with_indexes.loc[["first"]]        # print by index

# series and dataframe
series = students_performance_with_indexes.iloc[:,0]         # series
dataframe = students_performance_with_indexes[["gender"]]

#series
#dataframe

my_series_1 = pd.Series([1, 2, 3], index = ["A", "B", "C"])
my_series_2 = pd.Series([1, 2, 3], index = ["A", "B", "D"])
my_dataframe = pd.DataFrame({"col_name_1":my_series_1, "col_name_2":my_series_2})

#my_dataframe                                                # dataframe

#Filtration

#  students_performance.gender == "female"     # series with true and false

print(students_performance.loc[students_performance.gender == 'female', []])

mean_writing_score = students_performance["writing score"].mean()
print(students_performance.loc[students_performance["writing score"] > mean_writing_score])

query = ((students_performance['writing score'] > mean_writing_score) & (students_performance.gender == 'female'))
print(students_performance.loc[query])

#Rename
students_performance = students_performance\
    .rename(columns = 
        {'parental level of education': 'parental_level_of_education',
        'test preparation course': 'test_preparation_course',
        'math score': 'math_score',
        'reading score': 'reading_score',
        'writing score': 'writing_score'})

#students_performance.math_score                    # == students_performance['math_score']
writing_score_query = 80

students_performance.query("gender == 'female' & writing_score > @writing_score_query")
#Hard way

title_list = list(students_performance)              # list of title of dataframe
spec_title_list = [head for head in title_list if 'score' in head]
print(students_performance[spec_title_list])

# Easy way

students_performance.filter(like = 'score', axis = 1)       # axis = 0 for indexes(strings)

#Grouping and agregate
students_performance.groupby('gender', as_index=False) \
    .aggregate({'math_score': 'mean', 'reading_score': 'mean'})\
        .rename(columns = {'math_score':'mean_math_score', 'reading_score':'mean_reading_score'})

students_performance.sort_values(['gender', 'math_score'], ascending=False)\
    .groupby("gender").head(5)

students_performance['total_score'] = students_performance.math_score\
     + students_performance.reading_score\
        + students_performance.writing_score      # = series # it create new column

students_performance = students_performance.assign(total_score_log = np.log(students_performance.total_score))
#students_performance.head(2)

print(students_performance.drop(['total_score', 'lunch'], axis=1).head())

# ------------------------DOTA-----------------------

dota_dataset = pd.read_csv("/Users/nikitasulimenko/Desktop/Prog/Python/dota_hero_stats.csv")
legs_dota_hero = dota_dataset.groupby(['attack_type', 'primary_attr'])

#legs_dota_hero.loc(['attack_type', 'primary_attr'])
print(legs_dota_hero.count())