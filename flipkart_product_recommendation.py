#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import pandas as pd
import requests

#Create empty lists to store the data for this page
Product_name, Price, Rating, Total_Rating,Product_link = list(), list(), list(), list(), list()

# The outputfile after extraction
output_file = 'flipkart_details2'
user_input=input("Search for products,brands and more: ")
product = user_input.replace(" ","%20")

# URL used to get the information
base_url = f"https://www.flipkart.com/search?q={product}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page="
n=0
# Module to get the details from url
def scrape_page(url):
    global n
    # Send a GET request to the URL and get the response
    response = requests.get(url)    
    # Create a BeautifulSoup object from the response text using the html.parser
    soup = BeautifulSoup(response.text, 'html.parser')
    #page=0
    n+=1
    # Extract data from the page using BeautifulSoup selectors or regular expressions
    for flipkart in soup.find_all('div', class_='_1AtVbE col-12-12'):
        product_name = flipkart.find('div',class_ = '_4rR01T')
        if product_name is not None:        
            Product_name.append(product_name.text)
        else:
            #print("Product name not found")
            Product_name.append("N/A")

        price = flipkart.find('div', class_='_30jeq3 _1_WHN1')
        if price is not None:        
            Price.append(price.text)
        else:
            #print("Product name not found")
            Price.append("N/A")

        rating = flipkart.find('div', class_='_3LWZlK')  
        if rating is not None:        
            Rating.append(rating.text)
        else:
            #print("Product name not found")
            Rating.append("N/A")
            
        t_rating = flipkart.find('span', class_='_2_R_DZ')  
        
        if t_rating is not None:
            t_clean=((t_rating.text).split(" "))[0]
            #print(t_clean)
            Total_Rating.append(t_clean)
        else:
            #print("Product name not found")
            Total_Rating.append("N/A")
        try:
            link1 = flipkart.find('a', class_='_1fQZEK')['href']
            link=link1.split("?")[0]
            pro_link="https://www.flipkart.com"+link
            Product_link.append(pro_link)
        except:
            Product_link.append('N/A')
        #page+=1
        
    # Create a Pandas DataFrame with the lists and append it to the output file
    df = pd.DataFrame({'Product Name': Product_name, 'Price': Price, 'Rating': Rating,"Total Ratings":Total_Rating,"Product Link":Product_link})
    df.to_csv(output_file+'.csv', index=False, encoding='utf-8')
    
    # Return the number of pages in the  particular website
    return n

# Define the total number of pages to scrape
"""response = requests.get("https://www.flipkart.com/search?q=laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=1")
soup2 = BeautifulSoup(response.text, 'html.parser')
num_pages = soup2.find('div', class_="_2MImiq")
max_pages=int((num_pages.span.text).split(' ')[3])"""
max_pages=3

# Scrape each page in the range of page numbers
for page_num in range(1, max_pages + 1):
    url = base_url + str(page_num)
    # Save the data to a
    print(scrape_page(url))


# In[2]:


import pandas as pd 
file=output_file+".csv"
df=pd.read_csv(file)

# Drop rows with missing values in the 'Product Name' column
df = df.dropna(subset=['Product Name','Price','Product Link'])

# Drop duplicates based on all columns
df = df.drop_duplicates()

# Drop the row where the Name column contains 'Product name'
df = df[df['Product Name'] != 'Product Name']

# Save the cleaned DataFrame as a CSV file
df.to_csv('flipkart_link.csv', index=False)

# Read the CSV file back into a DataFrame to verify it was saved correctly
df_new = pd.read_csv('flipkart_link.csv')


#pd.set_option('display.max_columns', None)
df_new['Total Ratings'] = df_new['Total Ratings'].str.replace(',', '').fillna('0').astype(int)
#df_new
# create a 'Highly_Ratings' column based on the 'Total_Ratings' column
df_new['Highly Ratings'] = df_new['Total Ratings']> 1000
#df_new['Highly Ratings']
# filter the DataFrame to only show highly rated items
highly_rated = df_new[df_new['Highly Ratings']]
#highly_rated
# sort the 'Salary' column in descending order
sorted_df = highly_rated.sort_values('Total Ratings', ascending=False)
#sorted_df


from IPython.display import HTML

# render the DataFrame as HTML with clickable links
#highly_rated['Product Link'] = highly_rated['Product Link'].apply(lambda x: '<a href="{}" target="_blank">{}</a>'.format(x, x))
sorted_df.loc[:, 'Product Link'] = sorted_df['Product Link'].apply(lambda x: '<a href="{}" target="_blank">{}</a>'.format(x, x))   #.head(4)
HTML(sorted_df.to_html(escape=False))
# print the top 3 rows of the sorted dataframe
#print(sorted_df.head(5))


# In[3]:


#sorted_df.head()


# In[4]:


# Set the display options
#pd.set_option('display.max_colwidth', None)
#highly_rated["Product Link"]

