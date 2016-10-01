function! VimpairServerStart()
python << EOF
import socket
import sys
import vim
import time
def send_buffer_contents():
    server_socket = socket.socket()
    server_socket.settimeout(1.)
    time.sleep(1)
    try:
        server_socket.connect((socket.gethostbyname(socket.gethostname()), 50007))
        buffer_contents = reduce(lambda s1, s2: s1 + '\n' + s2, vim.current.buffer[:])
        server_socket.sendall(buffer_contents)
    finally:
        server_socket.close()
import threading
thread = threading.Thread(target=send_buffer_contents)
thread.start()
EOF
endfunction

function! VimpairServerStop()
  python thread.join()
endfunction
