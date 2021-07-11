import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = {'january': 0,
          'february':1,
          'march':2,
          'april':3,
          'may':4,
          'june':5,
          'all':6}
months = ['january', 'february', 'march', 'april', 'may', 'june']


DAYS = {'monday':0,
        'tuesday':1,
        'wednesday':2,
        'thursday':3,
        'friday':4,
        'saturday':5,
        'sunday':6
       }
days = ['monday','tuesday','wedensday','thursday','friday','saturday','sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Select a city to explore. You can choose either chicago, new york city or washington. \n').lower()
    while city not in CITY_DATA:
        city = input('city not found in data. You can choose either chicago, new york city or washington. Make sure to avoid misspells. \n').lower()


    # get user input for month (all, january, february, ... , june)
    month = input('Select a month from january till june or type all to get all data regardless of month. \n').lower()
    while month != 'all' and month not in MONTHS :
        month = input('month not found in data. You can choose either january, february, march, april, may, june or all. Make sure to avoid misspells. \n').lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Select one day of the week or type all to get all data redardless of day. \n').lower()
    while day != 'all' and day not in DAYS:
        day = input('day not found in data. You can choose either sunday, monday, tuesday, wednesday, thursday, friday or all. Make sure to avoid misspells. \n').lower()


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
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day = days.index(day)
        
        df = df[df['day_of_week'] == day]
    
    #df = df.dropna(inplace = True)
           
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month is: '+ months[df['month'].mode()[0] - 1])

    # display the most common day of week
    print('The most common day is: ' + days[df['day_of_week'].mode()[0]])

    # display the most common start hour
    def hour_format(hour):
        if hour < 12:
            return str(hour) + ' a.m.'
        else:
            return str(hour-12) + ' p.m.'
    print('The most common hour is: ' + hour_format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print ('The most commonly used start station is: '+ df['Start Station'].mode()[0] )


    # display most commonly used end station
    print ('The most commonly used end station is: '+ df['End Station'].mode()[0] )


    # display most frequent combination of start station and end station trip
    print ('The most frequent combination of start station and end station trip is: '+ str(df.groupby(['Start Station','End Station']).size().idxmax()) )  #found this solution here: https://stackoverflow.com/questions/53037698/how-can-i-find-the-most-frequent-two-column-combination-in-a-dataframe-in-python


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def duration_format(duration):
    """Returns duration in the form of hours and minutes and seconds."""
    hours = int(duration/3600)
    duration %= 3600
    minutes = int(duration/60)
    duration %= 60
    seconds = int(duration)
    return ('{} hours and {} minutes and {} seconds.'.format(hours, minutes,seconds))
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time: ' + duration_format(df['Trip Duration'].sum()) )  

    # display mean travel time
    print('Mean travel time: ' + duration_format(df['Trip Duration'].mean()) )


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print ('Number of subscribers: ' + str(df[df['User Type'] == 'Subscriber'].shape[0]))
    print ('Number of customers: ' + str(df[df['User Type'] == 'Customer'].shape[0]))
    print()

    # Display counts of gender
    print ('Number of male users: ' + str(df[df['Gender'] == 'Male'].shape[0]))
    print ('Number of female users: ' + str(df[df['Gender'] == 'Female'].shape[0]))
    print()


    # Display earliest, most recent, and most common year of birth
    print('Earliest year of birth :' + str(int(df['Birth Year'].min())))
    print('Most recent year of birth :' + str(int(df['Birth Year'].max())))
    print('Most common year of birth :' + str(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_raw_data(df):
    answer = input('\nWould you like to view raw data? Enter yes or no.\n')
    rows = np.array([0,5])
    while answer.lower() == 'yes':
        if rows[1] <= df.shape[0]:
            print(df.iloc[rows[0]:rows[1]])
            rows += 5
        else:
            print(df.iloc[rows[0]:])
            print('No more data')
            break
        answer = input('\nWould you like to view raw data? Enter yes or no.\n')
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        if city != 'washington': # washington.csv has no gender or birth year column
            user_stats(df)
        
        
        display_raw_data(df) 
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
