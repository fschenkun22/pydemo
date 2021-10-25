import socket
def main():
    # 创建套接字
    udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    localAddr = ("127.0.0.1",7788)
    udp_socket.bind(localAddr)# 绑定本地信息


    while True:
            rdata = udp_socket.recvfrom(1024)# 接受数据
            print(rdata)  # 打印
            print(rdata[0].decode('gbk'))
            if rdata[0].decode('gbk') == 'exit':
                udp_socket.close() # 关闭
                exit()

    

    
    
  
   


if __name__ == "__main__":
    main()