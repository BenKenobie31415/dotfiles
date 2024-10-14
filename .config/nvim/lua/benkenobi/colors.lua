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
            -- text = "#DFEFF5",
            -- base = "#030A17",
            -- crust = "#061021",
            -- mantle = "#0B162B",
            --
            -- rosewater = "#FFCFD6",
            -- flamingo = "#FFCFD6",
            -- pink = "#F872DC",
            -- mauve = "#8391F7",
            -- red = "#FF3571",
            -- maroon = "#F08B42",
            -- peach = "#F08B42",
            -- yellow = "#FFFF82",
            -- green = "#84FF7D",
            -- teal = "#82F0F2",
            -- sky = "#67C1FF",
            -- sapphire = "#86F6FF",
            -- blue = "#67C1FF",
            -- lavender = "#86F6FF",
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

