<h1>Public Radio</h1>

Public Radio broadcasts messages in three languages:  English, Spanish, and Chinese.  During a demo, this allows humans to understand conversations between devices.  In the real world, autonomous vehicles may not speak aloud when communicating with each other because sending and receiving messages is faster and more accurate.  Public Radio uses the translations database.  Open MySQL and create the translations database

```
CREATE DATABASE translations;
```

Create the lookup table

```
CREATE TABLE lookup (
lookup_ID int NOT NULL PRIMARY KEY AUTO_INCREMENT,
tag varchar(20),
language varchar(20),
phrase varchar(100));
```
Use the loadLookup.py script in the DB folder to begin loading translations


<h3>Running Public Radio</h3>
Go to your home directory and make a folder called /PublicRadio.  Copy roadTripTalks.py, send_2_yellow_wheels.py, send_2_AstroPiQuake.py, and quake.sh


<h3>Creating charts and graphs</h3>
Go to your /PublicRadio folder and copy ??? graphs


"yellow_drive        "," ENGLISH  "," I am driving                                          ","
"yellow_lost         "," ENGLISH  "," I got lost                                            ","
"yellow_drive        "," SPANISH  "," el auto amarillo esta conduciendo                     ","
"yellow_lost         "," SPANISH  "," el auto amarillo esta perdido                         ","
"yellow_drive        "," CHINESE  "," huang se qi che jia                                   ","
"yellow_lost         "," CHINESE  "," huang che dui le                                      ","
"yellow_depart       "," ENGLISH  "," I am leaving                                          ","
"yellow_arrive       "," ENGLISH  "," I arrived                                             ","
"yellow_refuel       "," ENGLISH  "," I charged batteries for ; seconds                     ","
"yellow_scheduleFuel "," ENGLISH  "," I will charge again in ; seconds                      ","
"yellow_depart       "," SPANISH  "," el amarillo se va                                     ","
"yellow_arrive       "," SPANISH  "," llego el amarillo                                     ","
"yellow_refuel       "," SPANISH  "," el amarillo cargo sus baterias por ; segundos         ","
"yellow_scheduleFuel "," SPANISH  "," el amarillo va a cargar en ; segundos                 ","
"yellow_depart       "," CHINESE  ","  ; huang che chu                                      ","
"yellow_arrive       "," CHINESE  ","  ; huang che dao le                                   ","
"yellow_refuel       "," CHINESE  "," gei huangse qiche dianchi chongdianle ; maio zhong    ","
"yellow_scheduleFuel "," CHINESE  "," zai ; miao jiang wei huangse qiche dianchi chongdian  ","
"quake               "," ENGLISH  "," Earthquake. Drop, cover, hold on                      ","
"quake               "," SPANISH  "," Terremoto. Agacharse, cubrirse, agarrarse             ","
"quake               "," CHINESE  "," di zhen                                               ","

