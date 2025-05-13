import socket
import os
import struct
import time
import sys
import subprocess
from checksum import checksum


ICMP_ECHO_REQUEST = 8  

class Tracert:

    @staticmethod
    def create_packet(seq):
        """Create an ICMP packet."""
        header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, os.getpid(), seq)
        my_checksum = checksum(header)
        header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), os.getpid(), seq)
        return header

    @classmethod
    def traceroute(cls, destination, max_hops=30):
        """Perform a traceroute to the destination."""
        """Преобразуем домен в ip адрес"""
        dest_addr = socket.gethostbyname(destination)
        print(f'Traceroute to {dest_addr} ({destination}), {max_hops} hops max:')
        
        for ttl in range(1, max_hops + 1):
            """Зачем: Для отправки и приема ICMP-пакетов (Echo Request и Time Exceeded)."""
            icmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
            """Зачем: Чтобы пакет "умирал" на определенном узле, заставляя его отправить ICMP Time Exceeded."""
            icmp.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
            
            icmp.settimeout(1)

            packet = cls.create_packet(ttl)
            start_time = time.time()
            icmp.sendto(packet, (destination, 0))

            try:
                recv_packet, addr = icmp.recvfrom(1024)
                round_trip_time = (time.time() - start_time) * 1000  
                print(f'{ttl}\t{round_trip_time:.2f} ms\t{addr[0]}')
                if addr[0] == dest_addr:
                    break  
            except socket.timeout:
                print(f'{ttl}\t* * * Request timed out.')

            icmp.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        destination = input("Введите домен или IP-адрес: ")
    else:
        destination = sys.argv[1]
    ex = Tracert
    ex.traceroute(destination)
    