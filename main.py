import pyodbc
import configparser
import sys
import time


def main():
    json_configuration = get_configuration_file()
    delete_order_id_user_input(json_configuration)


def delete_order_id_user_input(json_configuration):
    order_id_to_delete = input(f"Enter one order id/number to be deleted from database:")

    if len(order_id_to_delete) == 0:
        print(f"Error: Empty input found! Please try again.")
    else:
        if order_id_to_delete.isdigit():
            print(f"Status: Deleting {order_id_to_delete} from database {json_configuration['database_name']}.")
            delete_order_id_into_database(order_id_to_delete, json_configuration)
                  
    elif order_id_to_delete.endswith(".txt"):
            print(f"File .txt found for {order_id_to_delete}")
            order_id_to_delete_in_file = open(order_id_to_delete, "r")
            order_id_contents = order_id_to_delete_in_file.read().replace("\n", "','")

            if len(order_id_contents) > 0:
                delete_order_id_into_database(order_id_contents, json_configuration)
                  
        else:
            print(f"Error: Input {order_id_to_delete} is not a number! Please try again!")


def delete_order_id_into_database(order_id_to_delete, json_configuration):
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=' + json_configuration['server_name'] + ';'
                          'Database=' + json_configuration['database_name'] + ';'
                          'UID=' + json_configuration['user_id'] + ';'
                          'PWD=' + json_configuration['database_password'] + ';'
                          "Trusted_Connection=No")
    cursor = conn.cursor()

    sql_delete_query_1 = "DELETE FROM [dbo].[OrderStatus] where OrderID in('" + order_id_to_delete + "')"
    sql_delete_query_2 = "DELETE FROM [dbo].[NormalRemarks] where OrgOrderID in('" + order_id_to_delete + "')"
    sql_delete_query_3 = "DELETE FROM [dbo].[NormalOrders] where OrgOrderID in('" + order_id_to_delete + "')"
    sql_delete_query_4 = "DELETE FROM [dbo].[Articles] where OrgOrderID in('" + order_id_to_delete + "')"

    print(f"Status: Deleting {order_id_to_delete} from "
          f"[OrderStatus], "
          f"[NormalRemarks], "
          f"[NormalOrders] and [Articles].")

    cursor.execute(sql_delete_query_1)
    cursor.execute(sql_delete_query_2)
    cursor.execute(sql_delete_query_3)
    cursor.execute(sql_delete_query_4)
    cursor.commit()

    print(f"Status: Please check again since tool had successfully deleted {order_id_to_delete}.")


def get_configuration_file():
    config = configparser.ConfigParser()
    json_configuration = {}
    # for sandbox setup(no executable!)
    # configuration_file = sys.path[0] + '\configurationFile.ini'

    # for live setup(with executable already!)
    # do not forget to rename main.exe to DeleteOrderFromProHandlerTool.exe
    configuration_file = sys.executable.replace("DeleteOrderFromProHandlerTool.exe", "configurationFile.ini")

    config.read(configuration_file)
    database_settings = config["DATABASE"]

    json_configuration['server_name'] = database_settings['server_name']
    json_configuration['database_name'] = database_settings['database_name']
    json_configuration['user_id'] = database_settings['user_id']
    json_configuration['database_password'] = database_settings['database_password']

    return json_configuration


main()
time.sleep(10)
