function! _VimpairUpdate()
  python server.update()
endfunction

function! VimpairServerStart()
python << EOF
import sys, os, vim
sys.path.append(
    os.path.abspath(
        os.path.join(vim.eval('expand("<sfile>:p:h")'), 'ftplugin', 'python')
    )
)
from vimpair_server import create_server
EOF

  python server = create_server()
  python server.start()

  augroup Vimpair
    autocmd TextChanged * call _VimpairUpdate()
    autocmd TextChangedI * call _VimpairUpdate()
    autocmd InsertLeave * call _VimpairUpdate()
  augroup END
endfunction

function! VimpairServerStop()
  augroup Vimpair
    autocmd!
  augroup END

  python server.stop()
  python server = None
endfunction
