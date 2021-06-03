import mysql.connector, json, sys
db = mysql.connector.connect(host="localhost",user="bubble",passwd="bubble")
file=sys.argv[1]
with open(file) as json_file :
    parser = json.load(json_file)
ID=str(parser["device"])
state=str(parser["state"])
print("Connection ID:", db.connection_id)
#Connection established
cursor = db.cursor()
cursor.execute("use bubble")

try:
	#Device not found.
	sql = "INSERT INTO device_state (device_id, state) VALUES (%s, %s)"
	val = (ID, state)
	cursor.execute(sql, val)
	print("INSERT "+ID+" "+state)

except:
	try:
		#Device exists.
		sql = "UPDATE device_state SET state = %s WHERE device_id = %s"
		val = (state, ID)
		cursor.execute(sql, val)
		print("UPDATED "+ID+" "+state)
	except:
		print("ERROR "+ID+" "+state)
#Commit changes
db.commit()
cursor.close()
db.close()
