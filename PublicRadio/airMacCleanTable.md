<h1>Creating the Air MacClean table</h1>

CO2 and TVOC data can be saved in a database table.  This simple example shows how to load all the data.  In the real-world, data will be curated.  Use a database named, ai_lab_data.  If you have not created this database, then create it.

```
CREATE DATABASE ai_lab_data;
```

Use the ai_lab_data database

```
mysql> use ai_lab_data;
Database changed
```

Create the AirMacClean table.  Make sure the columns are arranged in the exact same order of the csv file containing data to be loaded.  Do not add a primary key

```
create table AirMacClean (
CO2 float(5,1),
TVOC float(5,1),
device_name varchar(11),
timestamp datetime);

mysql> show columns in AirMacClean;
+-------------+-------------+------+-----+---------+-------+
| Field       | Type        | Null | Key | Default | Extra |
+-------------+-------------+------+-----+---------+-------+
| CO2         | float(5,1)  | YES  |     | NULL    |       |
| TVOC        | float(5,1)  | YES  |     | NULL    |       |
| device_name | varchar(11) | YES  |     | NULL    |       |
| timestamp   | datetime    | YES  |     | NULL    |       |
+-------------+-------------+------+-----+---------+-------+
4 rows in set (0.00 sec)

```

Copy the AirMacClean.csv file into the folder with permissions to load data.  You can find this folder by showing variables.  Otherwise, you get an error similar to:  ERROR 1290 (HY000): The MySQL server is running with the --secure-file-priv option so it cannot execute this statement

```
mysql> mysql> show variables like "secure_file_priv";
+------------------+-----------------------+
| Variable_name    | Value                 |
+------------------+-----------------------+
| secure_file_priv | /var/lib/mysql-files/ |
+------------------+-----------------------+
1 row in set (0.00 sec)
```

Load the data

```
mysql> load data infile '/var/lib/mysql-files/AirMacClean.csv' into table AirMacClean fields terminated by ',' ignore 1 lines;
Query OK, 135 rows affected (0.02 sec)
Records: 135  Deleted: 0  Skipped: 0  Warnings: 0
```

Add a primary key field

```
mysql> alter table AirMacClean add air_ID int not null primary key auto_increment;
uery OK, 0 rows affected (0.04 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> show columns in AirMacClean;
+-------------+-------------+------+-----+---------+----------------+
| Field       | Type        | Null | Key | Default | Extra          |
+-------------+-------------+------+-----+---------+----------------+
| CO2         | float(5,1)  | YES  |     | NULL    |                |
| TVOC        | float(5,1)  | YES  |     | NULL    |                |
| device_name | varchar(11) | YES  |     | NULL    |                |
| timestamp   | datetime    | YES  |     | NULL    |                |
| air_ID      | int(11)     | NO   | PRI | NULL    | auto_increment |
+-------------+-------------+------+-----+---------+----------------+
5 rows in set (0.00 sec)

```

View the first 5 records in the enviro table

```
mysql> select * from AirMacClean limit 5;
+-------+------+-------------+---------------------+--------+
| CO2   | TVOC | device_name | timestamp           | air_ID |
+-------+------+-------------+---------------------+--------+
| 400.0 |  0.0 | AirMacClean | 2020-03-16 18:11:00 |      1 |
| 400.0 |  0.0 | AirMacClean | 2020-03-16 18:15:00 |      2 |
| 401.0 |  0.0 | AirMacClean | 2020-03-16 18:22:00 |      3 |
| 400.0 |  0.0 | AirMacClean | 2020-03-31 16:16:00 |      4 |
| 400.0 |  0.0 | AirMacClean | 2020-03-31 16:22:00 |      5 |
+-------+------+-------------+---------------------+--------+
5 rows in set (0.00 sec)
```

