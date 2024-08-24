local lsp_zero = require('lsp-zero')

lsp_zero.on_attach(function(client, bufnr)
  -- see :help lsp-zero-keybindings
  -- to learn the available actions
  lsp_zero.default_keymaps({buffer = bufnr})
end)

-- to learn how to use mason.nvim
-- read this: https://github.com/VonHeikemen/lsp-zero.nvim/blob/v3.x/doc/md/guides/integrate-with-mason-nvim.md
require('mason').setup({})
require('mason-lspconfig').setup({
  ensure_installed = {},
  handlers = {
    function(server_name)
      require('lspconfig')['lua_ls'].setup({})
      require('lspconfig')['basedpyright'].setup({})
    end,
  },
})

require('mason-tool-installer').setup({
    --Install these linters, formatters, debuggers automatically
    ensure_installed = {
        'black',
        'debugpy',
        'flake8',
        'isort',
        'mypy',
        'pylint',
    }
})
