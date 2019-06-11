import time
import pandas as pd
import numpy as np
import calendar   

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of city
        (str) month - name of the month to filter by, or "None" to apply no month filter
        (str) day - name of the day of week to filter by, or "None" to apply no day filter
    """

    print('\nHello! Let\'s explore some US bikeshare data!')
    #get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('-'*30)
    print ('*Cities-Bike data*\n')
    print ( 'Chicago')
    print ( 'New York City')
    print ( 'Washington')    
    print('-'*30)
    while True:
      city = input("\nWhich city would you like to filter by? See above\n").title()
      if city not in ('Chicago','New York City', 'Washington'):
        print("Incorrect input,See above options.")
        continue
      else:
        print('Great!!, now next step\n')
        break

    #get user input for month (None, january, february, ... , june)
    
    print('-'*30)
    print ('Select Month filters\n')
    print ( 'January')
    print ( 'February')
    print ( 'March')
    print ( 'April')
    print ( 'June')
    print ( 'None')
    print('-'*30)
    
    
    while True:
      month = input('Select from above options. Type None for no filters\n').title()
      if month not in ('January', 'February', 'March', 'April', 'May', 'June', 'None'):
        print("Incorrect input,See above options.")
        continue
      else:
        print('Great!!, now next step\n')
        break

    #get user input for day of week (None, monday, tuesday, ... sunday)
    
    print('-'*30)
    print ('Select day filters\n')
    print ( 'Sunday')
    print ( 'Monday')
    print ( 'Wednesday')
    print ( 'Thursday')
    print ( 'Friday')
    print ( 'None')
    print('-'*30)
    
    while True:
      day = input("Do you want to filter by day? If yes select above. Type None for no filters \n").title()
      if day not in ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'None'):
        print("Incorrect input,See above options.")
        continue
      else:
        break

    print ('\n**Analysis for**-', city.upper())
    print('-'*40)
    return city, month, day


def load_data(city, month, day):

    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of city
        (str) month - name of the month to filter by, or "None" to apply no month filter
        (str) day - name of the day of week to filter by, or "None" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Loading city data into file
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month #Extract month from date time and create a column
    df['d_week'] = df['Start Time'].dt.weekday_name #Gives name of the week and create a column
    df['start-end'] =  df['Start Station'].str.cat(df['End Station'], sep=' -- ') #Combining start and end station for better reporting
    
    
    # filter by month if applicable
    if month != 'None':
   	 	# Created a dictionary that houses the values for months 
        months = { 'January' : 1, 'February' : 2, 'March' : 3, 'April' : 4, 'May' : 5, 'June' : 6}
        month = months[month]


    	# Filtered month data frame if specified
        df = df[df['month'] == month]

        # Filtered day data frame if specified
    if day != 'None':
        # filter by day of week to create the new dataframe
        df = df[df['d_week'] == day.title()]    

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('**General overivew**\n')

    #display the most common month

    common_month = df['month'].mode()[0]
    print('Most common month:', calendar.month_name[int(common_month)]) #using calendar import to display name


    #display the most common day of week

    common_day = df['d_week'].value_counts(dropna =True).reset_index()['index'][0] 
    print('Most common day:', common_day)


    #display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0] #mode returns the highest value in a series
    print('Most common hour:', common_hour)

    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('**Trips and Stations analysis**\n')


    # display most popular start station

    Start_Station = df['Start Station'].value_counts(dropna =True).reset_index()['index'][0]
    print('\nMost popular start station-:', Start_Station.capitalize())


    #display most popular end station

    End_Station = df['End Station'].value_counts(dropna =True).reset_index()['index'][0]
    print('\nMost popular end station-:', End_Station.capitalize())


    #display most popular combination of start station and end station trip

    popular_round_trip_stations = df['start-end'].mode().to_string(index = False)
    print('\nMost common round trip station-: {}.'.format(popular_round_trip_stations))

    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('**Trip duration**\n')


    #display total trip duration

    total_trip_duration = np.sum(df['Trip Duration'])
    print('Total trip duration-:', round((total_trip_duration/(60*60*24*365)),0), " Years")


    #display average trip duration

    average_trip_duartion = np.mean(df['Trip Duration'])
    print('Average trip duartion-:', round((average_trip_duartion/60),2), " Minutes")
    
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('**User Stats**\n')


    #Display different user categories
    print ('User type-')
    user_count = df['User Type'].value_counts(dropna =True)
    print(user_count)


    try:
      earliest_birth_year = str(int(df['Birth Year'].min()))
      print('\nEarliest birth year:', earliest_birth_year)
    except KeyError:
      print("\nEarliest birth Year:\nData not available for Washington city.")

    try:
      most_recent_birth_year = str(int(df['Birth Year'].max()))
      print('\nMost recent birth year:', most_recent_birth_year)
    except KeyError:
      print("\nMost recent birth year:\n Data not available for Washington city.")

    try:
      most_common_birth_year = df.groupby('Birth Year')['Birth Year'].count()
      print('\nMost common birth year:', str(int(most_common_birth_year.index[0])))
    except KeyError:
      print("\nMost common birth year:\n Data not available for Washington city.")

    print('-'*40)

def user_data(df):
    '''Displays raw data based on user selection of city for analysis'''
    
    u_data = input('\n Would you like to see indiviudal trip data? Type - Yes/No\n').title()
    curr_row = 0
    
    while True:
        if u_data == 'No':
            return
        elif u_data == 'Yes':
             print(df[curr_row: curr_row + 5])
             curr_row = curr_row + 5
        else:
            print('Incorrect input. Please type -Yes/No\n')
        
        u_data = input('\nWould you like to see more data? Type - Yes/No \n').title()



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        user_data(df)
        program_restart = input('\n Would you like to analyze again? Type - Yes/No.\n').title()
        if program_restart != 'Yes':
            break


if __name__ == "__main__":
	main()