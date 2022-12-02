import json
import unittest
import os
import requests
import sqlite3
import matplotlib
import matplotlib.pyplot as plt

#state code should be two letter, lowercase
#date_iso should be year, month, day 

our_dates = ['2020-03-15', '2020-04-15','2020-05-15','2020-06-15','2020-07-15','2020-08-15','2020-09-15','2020-10-15', '2020-11-15','2020-12-15','2021-01-15','2021-02-15']

our_states = ['mi', 'ca', 'co', 'fl', 'il', 'oh', 'tx', 'ma', 'ga', 'hi', 'ak', 'ct', 'id', 'ks', 'or' ]

spring = ['03', '04', '05']
summer = ['06', '07', '08']
fall = ['09', '10', '11']
winter = ['12', '01', '02']

def get_data (state_code, date_iso):
    url = f' https://api.covidtracking.com/v2/states/{state_code}/{date_iso}/simple.json'
    r = requests.get(url)
    r_text = r.text
    data = json.loads(r_text)
    return data

test = get_data('td', '2020-04-14')
print(test)
def get_important_data(big_data):
    state_date_cases_list = []
    if 'error' in big_data:
        return []
    else:
        date = big_data["data"]['date']
        state = big_data["data"]['state']
        cases = big_data["data"]['cases']['total']
        state_date_cases_list.append(state)
        state_date_cases_list.append(date)
        state_date_cases_list.append(cases)
        return state_date_cases_list

# may_not_exist = get_data('mi', '2021-03-15')
# print("ERRO ?????")
# print(may_not_exist)
# important_error = get_important_data(may_not_exist)
# print("error important")
# print(important_error)

def state_data(state, date_list):
    single_state_data_dict = {}
    for date in date_list:
        small_dict = {}
        data = get_data(state, date)
        important_data = get_important_data(data)
        if len(important_data) != 3:
            small_dict[date] = "no data available for this date"
        else:
            cases = important_data[2]
            small_dict[date] = cases
        if state not in single_state_data_dict:
            single_state_data_dict[state] = small_dict
        else:
            if date not in single_state_data_dict.values():
                single_state_data_dict[state].update(small_dict)
    return single_state_data_dict


def full_data(state_list, date_list):
    list_of_state_dicts = []
    for state in state_list:
        single_dict = state_data(state, date_list)
        list_of_state_dicts.append(single_dict)
    return list_of_state_dicts

# full_list_of_dicts= full_data(our_states, our_dates)
# print('full')
# print(full_list_of_dicts)

# # def get_totals():

# def cases_by_season_per_state(full_list_of_dicts):
#     state_cases_season_dict = {}
#     for dict in full_list_of_dicts:
#         for state, small_dict in dict.items():
#             fall_case_total = 0
#             winter_case_total = 0
#             spring_case_total = 0
#             summer_case_total = 0
#             for date, cases in small_dict.items():
#                 month = date.split('-')[1]
#                 small_dict = {}
#                 if month in spring:
#                     spring_case_total += cases
#                     season = 'spring'
#                     small_dict[season] = spring_case_total
#                 elif month in summer:
#                     summer_case_total += cases
#                     season = 'summer'
#                     small_dict[season] = summer_case_total
#                 elif month in winter:
#                     winter_case_total += cases
#                     season = 'winter'
#                     small_dict[season] = winter_case_total
#                 else:
#                     fall_case_total += cases
#                     season = 'fall'
#                     small_dict[season] = fall_case_total
#                 if state not in state_cases_season_dict:
#                     state_cases_season_dict[state] = small_dict
#                 else:
#                     if season not in state_cases_season_dict.values():
#                         state_cases_season_dict[state].update(small_dict)
#     return state_cases_season_dict



# #{'mi': {'spring': 94408, 'summer': 246780, 'fall': 557674, 'winter': 1688153},
# # 'ca': {'spring': 99653, 'summer': 1112775, 'fall': 2637759, 'winter': 7883359}, 
# # 'co': {'spring': 29643, 'summer': 120292, 'fall': 307434, 'winter': 1079209}, 
# # 'fl': {'spring': 63363, 'summer': 935484, 'fall': 2269441, 'winter': 4442414}, 
# # 'il': {'spring': 115026, 'summer': 497553, 'fall': 1174579, 'winter': 3086375}, 
# # 'oh': {'spring': 34781, 'summer': 218561, 'fall': 613424, 'winter': 2335064}, 
# # 'tx': {'spring': 60746, 'summer': 900311, 'fall': 2586956, 'winter': 6137390}, 
# # 'ma': {'spring': 113477, 'summer': 340934, 'fall': 455247, 'winter': 1317437}, 
# # 'ga': {'spring': 51767, 'summer': 421416, 'fall': 1058063, 'winter': 2321932}, 
# # 'hi': {'spring': 1156, 'summer': 6535, 'fall': 41544, 'winter': 72034}}



def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


# # TASK 1
# # CREATE TABLE FOR EMPLOYEE INFORMATION IN DATABASE AND ADD INFORMATION
def create_table(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS Covid (state_key TEXT PRIMARY KEY, spring INTEGER, summer INTEGER, winter INTEGER, fall INTEGER)')
    conn.commit()


# # ADD EMPLOYEE'S INFORMTION TO THE TABLE

# def add_state(dictionary, cur, conn):
#     for state, small_dictionary in dictionary.items():
#         spring_cases = small_dictionary['spring']
#         summer_cases = small_dictionary['summer']
#         winter_cases = small_dictionary['winter']
#         fall_cases = small_dictionary['fall']
#         cur.execute('INSERT OR IGNORE INTO Covid (state_key, spring, summer, winter, fall) values (?,?,?,?,?)', (state, spring_cases, summer_cases, winter_cases, fall_cases))
#     conn.commit()

# # TASK 2: GET TEMP AND CASES INFO JOINED
# def connect_temp_and_covid_by_season(cur, conn):
#     cur.execute('SELECT Temperature.state_key, Temperature.spring, Temperature.summer, Temperature.winter, Temperature.fall, Covid.spring, Covid.summer, Covid.winter, Covid.fall FROM Covid JOIN Temperature ON Temp.state_key = Covid.state_key order by employees.hire_date limit 1')
#     list_of_matches= cur.fetchall()
#     return list_of_matches

# def find_something(list_of_matches):
#     for tup in list_of_matches:
#         state_key = tup[0]
#         temp_sprint = tup[1]
#         cases_spring = tup[4]
#         return something_for_visualization

# #  START VISUALIZATION

# def visualization_salary_data(cur, conn):
#     plt.xlabel("Temperature")
#     plt.ylabel("Covid Cases")
#     cur.execute('SELECT Covid.season, FROM Covid JOIN Temperature ON Jobs.state = Employees.state') 
#     result = cur.fetchall 
#     x,y = zip(*result)
#     plt.scatter(x, y)
#     cur.execute('SELECT min max FROM Jobs JOIN Employees ON Jobs.job_id = Employees.job_id') 
#     result = cur.fetchall 
#     x,y = zip(*result)
#     plt.scatter(x, y)


# def main(state_list, date_list):
#     full_data_in_list = full_data(state_list, date_list)
#     final_dictionary = cases_by_season_per_state(full_data_in_list)
#     cur, conn = setUpDatabase('Covid_Temp_Flu.db')
#     create_table(cur, conn)
#     add_state(final_dictionary, cur, conn)
    

# main(our_states, our_dates)