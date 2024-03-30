import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
#Get the file path and store it in df
def get_file(file_path):
    # file_path = input('Enter file path:')
    df = pd.read_csv(file_path)
    df.head()
    return df

#Data Cleaning
def data_cleaner(df):
    for i in df.columns:
        null_values = df[i].isnull().sum()
        print(f"There are {null_values} Null values for {i} column",'\n')
        if null_values==0:
            continue
        else:
            percent_null_value = df[i].isnull().sum()/df.shape[0]*100
            if percent_null_value>50:
                print("The column is having more than 50% null values it would be good if we remove it to maintain data accuracy")
                df.drop(columns=[i], inplace=True)
            else:
                print(f"The null values are {percent_null_value} which is less than 50%, So we can handle it by Data Imputation")
                #let's get the data type of the column first
                if df[i].dtype == 'float64' or df[i].dtype == 'int64':
                    df[i].fillna(round(df[i].mean()),inplace=True) #imputing mean to handle the missing values in numerical data
                    print(f"Data Imputed with mean now there are {df[i].isnull().sum()} missing values",'\n')
                elif df[i].dtype == 'object':
                    df[i].fillna(df[i].mode()[0],inplace=True) #imputing mode to handle missing values in categorical data
                    print(f"Data Imputed with mode now there are {df[i].isnull().sum()} missing values",'\n')

def convert_object_to_date(df):
    for column in df.columns:
        if df[column].dtype == 'O':  # Check if the column has 'object' type
            try:
                df[column] = pd.to_datetime(df[column])  # Convert to datetime type
            except ValueError:
                pass  # If conversion fails, ignore the column
    return df

def visualizer(df):
    for i in df.columns:
        for j in df.columns:
            if i == j:
                continue
            else: #Taking the type of visualization as an input from user
                type_of_visual = input(
                    f'Type of visualization for {i} and {j} column (bar, line, scatter), press enter to skip: ')
                if not type_of_visual:
                    #here we will take the default visualization on the basis of data types of columns
                    if df[i].dtype == 'datetime64[ns]' or df[j].dtype == 'datetime64[ns]':
                        type_of_visual = 'line'
                    elif df[i].dtype == 'int64' and df[j].dtype == 'int64':
                        type_of_visual = "scatter"
                    elif df[i].dtype == 'object' and df[j].dtype == 'object':
                        type_of_visual = 'bar'
                    else:
                        type_of_visual = random.choice(['bar','line','scatter'])

                title = input("What title would you want for this visualization, press enter to skip: ")
                if not title:
                    title = f'{type_of_visual} of {i} and {j}'

                plt.figure(figsize=(10, 6))  # Create a new figure for each plot

                custom_colors = ['blue', 'orange', 'green', 'red', 'purple']
                selected_color = input(f'Choose a color from the {custom_colors} list:')
                if not selected_color:
                    selected_color = random.choice(custom_colors)
                    print(f'The random color choosen is {selected_color}')
                if selected_color not in custom_colors:
                    selected_color = random.choice(custom_colors)
                    print(f"The selected color does not match with custome colors - {custom_colors}, random color taken is {selected_color}")

                try:
                    if type_of_visual == 'bar':
                        sns.barplot(x=df[i], y=df[j], data=df, palette=custom_colors)
                    elif type_of_visual == 'line':
                        sns.lineplot(x=df[i], y=df[j], data=df, palette=custom_colors)
                    elif type_of_visual == 'scatter':
                        sns.scatterplot(x=df[i], y=df[j], data=df, palette=custom_colors)
                except:
                    print(f'Invalid Type of visualization {type_of_visual}')
                    continue

                plt.title(title)
                plt.xlabel(i)
                plt.ylabel(j)
                plt.xticks(rotation=45)
                # plt.show()
                output_filename = f'{i}_vs_{j}_{type_of_visual}.png'
                plt.savefig(output_filename)

                plt.close()