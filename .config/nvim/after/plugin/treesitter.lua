local ok, configs = pcall(require, "nvim-treesitter.configs")
if not ok then
    return
end

configs.setup({
    ensure_installed = { "lua", "python", "json", "css", "java" },
	sync_install = false,
	auotpairs = {
		enable = true,
    },
	highlight = {
		enable = true,
		additional_vim_regex_highlighting = false,
    },
	context_commentstring = {
		enable = true,
		enable_autocmd = false,
    },
})
