function! _VimpairPythonSetup()
python << EOF
import sys, os, vim
sys.path.append(
    os.path.abspath(
        os.path.join(vim.eval('expand("<sfile>:p:h")'), 'ftplugin', 'python')
    )
)
from vimpair_server import create_server
from vimpair_client import create_client

server = None
client = None
EOF
endfunction

function! _VimpairUpdate()
  python server.update()
endfunction

function! _VimpairTimerCall()
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
endfunction

function! VimpairClientStop()
  python if client is not None: client.stop()
  python client = None
endfunction

call _VimpairPythonSetup()
