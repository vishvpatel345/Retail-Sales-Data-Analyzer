import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


class RetailAnalyzer:

    def __init__(self):
        self.data = None

    # Load sales data
    def load_data(self, file_path):
        if not os.path.exists(file_path):
            print("File not found. Please check the file name.")
            return False

        if not file_path.endswith(".csv"):
            print("Please select a CSV file.")
            return False

        try:
            self.data = pd.read_csv(file_path)

            required_columns = [
                "Date", "Product", "Category",
                "Price", "Quantity Sold", "Total Sales"
            ]

            for column in required_columns:
                if column not in self.data.columns:
                    print("Missing column:", column)
                    self.data = None
                    return False

            # Check missing values
            print("\nChecking missing values:")

            for column in self.data.columns:
                if self.data[column].isnull().any():
                    print("Missing values found in", column)

            # Convert data types
            self.data["Date"] = pd.to_datetime(
                self.data["Date"], errors="coerce"
            )

            self.data["Price"] = pd.to_numeric(
                self.data["Price"], errors="coerce"
            )

            self.data["Quantity Sold"] = pd.to_numeric(
                self.data["Quantity Sold"], errors="coerce"
            )

            self.data["Total Sales"] = pd.to_numeric(
                self.data["Total Sales"], errors="coerce"
            )

            # Remove rows with missing or invalid values
            self.data = self.data.dropna(
                subset=required_columns
            )

            # Remove invalid sales records
            self.data = self.data[
                (self.data["Price"] >= 0) &
                (self.data["Quantity Sold"] > 0)
            ]

            # Calculate total sales
            self.data["Total Sales"] = (
                self.data["Price"] * self.data["Quantity Sold"]
            )

            if self.data.empty:
                print("No valid sales data found.")
                self.data = None
                return False

            print("\nData loaded successfully!")
            print("Total records:", len(self.data))

            return True

        except Exception as e:
            print("Error loading file:", e)
            self.data = None
            return False

    # Calculate sales metrics
    def calculate_metrics(self):

        if self.data is None:
            print("Please load the data first.")
            return

        total_sales = self.data["Total Sales"].sum()

        average_sales = self.data["Total Sales"].mean()

        total_quantity = self.data["Quantity Sold"].sum()

        product_sales = self.data.groupby(
            "Product"
        )["Quantity Sold"].sum()

        popular_product = product_sales.idxmax()

        sales_array = np.array(
            self.data["Total Sales"]
        )

        average_numpy = np.mean(sales_array)

        print("\n----- SALES METRICS -----")

        print("Total Sales: ₹", round(total_sales, 2))

        print("Average Sales: ₹", round(average_sales, 2))

        print("Total Quantity Sold:", total_quantity)

        print("Most Popular Product:", popular_product)

        print("Average Sales using NumPy: ₹",
              round(average_numpy, 2))

    # Filter sales data
    def filter_data(self, condition):

        if self.data is None:
            print("Please load the data first.")
            return

        if condition == "category":

            category = input("Enter category name: ")

            result = self.data[
                self.data["Category"].str.lower()
                == category.lower()
            ]

        elif condition == "product":

            product = input("Enter product name: ")

            result = self.data[
                self.data["Product"].str.lower()
                == product.lower()
            ]

        elif condition == "date":

            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")

            start_date = pd.to_datetime(
                start_date, errors="coerce"
            )

            end_date = pd.to_datetime(
                end_date, errors="coerce"
            )

            if pd.isna(start_date) or pd.isna(end_date):
                print("Invalid date format.")
                return

            if start_date > end_date:
                print("Start date cannot be after end date.")
                return

            result = self.data[
                (self.data["Date"] >= start_date) &
                (self.data["Date"] <= end_date)
            ]

        else:
            print("Invalid filter option.")
            return

        if result.empty:
            print("No records found.")

        else:
            print("\nFiltered Sales Data:")
            print(result.to_string(index=False))

            print("\nFiltered Total Sales: ₹",
                  round(result["Total Sales"].sum(), 2))

    # Display summary
    def display_summary(self):

        if self.data is None:
            print("Please load the data first.")
            return

        print("\n----- DATA SUMMARY -----")

        print(self.data.describe())

        print("\nSales by Category:")

        category_sales = self.data.groupby(
            "Category"
        )["Total Sales"].sum()

        print(category_sales)

        print("\nSales by Product:")

        product_sales = self.data.groupby(
            "Product"
        )["Total Sales"].sum()

        print(product_sales)

        # Calculate growth percentage
        daily_sales = self.data.groupby(
            "Date"
        )["Total Sales"].sum().sort_index()

        if len(daily_sales) >= 2:

            first_sales = daily_sales.iloc[0]
            last_sales = daily_sales.iloc[-1]

            if first_sales != 0:
                growth = (
                    (last_sales - first_sales)
                    / first_sales
                ) * 100

                print("\nSales Growth: ",
                      round(growth, 2), "%")

            else:
                print("\nSales growth cannot be calculated "
                      "because the first day's sales are zero.")

    # Create charts
    def show_charts(self):

        if self.data is None:
            print("Please load the data first.")
            return

        # Bar chart
        category_sales = self.data.groupby(
            "Category"
        )["Total Sales"].sum()

        category_sales.plot(
            kind="bar",
            title="Total Sales by Category"
        )

        plt.xlabel("Category")
        plt.ylabel("Total Sales")
        plt.tight_layout()
        plt.show()

        # Line graph
        daily_sales = self.data.groupby(
            "Date"
        )["Total Sales"].sum().sort_index()

        plt.figure()

        plt.plot(
            daily_sales.index,
            daily_sales.values,
            marker="o"
        )

        plt.title("Sales Trend Over Time")
        plt.xlabel("Date")
        plt.ylabel("Total Sales")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        # Heatmap
        plt.figure()

        correlation = self.data[
            ["Price", "Quantity Sold", "Total Sales"]
        ].corr()

        sns.heatmap(
            correlation,
            annot=True,
            cmap="coolwarm"
        )

        plt.title("Sales Data Correlation")
        plt.tight_layout()
        plt.show()


# Main program
analyzer = RetailAnalyzer()

while True:

    print("\n===== RETAIL SALES DATA ANALYZER =====")

    print("1. Load Sales Data")
    print("2. Calculate Sales Metrics")
    print("3. Filter Sales Data")
    print("4. Display Summary")
    print("5. Show Charts")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":

        file_path = input(
            "Enter CSV file path (e.g. retail_sales.csv): "
        )

        analyzer.load_data(file_path)

    elif choice == "2":

        analyzer.calculate_metrics()

    elif choice == "3":

        print("\n1. Filter by Category")
        print("2. Filter by Product")
        print("3. Filter by Date Range")

        filter_choice = input("Enter your choice: ")

        if filter_choice == "1":
            analyzer.filter_data("category")

        elif filter_choice == "2":
            analyzer.filter_data("product")

        elif filter_choice == "3":
            analyzer.filter_data("date")

        else:
            print("Invalid choice.")

    elif choice == "4":

        analyzer.display_summary()

    elif choice == "5":

        analyzer.show_charts()

    elif choice == "6":

        print("Thank you for using Retail Sales Data Analyzer!")
        break

    else:

        print("Invalid choice. Please try again.")
        