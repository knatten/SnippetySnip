" Vim plugin for importing into a file selected lines from other files
" Version:     0.3
" Last change: 2011-08-28
" Author:      Anders Schau Knatten
" Contact:     anders AT knatten DOT org
" License:     This file is placed in the public domain.

function! SnippetySnip()
python << endpython
lines = insert_snippets(vim.current.buffer)
vim.current.buffer[:] = None
vim.current.buffer[0] = lines[0] #It seems we cannot get rid of line 0 in previous command
for line in lines[1:]:
    vim.current.buffer.append(line)
endpython
endfunction

python << endpython
import os
import vim
path = os.path.join(os.environ['HOME'], '.vim', 'python')
if not path in sys.path:
	sys.path.append(path)
from SnippetySnip.snippetysnip import insert_snippets
endpython
