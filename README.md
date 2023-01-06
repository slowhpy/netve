# netve
Alive IP scanner

![Build](https://img.shields.io/badge/Built%20with-Python-Blue)
[![Twitter](https://img.shields.io/twitter/follow/J_0K_3R?label=Follow)](https://twitter.com/J_0K_3R)

> Scan which IP is alive

You can scan the IP range and see which of them is alive, by choosing one of the 3 protocol (ARP,ICMP,TCP).

If the IP block one of the protocol you can change it to another one.

**netve** is being actively developed by [@J_0K_3R](https://twitter.com/J_0K_3R)

Installation & Usage
------------
**Requirement: python 3.x**
```
git clone https://github.com/j0k-3r/netve.git
```

How to use
---------------
```
python3 netve.py -h
```

Examples
---------------
```
python3 netve.py 10.10.x.0/24 -i eth0 --arp
```
```
python3 netve.py 10.10.x.0/24 -i eth0 --icmp
```
```
python3 netve.py 10.10.x.0/24 -i eth0 --tcp
```
