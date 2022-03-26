import time
import pandas as pd
import numpy as np
import termcolor
import pyfiglet

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
month_data = ['January','February','March','April','May','June']
day_data = ['Sunday','Monday','Tuesday','Wendesday','Thursday','Friday','Saturday']

def get_time(func):
    """decorator to calculate time taken to display results."""
    def new_func(*args, **kwargs):
            start_time = time.time()
            func(*args, *kwargs)
            print("\nThis took %s seconds." % (time.time() - start_time))
            print('-'*60)

    return new_func

def get_filters():
    """
     user input to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # get user input for city (chicago, new york city, washington). with a while loop to handle invalid inputs

    while True:
        city = input("Choose the city to analyze ?\n (chicago,new york city or washington)").strip().lower()
        if city not in CITY_DATA.keys():
            print("Country not included!please,choose anther one")
            continue
        else:
            break
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Choose the month to filter by, or all \n (all, january, february,march,april, may, june) ").strip().title()
        if month == "All":
            print("\n You choose to present all months")
            break
        elif month not in month_data:
            print("\n Month not included! ,enter correct choice")
            continue
        else:
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Choose the day to filter by, or all \n (all, sunday, monday, tuesday, wendesday, thursday, friday, saturday )" ).strip().title()
        if day == "All":
            print("\n You choose to present all days ")
            break
        elif day not in day_data:
            print("\n Wrong ,enter anther correct day pleace")
            continue
        else:
            break
    return city, month, day
    print('-'*60)

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['day'] = pd.DatetimeIndex(df['Start Time']).strftime("%A")
    df['month'] = pd.DatetimeIndex(df['Start Time']).strftime("%B")
    if month == "All" and day != "All":
        df = df[df['day'] == day]
    elif month != "All" and day =="All":
        df = df[df['month'] == month]
    elif month != "All" and day != "All":
        df = df[np.logical_and(df['month'] == month , df['day'] == day)]
    return df
    print('-'*60)

@get_time
def raw_data(df):
    """display raw data after asking user ."""
    row_index = 0
    answer = input("\nDo you want to see 5 lines of raw data ? yes / no\n").lower()
    while answer == "yes":
        print(df[row_index : row_index + 5])
        answer = input("\nDo you want to see anther 5 lines of raw data ? yes / no\n").lower()
        row_index += 5
        if answer == "no" or row_index == 29999:
            break

@get_time
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    # display the most common month
    print('\nThe most common month is: {}.'.format(df["month"].mode()[0]))

    # display the most common day of week
    print('\nThe most common day of week is: {}.'.format(df["day"].mode()[0]))

    # display the most common start hour
    df['start hour'] = pd.DatetimeIndex((df['Start Time'])).strftime("%I %p")
    print('\nThe most common start hour is: {}.'.format(df["start hour"].mode()[0]))

@get_time
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')

    # display most commonly used start station
    print('\nThe most common used start station is: {}.'.format(df["Start Station"].mode()[0]))
    # display most commonly used end station
    print('\nThe most common used end station is: {}.'.format(df["End Station"].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + '=>' + df['End Station']
    print('\nThe most frequent trip is: {}.'.format(df["Trip"].mode()[0]))

@get_time
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')

    # display total travel time
    print('\nThe total travel time is: {:.2f} Days .'.format(df["Trip Duration"].sum()/(24*60*60)))

    # display mean travel time
    print('\nThe mean travel time is: {:.2f} Minutes.'.format(df["Trip Duration"].mean()/60))


@get_time
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')

    # Display counts of user types
    print('\nThe counts of user types are:\n {}.'.format(df.groupby('User Type')["User Type"].count()))

    # Display counts of gender
    if 'Gender' in df:
        print('\nThe counts of gender are:\n {}.'.format(df.groupby('Gender')["Gender"].count()))

    print('-' * 50)
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('\nThe earliest year of birth is : {}.'.format(df["Birth Year"].min()))
        print('\nThe most recent year of birth is : {}.'.format(df["Birth Year"].max()))
        print('\nThe most common year of birth is : {}.'.format(df["Birth Year"].mode()[0]))

@get_time
def main():
    print(termcolor.colored(pyfiglet.figlet_format('Hello! Let\'s explore some US bikeshare data!'),color="blue"))
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print('-' * 50)
        raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()


