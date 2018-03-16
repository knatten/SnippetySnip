" Vim plugin for importing into a file selected lines from other files
" Version:     1.0
" Last change: 2013-10-13
" Author:      Anders Schau Knatten
" Contact:     anders AT knatten DOT org
" License:     This file is placed in the public domain.

let g:plugin_path = expand('<sfile>:p:h')

function! s:UsingPython3()
  if has('python3')
    return 1
  endif
    return 0
endfunction
let s:using_python3 = s:UsingPython3()
let s:python_until_eof = s:using_python3 ? "python3 << endpython" : "python << endpython"
let s:python_command = s:using_python3 ? "py3 " : "py "

function! SnippetySnip()
let saved_pos = getpos(".")
exec s:python_until_eof
lines = insert_snippets(vim.current.buffer)
vim.current.buffer[:] = None
vim.current.buffer[0] = lines[0] #It seems we cannot get rid of line 0 in previous command
for line in lines[1:]:
    vim.current.buffer.append(line)
endpython
call setpos(".", saved_pos)
endfunction

function! SnippetySnipPrintCurrentSnippetString()
    if exists("g:SnippetySnipArguments")
        let l:arguments = ':' . g:SnippetySnipArguments
    else
        let l:arguments = ''
    endif
    python vim.command("let l:snippetname='%s'" % get_current_snippet_name(vim.current.buffer, int(vim.eval("line('.')"))))
    echo '<!-- snippetysnip:' . fnamemodify(bufname('%'), ':p') . ':' . l:snippetname . arguments . ' -->'
endfunction

exec s:python_until_eof
import os
import vim
plugin_path = os.path.join(vim.eval("g:plugin_path"), "..", "..", "python")
sys.path.append(plugin_path)

from SnippetySnip.snippetysnip import insert_snippets, get_current_snippet_name
endpython
