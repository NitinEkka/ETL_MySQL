import mysql.connector

# ESTABLISHING CONNECTION

my_db = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    passwd='1234',
    database='etldb',
)

# CREATING CURSOR FOR EXECUTING SQL QUERIES

mycursor = my_db.cursor()
mycursor.execute('CREATE IF NOT EXIST DATABASE ETLDB')
mycursor.execute('CREATE TABLE Customer(Customer_id INT Primary Key,Age INT)')
mycursor.execute('CREATE TABLE Sales(Sales_id INT NOT NULL Primary Key,Customer_id INT Foreign Key Reference Customer(Customer_id))')
mycursor.execute('CREATE TABLE Items(Item_id INT Primary Key NOT NULL,Item_name VARCHAR(45) NOT NULL)')
mycursor.execute('CREATE TABLE Orders(Order_id INT Primary Key NOT NULL,Sales_id int unique Foreign Key Reference Sales(Sales_id),Item_id INT unique Foreign Key Reference Items(Item_id), Quantity INT)')

# FORMULA TEMPLATES TO ADD VALUES IN DIFFERENT TABLES

mysqlformula_adding_customer = "INSERT INTO Customer (Customer_id, Age) VALUES (%s, %s)"
mysqlformula_adding_Sales = "INSERT INTO Sales (Sales_id, Customer_id) VALUES (%s, %s)"
mysqlformula_adding_Items = "INSERT INTO Items (Item_id, Item_name) VALUES (%s, %s)"
mysqlformula_adding_Orders = "INSERT INTO Orders (Order_id, Sales_id, Item_id, Quantity) VALUES (%s, %s, %s, %s)"

# POPULATING CUSTOMER TABLE

user_ipt_str_customer = str(input("Enter The Values for Customer : "))
user_customer_lst = user_ipt_str_customer.split()
use_tuple_customer = tuple(user_customer_lst)
mycursor.execute(mysqlformula_adding_customer,use_tuple_customer)

# POPULATING SALES TABLE

user_ipt_str_Sales = str(input("Enter The Values for Sales : "))
user_Sales_lst = user_ipt_str_Sales.split()
use_tuple_Sales = tuple(user_Sales_lst)
mycursor.execute(mysqlformula_adding_Sales,use_tuple_Sales)

# POPULATING ITEMS TABLE

user_ipt_str_Items = str(input("Enter The Values for Items : "))
user_Items_lst = user_ipt_str_Items.split()
use_tuple_Items = tuple(user_Items_lst)
mycursor.execute(mysqlformula_adding_Items,use_tuple_Items)

# POPULATING ORDERS TABLE

user_ipt_str_Orders = str(input("Enter The Values for Orders : "))
user_Orders_lst = user_ipt_str_Orders.split()
use_tuple_Orders = tuple(user_Orders_lst)
mycursor.execute(mysqlformula_adding_Orders,use_tuple_Orders)

# DELETING VALUES IN CUSTOMER TABLE

mysqlformula_deleting_Customer = "DELETE from Customer Where Customer_id = %s"
info_del_str_customer = str(input("Enter the Customer_id you want to delete : "))
mycursor.execute(mysqlformula_deleting_Customer, info_del_str_customer)

# DELETING VALUES IN SALES TABLE

mysqlformula_deleting_Sales = "DELETE from Sales Where Sales_id = %s"
info_del_str_Sales = str(input("Enter the Sales_id you want to delete : "))
mycursor.execute(mysqlformula_deleting_Sales, info_del_str_Sales)

# DELETING VALUES IN ORDERS TABLE

mysqlformula_deleting_Orders = "DELETE from Orders Where Order_id = %s"
info_del_str_Orders = str(input("Enter the Order_id you want to delete : "))
mycursor.execute(mysqlformula_deleting_Orders, info_del_str_Orders)

# DELETING VALUES IN ITEMS TABLE

mysqlformula_deleting_Items = "DELETE from Items Where Item_id = %s"
info_del_str_Items = str(input("Enter the Item_id you want to delete : "))
mycursor.execute(mysqlformula_deleting_Items, info_del_str_Items)

# EXECUTING FINAL SELECT QUERY

mycursor.execute('SELECT C.Customer_id , C.Age , O.Item_id , O.Quantity , (Select Max(O.Quantity) FROM (VALUES ([O.Item_id])) AS QuantityTbl(Quantity)) as MaxQuantity FROM Customer C, Sales S, Orders O where S.Customer_id = C.Customer_id AND O.Sales_id = S.Sales_id GROUP BY O.Item_id INTO OUTFILE '/var/lib/mysql-files/etl.csv' FIELDS TERMINATED BY ';' ENCLOSED BY '"' LINES TERMINATED BY '\n'')
