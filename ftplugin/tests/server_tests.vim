function! _Vimpair_test_listen_to_server()
python << EOF
import socket
import vim
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(1.)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    client_socket.bind((socket.gethostbyname(socket.gethostname()), 50007))
    client_socket.listen(1)
    connection, _address = client_socket.accept()
    vim.vars['Vimpair_test_output'] = connection.recv(1024)
finally:
    client_socket.close()
EOF
endfunction
  

function! Vimpair_server_sends_buffer_content_to_connected_client()
  call VimpairServerStart()

  call _Vimpair_test_listen_to_server()

  call assert_match('.*' . g:Vimpair_test_content . '.*', g:Vimpair_test_output)
endfunction


execute("source " . expand("<sfile>:p:h") . "/test_util.vim")

call _Vimpair_run_tests([function("Vimpair_server_sends_buffer_content_to_connected_client")])
