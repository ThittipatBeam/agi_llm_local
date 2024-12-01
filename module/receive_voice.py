import socket
import struct
import os


def receive_message():
    if not os.path.exists("voice/output"):
        os.makedirs("voice/output")

    if not os.path.exists("voice/pcm"):
        os.makedirs("voice/pcm")

    if os.path.exists("voice/audio.pcm"):
        os.remove("voice/audio.pcm")

    keep_audio = True

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 9595))
    print("Server is listening on port 9595 ...")
    flag = False

    while True:
        data, addr = server_socket.recvfrom(10240 + 8)

        if len(data) >= 8:
            status, length = struct.unpack('ii', data[:8])
            message = data[8:8+length]
            print(f"Status: {status}, Length: {length}")
            if keep_audio:
                with open("voice/audio.pcm", "ab") as f:
                    f.write(message)
        else:
            print("Invalid data")
            "Invalid data"
            break

        if status == 1:
            flag = True;

        if status == 3:
            if flag:
                # convert_pcm_to_mp3()
                server_socket.close()
                print("Connection closed")
                flag = False
                return True
            return False