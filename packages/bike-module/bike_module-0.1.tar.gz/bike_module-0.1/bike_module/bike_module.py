from flask import Flask, request, jsonify
import sqlite3

def compare_with_odo(bike_one_milage,bike_two_milage,common_odo,gas_price):
     bike_one_cost=(common_odo/bike_one_milage)*gas_price
     bike_two_cost=(common_odo/bike_two_milage)*gas_price
     return [bike_one_cost,bike_two_cost]

       
class bikedata():
    
    def add_bike_details():
        try:
            data = request.get_json()
            brand= data['brand'].capitalize()
            model= data['model'].capitalize()
            year= data['year']
            category= data['category'].capitalize()
            price= data['price']
            capacity= data['capacity']
            power= data['power'].capitalize()
            torque= data['torque'].capitalize()
            milage= data['milage']
            height= data['height']
            weight= data['weight']
            abs= data['abs'].capitalize()
            status="ACTIVE"

            connectdb=sqlite3.connect('BikeLelo.db')
            cursor=connectdb.cursor()

            if (not brand or not model or not year or not category or not 
                price or not capacity or not power or not torque or not
                milage or not height or not weight or not height or not abs) :
                return jsonify({"message":" All fields are Mandatory"}),400
            
            cursor.execute("""INSERT INTO BikeData (BRAND,MODEL,YEAR,CATEGORY,
                        PRICE,CAPACITY,POWER,TORQUE,MILAGE,HEIGHT,WEIGHT,ABS,STATUS)
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (brand,model,year,category,price,capacity,power,torque,
                            milage,height,weight,abs,status))
            
            connectdb.commit()
            connectdb.close()
        except sqlite3.Error as e:
            return jsonify({"error": f"Database error: {str(e)}"}), 500
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
    def view_all_bike_details():
        try:
            connectdb=sqlite3.connect('BikeLelo.db')
            cursor=connectdb.cursor()
            cursor.execute("SELECT * FROM BikeData ")
            all_bike_data=cursor.fetchall() #[[]]
            connectdb.close()
            table_columns=["BIKEID","BRAND","MODEL","YEAR","NAME","CATEGORY",
                        "PRICE","CAPACITY","POWER","TORQUE","MILAGE",
                        "HEIGHT","WEIGHT","ABS","STATUS"]
            data_list=list()
            for item in all_bike_data:
                data_list.append(dict(zip(table_columns,item))) #[{}]
            return jsonify(data_list), 200
        except sqlite3.Error as e:
            return jsonify({"error": f"Database error: {str(e)}"}), 500
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    def view_bike_details(bike_id):
        try:
            connectdb=sqlite3.connect('BikeLelo.db')
            cursor=connectdb.cursor()

            cursor.execute("SELECT BIKEID FROM BikeData")
            bike_id_ll=cursor.fetchall()
            bike_ids=list()
            for row in bike_id_ll:
                bike_ids.append(row[0])
            if not bike_id in bike_ids:
                return jsonify(f" Bike ID {bike_id} is not in database")
            else:
                cursor.execute("SELECT * FROM BikeData  WHERE BIKEID =? ",(bike_id,))
                bike_data=cursor.fetchall()
                table_columns=["BIKEID","BRAND","MODEL","YEAR","NAME","CATEGORY",
                            "PRICE","CAPACITY","POWER","TORQUE","MILAGE",
                            "HEIGHT","WEIGHT","ABS","STATUS"]
                connectdb.close()
                data_list=list()
                for item in bike_data:
                    data_list.append(dict(zip(table_columns,item)))
                return jsonify(data_list), 200
            
        except sqlite3.Error as e:
            return jsonify({"error": f"Database error: {str(e)}"}), 500
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500


    def deactive_bike_data():
        try:
            data = request.get_json()
            bike_id=data["bike_id"]
            status="INACTIVE"

            connectdb=sqlite3.connect('BikeLelo.db')
            cursor=connectdb.cursor()

            cursor.execute("SELECT BIKEID FROM BikeData")
            bike_id_ll=cursor.fetchall()
            bike_ids=list()
            for row in bike_id_ll:
                bike_ids.append(row[0])
            if not bike_id in bike_ids:
                    return jsonify(f" Bike ID {bike_id} is not in database")
            else:
                cursor.execute("UPDATE BikeData SET STATUS =? WHERE BIKEID =?",
                        (status,bike_id))
                connectdb.commit()
            connectdb.close()
        except sqlite3.Error as e:
            return jsonify({"error": f"Database error: {str(e)}"}), 500
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    def delete_bike_data():
        try:
            data = request.get_json()
            bike_id=data["bike_id"]

            connectdb=sqlite3.connect('BikeLelo.db')
            cursor=connectdb.cursor()

            cursor.execute("SELECT BIKEID FROM BikeData")
            bike_id_ll=cursor.fetchall()
            bike_ids=list()
            for row in bike_id_ll:
                bike_ids.append(row[0])
            if not bike_id in bike_ids:
                    return jsonify(f" Bike ID {bike_id} is not in database")
            else:
                cursor.execute("DELETE  FROM BikeData WHERE BIKEID =?",(bike_id,))
                connectdb.commit()
            connectdb.close() 
        except sqlite3.Error as e:
            return jsonify({"error": f"Database error: {str(e)}"}), 500
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500


class customer_need():
     
    def filter_bike_data():
        try:
            user_need = request.get_json()
            if not user_need:
                return jsonify({"error": "Invalid JSON data"}), 400
            
            connectdb = None
            try:
                connectdb = sqlite3.connect('BikeLelo.db')
                cursor = connectdb.cursor()
                cursor.execute("SELECT * FROM BikeData")
                all_bike_data = cursor.fetchall()
            except sqlite3.Error as e:
                return jsonify({"error": f"Database error: {str(e)}"}), 500
            finally:
                if connectdb:
                    connectdb.close()

            table_columns = ["BIKEID", "BRAND", "MODEL", "YEAR", "NAME", "CATEGORY", "PRICE", "CAPACITY", "POWER", "TORQUE", "MILAGE", "HEIGHT", "WEIGHT", "ABS", "STATUS"]

            # Convert the data from list of lists to list of dictionaries
            data_list = [dict(zip(table_columns, item)) for item in all_bike_data]
            
            price_list=list()
            if not "PRICE" in user_need.keys():
                filtered_data = [record for record in data_list if all(record.get(prop) == value for prop, value in user_need.items())]
                return jsonify(filtered_data), 200
            else:
                needed_price=user_need["PRICE"]
                bike_list = [record for record in data_list if record.get("PRICE") <= needed_price]
                user_need.pop("PRICE")
                filtered_data = [record for record in bike_list if all(record.get(prop) == value for prop, value in user_need.items())]
                return jsonify(filtered_data), 200
        
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    
   
    
    def compare_bike():
        try:
            compare_bike = request.get_json()
            bike_one = compare_bike["bike_one_id"]
            bike_two = compare_bike["bike_two_id"]
            com_type = compare_bike['compare_type']
            common_odo = compare_bike['common_odo']
            gas_price = compare_bike['gas_price']

            connectdb = sqlite3.connect('BikeLelo.db')
            curser = connectdb.cursor()

            curser.execute("SELECT BIKEID FROM BikeData")
            bike_id_ll=curser.fetchall()
            bike_ids=list()
            for row in bike_id_ll:
                bike_ids.append(row[0])


            if not bike_one in bike_ids:
                return jsonify(f" Bike ID {bike_one} is not in database")
            elif not bike_two in bike_ids:
                return jsonify(f" Bike ID {bike_two} is not in database")
            else:
                if common_odo==0:
                    return jsonify("Common odo cannot be 0")
                if gas_price==0:
                    return jsonify("gas price  cannot be 0")
                else:
                    curser.execute("SELECT * FROM BikeData WHERE BIKEID=?", (bike_one,))
                    bike_one_data = curser.fetchone()
                    [bike_one_milage, bike_one_price, bike_one_name] = [bike_one_data[10], bike_one_data[6], bike_one_data[4]]

                    curser.execute("SELECT * FROM BikeData WHERE BIKEID=?", (bike_two,))
                    bike_two_data = curser.fetchone()
                    [bike_two_milage, bike_two_price, bike_two_name] = [bike_two_data[10], bike_two_data[6], bike_two_data[4]]

                    if com_type == "odo":
                        com_result = compare_with_odo(bike_one_milage, bike_two_milage, common_odo, gas_price)
                        result = f"""The gas cost to run {common_odo} km for {bike_one_name} is {com_result[0]} and for {bike_two_name} is {com_result[1]} and total cost will be {com_result[0] + bike_one_price} for {bike_one_name} and {com_result[1] + bike_two_price} for {bike_two_name}"""
                        return jsonify(result), 200
                    else:
                        return jsonify({"error": "Invalid comparison type"}), 400
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

