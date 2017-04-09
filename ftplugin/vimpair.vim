python << EOF
import sys, os, vim
python_path = os.path.abspath(
  os.path.join(vim.eval('expand("<sfile>:p:h")'), 'python')
)
if not python_path in sys.path:
  sys.path.append(python_path)

from vimpair_server import create_server
from vimpair_client import create_client

server = None
client = None
EOF

let g:_VimpairClientTimer = ""

function! _VimpairUpdate()
  python server.update()
endfunction

function! _VimpairTimerCall(timer)
  python if client is not None: client.on_timer()
endfunction

function! VimpairServerStart()
  python server = create_server()
  python server.start()

  augroup Vimpair
    autocmd TextChanged * call _VimpairUpdate()
    autocmd TextChangedI * call _VimpairUpdate()
    autocmd InsertLeave * call _VimpairUpdate()
    autocmd CursorMoved * call _VimpairUpdate()
    autocmd CursorMovedI * call _VimpairUpdate()
  augroup END
endfunction

function! VimpairServerStop()
  augroup Vimpair
    autocmd!
  augroup END

  python if server is not None: server.stop()
  python server = None
endfunction

function! VimpairClientStart()
  python client = create_client()
  python client.start()
  let g:_VimpairClientTimer = timer_start(200, '_VimpairTimerCall', {'repeat': -1})
endfunction

function! VimpairClientStop()
  if g:_VimpairClientTimer != ""
    call timer_stop(g:_VimpairClientTimer)
    let g:_VimpairClientTimer = ""
  endif
  python if client is not None: client.stop()
  python client = None
endfunction
