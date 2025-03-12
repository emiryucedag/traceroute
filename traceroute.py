import os
import sys
import time
import socket
import struct

#veri paketinin toplamını bulup bitlik parçalara dönüştürme
def toplam_data(data):
    sum = 0
    count_sinir = (len(data) // 2) * 2
    count = 0

    for count in range(0, count_sinir, 2):
        ikilik_byte = data[count + 1] * 256 + data[count]
        sum += ikilik_byte
        sum = sum & 0xffffffff  # 32 bitlik sayi elde etme

    if count_sinir < len(data):
        sum += data[len(data) - 1]
        sum = sum & 0xffffffff

    # tasan bitleri geri ekleme
    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)
    toplam = ~sum #tumleyenini aldik
    toplam = toplam & 0xffff
    toplam = toplam >> 8 | (toplam << 8 & 0xff00)
    return toplam

# ping paketi olusturma
def ping(id):
    paket_baslik = struct.pack('bbHHh', 8, 0, 0, id, 1)
    data = struct.pack('d', time.time())
    toplamData = toplam_data(paket_baslik + data)
    paket_baslik = struct.pack('bbHHh', 8, 0, socket.htons(toplamData), id, 1)
    return paket_baslik + data

# Traceroute paketi gönderip yanıt elde etme
def paket_yollama(hedef_adres, ttl):
    timeout=2
    icmp_protocol = socket.getprotobyname('icmp')  # icmp protokol numarsini alma
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp_protocol)  # icmp paketini alma için soket oluşturma
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp_protocol)  # icmp paketini gonderme için soket olusturma
    send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)  # soketin ttl degerini ayarlama
    recv_socket.settimeout(timeout)  # timeout'u ayarlama
    recv_socket.bind(("", 0))  # Alıcı soketi porta baglama

    paketno = os.getpid() & 0xFFFF
    paket = ping(paketno)

    send_socket.sendto(paket, (hedef_adres, 1))
    baslangic = time.time()

    try:
        data, anlik = recv_socket.recvfrom(512)
        zaman = (time.time() - baslangic) * 1000
        anlik = anlik[0]
    except socket.error:
        return None, None
    finally:
        send_socket.close()
        recv_socket.close()

    return anlik, zaman

#traceroute işlemi (maxHop'u 30 aldık )
def traceroute(hedef_adres):
    maxHop=30
    hedef= socket.gethostbyname(hedef_adres)
    
    print(f" Tracing route to {hedef_adres}...")
    ttl = 1
    for ttl in range(1, maxHop, 1):
        anlikAdres, zaman = paket_yollama(hedef, ttl)
        if anlikAdres is not None:
            try:
                anlik = socket.gethostbyaddr(anlikAdres)[0]  # ana ip adresi alır
            except socket.herror:
                anlik = anlikAdres
            print(f"{ttl}\t{anlikAdres}")
        else:
            print(f"{ttl}\t* * *\tRequest timed out.")
        
        if anlikAdres == hedef:
            print("Reached.")
            break
            
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Hatalı kullanım!")
        sys.exit(1)

    hedef_adres = sys.argv[1]
    
    traceroute(hedef_adres)

