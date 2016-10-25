function! _Vimpair_test_listen_to_server(Keep_connection_alive)
python << EOF
import socket
import vim
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(1.)
client_socket.connect(
    (socket.gethostbyname(socket.gethostname()), 50007)
)

def fetch_server_output(close_connection=True):
    received = client_socket.recv(1024)
    vim.vars['Vimpair_test_output'] = received
    if close_connection:
      client_socket.close()
EOF

  if a:Keep_connection_alive == 1
    python fetch_server_output(close_connection=False)
  else
    python fetch_server_output(close_connection=True)
  endif
endfunction


function! Vimpair_server_sends_buffer_content_to_connected_client()
  call VimpairServerStart()

  let Keep_connection_alive = 0
  call _Vimpair_test_listen_to_server(Keep_connection_alive)

  call _Vimpair_assert_output_contains(g:Vimpair_test_content)
endfunction

function! Vimpair_server_sends_buffer_content_on_changes()
  call VimpairServerStart()
  let Keep_connection_alive = 1
  call _Vimpair_test_listen_to_server(Keep_connection_alive)

  execute("normal A. Adding some more")

  python fetch_server_output()
  call _Vimpair_assert_output_contains('Adding some more')
endfunction

function! Vimpair_server_sends_cursor_position_to_connected_client()
  call VimpairServerStart()

  let Keep_connection_alive = 0
  call _Vimpair_test_listen_to_server(Keep_connection_alive)

  call _Vimpair_assert_output_contains('(1, 0)')
endfunction

function! Vimpair_server_sends_cursor_position_on_changes()
  call VimpairServerStart()
  let Keep_connection_alive = 1
  call _Vimpair_test_listen_to_server(Keep_connection_alive)

  execute("normal A. Adding some more")

  python fetch_server_output()
  call _Vimpair_assert_output_contains('(1, 17)')
endfunction


execute("source " . expand("<sfile>:p:h") . "/test_util.vim")

call _Vimpair_run_tests(
      \ [function("Vimpair_server_sends_buffer_content_to_connected_client"),
      \  function("Vimpair_server_sends_buffer_content_on_changes"),
      \  function("Vimpair_server_sends_cursor_position_to_connected_client"),
      \  function("Vimpair_server_sends_cursor_position_on_changes")])
