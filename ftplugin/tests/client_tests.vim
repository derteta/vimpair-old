function! _Vimpair_test_listen_for_client_connection()
python << EOF
import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.settimeout(1.)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((socket.gethostbyname(socket.gethostname()), 50007))
server_socket.listen(1)
connection, _address = server_socket.accept()
connection.setblocking(1)
EOF
endfunction


function! Vimpair_client_applies_retrieved_buffer_content()
  " Clear buffer content. Should not be filled in the first place.
  execute("normal ggdG")
  call VimpairClientStart()
  call _Vimpair_test_listen_for_client_connection()

  python connection.sendall(vim.vars['Vimpair_test_content'])

  python import time; time.sleep(1)
  call _Vimpair_assert_client_buffer_contents_is(g:Vimpair_test_content)
endfunction


execute("source " . expand("<sfile>:p:h") . "/test_util.vim")

call _Vimpair_run_tests(
      \ [function("Vimpair_client_applies_retrieved_buffer_content")])
