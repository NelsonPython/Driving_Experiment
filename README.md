# Drive I-5

This is the repository for the [Drive I-5 tutorial](http://i18nelson.com/Tutorial-DriveI5/EVehicles.htm) that runs in the [AI Lab](https://github.com/NelsonPython/AI_Lab).  You can build your own lab by following these [instructions](https://github.com/NelsonPython/AI_Lab) or you can <a href="http://www.i18nelson.com/contactMe.php">schedule time in the AI Lab</a>.  

First, follow these instructions to configure each device:</h2>

[AstroPiQuake](AstroPiQuake/README.md)

[Enviro](Enviro/README.md)

[Air MacClean](AirMacClean/README.md)

[Bumblebee AV](BumblebeeAV/README.md)

[Public Radio](PublicRadio/README.md)

[MOBI Data Mart](DataMart/README.md)

After your devices are configured, follow these steps to conduct experiments:

1. Power on all your devices

2. If you don't have a static IP address for Public Radio, get the current IP address

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

3. In order to control the devices via SSH, you can find their current ip addresses based on their MAC address by running this script:

```
python3 nmap2mac.py
```

4. Use PuTTY to connect to AstroPiQuake.  Run the emoji listener so devices can send emojis to the LED panel

```
python3 emoji.py
```

5. Use PuTTY to connect to BumbleBee AV.  Run the listener so the AV can respond to messages such as an earthquake alert

```
python3 listener.py
```

6. Go to the MOBI Data Mart website, click on Roadtrip, and choose your route


7. Use PuTTY to open another session with Bumblebee AV.  Drive the experiment

```
python3 socketSports.py -ip 192.168.1.x
```

8. To simulate an earthquake, go to Public Radio, open a new terminal, and run ./quake.sh
