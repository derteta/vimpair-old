function! VimpairServerStart()
python << EOF
import sys, os, vim
sys.path.append(
    os.path.abspath(
        os.path.join(vim.eval('expand("<sfile>:p:h")'), 'ftplugin', 'python')
    )
)
from vimpair_server import VimpairServer
EOF

  python server = VimpairServer()
  python server.start()
endfunction

function! VimpairServerStop()
  python server.stop()
  python server = None
endfunction
