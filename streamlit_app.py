# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customise your Smoothie App :cup_with_straw: {st.__version__}")
st.write(
  """Choose your fruits
  """)


name_on_order = st.text_input("Name on Smoothie: ")
st.write("The name on your smoothie will be: ", name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients: ' , my_dataframe,
    max_selections=5
)

if ingredients_list:
   # st.write(ingredients_list)
  #  st.text(ingredients_list)

    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
 #   st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string +"""','"""+name_on_order+ """')"""

 #   st.write(my_insert_stmt)
   # st.stop()
    time_insert=st.button('Submit')

    if time_insert:
        session.sql(my_insert_stmt).collect()

        st.success(name_on_order+' your smoothie is ordered ... yayy!!', icon='✅')

        
#new section to display smootie nutrition info
import requests
smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(smoothiefroot_response)
