# Team 9
# IS 303 - Section 003
# Retail Sales Data
# Description: This program reads retail sales data from an Excel file, processes it, and stores it in a PostgreSQL database. It allows users to view summaries of the data and generates visualizations based on user input.

import sqlalchemy
import pandas as pd
import matplotlib.pyplot as plot

# Menu loop to ask the user for input
while True:
    menuChoice = input("If you want to import data, enter 1. If you want to see summaries of stored data, enter 2. Enter any other value to exit the program: ")
    try:
        if int(menuChoice) == 1:
            #Part 1-1: Import data from the Excel file into Python
            salesData = pd.read_excel('Retail_Sales_Data.xlsx')

            #Part 1-2:
            # Split the name column into first_name and last_name
            separatedNames = salesData["name"].str.split("_", expand=True)
            
            # Insert the new columns into the dataframe
            salesData.insert(1, "first_name", separatedNames[0])
            salesData.insert(2, "last_name", separatedNames[1])
            
            # Delete the original name column
            del salesData["name"]

            #Part 1-3:

            #Part 1-4:

            #Part 1-5: Print success message.
            print("You\'ve imported the excel file into your postgres database.")

        elif int(menuChoice) == 2:
            #Part 2-1: Print category message.
            print("The following are all the categories that have been sold:")

            #Part 2-2:
    
            #Part 2-3: Ask the user for a category number.
            selectedCategory = input("Please enter the number of the category you want to see summarized: ")

            #Part 2-4:
            
            #Part 2-5:
            # Group by product and sum the total_price
            dfProductSales = dfFiltered.groupby('product')['total_price'].sum()
                    
                    # Create the chart
            dfProductSales.plot(kind='bar')  # creates the chart
            plot.title(f"Total Sales in {requestedCategory}")  # adds title to the top of the chart
            plot.xlabel("Product")  # label for the x-axis
            plot.ylabel("Total Sales")  # label for the y-axis
            plot.show()  # makes the chart pop up on the screen
        else:
                    print("Invalid category number.")
    except ValueError:
                print("Please enter a valid number.")
            
        #Exit the program if the user enters anything other than 1 or 2
        else:
            print("Closing the program.")
            break
    except ValueError:
        print("Closing the program.")
        break
            

