import time
import pandas as pd
import numpy as np

# City data file mapping
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Get user input for city
    while True:
        city = input("Enter the city name (chicago, new york city, washington): ").lower()
        if city in CITY_DATA:
            break
        print("Invalid city. Please choose from chicago, new york city, or washington.")
    
    # Get user input for month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Enter the month (january, february, ... , june) or 'all': ").lower()
        if month in months:
            break
        print("Invalid month. Please choose a month from january to june, or 'all'.")
    
    # Get user input for day of week
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Enter the day of the week (monday, tuesday, ...) or 'all': ").lower()
        if day in days:
            break
        print("Invalid day. Please choose a day of the week or 'all'.")
    
    print('-'*40)
    return city, month, day

def filter_data(df, column, value):
    """
    Filters the DataFrame based on the given column and value.
    Args:
        df (DataFrame): The DataFrame to filter.
        column (str): The column name to filter by.
        value (str or int): The value to filter for (or 'all' to skip filtering).
    Returns:
        DataFrame: The filtered DataFrame.
    """
    if value != 'all':
        return df[df[column] == value]
    return df

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
    # Load data
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extract month, day of week, and hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour
    
    # Filter by month
    if month != 'all':
        month_index = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = filter_data(df, 'month', month_index)
    
    # Filter by day of week
    df = filter_data(df, 'day_of_week', day)
    
    return df

def display_raw_data(df):
    """
    Displays raw data in increments of 5 rows upon user request.
    Args:
        df - Pandas DataFrame containing the filtered city data
    """
    print('\nRaw data is available to review.')
    start_row = 0
    
    while True:
        view_data = input("\nWould you like to view 5 rows of raw data? Enter yes or no: ").lower()
        if view_data != 'yes':
            break
        
        # Display 5 rows of data
        print(df.iloc[start_row:start_row + 5])
        start_row += 5
        
        # Stop if no more data
        if start_row >= len(df):
            print("\nNo more rows to display.")
            break

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Most common month
    most_common_month = df['month'].mode()[0]
    print(f"Most common month: {most_common_month}")
    
    # Most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print(f"Most common day of week: {most_common_day.title()}")
    
    # Most common start hour
    most_common_hour = df['hour'].mode()[0]
    print(f"Most common start hour: {most_common_hour}")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f"Most common start station: {most_common_start_station}")
    
    # Most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f"Most common end station: {most_common_end_station}")
    
    # Most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + " to " + df['End Station']
    most_common_trip = df['trip'].mode()[0]
    print(f"Most common trip: {most_common_trip}")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time: {total_travel_time} seconds")
    
    # Mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean travel time: {mean_travel_time} seconds")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Counts of user types
    user_types = df['User Type'].value_counts()
    print(f"User types:\n{user_types}")
    
    # Gender and birth year stats (only available for NYC and Chicago)
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print(f"\nGender breakdown:\n{gender_counts}")
    
    if 'Birth Year' in df:
        earliest_birth = int(df['Birth Year'].min())
        most_recent_birth = int(df['Birth Year'].max())
        most_common_birth = int(df['Birth Year'].mode()[0])
        print(f"\nEarliest birth year: {earliest_birth}")
        print(f"Most recent birth year: {most_recent_birth}")
        print(f"Most common birth year: {most_common_birth}")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
