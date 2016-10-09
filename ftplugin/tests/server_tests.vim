function! _Vimpair_test_listen_to_server(Keep_connection_alive)
python << EOF
import socket
import vim
import time
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(1.)
time.sleep(.5)
client_socket.connect(
    (socket.gethostbyname(socket.gethostname()), 50007)
)

def fetch_server_output():
    received = client_socket.recv(1024)
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
