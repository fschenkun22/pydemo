import socket

def main():
    print("run")
    udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    data = input('please in put data:')
    dest_ip = input('sent to ip:')
    dest_port = int(input('insert dest port:'))

    udp_socket.sendto(data.encode("utf-8"),(dest_ip,dest_port))
    recv_data = udp_socket.recvfrom(1024)
    print(recv_data)
    if data == "exit":
        udp_socket.close()
        exit()

    udp_socket.close()


if __name__ == "__main__":
    while True:
        main()