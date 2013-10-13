" Vim plugin for importing into a file selected lines from other files
" Version:     1.0
" Last change: 2013-10-13
" Author:      Anders Schau Knatten
" Contact:     anders AT knatten DOT org
" License:     This file is placed in the public domain.

function! SnippetySnip()
let saved_pos = getpos(".")
python << endpython
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

python << endpython
import os
import vim
path = os.path.join(os.environ['HOME'], '.vim', 'python')
if not path in sys.path:
	sys.path.append(path)
from SnippetySnip.snippetysnip import insert_snippets, get_current_snippet_name
endpython
