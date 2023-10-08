<h1>Creating the AstroPiQuake table</h1>

<b>AstroPiQuake data can be saved in a database table</b>

To get started, these instructions explain how to load data from a csv file. You can also load data when sensor readings are taken.

Use a database named, ai_lab_data.  If you have not created this database, then create it.

```
CREATE DATABASE ai_lab_data;
```

Use the ai_lab_data database

```
mysql> use ai_lab_data;
Database changed
```

Create the AstroPiQuake table.  Make sure the columns are arranged in the exact same order of the csv file containing data to be loaded.  Do not add a primary key

```
create table AstroPiQuake (
device_name varchar(12),
humidity varchar(20),
lat varchar(20),
lng varchar(20),
pitch varchar(20),
pressure varchar(20),
roll varchar(20),
temperature varchar(20),
timestamp datetime,
x varchar(20),
y varchar(20),
yaw varchar(20),
z varchar(20));

mysql> show columns in AstroPiQuake;
+-------------+-------------+------+-----+---------+-------+
| Field       | Type        | Null | Key | Default | Extra |
+-------------+-------------+------+-----+---------+-------+
| device_name | varchar(12) | YES  |     | NULL    |       |
| humidity    | varchar(20) | YES  |     | NULL    |       |
| lat         | varchar(20) | YES  |     | NULL    |       |
| lng         | varchar(20) | YES  |     | NULL    |       |
| pitch       | varchar(20) | YES  |     | NULL    |       |
| pressure    | varchar(20) | YES  |     | NULL    |       |
| roll        | varchar(20) | YES  |     | NULL    |       |
| temperature | varchar(20) | YES  |     | NULL    |       |
| timestamp   | datetime    | YES  |     | NULL    |       |
| x           | varchar(20) | YES  |     | NULL    |       |
| y           | varchar(20) | YES  |     | NULL    |       |
| yaw         | varchar(20) | YES  |     | NULL    |       |
| z           | varchar(20) | YES  |     | NULL    |       |
+-------------+-------------+------+-----+---------+-------+
13 rows in set (0.00 sec)
```

Copy the AstroPiQuake.csv file into the folder with permissions to load data.  You can find this folder by showing variables.  Otherwise, you get an error similar to:  ERROR 1290 (HY000): The MySQL server is running with the --secure-file-priv option so it cannot execute this statement

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
mysql> load data infile '/var/lib/mysql-files/AstroPiQuake.csv' into table AstroPiQuake fields terminated by ',' ignore 1 lines;
Query OK, 345 rows affected (0.02 sec)
Records: 345  Deleted: 0  Skipped: 0  Warnings: 0
```

Add a primary key field

```
mysql> alter table AstroPiQuake add quake_ID int not null primary key auto_increment;
Query OK, 0 rows affected (0.06 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> show columns in AstroPiQuake;
+-------------+-------------+------+-----+---------+----------------+
| Field       | Type        | Null | Key | Default | Extra          |
+-------------+-------------+------+-----+---------+----------------+
| device_name | varchar(12) | YES  |     | NULL    |                |
| humidity    | varchar(20) | YES  |     | NULL    |                |
| lat         | varchar(20) | YES  |     | NULL    |                |
| lng         | varchar(20) | YES  |     | NULL    |                |
| pitch       | varchar(20) | YES  |     | NULL    |                |
| pressure    | varchar(20) | YES  |     | NULL    |                |
| roll        | varchar(20) | YES  |     | NULL    |                |
| temperature | varchar(20) | YES  |     | NULL    |                |
| timestamp   | datetime    | YES  |     | NULL    |                |
| x           | varchar(20) | YES  |     | NULL    |                |
| y           | varchar(20) | YES  |     | NULL    |                |
| yaw         | varchar(20) | YES  |     | NULL    |                |
| z           | varchar(20) | YES  |     | NULL    |                |
| quake_ID    | int(11)     | NO   | PRI | NULL    | auto_increment |
+-------------+-------------+------+-----+---------+----------------+
14 rows in set (0.00 sec)
```

View the first 5 records in the enviro table

```
mysql> select * from AstroPiQuake limit 5;
+--------------+--------------------+-----------+---------------------+----------------+------------------+----------------+--------------------+---------------------+---------------+---------------+----------------+---------------+----------+
| device_name  | humidity           | lat       | lng                 | pitch          | pressure         | roll           | temperature        | timestamp           | x             | y             | yaw            | z             | quake_ID |
+--------------+--------------------+-----------+---------------------+----------------+------------------+----------------+--------------------+---------------------+---------------+---------------+----------------+---------------+----------+
| AstroPiQuake | 36.788185119628906 | 33.893916 | -118.32341100000001 | 359.5425133958 | 998.36572265625  | 268.8060052965 | 26.40833282470703  | 2020-03-16 18:03:00 | 0.0077582696  | -0.9682807326 | 138.1091707537 | -0.0216925722 |        1 |
| AstroPiQuake | 36.947242736816406 | 33.893916 | -118.32341100000001 | 359.4132737836 | 998.423583984375 | 268.7905963898 | 26.53666687011719  | 2020-03-16 18:06:00 | 0.0082431613  | -0.9690043926 | 137.4922544075 | -0.021451544  |        2 |
| AstroPiQuake | 36.73990249633789  | 33.893916 | -118.32341100000001 | 359.4700679805 | 998.41845703125  | 269.0744180705 | 26.518333435058594 | 2020-03-16 18:12:00 | 0.0084856069  | -0.9699693322 | 136.7097606154 | -0.0154258292 |        3 |
| AstroPiQuake | 37.11481475830078  | 33.893916 | -118.32341100000001 | 359.4843855511 | 998.37158203125  | 269.1028931292 | 26.35333251953125  | 2020-03-16 18:18:00 | 0.008970499   | -0.9704517722 | 137.0307521857 | -0.0166309718 |        4 |
| AstroPiQuake | 37.45564651489258  | 33.893916 | -118.32341100000001 | 358.555684036  | 998.36083984375  | 268.0266807122 | 26.316665649414066 | 2020-03-16 18:24:00 | -0.0009873426 | -0.9842016697 | 140.6240464061 | -0.0098821726 |        5 |
+--------------+--------------------+-----------+---------------------+----------------+------------------+----------------+--------------------+---------------------+---------------+---------------+----------------+---------------+----------+
5 rows in set (0.00 sec)
```

