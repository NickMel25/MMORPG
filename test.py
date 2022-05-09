import socket
monster_udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
monster_udp_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
monster_udp_client.bind((socket.gethostbyname(socket.gethostname()), 32456))