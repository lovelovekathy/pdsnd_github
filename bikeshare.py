import time
import pandas as pd
import numpy as np

#Load in Data 
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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, New York, or Washington?\n").lower()
    valid1 = {'chicago','new york','washington'}    
    while city not in valid1: 
        print('Invalid input. Please type valid city names.')
        city = input("Would you like to see data for Chicago, New York, or Washington?").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    choose_filter = input('Would you like to filter the data by month, day, both, or not at all? \n Type "none"for no time filter.\n')
    valid2 = {'month','day','both','none'}
    while choose_filter not in valid2:
        print('Invalid input. Please choose a valid filter.')
        choose_filter = input('Would you like to filter the data by month, day, both, or not at all? \n Type "none"for no time filter.\n')

    if choose_filter in {'both'}:
        month = input("Which month do you want to look at? (Choose from january, february, march, april,may, and june.)\n")
        valid3 = {'january','february','march','april','may','june'}
        while month not in valid3: 
            print('Invalid input. Please enter lowercase letters for months.')
            month = input("Which month do you want to look at? (Choose from january, february, march, april,may, and june.)\n")
        day = input("Which day? Please type your response as an integer (e.g., 1 = Sunday).\n")
        valid4 = {'1','2','3','4','5','6','7','all'}
        while day not in valid4:
            print('Invalid input. Please use an integer for the day of week.')
            day = input("Which day? Please type your response as an integer (e.g., 1 = Sunday).\n")
    elif choose_filter in {'month'}:
        month = input("Which month do you want to look at? (Choose from january, february, march, april,may, and june.)\n")
        valid3 = {'january','february','march','april','may','june'}
        while month not in valid3: 
            print('Invalid input. Please enter lowercase letters for months.')
            month = input("Which month do you want to look at? (Choose from january, february, march, april,may, and june.)\n")
        day = 'all'
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    elif choose_filter in {'day'}: 
        day = input("Which day? Please type your response as an integer (e.g., 1 = Sunday).\n")
        valid4 = {'1','2','3','4','5','6','7','all'}
        while day not in valid4:
            print('Invalid input. Please use an integer for the day of week.')
            day = input("Which day? Please type your response as an integer (e.g., 1 = Sunday).\n")
        month = 'none'
    else:
        month = 'none'
        day = 'all'

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
    df = pd.read_csv(CITY_DATA[city])
    # print(df.columns)
    # print(df.head())
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df["Start Time"],format = '%Y-%m-%d %H:%M:%S')
    # print(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday.astype(int) +2
    df['day_of_week'] = df['day_of_week'].replace(8,1)
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'none':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == int(day)]
        #df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # TO DO: display the most common month

    most_common_month = df['month'].mode()[0]

    print('Most Common Month:', most_common_month)

    # TO DO: display the most common day of week
    most_common_dayofweek = df['day_of_week'].mode()[0]

    print('Most Common Day of Week:', most_common_dayofweek)

    # TO DO: display the most common start hour
    most_common_hour = df['hour'].mode()[0]

    print('Most Common Start Hour:', most_common_hour)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_startstation = df['Start Station'].mode()[0]

    print('Most Common Start Station:', most_common_startstation)

    # TO DO: display most commonly used end station
    most_common_endstation = df['End Station'].mode()[0]

    print('Most Common End Station:', most_common_endstation)


    # TO DO: display most frequent combination of start station and end station trip
    most_common_trip = df.groupby(['Start Station','End Station']).size().idxmax()

    print ('Most Frequent Trip: Starting from {} to {}'.format(most_common_trip[0],most_common_trip[1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total Travel Time: " , total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean Travel Time: ",mean_travel_time) 


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    # print value counts for each user type
    user_types = df['User Type'].value_counts()
    print("User Types:\n",user_types)

    # TO DO: Display counts of gender
    gender_count = df['Gender'].value_counts()
    print("Counts of Gender:\n",gender_count)

    # TO DO: Display earliest, most recent, and most common year of birth
    #print(df['birthyear'].describe())
    earliest_year_birth = df['Birth Year'].min()
    #print(earliest_year_birth)
    most_recent_year_birth = df['Birth Year'].max()
    #print(most_recent_year_birth)
    most_common_year_birth = df['Birth Year'].mode()[0]
    #print (most_common_year_birth)
    
    print("The oldest customer was born in: {}. \nThe youngest customer was born in: {}. \nThe customers' most common year of birth is: {}".format(earliest_year_birth,most_recent_year_birth,most_common_year_birth))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        valid6 = {'new york','chicago'}
        if city not in valid6: 
            print('User Data Not Available for This City.')
            print('-'*40)
        else: 
            user_stats(df)
    
    #Script should prompt the user if they want to see 5 lines of raw data, 
    #display that data if the answer is 'yes', 
    #and continue these prompts and displays until the user says 'no'.
    #return most_common_month, most_common_dayofweek, most_common_hour
     
        see_data = input("Do you want to see 5 lines of raw data? \n Type y or n: ")
        valid5 = {'y','n'}
        while see_data not in valid5:
            print("Invalid Input. Please Choose from y or n.")
            see_data = input("Do you want to see 5 lines of raw data? \n Type y or n: ")
        count = 0
        while see_data == 'y':
            count += 1
            lines_display = df.head(count*5)
            print(lines_display)
            see_data = input('Press y if you want to see more lines: \n Press n to exit:')

        print('-'*40)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
