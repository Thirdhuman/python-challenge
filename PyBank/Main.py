#PyBank

'''
In this challenge, you are tasked with creating a Python script for analyzing the financial records of your company. 
You will be given two sets of revenue data (budget_data_1.csv and budget_data_2.csv). 
Each dataset is composed of two columns: Date and Revenue. 
(Thankfully, your company has rather lax standards for accounting so the records are simple.)

Your task is to create a Python script that analyzes the records to calculate each of the following:

#1. The total number of months included in the dataset
#2. The total amount of revenue gained over the entire period
#3. The average change in revenue between months over the entire period
#4. The greatest increase in revenue (date and amount) over the entire period
#5. The greatest decrease in revenue (date and amount) over the entire period

Financial Analysis
----------------------------
Total Months: 25
Total Revenue: $1241412
Average Revenue Change: $216825
Greatest Increase in Revenue: Sep-16 ($815531)
Greatest Decrease in Revenue: Aug-12 ($-652794)
'''

import pandas as pd
import os
import csv

os.chdir("/Users/rorr/PythonStuff/")
csvpath = os.path.join("Resources", "budget_data_2.csv")

budget_df = pd.read_csv(csvpath, encoding="utf-8")

budget_df.head()

#1. The total number of months included in the dataset
months = budget_df["Revenue"].count()

months

#2. The total amount of revenue gained over the entire period
total_rev = budget_df["Revenue"].sum()
total_rev

#3. The average change in revenue between months over the entire period
average_change = (total_rev / months)

#4. The greatest increase in revenue (date and amount) over the entire period
greatest_increase = budget_df.loc[budget_df['Revenue'].idxmax()]

greatest_increase.Date
greatest_increase.Revenue

#5. The greatest decrease in revenue (date and amount) over the entire period
greatest_decrease = budget_df.loc[budget_df['Revenue'].idxmin()]
greatest_decrease.Date
greatest_decrease.Revenue

print("Financial Analysis")
print("-------------------------")
print("Total Months: " + str(months))
print("Total Revenue: " + str(total_rev))
print("Average Revenue Change: " + str(average_change))
print("Greatest Increase in Revenue: " + str(greatest_increase.Date) + " (" + (greatest_increase.Revenue).astype(str) + ")")
print("Greatest Decrease in Revenue: " + str(greatest_decrease.Date) + " (" + (greatest_decrease.Revenue).astype(str) + ")")

text = open("Financial Analysis.txt", "w")
text.write("Financial Analysis")
text.write('\n')
text.write("-------------------------")
text.write('\n')
text.write("Total Months: " + str(months))
text.write('\n')
text.write("Total Revenue: " + str(total_rev))
text.write('\n')
text.write("Average Revenue Change: " + str(average_change))
text.write('\n')
text.write("Greatest Increase in Revenue: " + str(greatest_increase))
text.write('\n')
text.write("Greatest Decrease in Revenue: " + str(greatest_decrease))
text.write('\n')
text.close()