-Traceroute Implementation in Python-
This Python script implements a Traceroute tool using raw ICMP sockets. Traceroute is a network diagnostic tool that helps track the route that packets take from the sender's machine to a specified destination.

-How It Works-
The script sends ICMP Echo Request (ping) packets to the destination with an increasing Time-to-Live (TTL) value.
Each router in the path decrements the TTL and sends back an ICMP Time Exceeded response if the TTL reaches zero.
The script captures these responses and prints the IP addresses of the intermediate routers.
The process continues until the packet reaches the final destination or the maximum hop limit (30) is reached.

-Usage-
Run the script in the terminal with a target domain or IP address:
python traceroute.py example.com

-Key Features-
Uses raw sockets to send and receive ICMP packets.
Calculates checksum for ICMP packets.
Supports hostname resolution for intermediate routers.
Implements timeouts to handle unreachable hosts.

Example Output:
Tracing route to example.com...
1    192.168.1.1
2    203.0.113.1
3    198.51.100.2
4    93.184.216.34
Reached.

This output shows the routers that the packet passes through before reaching the destination.
