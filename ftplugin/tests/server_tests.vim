function! _Vimpair_test_listen_to_server(Keep_connection_alive)
python << EOF
import socket
import vim
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(1.)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.bind((socket.gethostbyname(socket.gethostname()), 50007))
client_socket.listen(1)

connection, _address = client_socket.accept()
connection.setblocking(1)

def fetch_server_output():
    received = connection.recv(1024)
    vim.vars['Vimpair_test_output'] = received

fetch_server_output()
EOF

  if a:Keep_connection_alive == 0
    python client_socket.close()
  endif
endfunction


function! Vimpair_server_sends_buffer_content_to_connected_client()
  call VimpairServerStart()

  let Keep_connection_alive = 0
  call _Vimpair_test_listen_to_server(Keep_connection_alive)

  call assert_match('.*' . g:Vimpair_test_content . '.*', g:Vimpair_test_output)
endfunction

function! Vimpair_server_sends_buffer_content_on_changes()
  call VimpairServerStart()
  let Keep_connection_alive = 1
  call _Vimpair_test_listen_to_server(Keep_connection_alive)

  execute("normal A. Adding some more")
  python fetch_server_output()
  python client_socket.close()

  call assert_match('.*Adding some more.*', g:Vimpair_test_output)
endfunction


execute("source " . expand("<sfile>:p:h") . "/test_util.vim")

call _Vimpair_run_tests(
      \ [function("Vimpair_server_sends_buffer_content_to_connected_client"),
      \  function("Vimpair_server_sends_buffer_content_on_changes")])
