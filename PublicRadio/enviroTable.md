<h1>Creating an enviro table</h1>

mysql> use ai_lab_data;
Database changed
mysql> 






mysql> create table enviro (
    -> RGB_blue int(3),
    -> device_name varchar(5),
    -> RGB_green int(3),
    -> heading int(5),
    -> lat varchar(15),
    -> lng varchar(15),
    -> lux int(6),
    -> pressure varchar(15),
    -> RGB_red int(3),
    -> temperature varchar(15),
    -> timestamp date,
    -> acc_x varchar(15),
    -> acc_y varchar(15),
    -> acc_z varchar(15));
Query OK, 0 rows affected (0.02 sec)

mysql> show columns in enviro;
+-------------+-------------+------+-----+---------+-------+
| Field       | Type        | Null | Key | Default | Extra |
+-------------+-------------+------+-----+---------+-------+
| RGB_blue    | int(3)      | YES  |     | NULL    |       |
| device_name | varchar(5)  | YES  |     | NULL    |       |
| RGB_green   | int(3)      | YES  |     | NULL    |       |
| heading     | int(5)      | YES  |     | NULL    |       |
| lat         | varchar(15) | YES  |     | NULL    |       |
| lng         | varchar(15) | YES  |     | NULL    |       |
| lux         | int(6)      | YES  |     | NULL    |       |
| pressure    | varchar(15) | YES  |     | NULL    |       |
| RGB_red     | int(3)      | YES  |     | NULL    |       |
| temperature | varchar(15) | YES  |     | NULL    |       |
| timestamp   | date        | YES  |     | NULL    |       |
| acc_x       | varchar(15) | YES  |     | NULL    |       |
| acc_y       | varchar(15) | YES  |     | NULL    |       |
| acc_z       | varchar(15) | YES  |     | NULL    |       |
+-------------+-------------+------+-----+---------+-------+
14 rows in set (0.00 sec)




mysql> alter table enviro add enviro_ID int not null primary key auto_increment; 
Query OK, 0 rows affected (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> show columns in enviro;                                                  +-------------+-------------+------+-----+---------+----------------+
| Field       | Type        | Null | Key | Default | Extra          |
+-------------+-------------+------+-----+---------+----------------+
| RGB_blue    | int(3)      | YES  |     | NULL    |                |
| device_name | varchar(5)  | YES  |     | NULL    |                |
| RGB_green   | int(3)      | YES  |     | NULL    |                |
| heading     | int(5)      | YES  |     | NULL    |                |
| lat         | varchar(15) | YES  |     | NULL    |                |
| lng         | varchar(15) | YES  |     | NULL    |                |
| lux         | int(6)      | YES  |     | NULL    |                |
| pressure    | varchar(15) | YES  |     | NULL    |                |
| RGB_red     | int(3)      | YES  |     | NULL    |                |
| temperature | varchar(15) | YES  |     | NULL    |                |
| timestamp   | date        | YES  |     | NULL    |                |
| acc_x       | varchar(15) | YES  |     | NULL    |                |
| acc_y       | varchar(15) | YES  |     | NULL    |                |
| acc_z       | varchar(15) | YES  |     | NULL    |                |
| enviro_ID   | int(11)     | NO   | PRI | NULL    | auto_increment |
+-------------+-------------+------+-----+---------+----------------+
15 rows in set (0.00 sec)


mysql> load data infile 'AI-PMP/sensorData/Enviro.csv'
    -> into table enviro
    -> fields terminated by ','
    -> enclosed by '"'
    -> lines terminated by '\r\n'
    -> ignore 1 lines;
ERROR 1290 (HY000): The MySQL server is running with the --secure-file-priv option so it cannot execute this statement


mysql> mysql> show variables like "secure_file_priv";
+------------------+-----------------------+
| Variable_name    | Value                 |
+------------------+-----------------------+
| secure_file_priv | /var/lib/mysql-files/ |
+------------------+-----------------------+
1 row in set (0.00 sec)

mysql> load data infile '/var/lib/mysql-files/Enviro.csv' into table enviro fields terminated by ',' ignore 1 lines;
Query OK, 394 rows affected, 394 warnings (0.02 sec)
Records: 394  Deleted: 0  Skipped: 0  Warnings: 394


mysql> show columns in enviro;
+-------------+-------------+------+-----+---------+----------------+
| Field       | Type        | Null | Key | Default | Extra          |
+-------------+-------------+------+-----+---------+----------------+
| RGB_blue    | int(3)      | YES  |     | NULL    |                |
| device_name | varchar(6)  | YES  |     | NULL    |                |
| RGB_green   | int(3)      | YES  |     | NULL    |                |
| heading     | varchar(20) | YES  |     | NULL    |                |
| lat         | varchar(20) | YES  |     | NULL    |                |
| lng         | varchar(20) | YES  |     | NULL    |                |
| lux         | int(6)      | YES  |     | NULL    |                |
| pressure    | varchar(20) | YES  |     | NULL    |                |
| RGB_red     | int(3)      | YES  |     | NULL    |                |
| temperature | varchar(20) | YES  |     | NULL    |                |
| timestamp   | date        | YES  |     | NULL    |                |
| acc_x       | varchar(20) | YES  |     | NULL    |                |
| acc_y       | varchar(20) | YES  |     | NULL    |                |
| acc_z       | varchar(20) | YES  |     | NULL    |                |


mysql> select * from enviro limit 5;
+----------+-------------+-----------+---------+-----------+-------------+------+-------------------+---------+--------------------+------------+-------------------+------------------+------------------+
| RGB_blue | device_name | RGB_green | heading | lat       | lng         | lux  | pressure          | RGB_red | temperature        | timestamp  | acc_x             | acc_y            | acc_z            |
+----------+-------------+-----------+---------+-----------+-------------+------+-------------------+---------+--------------------+------------+-------------------+------------------+------------------+
|        0 | Enviro      |         0 | 265.88  | 33.893916 | -118.323411 |    0 | 99522.92466995298 |       0 | 23.54730162054575  | 2020-03-16 | -1.99951171875    | 1.99951171875    | -1.99951171875   |
|      104 | Enviro      |       101 | 265.2   | 33.893916 | -118.323411 | 1021 | 99524.2382364979  |      98 | 23.84600931729765  | 2020-03-16 | -0.05694580078125 | 0.913330078125   | -0.369384765625  |
|      104 | Enviro      |       101 | 272.7   | 33.893916 | -118.323411 |  921 | 99512.4189152995  |      99 | 24.06680736091248  | 2020-03-16 | -0.09088134765625 | 0.9161376953125  | -0.3526611328125 |
|      104 | Enviro      |       100 | 278.98  | 33.893916 | -118.323411 |  771 | 99508.05125572513 |      96 | 24.297643939685077 | 2020-03-16 | -0.10552978515625 | 0.924072265625   | -0.34033203125   |
|      105 | Enviro      |       103 | 282.87  | 33.893916 | -118.323411 |  680 | 99513.53969794454 |     100 | 24.36579334292501  | 2020-03-16 | -0.11151123046875 | 0.92510986328125 | -0.3228759765625 |
+----------+-------------+-----------+---------+-----------+-------------+------+-------------------+---------+--------------------+------------+-------------------+------------------+------------------+
5 rows in set (0.00 sec)





| enviro_ID   | int(11)     | NO   | PRI | NULL    | auto_increment |
+-------------+-------------+------+-----+---------+----------------+
15 rows in set (0.00 sec)


mysql> alter table enviro add enviro_ID int not null primary key auto_increment;
Query OK, 0 rows affected (0.06 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> show columns in enviro;
+-------------+-------------+------+-----+---------+----------------+
| Field       | Type        | Null | Key | Default | Extra          |
+-------------+-------------+------+-----+---------+----------------+
| RGB_blue    | int(3)      | YES  |     | NULL    |                |
| device_name | varchar(6)  | YES  |     | NULL    |                |
| RGB_green   | int(3)      | YES  |     | NULL    |                |
| heading     | varchar(20) | YES  |     | NULL    |                |
| lat         | varchar(20) | YES  |     | NULL    |                |
| lng         | varchar(20) | YES  |     | NULL    |                |
| lux         | int(6)      | YES  |     | NULL    |                |
| pressure    | varchar(20) | YES  |     | NULL    |                |
| RGB_red     | int(3)      | YES  |     | NULL    |                |
| temperature | varchar(20) | YES  |     | NULL    |                |
| timestamp   | date        | YES  |     | NULL    |                |
| acc_x       | varchar(20) | YES  |     | NULL    |                |
| acc_y       | varchar(20) | YES  |     | NULL    |                |
| acc_z       | varchar(20) | YES  |     | NULL    |                |
| enviro_ID   | int(11)     | NO   | PRI | NULL    | auto_increment |
+-------------+-------------+------+-----+---------+----------------+
15 rows in set (0.00 sec)

mysql> select * from enviro limit 5;
+----------+-------------+-----------+---------+-----------+-------------+------+-------------------+---------+--------------------+------------+-------------------+------------------+------------------+-----------+
| RGB_blue | device_name | RGB_green | heading | lat       | lng         | lux  | pressure          | RGB_red | temperature        | timestamp  | acc_x             | acc_y            | acc_z            | enviro_ID |
+----------+-------------+-----------+---------+-----------+-------------+------+-------------------+---------+--------------------+------------+-------------------+------------------+------------------+-----------+
|        0 | Enviro      |         0 | 265.88  | 33.893916 | -118.323411 |    0 | 99522.92466995298 |       0 | 23.54730162054575  | 2020-03-16 | -1.99951171875    | 1.99951171875    | -1.99951171875   |         1 |
|      104 | Enviro      |       101 | 265.2   | 33.893916 | -118.323411 | 1021 | 99524.2382364979  |      98 | 23.84600931729765  | 2020-03-16 | -0.05694580078125 | 0.913330078125   | -0.369384765625  |         2 |
|      104 | Enviro      |       101 | 272.7   | 33.893916 | -118.323411 |  921 | 99512.4189152995  |      99 | 24.06680736091248  | 2020-03-16 | -0.09088134765625 | 0.9161376953125  | -0.3526611328125 |         3 |
|      104 | Enviro      |       100 | 278.98  | 33.893916 | -118.323411 |  771 | 99508.05125572513 |      96 | 24.297643939685077 | 2020-03-16 | -0.10552978515625 | 0.924072265625   | -0.34033203125   |         4 |
|      105 | Enviro      |       103 | 282.87  | 33.893916 | -118.323411 |  680 | 99513.53969794454 |     100 | 24.36579334292501  | 2020-03-16 | -0.11151123046875 | 0.92510986328125 | -0.3228759765625 |         5 |
+----------+-------------+-----------+---------+-----------+-------------+------+-------------------+---------+--------------------+------------+-------------------+------------------+------------------+-----------+
5 rows in set (0.00 sec)

mysql> 
