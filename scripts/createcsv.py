'''
Python script to create CSV files for bakery pipeline data.
Using ChatGPT-generated dummy data to simulate Shopify data 
for orders and products, and ingredient/recipe data for cost calculations.
'''

import pandas as pd

output_path = "/Users/katiewojciechowski/Projects/bakery-project/bakery-pipeline/source-data/"

# ----------------------
# Shopify Products
# ----------------------

# To CSV titled shopify_products.csv
# Features: sku,product_name,category,price

products_data = [
    {"cookie_sku":"CK-CHOC-001","product_name":"Chocolate Chip Cookies","category":"Dozen Cookies","price":28.00},
    {"cookie_sku":"CK-SUGAR-001","product_name":"Emmy's Sugar Cookies","category":"Dozen Cookies","price":28.00},
    {"cookie_sku":"CK-NUTMARB-001","product_name":"Nutella Marbled Chocolate Chip Cookies","category":"Dozen Cookies","price":28.00},
    {"cookie_sku":"ADD-NUTELLA","product_name":"Nutella Stuffing","category":"Add-on","price":4.00},
    {"cookie_sku":"ADD-PB","product_name":"Crunchy Peanut Butter Stuffing","category":"Add-on","price":4.00},
    {"cookie_sku":"ADD-SEASALT","product_name":"Sea Salt Topping","category":"Add-on","price":0.00}
]

products_df = pd.DataFrame(products_data)
products_df.to_csv(output_path + "shopify_products.csv", index=False)

# ----------------------
# Ingredients
# ----------------------

# To CSV titled ingredients.csv
# Features: ingredient,unit,grams_per_unit,supplier,container_description,container_grams,cost_per_unit,cost_per_gram

ingredients_data = [
    {"ingredient":"All-purpose flour","unit":"cup","grams_per_unit":120,"supplier":"FlourCo","container_description":"1 lb bag","container_grams":454,"cost_per_unit":0.25,"cost_per_gram":0.002083},
    {"ingredient":"Butter","unit":"cup","grams_per_unit":227,"supplier":"DairyBest","container_description":"4-stick box (1 lb)","container_grams":454,"cost_per_unit":1.20,"cost_per_gram":0.005286},
    {"ingredient":"White sugar","unit":"cup","grams_per_unit":200,"supplier":"SweetSource","container_description":"4 lb bag","container_grams":1814,"cost_per_unit":0.40,"cost_per_gram":0.002000},
    {"ingredient":"Brown sugar","unit":"cup","grams_per_unit":220,"supplier":"SweetSource","container_description":"2 lb bag","container_grams":907,"cost_per_unit":0.45,"cost_per_gram":0.002045},
    {"ingredient":"Chocolate chips","unit":"cup","grams_per_unit":170,"supplier":"CocoaWorld","container_description":"24 oz bag","container_grams":680,"cost_per_unit":1.50,"cost_per_gram":0.008824},
    {"ingredient":"Eggs","unit":"count","grams_per_unit":50,"supplier":"FarmFresh","container_description":"Dozen eggs","container_grams":600,"cost_per_unit":0.30,"cost_per_gram":0.006000},
    {"ingredient":"Vanilla extract","unit":"tbsp","grams_per_unit":13,"supplier":"FlavorHouse","container_description":"8 oz bottle","container_grams":227,"cost_per_unit":0.80,"cost_per_gram":0.061538},
    {"ingredient":"Baking soda","unit":"tsp","grams_per_unit":4.6,"supplier":"BakeSupply","container_description":"1 lb box","container_grams":454,"cost_per_unit":0.05,"cost_per_gram":0.010870},
    {"ingredient":"Baking powder","unit":"tsp","grams_per_unit":4.0,"supplier":"BakeSupply","container_description":"1 lb container","container_grams":454,"cost_per_unit":0.05,"cost_per_gram":0.012500},
    {"ingredient":"Salt","unit":"tsp","grams_per_unit":6,"supplier":"SaltWorks","container_description":"3 lb box","container_grams":1360,"cost_per_unit":0.02,"cost_per_gram":0.003333},
    {"ingredient":"Nutella","unit":"cup","grams_per_unit":300,"supplier":"Hazelnut Corp","container_description":"26 oz jar","container_grams":737,"cost_per_unit":1.75,"cost_per_gram":0.005833},
    {"ingredient":"Crunchy peanut butter","unit":"cup","grams_per_unit":250,"supplier":"NuttyFoods","container_description":"16 oz jar","container_grams":454,"cost_per_unit":1.20,"cost_per_gram":0.004800},
    {"ingredient":"Sea salt","unit":"tsp","grams_per_unit":6,"supplier":"SaltWorks","container_description":"1 lb pouch","container_grams":454,"cost_per_unit":0.03,"cost_per_gram":0.005000}
]

ingredients_df = pd.DataFrame(ingredients_data)
ingredients_df.to_csv(output_path + "ingredients.csv", index=False)

# ----------------------
# Recipes
# ----------------------

# To CSV titled recipes.csv
# Features: sku,ingredient,quantity_unit,quantity

recipes_data = [
    {"sku":"CK-CHOC-001","ingredient":"All-purpose flour","quantity_unit":"cups","quantity":2.5},
    {"sku":"CK-CHOC-001","ingredient":"Butter","quantity_unit":"cups","quantity":1},
    {"sku":"CK-CHOC-001","ingredient":"White sugar","quantity_unit":"cups","quantity":1},
    {"sku":"CK-CHOC-001","ingredient":"Brown sugar","quantity_unit":"cups","quantity":1},
    {"sku":"CK-CHOC-001","ingredient":"Chocolate chips","quantity_unit":"cups","quantity":2},
    {"sku":"CK-CHOC-001","ingredient":"Eggs","quantity_unit":"count","quantity":2},
    {"sku":"CK-CHOC-001","ingredient":"Vanilla extract","quantity_unit":"tbsp","quantity":1},
    {"sku":"CK-CHOC-001","ingredient":"Baking soda","quantity_unit":"tsp","quantity":1},
    {"sku":"CK-CHOC-001","ingredient":"Salt","quantity_unit":"tsp","quantity":0.5},
    {"sku":"CK-SUGAR-001","ingredient":"All-purpose flour","quantity_unit":"cups","quantity":3},
    {"sku":"CK-SUGAR-001","ingredient":"Butter","quantity_unit":"cups","quantity":1},
    {"sku":"CK-SUGAR-001","ingredient":"White sugar","quantity_unit":"cups","quantity":1.5},
    {"sku":"CK-SUGAR-001","ingredient":"Eggs","quantity_unit":"count","quantity":2},
    {"sku":"CK-SUGAR-001","ingredient":"Vanilla extract","quantity_unit":"tsp","quantity":2},
    {"sku":"CK-SUGAR-001","ingredient":"Baking powder","quantity_unit":"tsp","quantity":1},
    {"sku":"CK-SUGAR-001","ingredient":"Salt","quantity_unit":"tsp","quantity":0.25},
    {"sku":"CK-NUTMARB-001","ingredient":"All-purpose flour","quantity_unit":"cups","quantity":2.5},
    {"sku":"CK-NUTMARB-001","ingredient":"Butter","quantity_unit":"cups","quantity":1},
    {"sku":"CK-NUTMARB-001","ingredient":"Brown sugar","quantity_unit":"cups","quantity":1.25},
    {"sku":"CK-NUTMARB-001","ingredient":"Eggs","quantity_unit":"count","quantity":2},
    {"sku":"CK-NUTMARB-001","ingredient":"Chocolate chips","quantity_unit":"cups","quantity":1.5},
    {"sku":"CK-NUTMARB-001","ingredient":"Nutella","quantity_unit":"cups","quantity":0.75},
    {"sku":"CK-NUTMARB-001","ingredient":"Baking soda","quantity_unit":"tsp","quantity":1},
    {"sku":"CK-NUTMARB-001","ingredient":"Salt","quantity_unit":"tsp","quantity":0.5},
    {"sku":"ADD-NUTELLA","ingredient":"Nutella","quantity_unit":"cups","quantity":0.25},
    {"sku":"ADD-PB","ingredient":"Crunchy peanut butter","quantity_unit":"cups","quantity":0.25},
    {"sku":"ADD-SEASALT","ingredient":"Sea salt","quantity_unit":"tsp","quantity":0.1},
]

recipes_df = pd.DataFrame(recipes_data)
recipes_df.to_csv(output_path + "recipes.csv", index=False)

# ----------------------
# Shopify Orders
# ----------------------

# To CSV titled shopify_orders.csv
# Features: order_id,date,product_sku,quantity,add_on_sku,total_price

order_list = [
    {"order_id":"1001","date":"2024-01-02","sku":"CK-CHOC-001","quantity":1,"add_on_sku":"ADD-NUTELLA","total_price":32.00},
    {"order_id":"1002","date":"2024-01-02","sku":"CK-SUGAR-001","quantity":2,"add_on_sku":"","total_price":56.00},
    {"order_id":"1003","date":"2024-01-03","sku":"CK-NUTMARB-001","quantity":1,"add_on_sku":"ADD-SEASALT","total_price":28.00},
    {"order_id":"1004","date":"2024-01-03","sku":"CK-CHOC-001","quantity":3,"add_on_sku":"ADD-PB","total_price":96.00},
    {"order_id":"1005","date":"2024-01-03","sku":"CK-SUGAR-001","quantity":1,"add_on_sku":"ADD-SEASALT","total_price":28.00},
    {"order_id":"1006","date":"2024-01-04","sku":"CK-CHOC-001","quantity":2,"add_on_sku":"","total_price":56.00},
    {"order_id":"1007","date":"2024-01-04","sku":"CK-NUTMARB-001","quantity":1,"add_on_sku":"ADD-NUTELLA","total_price":32.00},
    {"order_id":"1008","date":"2024-01-05","sku":"CK-SUGAR-001","quantity":4,"add_on_sku":"ADD-SEASALT","total_price":112.00},
    {"order_id":"1009","date":"2024-01-05","sku":"CK-CHOC-001","quantity":2,"add_on_sku":"ADD-PB","total_price":64.00},
    {"order_id":"1010","date":"2024-01-06","sku":"CK-NUTMARB-001","quantity":3,"add_on_sku":"","total_price":84.00},
    {"order_id":"1011","date":"2024-01-06","sku":"CK-SUGAR-001","quantity":1,"add_on_sku":"ADD-NUTELLA","total_price":32.00},
    {"order_id":"1012","date":"2024-01-06","sku":"CK-CHOC-001","quantity":2,"add_on_sku":"ADD-SEASALT","total_price":56.00},
    {"order_id":"1013","date":"2024-01-07","sku":"CK-SUGAR-001","quantity":2,"add_on_sku":"","total_price":56.00},
    {"order_id":"1014","date":"2024-01-07","sku":"CK-NUTMARB-001","quantity":1,"add_on_sku":"","total_price":28.00},
    {"order_id":"1015","date":"2024-01-07","sku":"CK-CHOC-001","quantity":5,"add_on_sku":"ADD-SEASALT","total_price":140.00},
    {"order_id":"1016","date":"2024-01-08","sku":"CK-CHOC-001","quantity":2,"add_on_sku":"ADD-PB","total_price":64.00},
    {"order_id":"1017","date":"2024-01-08","sku":"CK-SUGAR-001","quantity":1,"add_on_sku":"ADD-SEASALT","total_price":28.00},
    {"order_id":"1018","date":"2024-01-08","sku":"CK-NUTMARB-001","quantity":2,"add_on_sku":"ADD-NUTELLA","total_price":64.00},
    {"order_id":"1019","date":"2024-01-09","sku":"CK-NUTMARB-001","quantity":1,"add_on_sku":"","total_price":28.00},
    {"order_id":"1020","date":"2024-01-09","sku":"CK-SUGAR-001","quantity":3,"add_on_sku":"ADD-SEASALT","total_price":84.00},
    {"order_id":"1021","date":"2024-01-10","sku":"CK-CHOC-001","quantity":1,"add_on_sku":"","total_price":28.00},
    {"order_id":"1022","date":"2024-01-10","sku":"CK-CHOC-001","quantity":2,"add_on_sku":"ADD-NUTELLA","total_price":64.00},
    {"order_id":"1023","date":"2024-01-10","sku":"CK-SUGAR-001","quantity":2,"add_on_sku":"","total_price":56.00},
    {"order_id":"1024","date":"2024-01-11","sku":"CK-NUTMARB-001","quantity":3,"add_on_sku":"ADD-SEASALT","total_price":84.00},
    {"order_id":"1025","date":"2024-01-11","sku":"CK-CHOC-001","quantity":1,"add_on_sku":"ADD-PB","total_price":32.00},
    {"order_id":"1026","date":"2024-01-11","sku":"CK-SUGAR-001","quantity":4,"add_on_sku":"","total_price":112.00},
    {"order_id":"1027","date":"2024-01-12","sku":"CK-NUTMARB-001","quantity":2,"add_on_sku":"ADD-NUTELLA","total_price":64.00},
    {"order_id":"1028","date":"2024-01-12","sku":"CK-SUGAR-001","quantity":1,"add_on_sku":"","total_price":28.00},
    {"order_id":"1029","date":"2024-01-12","sku":"CK-CHOC-001","quantity":1,"add_on_sku":"","total_price":28.00},
    {"order_id":"1030","date":"2024-01-13","sku":"CK-SUGAR-001","quantity":2,"add_on_sku":"ADD-SEASALT","total_price":56.00},
    {"order_id":"1031","date":"2024-01-13","sku":"CK-CHOC-001","quantity":3,"add_on_sku":"","total_price":84.00},
    {"order_id":"1032","date":"2024-01-14","sku":"CK-NUTMARB-001","quantity":1,"add_on_sku":"ADD-SEASALT","total_price":28.00},
    {"order_id":"1033","date":"2024-01-14","sku":"CK-SUGAR-001","quantity":1,"add_on_sku":"","total_price":28.00},
    {"order_id":"1034","date":"2024-01-14","sku":"CK-CHOC-001","quantity":4,"add_on_sku":"ADD-NUTELLA","total_price":128.00},
    {"order_id":"1035","date":"2024-01-15","sku":"CK-SUGAR-001","quantity":3,"add_on_sku":"","total_price":84.00},
    {"order_id":"1036","date":"2024-01-15","sku":"CK-NUTMARB-001","quantity":2,"add_on_sku":"ADD-PB","total_price":64.00},
    {"order_id":"1037","date":"2024-01-15","sku":"CK-CHOC-001","quantity":1,"add_on_sku":"","total_price":28.00},
    {"order_id":"1038","date":"2024-01-16","sku":"CK-CHOC-001","quantity":2,"add_on_sku":"ADD-SEASALT","total_price":56.00},
    {"order_id":"1039","date":"2024-01-16","sku":"CK-NUTMARB-001","quantity":1,"add_on_sku":"","total_price":28.00},
    {"order_id":"1040","date":"2024-01-16","sku":"CK-SUGAR-001","quantity":4,"add_on_sku":"ADD-NUTELLA","total_price":128.00},
    {"order_id":"1041","date":"2024-01-17","sku":"CK-CHOC-001","quantity":3,"add_on_sku":"","total_price":84.00},
    {"order_id":"1042","date":"2024-01-17","sku":"CK-NUTMARB-001","quantity":1,"add_on_sku":"ADD-SEASALT","total_price":28.00},
    {"order_id":"1043","date":"2024-01-18","sku":"CK-SUGAR-001","quantity":1,"add_on_sku":"","total_price":28.00},
    {"order_id":"1044","date":"2024-01-18","sku":"CK-CHOC-001","quantity":2,"add_on_sku":"ADD-NUTELLA","total_price":64.00},
    {"order_id":"1045","date":"2024-01-18","sku":"CK-NUTMARB-001","quantity":3,"add_on_sku":"","total_price":84.00},
    {"order_id":"1046","date":"2024-01-19","sku":"CK-NUTMARB-001","quantity":2,"add_on_sku":"ADD-SEASALT","total_price":56.00},
    {"order_id":"1047","date":"2024-01-19","sku":"CK-SUGAR-001","quantity":1,"add_on_sku":"ADD-NUTELLA","total_price":32.00},
    {"order_id":"1048","date":"2024-01-20","sku":"CK-CHOC-001","quantity":4,"add_on_sku":"","total_price":112.00},
    {"order_id":"1049","date":"2024-01-20","sku":"CK-SUGAR-001","quantity":2,"add_on_sku":"ADD-SEASALT","total_price":56.00},
    {"order_id":"1050","date":"2024-01-20","sku":"CK-NUTMARB-001","quantity":1,"add_on_sku":"","total_price":28.00},
    {"order_id":"1051","date":"2024-01-21","sku":"CK-CHOC-001","quantity":1,"add_on_sku":"","total_price":28.00},
    {"order_id":"1052","date":"2024-01-21","sku":"CK-SUGAR-001","quantity":3,"add_on_sku":"ADD-NUTELLA","total_price":96.00},
    {"order_id":"1053","date":"2024-01-22","sku":"CK-NUTMARB-001","quantity":2,"add_on_sku":"ADD-PB","total_price":64.00},
    {"order_id":"1054","date":"2024-01-22","sku":"CK-CHOC-001","quantity":3,"add_on_sku":"ADD-SEASALT","total_price":84.00},
    {"order_id":"1055","date":"2024-01-23","sku":"CK-SUGAR-001","quantity":1,"add_on_sku":"","total_price":28.00},
    {"order_id":"1056","date":"2024-01-23","sku":"CK-NUTMARB-001","quantity":1,"add_on_sku":"","total_price":28.00},
    {"order_id":"1057","date":"2024-01-23","sku":"CK-CHOC-001","quantity":5,"add_on_sku":"ADD-NUTELLA","total_price":160.00},
    {"order_id":"1058","date":"2024-01-24","sku":"CK-NUTMARB-001","quantity":2,"add_on_sku":"","total_price":56.00},
    {"order_id":"1059","date":"2024-01-24","sku":"CK-SUGAR-001","quantity":4,"add_on_sku":"ADD-SEASALT","total_price":112.00},
    {"order_id":"1060","date":"2024-01-25","sku":"CK-CHOC-001","quantity":1,"add_on_sku":"","total_price":28.00},
    {"order_id":"1061","date":"2024-01-25","sku":"CK-SUGAR-001","quantity":3,"add_on_sku":"ADD-PB","total_price":96.00},
    {"order_id":"1062","date":"2024-01-26","sku":"CK-NUTMARB-001","quantity":3,"add_on_sku":"ADD-NUTELLA","total_price":96.00},
    {"order_id":"1063","date":"2024-01-26","sku":"CK-CHOC-001","quantity":2,"add_on_sku":"","total_price":56.00},
    {"order_id":"1064","date":"2024-01-26","sku":"CK-SUGAR-001","quantity":1,"add_on_sku":"","total_price":28.00},
    {"order_id":"1065","date":"2024-01-27","sku":"CK-CHOC-001","quantity":1,"add_on_sku":"ADD-SEASALT","total_price":28.00},
    {"order_id":"1066","date":"2024-01-27","sku":"CK-NUTMARB-001","quantity":2,"add_on_sku":"","total_price":56.00},
    {"order_id":"1067","date":"2024-01-28","sku":"CK-SUGAR-001","quantity":3,"add_on_sku":"ADD-NUTELLA","total_price":96.00},
    {"order_id":"1068","date":"2024-01-28","sku":"CK-CHOC-001","quantity":2,"add_on_sku":"ADD-PB","total_price":64.00},
    {"order_id":"1069","date":"2024-01-29","sku":"CK-NUTMARB-001","quantity":4,"add_on_sku":"","total_price":112.00},
    {"order_id":"1070","date":"2024-01-29","sku":"CK-SUGAR-001","quantity":1,"add_on_sku":"","total_price":28.00},
    {"order_id":"1071","date":"2024-01-29","sku":"CK-CHOC-001","quantity":2,"add_on_sku":"ADD-NUTELLA","total_price":64.00},
    {"order_id":"1072","date":"2024-01-30","sku":"CK-NUTMARB-001","quantity":1,"add_on_sku":"","total_price":28.00},
    {"order_id":"1073","date":"2024-01-30","sku":"CK-SUGAR-001","quantity":2,"add_on_sku":"ADD-SEASALT","total_price":56.00},
    {"order_id":"1074","date":"2024-01-30","sku":"CK-CHOC-001","quantity":3,"add_on_sku":"","total_price":84.00},
    {"order_id":"1075","date":"2024-02-01","sku":"CK-CHOC-001","quantity":1,"add_on_sku":"","total_price":28.00},
    {"order_id":"1076","date":"2024-02-01","sku":"CK-NUTMARB-001","quantity":2,"add_on_sku":"ADD-NUTELLA","total_price":64.00},
    {"order_id":"1077","date":"2024-02-02","sku":"CK-SUGAR-001","quantity":4,"add_on_sku":"","total_price":112.00},
    {"order_id":"1078","date":"2024-02-02","sku":"CK-CHOC-001","quantity":2,"add_on_sku":"","total_price":56.00},
    {"order_id":"1079","date":"2024-02-02","sku":"CK-NUTMARB-001","quantity":1,"add_on_sku":"ADD-SEASALT","total_price":28.00},
    {"order_id":"1080","date":"2024-02-03","sku":"CK-SUGAR-001","quantity":1,"add_on_sku":"","total_price":28.00},
    {"order_id":"1081","date":"2024-02-03","sku":"CK-CHOC-001","quantity":3,"add_on_sku":"ADD-NUTELLA","total_price":96.00},
    {"order_id":"1082","date":"2024-02-04","sku":"CK-NUTMARB-001","quantity":3,"add_on_sku":"","total_price":84.00},
    {"order_id":"1083","date":"2024-02-04","sku":"CK-SUGAR-001","quantity":2,"add_on_sku":"ADD-PB","total_price":64.00},
    {"order_id":"1084","date":"2024-02-05","sku":"CK-CHOC-001","quantity":2,"add_on_sku":"ADD-SEASALT","total_price":56.00},
    {"order_id":"1085","date":"2024-02-05","sku":"CK-NUTMARB-001","quantity":1,"add_on_sku":"","total_price":28.00},
    {"order_id":"1086","date":"2024-02-05","sku":"CK-SUGAR-001","quantity":2,"add_on_sku":"","total_price":56.00},
    {"order_id":"1087","date":"2024-02-06","sku":"CK-CHOC-001","quantity":4,"add_on_sku":"ADD-NUTELLA","total_price":128.00},
    {"order_id":"1088","date":"2024-02-06","sku":"CK-SUGAR-001","quantity":1,"add_on_sku":"ADD-SEASALT","total_price":28.00},
    {"order_id":"1089","date":"2024-02-07","sku":"CK-NUTMARB-001","quantity":2,"add_on_sku":"ADD-PB","total_price":64.00},
    {"order_id":"1090","date":"2024-02-07","sku":"CK-CHOC-001","quantity":3,"add_on_sku":"","total_price":84.00},
    {"order_id":"1091","date":"2024-02-08","sku":"CK-SUGAR-001","quantity":3,"add_on_sku":"ADD-NUTELLA","total_price":96.00},
    {"order_id":"1092","date":"2024-02-08","sku":"CK-NUTMARB-001","quantity":1,"add_on_sku":"","total_price":28.00},
    {"order_id":"1093","date":"2024-02-09","sku":"CK-CHOC-001","quantity":2,"add_on_sku":"ADD-SEASALT","total_price":56.00},
    {"order_id":"1094","date":"2024-02-09","sku":"CK-SUGAR-001","quantity":1,"add_on_sku":"","total_price":28.00},
    {"order_id":"1095","date":"2024-02-09","sku":"CK-NUTMARB-001","quantity":2,"add_on_sku":"ADD-NUTELLA","total_price":64.00},
    {"order_id":"1096","date":"2024-02-10","sku":"CK-SUGAR-001","quantity":4,"add_on_sku":"","total_price":112.00},
    {"order_id":"1097","date":"2024-02-10","sku":"CK-CHOC-001","quantity":1,"add_on_sku":"","total_price":28.00},
    {"order_id":"1098","date":"2024-02-11","sku":"CK-NUTMARB-001","quantity":3,"add_on_sku":"","total_price":84.00},
    {"order_id":"1099","date":"2024-02-11","sku":"CK-SUGAR-001","quantity":2,"add_on_sku":"ADD-SEASALT","total_price":56.00},
    {"order_id":"1100","date":"2024-02-11","sku":"CK-CHOC-001","quantity":2,"add_on_sku":"ADD-NUTELLA","total_price":64.00}
]

orders_df = pd.DataFrame(order_list)
orders_df['date'] = pd.to_datetime(orders_df['date'])  # Convert to datetime
orders_df.to_csv(output_path + "shopify_orders.csv", index=False)