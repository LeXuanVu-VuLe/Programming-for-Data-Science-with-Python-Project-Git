import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington).
    while True:
        city = input('Enter the name of the city (Chicago, New York City, Washington): ').lower()
        if city in CITY_DATA:
            break
        else:
            print('Invalid city name. Please select from the suggested list!')

    # Get user input for month (all, january, february, ... , june).
    while True:
        month = input('Enter the month to filter by (All, January, February, ... June): ').lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print('Invalid month. Please select from the suggested list!')

    # Get user input for day of week (all, monday, tuesday, ... sunday).
    while True:
        day = input('Enter the day of the week to filter by (All, Monday, Tuesday, ... Sunday): ').lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print('Invalid day. Please select from the suggested list!')

    print('-'*40)
    return city, month, day


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
    # Load data from the CSV file with city name.
    df = pd.read_csv(CITY_DATA[city.lower()])

    if 'Start Time' in df:
        # Filter with month.
        if month.lower() != 'all':
            df = df[pd.to_datetime(df['Start Time']).dt.month_name() == month.title()]

        # Filter with day.
        if day.lower() != 'all':
            df = df[pd.to_datetime(df['Start Time']).dt.day_name() == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if 'Start Time' in df:
        # Show the most common month.
        print('\nThe most common month: ' + pd.to_datetime(df['Start Time']).dt.month_name().mode()[0])

        # Show the most common day of week.
        print('\nThe most common day of week: ' + pd.to_datetime(df['Start Time']).dt.day_name().mode()[0])

        # Show the most common start hour.
        print('\nThe most common start hour: ' + str(pd.to_datetime(df['Start Time']).dt.hour.mode()[0]) + '\n')
    else:
        print('\nNot exist Start Time in file.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    if 'Start Station' in df:
        # Show the most commonly used start station.
        print('\nThe most commonly used start station: ' + df['Start Station'].mode()[0])
    else:
        print('\nNot exist Start Station in file.')

    if 'End Station' in df:
        # Show the most commonly used end station.
        print('\nThe most commonly used end station: ' + df['End Station'].mode()[0])
    else:
        print('\nNot exist End Station in file.')

    if ('Start Station' in df) and ('End Station' in df):
        # Show the most frequent combination of start station and end station trip.
        print('\nThe most frequent combination of start station and end station trip: ' + (df['Start Station'] + ' - ' + df['End Station']).mode()[0] + '\n')
    else:
        print('\nNot exist Start Station or Not exist End Station in file.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    if 'Trip Duration' in df:
        # Caculator total travel time.
        print('\nTotal travel time: ' + str(df['Trip Duration'].sum()) + 's')

        # Caculator mean travel time.
        print('\nMean travel time: ' + str(df['Trip Duration'].mean()) + 's')
    else:
        print('\nNot exist Trip Duration in file.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if 'User Type' in df:
        # Counts of user types.
        print('\nCounts of user types: \n')
        for user_type, countUT in df['User Type'].value_counts().items():
            print(user_type + ': ' + str(countUT))
    else:
        print('\nNot exist User Type in file.')

    if 'Gender' in df:
        # Counts of gender.
        print('\n\nCounts of gender: \n')
        for gender, countG in df['Gender'].value_counts().items():
            print(gender + ': ' + str(countG))
    else:
        print('\nNot exist Gender in file.')

    if 'Birth Year' in df:
        # Get earliest, most recent, and most common year of birth.
        print('\n\nEarliest year of birth: ' + str(int(df['Birth Year'].min())))

        print('\nMost recent year of birth: ' + str(int(df['Birth Year'].max())))

        print('\nMost common year of birth: ' + str(int(df['Birth Year'].mode()[0])))
    else:
        print('\nNot exist Birth Year in file.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Prompt the user if they want to see 5 lines of raw data.
        start_loc  = 0
        while True:
            view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?\n")
            if view_data.lower() != 'yes':
                break
            print(df.iloc[start_loc : start_loc  + 5])
            start_loc  += 5

            # Check if there is more raw data to display.
            if start_loc  >= len(df):
                print("No more raw data to display.")
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
