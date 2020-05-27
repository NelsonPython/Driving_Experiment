import mysql.connector
import pandas as pd

db = mysql.connector.connect(
	host = "localhost",
	user = "USERNAME",
	password = "PASSWORD",
	database = "translations"
)

conn = db.cursor()

translations = {'LOOKUP':['tmp1','tmp2','hum','flowers','vegetables','palm trees','startWater1','startWater2','stopWater','co2', 'badAir', 'unknown'],
            'ENGLISH':['the temperature is ',' degrees Farenheit ',' percent humidity','flowers','vegetables','palm trees','I started watering the ','.',' have been watered','the carbon dioxide level is ', 'WARNING!  DANGER! go outside now!','I do not know'],
            'SPANISH':['la temperatura es de',' grados centigrados ',' por ciento de humedad','las flores','las verduras','palmeras','empece a regar','.',' han sido regadas','el nivel de dioxido de carbono es ', 'CUIDADO! PELIGRO! vete ahora', 'no lo se'],
            'CHINESE':['wendu wei sheshi',' du shidu wei ',' bai fen','hua','shucai','zonglu shu','wo kaishi gei','jiao shui','yijing jiao shile', 'eryanghuatan shuiping shi ', 'JING GAO xianzai chufa', 'wo bu zhidao']}

df = pd.DataFrame(translations, columns=['LOOKUP','ENGLISH','SPANISH','CHINESE'])
for idx, row in df.iterrows():
    sql = "insert into lookup (TAG,LANGUAGE,PHRASE) values ('"+row.LOOKUP+"','ENGLISH','"+row.ENGLISH+"')"
    print(sql)
    conn.execute(sql)
    db.commit()
    print(conn.rowcount, " record inserted")


for idx, row in df.iterrows():
    sql = "insert into lookup (TAG,LANGUAGE,PHRASE) values ('"+row.LOOKUP+"','SPANISH','"+row.SPANISH+"')"
    print(sql)
    conn.execute(sql)
    db.commit()
    print(conn.rowcount, " record inserted")


for idx, row in df.iterrows():
    sql = "insert into lookup (TAG,LANGUAGE,PHRASE) values ('"+row.LOOKUP+"','CHINESE','"+row.CHINESE+"')"
    print(sql)
    conn.execute(sql)
    db.commit()
    print(conn.rowcount, " record inserted")
