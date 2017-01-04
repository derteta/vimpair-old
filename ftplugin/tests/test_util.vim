execute("source " . expand("<sfile>:p:h") . "/../vimpair.vim")
let g:Vimpair_test_content="Some random buffer content"

function! _Vimpair_test_setUp()
  let g:Vimpair_test_output=""
  execute("vnew")
  call append(0, g:Vimpair_test_content)
endfunction

function! _Vimpair_test_tearDown()
  call VimpairServerStop()
  call VimpairClientStop()
  execute("q!")
endfunction

function! _Vimpair_assert_output_contains(Text)
  call assert_match('.*' . a:Text . '.*', g:Vimpair_test_output)
endfunction

function! _Vimpair_assert_client_buffer_contents_is(Text)
  " only using single line content for now
  call assert_match(a:Text, getline(1))
endfunction

function! _Vimpair_test_show_results()
  if v:errors == []
    echo "Vimpair: All tests passed"
  else
    for error in v:errors
      :echoerr error
    endfor
  endif
  let v:errors = []
endfunction

function! _Vimpair_run_tests(Tests)
  let v:errors = []

  for Test in a:Tests
    call _Vimpair_test_setUp()
    call Test()
    call _Vimpair_test_tearDown()
  endfor

  call _Vimpair_test_show_results()
endfunction
