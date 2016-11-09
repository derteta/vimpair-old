function! _VimpairPythonSetup()
python << EOF
import sys, os, vim
sys.path.append(
    os.path.abspath(
        os.path.join(vim.eval('expand("<sfile>:p:h")'), 'ftplugin', 'python')
    )
)
from vimpair_server import create_server

server = None
EOF
endfunction

function! _VimpairUpdate()
  python server.update()
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

call _VimpairPythonSetup()
