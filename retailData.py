# Team 9
# IS 303 - Section 003
# Retail Sales Data
# Description: This program reads retail sales data from an Excel file, 
# processes it, and stores it in a PostgreSQL database. 
# It allows users to view summaries of the data and generates visualizations based on user input.

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import pandas as pd
import matplotlib.pyplot as plot

# Menu loop to ask the user for input
while True:
    menuChoice = input("If you want to import data, enter 1. If you want to see summaries of stored data, enter 2. Enter any other value to exit the program: ")
    try:
        if int(menuChoice) == 1:
            # Part 1-1: Import data from the Excel file into Python
            salesData = pd.read_excel('Retail_Sales_Data.xlsx')

            # Part 1-2:
            # Split the name column into first_name and last_name
            separatedNames = salesData["name"].str.split("_", expand=True)
            salesData.insert(1, "first_name", separatedNames[0])
            salesData.insert(2, "last_name", separatedNames[1])
            del salesData["name"]

            # Part 1-3: Replace incorrect data in category column
            productCategoriesDict = {
                'Camera': 'Technology',
                'Laptop': 'Technology',
                'Gloves': 'Apparel',
                'Smartphone': 'Technology',
                'Watch': 'Accessories',
                'Backpack': 'Accessories',
                'Water Bottle': 'Household Items',
                'T-shirt': 'Apparel',
                'Notebook': 'Stationery',
                'Sneakers': 'Apparel',
                'Dress': 'Apparel',
                'Scarf': 'Apparel',
                'Pen': 'Stationery',
                'Jeans': 'Apparel',
                'Desk Lamp': 'Household Items',
                'Umbrella': 'Accessories',
                'Sunglasses': 'Accessories',
                'Hat': 'Apparel',
                'Headphones': 'Technology',
                'Charger': 'Technology'
            }
            salesData["category"] = salesData["product"].map(productCategoriesDict)

            # Part 1-4: Save the results to the PostgreSQL database
            username = 'postgres'
            password = 'admin'
            host = 'localhost'
            port = '5432'
            database = 'is303postgres'
            try:
                engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')
                conn = engine.connect()
            except OperationalError as e:
                print("Error: Unable to connect to the database. Please ensure the database 'is303postgres' exists.")
                print(e)
                exit()

            salesData.to_sql('sale', conn, if_exists='replace', index=True)

            # Part 1-5: Print success message
            print("You've imported the excel file into your postgres database.")

        elif int(menuChoice) == 2:
            # Part 2-1: Print category message
            print("The following are all the categories that have been sold:")

            # Part 2-2: Connect to database and display categories
            username = 'postgres'
            password = 'admin'
            host = 'localhost'
            port = '5432'
            database = 'is303postgres'
            try:
                engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')
                conn = engine.connect()
            except OperationalError as e:
                print("Error: Unable to connect to the database. Please ensure the database 'is303postgres' exists.")
                print(e)
                exit()

            query = "SELECT DISTINCT category FROM sale ORDER BY category"
            dfCategories = pd.read_sql(text(query), engine)
            category_list = dfCategories['category'].tolist()

            for iCount, category in enumerate(category_list, start=1):
                print(f"{iCount}: {category}")
            print("0: Return to the main menu")

            # Part 2-3: Allow repeated requests for summaries until the user enters 0
            while True:
                selectedCategory = input("Please enter the number of the category you want to see summarized (or 0 to return to the main menu): ")
                try:
                    selectedCategory = int(selectedCategory)
                    if selectedCategory == 0:
                        print("Returning to the main menu...")
                        break
                    elif 1 <= selectedCategory <= len(category_list):
                        categoryName = category_list[selectedCategory - 1]

                        # Part 2-4: Filter data for the selected category
                        dftotalSales = pd.read_sql(text("SELECT * FROM sale"), conn)
                        dfFiltered = dftotalSales.query('category == @categoryName')

                        if not dfFiltered.empty:
                            totalSales = dfFiltered['total_price'].sum()
                            averageSale = dfFiltered['total_price'].mean()
                            totalUnitsSold = dfFiltered['quantity_sold'].sum()

                            print(f"\nSummary of Category: {categoryName}")
                            print(f"Total Sales: ${totalSales:,.2f}")
                            print(f"Average Sale Amount: ${averageSale:,.2f}")
                            print(f"Total Units Sold: {totalUnitsSold}")

                            # Part 2-5: Create the chart
                            dfProductSales = dfFiltered.groupby('product')['total_price'].sum()
                            dfProductSales.plot(kind='bar')
                            plot.title(f"Total Sales in {categoryName}")
                            plot.xlabel("Product")
                            plot.ylabel("Total Sales")
                            plot.show()
# Handle any input errors, and allow for exiting the program
                        else:
                            print("Invalid category name or no data available for the selected category.")
                    else:
                        print("Invalid category number.")
                except ValueError:
                    print("Please enter a valid number.")
        else:
            print("Closing the program.")
            break
    except ValueError:
        print("Closing the program.")
        break
