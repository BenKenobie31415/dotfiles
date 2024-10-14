-- function SetColors(color)
-- 	color = color or "catppuccin-mocha"
-- 	vim.cmd.colorscheme(color)
--
-- 	vim.api.nvim_set_hl(0, "Normal", { bg = "none" })
-- 	vim.api.nvim_set_hl(0, "NormalFloat", { bg = "none" })
--
-- end
--
-- SetColors()
require("catppuccin").setup({
    flavour = "mocha", -- latte, frappe, macchiato, mocha
    background = { -- :h background
        light = "latte",
        dark = "mocha",
    },
    transparent_background = true,
    show_end_of_buffer = true, -- show the '~' characters after the end of buffers
    term_colors = false,
    dim_inactive = {
        enabled = false,
        shade = "dark",
        percentage = 0.15,
    },
    no_italic = false, -- Force no italic
    no_bold = false, -- Force no bold
    styles = {
        comments = { "italic" },
        conditionals = { "italic" },
        loops = {},
        functions = {},
        keywords = {},
        strings = {},
        variables = {},
        numbers = {},
        booleans = {},
        properties = {},
        types = {},
        operators = {},
    },
    color_overrides = {
        mocha = {
            -- text = "[text]",
            -- base = "[background_0]",
            -- crust = "[background_1]",
            -- mantle = "[background_2]",
            --
            -- rosewater = "[light_red]",
            -- flamingo = "[light_red]",
            -- pink = "[pink]",
            -- mauve = "[light_purple]",
            -- red = "[red]",
            -- maroon = "[orange]",
            -- peach = "[orange]",
            -- yellow = "[yellow]",
            -- green = "[light_green]",
            -- teal = "[teal]",
            -- sky = "[light_blue]",
            -- sapphire = "[light_teal]",
            -- blue = "[light_blue]",
            -- lavender = "[light_teal]",
        }
    },
    custom_highlights = {},
    integrations = {
        cmp = true,
        gitsigns = true,
        nvimtree = true,
        telescope = true,
        notify = false,
        mini = false,
        -- For more plugins integrations please scroll down (https://github.com/catppuccin/nvim#integrations)
    },
})

-- setup must be called before loading
vim.cmd.colorscheme "catppuccin"

