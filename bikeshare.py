# Current Version: 1.0
# The followings can be considered to integrate for the next versions:
# 1) Optional monthly and weekly filters on the applicable stats
# 2) Optinoal expanding the results to top # (# would be the users desire)

import numpy as np
import pandas as pd
from os import system, name
import time
import datetime
import re
import calendar


# make a dictionary of filenames:
cityData = {'chicago': 'chicago.csv',
            'new york city': 'new_york_city.csv',
            'washington': 'washington.csv'}


def main():

    # Welcoming meassge
    print("*" * 153)
    print("* Welcome to the bikeshare data query maker. Here we would like you to answer some questions first, then we will provide you with some interesting data *")
    print("*" * 153)

    # Get the city
    city = get_city()
    clear()
    print(f"You have selecetd {city.capitalize()}", end="\n\n")

    # Load DataFrame
    startTime = time.time()
    df = load_data(city)
    timeLoadDB = time.time() - startTime
    # print(df.head())

    # Get information most popular times of travel
    startTime = time.time()
    get_popular_times_of_travel(df, city)
    timeMostPopularTimesOfTravel = time.time() - startTime

    # Get information about most popular station(s) and route(s)
    startTime = time.time()
    get_popular_stations_and_trip(df, city)
    timeMostPopularStationRoute = time.time() - startTime

    # Get information about trip durations
    startTime = time.time()
    get_trip_duration(df, city)
    timeTripDurations = time.time() - startTime

    # Get information about users
    startTime = time.time()
    get_user_info(df, city)
    timeUserInfo = time.time() - startTime

    # Print time stats
    print("-" * 60)
    print(
        f"Time took to load the database: {np.round(timeLoadDB, decimals=3)} s")
    print(
        f"Time took to evaluate information about most popular times of travel: {np.round(timeMostPopularTimesOfTravel, decimals=3)} s")
    print(
        f"Time took to evaluate information about most popular station(s) and route(s): {np.round(timeMostPopularStationRoute, decimals=3)} s")
    print(
        f"Time took to evaluate information about trip durations: {np.round(timeTripDurations, decimals=3)} s")
    print(
        f"Time took to evaluate information user informations: {np.round(timeUserInfo, decimals=3)} s")
    print(f"Total time: {np.round((timeLoadDB + timeMostPopularTimesOfTravel + timeMostPopularStationRoute + timeTripDurations + timeUserInfo), decimals=3)} s")
    print("-" * 60)


def get_city():
    '''
    prompts the user to input a valid name of the city for which they would like to know about


    returns:
        (str) city - chicago, new york city or washington
    '''
    while True:
        valueGiven = input(
            "Which one of the follwing cities you would like to know about: \n1.Chicago(c), 2.Washington(w) or 3.New York City[ny]\n")

        # Check for input Chicago
        if re.search("c(hicago)?|1", valueGiven, re.IGNORECASE):
            city = "chicago"
            return city
            break

        # Check for input Washington
        elif re.search("w(ashington)?|2", valueGiven, re.IGNORECASE):
            city = "washington"
            return city
            break

        # Check for input New York City
        elif re.search("n(ew york cit)?y|n|3", valueGiven, re.IGNORECASE):
            city = "new york city"
            return city
            break

        # Check for input > 24
        else:
            print("Invalid input\nValid example: Type c for Chicago, type w for Washington or type ny for New York city")


def load_data(city):
    '''
    loads the data from the chosen city into a pandas DataFrame and adds columns 'month', 'day of the week' and 'hour' to the dataFrame


    returns:
        (pandas DataFrame) df - with added columns
    '''

    # Load data
    df = pd.read_csv(cityData[city])

    # Convert the Start Time column to datetime
    if df['Start Time'].dtype == object:
        df['Start Time'] = pd.to_datetime(df["Start Time"])

    # Add month to the DataFrame
    df['month'] = df['Start Time'].dt.month

    # Add day of the week to the DataFrame
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Add the hour column to the Table
    df['hour'] = df['Start Time'].dt.hour

    # Add the routes column to the Table
    df['route'] = df['Start Station'] + " → " + df['End Station']

    return df


def get_popular_times_of_travel(df, city):
    ''' returns a statistical summary acquired from the given DataFrame '''

    try:
        # Get most populars times of travel
        mostPopularMonth = calendar.month_name[int(df['month'].mode()[0])]
        mostPopularDayOfWeek = df['day_of_week'].mode()[0]
        mostPopularHour = df.hour.mode()[0]

    except:
        print("Error Code 011: Check get_popular_times_of_travel")

    else:
        # Print the populars times of travel
        print(f"Popular times of travel in {city}")
        print(
            f"\t * {mostPopularMonth} is the most popular month for bikesharing")
        print(
            f"\t * {mostPopularDayOfWeek} is the most popular day of the week for bikesharing")
        print(
            f"\t * {mostPopularHour} is the most popular hour of the day (24-hour-format) for bikesharing")


def get_popular_stations_and_trip(df, city):
    ''' returns a statistical summary about the most popular stations and routes '''

    try:
        # month, day of the week, hour, Start Station, End Station, route for the given city [the number of instances a customer rented a bike]
        # Get most populars stations and route
        mostPopularStartStation = df['Start Station'].mode()[0]
        mostPopularEndStation = df['End Station'].mode()[0]
        mostPopularRoute = df['route'].mode()[0]

    except:
        print("Error Code 012: Check get_popular_stations_and_trip")

    else:
        print("Popular station(s) and route(s)")
        print(
            f"\t * {mostPopularStartStation} is the most popular starting station for bikesharing")
        print(
            f"\t * {mostPopularEndStation} is the most popular end station for bikesharing")
        print(
            f"\t * The route {mostPopularRoute} is the most popular route for bikesharing")


def get_trip_duration(df, city):
    ''' returns a statistical summary acquired from the given DataFrame '''
    # Improvement ideas:
    # Using most presantable time formats → check datetime

    try:
        # Get stats about trip durations
        totalTimeTravelInSeconds = df['Trip Duration'].sum()
        totalTimeTravelInDays = totalTimeTravelInSeconds / (60 * 60 * 24)
        averageTripTime = np.average(df['Trip Duration'])

    except:
        print("Error Code 013: get_trip_duration")

    else:
        # Print the most populars
        print("Trip durations")
        print(f"\t * {int(np.round((totalTimeTravelInSeconds/60/60)))} hours is the total amount of hours customers used bikesharing serives\n\t   that is roughly about {int(np.round(totalTimeTravelInDays))} days of total riding")
        print(f"\t * {int(np.round((averageTripTime / 60)))} minutes is the average amount of time for each trip made by customers")


def get_user_info(df, city):
    ''' returns a statistical summary about registered users'''

    # Initializing local variables
    genders = []
    earliestYearOfBirth = 0
    mostRecentYearOfBirth = 0
    mostCommonYearOfBirth = 0
    currentYear = 0

    try:
         # Get availabe user Information
        userTypeList = df['User Type'].dropna().unique().tolist()

        # Get stats about gender and the age of the users (only available in NYC and Chocago)
        if city != 'washington':

            # Create list of all the registered genders while removing NaN valuees
            genders = df['Gender'].dropna().unique().tolist()

           # Counting total number of users with valid registered gender
            totalUsers = df.groupby('Gender')['Gender'].count().sum()

            earliestYearOfBirth = int(df['Birth Year'].min())
            mostRecentYearOfBirth = int(df['Birth Year'].max())
            mostCommonYearOfBirth = int(df['Birth Year'].sort_values()[0])
            currentYear = datetime.datetime.now().year

    except:
        print("Error Code 014: Check get_user_info")

    else:
        # Print user Type data
        print("Popular station(s) and route(s)")

        for user in userTypeList:
            print(
                f"\t * There are {df.groupby('User Type')['User Type'].count().loc[user]} users using the bikeshare serivces as a {user}")

        if city != 'washington':

            # Print Informaion abot gender of the users
            for gender in genders:
                print(
                    f"\t * There are {df.groupby('Gender')['Gender'].count().loc[gender]} {gender} using using the bikeshare serivces, that makes up {np.round((df.groupby('Gender')['Gender'].count().loc[gender] / totalUsers) * 100)} % of the total customers")

            # Print age related (oldest user)
            print(
                f"\t * The earliest registered year of birth is {earliestYearOfBirth} That would mean the user was {currentYear - earliestYearOfBirth} years old by the time of usage")

            # Warn about potential faulty data
            if currentYear - earliestYearOfBirth > 100:
                print(f"\t   It makes sense that we re-evaluate the whole proccess of obtaining and recording the data regarding the user's date of birth to minimize the faulty registerations")

            # Print age related (youngest user)
            print(
                f"\t * The most recent registered year of birth is {mostRecentYearOfBirth} That would mean the user was {currentYear - mostRecentYearOfBirth} years old by the time of usage")

            # Print age related (most common year of birth)
            print(
                f"\t * The most common registered year of birth is {mostCommonYearOfBirth} That would mean the user was {currentYear - mostCommonYearOfBirth} years old by the time of usage")


def clear():
    ''' 
    function clears the screen

    Source: https://www.geeksforgeeks.org/clear-screen-python/
    '''

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


if __name__ == "__main__":
    main()
