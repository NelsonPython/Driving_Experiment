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
Use the loadLookup.py script in the DB folder to begin loading translations.  Insert translations using these commands.  Make sure each tag has a translation.  Use any language you prefer.

```
INSERT INTO lookup (tag,language,phrase) VALUES ("yellow_drive","ENGLISH","I am driving");
INSERT INTO lookup (tag,language,phrase) VALUES ("yellow_lost","ENGLISH","I got lost");                                   
INSERT INTO lookup (tag,language,phrase) VALUES ("yellow_drive","SPANISH","el auto amarillo esta conduciendo");
INSERT INTO lookup (tag,language,phrase) VALUES ("yellow_lost","SPANISH","el auto amarillo esta perdido");            
INSERT INTO lookup (tag,language,phrase) VALUES ("yellow_drive","CHINESE","huang se qi che jia");                        
INSERT INTO lookup (tag,language,phrase) VALUES ("yellow_lost","CHINESE","huang che dui le");                                
INSERT INTO lookup (tag,language,phrase) VALUES ("yellow_depart","ENGLISH","I am leaving");                                      
INSERT INTO lookup (tag,language,phrase) VALUES ("yellow_arrive","ENGLISH","I arrived");                                        
INSERT INTO lookup (tag,language,phrase) VALUES ("yellow_refuel","ENGLISH","I charged batteries for ; seconds");
INSERT INTO lookup (tag,language,phrase) VALUES ("yellow_scheduleFuel","ENGLISH","I will charge again in ; seconds");                   
INSERT INTO lookup (tag,language,phrase) VALUES ("yellow_depart","SPANISH","el amarillo se va");
INSERT INTO lookup (tag,language,phrase) VALUES ("yellow_arrive","SPANISH","llego el amarillo");                                   
INSERT INTO lookup (tag,language,phrase) VALUES ("yellow_refuel","SPANISH","el amarillo cargo sus baterias por ; segundos");
INSERT INTO lookup (tag,language,phrase) VALUES ("yellow_scheduleFuel","SPANISH","el amarillo va a cargar en ; segundos");          
INSERT INTO lookup (tag,language,phrase) VALUES ("yellow_depart","CHINESE"," ; huang che chu");
INSERT INTO lookup (tag,language,phrase) VALUES ("yellow_arrive","CHINESE"," ; huang che dao le");                                   
INSERT INTO lookup (tag,language,phrase) VALUES ("yellow_refuel","CHINESE","gei huangse qiche dianchi chongdianle ; maio zhong");
INSERT INTO lookup (tag,language,phrase) VALUES ("yellow_scheduleFuel","CHINESE","zai ; miao jiang wei huangse qiche dianchi chongdian");
INSERT INTO lookup (tag,language,phrase) VALUES ("quake","ENGLISH","Earthquake. Drop, cover, hold on");                      
INSERT INTO lookup (tag,language,phrase) VALUES ("quake","SPANISH","Terremoto. Agacharse, cubrirse, agarrarse");             
INSERT INTO lookup (tag,language,phrase) VALUES ("quake","CHINESE","di zhen");
```

<h3>Running Public Radio</h3>
Go to your home directory and make a folder called /PublicRadio.  Copy roadTripTalks.py, send_2_yellow_wheels.py, send_2_AstroPiQuake.py, and quake.sh


<h3>Creating charts and graphs</h3>
Go to your /PublicRadio folder and copy ??? graphs

