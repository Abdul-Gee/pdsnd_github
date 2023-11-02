import time
import pandas as pd
import numpy as np

#Creating a dictionary containing the data sources for the three cities
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#Figuring out the filtering requirements of the user
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! I\'m Gee currently refactoring data. Let\'s explore some US bikeshare data!')
    #Initializing an empty city variable to store city choice from user
    #Currently refactoring data for Udacity project
    city = ''
    while city not in CITY_DATA.keys():
        print("\nWelcome. What city would you like to see the data for?")
        print("\n1. Chicago \n2. New York City \n3. Washington")
        print("\nPlease type in full name of city; not case sensitive.")
        #Taking user input and converting into lowercase
        city = input().lower()

        if city not in CITY_DATA.keys():
            print("\nSorry, input is invalid. Please type in either \'Chicago\', \'New York\', or \'Washington\'...")
            print("\nRestarting...")

    print(f"\nYou have chosen {city.title()} as your city.")

    #Creating a dictionary to store the available months, including the 'all' option
    MONTH_DICT = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    #Initializing an empty city variable to store month choice from user
    month = ''
    while month not in MONTH_DICT.keys():
        print("\nPlease enter the month, between January to June, whose data you would like to explore:")
        print("\nType in month's name; not case sensitive")
        print("\n(You may also opt to view the data for all months by typing 'All' as your input)")
        #Taking user input and converting into lowercase
        month = input().lower()

        if month not in MONTH_DICT.keys():
            print("\nSorry, input is invalid. Please try again in the accepted input format.")
            print("\nRestarting...")

    print(f"\nYou have chosen {month.title()} as your month.")

    #Creating a list to store all the days, including the 'all' option
    DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    #Initializing an empty city variable to store day choice from user
    day = ''
    while day not in DAY_LIST:
        print("\nPlease enter a day of the week you would like to look at:")
        print("\nType in name of day; not case sensitive.")
        print("\n(You can also view the data for all days in a week by typing 'All' as your input.)")
        #Taking user input and converting into lowercase
        day = input().lower()

        if day not in DAY_LIST:
            print("\nSorry, input is invalid. Please try again in the accepted input format.")
            print("\nRestarting...")

    print(f"\nYou have chosen {day.title()} as your day.")

    print(f"\nBelow is the data for city: {city.upper()}, month/s: {month.upper()} and day/s: {day.upper()}.")

    print('-'*60)
    return city, month, day

#Function to load data from .csv files
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
    #Load data file into a dataframe
    print("\nLoading data...")
    df = pd.read_csv(CITY_DATA[city])

    #Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #Filter by month if applicable
    if month != 'all':
        #use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #Filter by month to create new dataframe
        df = df[df['month'] == month]

    #Filter by day of week if applicable
    if day != 'all':
        #Filter by day of week to create new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

#Function to calculate all the time-related statistics for the chosen data
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Find and print the most popular month using mode method
    popular_month = df['month'].mode()[0]

    print(f"\nThe most popular month (1 = January,...,6 = June) is {popular_month}.")

    #Find and print the most popular day using mode method
    popular_day = df['day_of_week'].mode()[0]

    print(f"\nThe most popular day is {popular_day}.")

    #Extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    #Find the most start popular hour using mode method
    popular_hour = df['hour'].mode()[0]

    print(f"\nMost popular start hour: {popular_hour}:00")

    #Prints the time taken to perform the calculation
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

#Function to calculate station related statistics
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Display the most commonly used start station using mode method
    common_start_station = df['Start Station'].mode()[0]

    print(f"The most commonly used start station: {common_start_station}")

    #Display the most commonly used end station using mode method
    common_end_station = df['End Station'].mode()[0]

    print(f"\nThe most commonly used end station: {common_end_station}")

    #Combining two columns in the df to a new column 'Start To End'
    #Using mode to find out the most common combination of start and end stations
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    combo = df['Start To End'].mode()[0]

    print(f"\nThe most frequent combination of start station and end station trip is from {combo}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

#Function to calculate time related statistics
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Total travel time using sum method
    total_duration = df['Trip Duration'].sum()
    #Travel time in minutes and seconds format
    minute, second = divmod(total_duration, 60)
    #Travel time in hour and minutes format
    hour, minute = divmod(minute, 60)
    print(f"The total travel time is {hour} hours, {minute} minutes and {second} seconds.")

    #Average travel time using mean method
    average_duration = round(df['Trip Duration'].mean())
    #Average travel time in minutes and seconds format
    mins, sec = divmod(average_duration, 60)
    #Average travel time in hours, mins, sec format if the mins exceed 60
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(f"\nThe average travel time is {hrs} hours, {mins} minutes and {sec} seconds.")
    else:
        print(f"\nThe average travel time is {mins} minutes and {sec} seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Count of total users using value_counts method and their types (e.g. Subscriber or Customer)
    user_type = df['User Type'].value_counts()

    print(f"Below are the counts for each user type:\n\n{user_type}")

    #What is the user count by gender?
    try:
        gender = df['Gender'].value_counts()
        print(f"\nBelow are the counts for each gender:\n\n{gender}")
    except:
        print("\nThere is no 'Gender' column in this file.")

    #What is the earliest, most recent, and most common year of birth?
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest year of birth: {earliest}\n\nThe most recent year of birth: {recent}\n\nThe most common year of birth: {common_year}")
    except:
        print("There are no birth year details in this file.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)

#Function to display the data frame itself as per user request
def display_data(df):
    """Displays 5 rows of data from the csv file for the selected city.

    Args:
        param1 (df): The data frame you wish to work with.

    Returns:
        None.
    """
    BIN_RESPONSE_LIST = ['yes', 'no']
    rdata = ''
    counter = 0
    while rdata not in BIN_RESPONSE_LIST:
        print("\nDo you wish to view the raw data?")
        print("\nAccepted responses:\nYes or yes\nNo or no")
        rdata = input().lower()
        #the raw data from the df is displayed if user opts for it
        if rdata == "yes":
            print(df.head())
        elif rdata not in BIN_RESPONSE_LIST:
            print("\nPlease check your input.")
            print("Input does not seem to match any of the accepted responses.")
            print("\nRestarting...\n")

    #Extra while loop here to ask user if they want to continue viewing data
    while rdata == 'yes':
        print("Do you wish to view more raw data?")
        counter += 5
        rdata = input().lower()
        #If user opts for it, this displays next 5 rows of data
        if rdata == "yes":
             print(df[counter:counter+5])
        elif rdata != "yes":
             break

    print('-'*60)

#Main function to call all the previous functions
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
