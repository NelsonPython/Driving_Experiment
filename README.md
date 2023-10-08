# Driving Experiment

Get started by configuring each device in the [STEM Lab](https://github.com/NelsonPython/STEM_Lab).  You can build your own lab by following these [instructions](https://github.com/NelsonPython/AI_Lab) or you can <a href="http://www.NormLTranz.com/contactMe.php">schedule time in the STEM Lab</a>.  

[AstroPiQuake](AstroPiQuake/README.md)

[Enviro](Enviro/README.md)

[Air MacClean](AirMacClean/README.md)

[Bumblebee Rover](Bumblebee_Rover/README.md)

[Public Data Cloud](Public_Data_Cloud/README.md)

[Data Mart](DataMart/README.md)

After your devices are configured, follow these steps to conduct experiments:

1. Power on all your devices

2. If you don't have a static IP address for Public Data Cloud, get the current IP address

```
ip addr
```

In this example, the ip address is:  192.168.1.8

```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:86:dd:45 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.8/24 brd 192.168.1.255 scope global dynamic noprefixroute enp0s3
       valid_lft 601665sec preferred_lft 601665sec
    inet6 fe80::ae56:b667:f535:22cd/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
```

3. In order to control the devices via SSH, you can find their current ip addresses using Nmap and their MAC address.  Here's a sample script:

```
python3 nmap2mac.py
```

4. Connect remotely to AstroPiQuake.  Run the emoji listener so devices can send emojis to the LED panel

```
python3 emoji.py
```

5. Connect remotely to BumbleBee Rover.  Run the listener so the rover can respond to messages such as an earthquake alert

```
python3 listener.py
```

6. Go to the Public Data Cloud website, click on Roadtrip, and choose your route


7. Open another session with Bumblebee Rover.  Drive the experiment

```
python3 socketSports.py -ip 192.168.1.x
```

8. To simulate an earthquake, go to Public Data Cloud, open a new terminal, and run ./quake.sh
