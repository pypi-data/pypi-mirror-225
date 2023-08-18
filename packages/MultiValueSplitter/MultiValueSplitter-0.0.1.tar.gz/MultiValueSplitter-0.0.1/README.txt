.. _Data Preprocessing Library:

Data Preprocessing Library
==========================

This Python library provides a function to preprocess data by splitting a specified columns values and filling down other specified columns. This is particularly useful for handling multi-valued cells in a DataFrame.

Functionality
-------------

The main function in this library is process_data(file_name, column_to_split, column_to_fill, separator). 

- file_name: The name of the CSV file to be processed.
- column_to_split: The name of the column whose values need to be split.
- column_to_fill: A list of column names that need to be filled down (forward filled).
- separator: The character or string used as the separator for splitting the values in the column_to_split.

The function reads the specified CSV file into a DataFrame, splits the values in the column_to_split based on the provided separator, and then fills down the specified column_to_fill. The processed DataFrame is returned by the function.

Usage
-----

Here is a sample usage of the process_data function:

    from data_processing import process_data

    df = process_data(data.csv, Column1, [Column2, Column3, Column4], ,)
    
    print(df)

In this example, data.csv is the CSV file to be processed, Column1 is the column to be split, [Column2, Column3, Column4] are the columns to be filled down, and , is the separator for splitting.