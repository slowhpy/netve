from scapy.all import *
import argparse
import textwrap


parser = argparse.ArgumentParser(
    description = 'Alive IP scanner',
    formatter_class = argparse.RawDescriptionHelpFormatter,
    epilog = textwrap.dedent('''Examples:
    netve.py <IP_Range> -i <interface> --<packet_protocol>''')
)
parser.add_argument('IP_Range', help = 'Add IP Range')
parser.add_argument('-i', '--interface', default='eth0', help = 'Add interface')
parser.add_argument('--arp', help='send ARP packet', action='store_true')
parser.add_argument('--icmp', help='send ICMP packet', action='store_true')
parser.add_argument('--tcp', help='send TCP packet', action='store_true')
args = parser.parse_args()
IP_Range = args.IP_Range
interface = args.interface
arp = args.arp
icmp = args.icmp
tcp = args.tcp
broadcastMac = 'ff:ff:ff:ff:ff:ff'
port = 80

def ARP_Packet(arp):
    # Send ARP packet and check for response
    ans, unans = arping(IP_Range)
    mac = ans[0][1].src
    packet = Ether(src=mac, dst=broadcastMac)/ARP(pdst=IP_Range)
    ans, unans = srp(packet, timeout=2, iface=interface, inter=0.1)
    arp_list = []
    for send, receive in ans:
        if receive.haslayer(ARP):
            arp_list.append(receive.sprintf(r"%Ether.src% - %ARP.psrc%"))
    ip_list = [ip.strip() for ip in arp_list]
    for ip in sorted(ip_list, key = lambda ip: [int(ip) for ip in ip.split('.')]):
        print(ip)

def ICMP_Packet(icmp):
    # If no ARP responses were received, try sending an ICMP packet
    try:
        ans, unans = sr(IP(dst=IP_Range)/ICMP())
        icmp_list=[]
        for send, receive in ans:
            if receive.haslayer(ICMP):
                icmp_list.append(f"{receive.src}")
        ip_list = [ip.strip() for ip in icmp_list]
        for ip in sorted(ip_list, key = lambda ip: [int(ip) for ip in ip.split('.')]):
            print(ip)
    except Exception as e:
        print(f"Error sending ICMP packet: {e}")

def TCP_Packet(tcp):
    # If no ARP or ICMP responses were received, try sending a TCP SYN packet
    try:
        ans, unans = sr(IP(dst=IP_Range)/TCP(dport=port, flags="S"))
        tcp_list=[]
        for send, receive in ans:
            if receive.haslayer(TCP):
                tcp_list.append(f"{receive.src}")
        ip_list = [ip.strip() for ip in tcp_list]
        for ip in sorted(ip_list, key = lambda ip: [int(ip) for ip in ip.split(".")] ):
            print(ip)  
    except Exception as e:
        print(f"Error sending TCP SYN packet: {e}")


try:
    if arp:

        ARP_Packet(arp)

    elif icmp:

        ICMP_Packet(icmp)

    elif tcp:

        TCP_Packet(tcp)

    else:

        print("choose one of the protocol (arp, icmp, tcp)")

# If no responses were received for any of the packet types, print a message
except:

    print(f"No responses received for IP range {IP_Range}")


