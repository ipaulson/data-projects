import csv
import itertools
import pandas as pd

## Filenames
chicago = './data/chicago.csv'
new_york_city = './data/new_york_city.csv'
washington = './data/washington.csv'

'''
Function: get_city()
    Asks the user for a city and returns the filename for that city's bike share data.
Args:
    none.
Returns:
    (str) filename for a city's bikeshare data.
'''
def get_city():
    city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                 'Would you like to see data for Chicago, New York, or Washington?\n')
    city = city.strip().lower()

    valid_cities = ['chicago','new york', 'washington']

    while city not in valid_cities:
        city = input('\nSorry, I don\'t know that city. Try again.\n'
            'Would you like to see data for Chicago, New York, or Washington?\n')

    if city == 'chicago':
        return chicago
    elif city == 'new york':
        return new_york_city
    elif city == 'washington':
        return washington

'''
Function: get_time_period()
    Asks the user for a time period and returns the specified filter.
Args:
    none.
Returns:
    (str) month, day, or none for time_period filter.
'''
def get_time_period():
    time_period = input('\nWould you like to filter the data by month, day, or not at'
                        ' all? Type "none" for no time filter.\n')
    time_period = time_period.strip().lower()
    
    valid_time_periods = ['month','day','none']

    while time_period not in  valid_time_periods:
        time_period = input('\nI don\'t understand that.'
                            '\nWould you like to filter the data by month, day, or not at'
                            ' all? Type "none" for no time filter.\n')

    return time_period

'''
Function: get_month()
    Asks the user for a month and returns the specified month.
Args:
    none.
Returns:
    (str) month
'''
def get_month():
    month = input('\nWhich month? January, February, March, April, May, or June?\n')
    month = month.strip().lower()

    valid_months = ['january','february','march','april','may','june']

    while month not in valid_months:
        month = input('\nI don\'t have data for that month\n'
                      'Which month? January, February, March, April, May, or June?\n')

    return month

'''
Function: get_day()
    Asks the user for a day and returns the specified day.
Args:
    (str) month.
Returns:
    (int) day of the month
'''
def get_day(month):
    while True:
        try:
            day = int(input('\nWhich day? Please type your response as an integer.\n'))
        except ValueError:
            print('\nI don\'t know what that is. Try an int.')
            continue 
        if day < 1:
            print("That date is too low.")
            continue
        elif month == 'february' and day > 28:
            print("That date is too high.")
            continue
        elif (month == 'april' or month == 'june') and day > 30:
            print("That date is too high.")
            continue
        elif day > 31:
            print("That date is too high.")
            continue
        else: 
            break

    return day

def load_data(city, month, day):
    # load data file into pandas dataframe
    df = pd.read_csv(city)

    # convert the Start Time to a dataframe
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    df['date'] = df['Start Time'].dt.day

    # filter by month
    if month != 'all':
        months = ['january','february','march','april','may','june']
        month = months.index(month) + 1

        df = df = df[df['month'] == month]

    if day != 'all':
        df = df[df['date'] == day]

    return df

'''
Question:
    What is the most popular month for start time?
Function    
    Takes a dataframe for the city and returns the most popular month
Args:
    city_file
Returns:
    (str) most popular_month
'''
def popular_month(df):

    popular_month = df['month'].mode()[0]

    if popular_month == 1:
        return 'January'
    if popular_month == 2:
        return 'February'
    if popular_month == 3:
        return 'March'
    if popular_month == 4:
        return 'April'
    if popular_month == 5:
        return 'May'
    if popular_month == 6:
        return 'June'

def popular_day(df):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What is the most popular day of week (Monday, Tuesday, etc.) for start time?
    '''
    # TODO: complete function

    popular_day = df['day_of_week'].mode()[0]

    return popular_day

def popular_hour(df):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What is the most popular hour of day for start time?
    '''
    # TODO: complete function

    popular_hour = df['hour'].mode()[0]

    if popular_hour == 0:
        return '12 a.m.'
    elif popular_hour == 12:
        return '12 p.m.'
    elif popular_hour <= 11:
        return '{} a.m.'.format(popular_hour)
    elif popular_hour > 12:
        popular_hour -= 12
        return '{} p.m.'.format(popular_hour)

def trip_duration(df):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What is the total trip duration and average trip duration?
    '''
    # TODO: complete function

    total_duration = df['Trip Duration'].sum()
    avg_duration = df['Trip Duration'].mean()

    total_hours = total_duration / 3600.00
    avg_hours = avg_duration / 60.00

    return (total_hours, avg_hours)

def popular_stations(df):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What is the most popular start station and most popular end station?
    '''
    # TODO: complete function
    popular_start = df['Start Station'].mode()[0]
    popular_end = df['End Station'].mode()[0]

    return(popular_start, popular_end)

def popular_trip(df):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What is the most popular trip?
    '''
    # TODO: complete function
    popular_trip = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().idxmax()
    
    return popular_trip

def users(df):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What are the counts of each user type?
    '''
    # TODO: complete function

    user_types_count = pd.value_counts(df['User Type']).values

    return user_types_count

def gender(df):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What are the counts of gender?
    '''
    # TODO: complete function
    genders = pd.value_counts(df['Gender']).values

    return genders

def birth_years(df):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What are the earliest (i.e. oldest user), most recent (i.e. youngest user),
    and most popular birth years?
    '''
    # TODO: complete function
    most_common_year = str(int(df['Birth Year'].mode()[0]))
    youngest = str(int(df['Birth Year'].max()))
    oldest = str(int(df['Birth Year'].min()))

    return (most_common_year, oldest, youngest)


def display_data(city):
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.

    Args:
        none.
    Returns:
        TODO: fill out return type and description (see get_city for an example)
    '''
    display = input('\nWould you like to view individual trip data?'
                    'Type \'yes\' or \'no\'.\n')

    valid_input = ['yes','no']

    while display not in valid_input:
        print("I don't understand that.")
        display = input('\nWould you like to view individual trip data?'
                    'Type \'yes\' or \'no\'.\n')

    start = 1
    end = 6    
    while display == 'yes':
        with open(city, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in itertools.islice(reader, start, end):
                print(row)
                start +=5
                end +=5
        display = input('\nWould you like to continue to view individual trip data?'
                    'Type \'yes\' or \'no\'.\n')
        while display not in valid_input:
            print("I don't understand that.")
            display = input('\nWould you like to continue to view individual trip data?'
                    'Type \'yes\' or \'no\'.\n')

'''
Function: statistics()
    Calculates and prints out the descriptive statistics about a city and time period
    specified by the user via raw input.
Args:
    none.
Returns:
    none.
'''
def statistics():
    # Filter by city (Chicago, New York, Washington)
    city = get_city()

    # Filter by time period (month, day, none)
    time_period = get_time_period()

    if time_period == 'month':
        month = get_month()
    else:
        month = 'all'

    if time_period == 'day':
        month = get_month()
        day = get_day(month)
    else:
        day = 'all'

    print("Loading city data...\n")

    df = load_data(city, month, day)

    print('Here are your stats:\n')

    # What is the most popular month for start time?
    if time_period == 'none':
        
        #TODO: call popular_month function and print the results
        print(popular_month(df) + " is the most popular month.\n")

    # What is the most popular day of week (Monday, Tuesday, etc.) for start time?
    if time_period == 'none' or time_period == 'month':
        
        # TODO: call popular_day function and print the results
        print(popular_day(df) + " is the most popular day.\n")        

    # What is the most popular hour of day for start time?
    # TODO: call popular_hour function and print the results
    print(popular_hour(df) + " is the most popular hour of the day.\n")
    
    # What is the total trip duration and average trip duration?
    # TODO: call trip_duration function and print the results
    durations = trip_duration(df)
    print("The total duration is {} hours.\nThe average duration is {} minutes.\n".format(durations[0],durations[1]))

    # What is the most popular start station and most popular end station?
    # TODO: call popular_stations function and print the results
    stations = popular_stations(df)
    print("The most popular start station is {}.\nThe most popular end station is {}.\n".format(stations[0],stations[1]))

    # What is the most popular trip?
    # TODO: call popular_trip function and print the results
    trip = popular_trip(df)
    #print(trip)
    print("The most popular trip is {} to {}.\n".format(trip[0],trip[1]))

    # What are the counts of each user type?
    # TODO: call users function and print the results
    types = users(df)
    print("There are {} subscirbers and {} customers.\n".format(types[0],types[1]))

    # What are the counts of gender?
    # TODO: call gender function and print the results
    if city != washington:
        genders = gender(df)
        print("There are {} males and {} females.\n".format(genders[0],genders[1]))

    # What are the earliest (i.e. oldest user), most recent (i.e. youngest user), and
    # most popular birth years?
    # TODO: call birth_years function and print the results
    if city != washington:
        years = birth_years(df)
        print("The most common birth year is {}.\nThe oldest rider was born in the year {}.\nThe youngest rider was born in the year {}.".format(years[0],years[1],years[2]))

    # Display five lines of data at a time if user specifies that they would like to
    display_data(city)

    # Restart?
    restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n')
    if restart.lower() == 'yes':
        statistics()

if __name__ == "__main__":
  statistics()