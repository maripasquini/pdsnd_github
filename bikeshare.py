import time
import pandas as pd
import numpy as np
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = ['chicago', 'new york', 'washington']

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

FILTER_OPTIONS = ['month', 'day', 'both', 'none']

def get_user_answer(question, filter_options):
    """ Validates user input considering filter options """
    while True:
        answer = input(question).lower()
        if (answer not in (filter_options)):
            print('Not an appropriate choice.')
        else:
            break
    return answer

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_user_answer('\nWould you like to see data for Chicago, New York or Washington?\n', CITIES)

    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    option = get_user_answer('\nWould you like to filter the data by month, day, both or not at all? Type "none" for no time filter.\n', FILTER_OPTIONS)
    month = 'all'
    day = 'all'
    if (option == 'month'):
        month = get_user_answer('\nWich month? January, February, March, April, May, or June?.\n', MONTHS)
    elif (option == 'day'):
        day = get_user_answer('\nWich day? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday.\n', DAYS)
    elif (option == 'both'):
        month = get_user_answer('\nWich month? January, February, March, April, May, or June?.\n', MONTHS)
        day = get_user_answer('\nWich day? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday.\n', DAYS)

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time 2'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time 2'].dt.month
    df['day_of_week'] = df['Start Time 2'].dt.weekday_name
    df['hour'] = df['Start Time 2'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def count_popular(column):
    """ Gets popular value and counts it """
    column_count = column.value_counts()
    popular = column_count.idxmax()
    popular_count = column_count.max()

    return popular, popular_count

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month, popular_month_count = count_popular(df['month'])
    print('\nMost common month: {}, count: {}'.format(popular_month, popular_month_count))

    # TO DO: display the most common day of week
    popular_day_of_week, popular_day_of_week_count = count_popular(df['day_of_week'])
    print('Most common day of week: {}, count: {}'.format(popular_day_of_week, popular_day_of_week_count))

    # TO DO: display the most common start hour
    popular_hour, popular_hour_count = count_popular(df['hour'])
    print('Most common start hour: {}, count: {}'.format(popular_hour, popular_hour_count))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station, popular_start_station_count = count_popular(df['Start Station'])
    print('Most commonly used start station: {}, count: {}'.format(popular_start_station, popular_start_station_count))

    # TO DO: display most commonly used end station
    popular_end_station, popular_end_station_count = count_popular(df['End Station'])
    print('Most commonly used end station: {}, count: {}'.format(popular_end_station, popular_end_station_count))

    # TO DO: display most frequent combination of start station and end station trip
    popular_start_end_stations = df[['Start Station', 'End Station']].mode().loc[0]
    print('Most frequent combination of start station and end station trip: {}, {}'.format(popular_start_end_stations[0], popular_start_end_stations[1]))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time: ', total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time: ', mean_travel_time)

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of user types:')
    print_format(user_types)

    # TO DO: Display counts of gender
    if ('Gender' in df.columns):
        gender = df['Gender'].value_counts()
        print('\nCounts of gender:')
        print_format(gender)

    # TO DO: Display earliest, most recent, and most common year of birth
    if ('Birth Year' in df.columns):
        birth_year = df['Birth Year']
        # Earliest of birth_year
        print('\nEarliest year of birth: ', int(birth_year.min()))
        # Most recent of birth_year
        print('Most recent year of birth: ', int(birth_year.max()))
        # Most common of birth_year
        popular_birth_year, popular_birth_year_count = count_popular(birth_year)
        print('Most common year of birth: {}, count: {}'.format(int(popular_birth_year), popular_birth_year_count))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)

def print_format(counts):
    """ Formats the printing """
    for index, count in enumerate(counts):
        print("{}: {}".format(counts.index[index], count))

def display_raw_data(df):
    """Displays raw bikeshare data."""
    df = df.fillna('').drop(['Unnamed: 0', 'Start Time 2', 'month', 'day_of_week', 'hour'], axis=1)
    length = df.shape[0]
    answer = 'yes'

    for i in range(0, length, 5):
        if (answer == 'yes'):
            json_records = df.iloc[i:i+5].to_json(orient='records', lines=True).split('\n')
            for record in json_records:
                parsed = json.loads(record)
                print(json.dumps(parsed, indent=4))
            answer = get_user_answer('\nWould you like to continue? Type yes or no.\n', ['yes', 'no'])
        else:
            break

def main():
    while True:
        city, month, day = get_filters()

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        answer = get_user_answer('Would you like to see the raw data? Type yes or no.\n', ['yes', 'no'])
        if (answer == 'yes'):
            display_raw_data(df)
            print('-'*40)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart != 'yes':
            break


if __name__ == "__main__":
	main()
