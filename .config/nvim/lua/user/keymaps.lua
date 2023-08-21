local opts = { noremap = true, silent = true }
local keymap = vim.api.nvim_set_keymap

local function nkeymap(key, map, options)
    keymap("n", key, map, options)
end

keymap("", "<Space>", "<Nop>", opts)
keymap("i", "<C-j>", "<Nop>", opts)
keymap("i", "<C-k>", "<Nop>", opts)
vim.g.mapleader = " "
vim.g.maplocalleader = " "

nkeymap("<C-h>", "<C-w>h", opts)
nkeymap("<C-j>", "<C-w>j", opts)
nkeymap("<C-k>", "<C-w>k", opts)
nkeymap("<C-l>", "<C-w>l", opts)
nkeymap("<C-d>", "<C-d>zz", opts)
nkeymap("<C-u>", "<C-u>zz", opts)
nkeymap("<Esc>", ":noh<Cr>", opts)

keymap("v", "<", "<gv", opts)
keymap("v", ">", ">gv", opts)

nkeymap("<leader>e", ":NvimTreeToggle<CR>", opts)
