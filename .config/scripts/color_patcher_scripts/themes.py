from color_template_lib import Color

themes: dict[str, dict[Color, str]] = {
    "nightsky" : {
        Color.LIGHT_RED :   '#FFCFD6',
        Color.YELLOW :      '#FFFF82',
        Color.LIGHT_GREEN : '#84FF7D',
        Color.LIGHT_TEAL :  '#86F6FF',
        Color.LIGHT_BLUE :  '#67C1FF',
        Color.LIGHT_PURPLE :'#8391F7',

        Color.RED :         '#FF3571',
        # Color.ORANGE :      '#FF6571',
        # Color.ORANGE :      '#F6791E',
        Color.ORANGE :      '#F08B42',
        Color.GREEN :       '#63C12A',
        Color.TEAL :        '#82F0F2',
        Color.BLUE :        '#0F81D5',
        Color.PURPLE :      '#D07CFF',
        Color.PINK :        '#F872DC',

        Color.TEXT :        '#DFEFF5',
        Color.TEXT_DARKER : '#949FA4',
        Color.TEXT_DARK :   '#4A5052',

        Color.BACKGROUND_8 :'#404E69',
        Color.BACKGROUND_7 :'#34435E',
        Color.BACKGROUND_6 :'#293854',
        Color.BACKGROUND_5 :'#202F4A',
        Color.BACKGROUND_4 :'#182640',
        Color.BACKGROUND_3 :'#111E36',
        Color.BACKGROUND_2 :'#0B162B',
        Color.BACKGROUND_1 :'#061021',
        Color.BACKGROUND_0 :'#030A17',

        Color.ACCENT :      '#67C1FF',
    },
    "catppuccin-mocha": {
        Color.LIGHT_RED :   '#F5E0DC',
        Color.YELLOW :      '#F9E2AF',
        Color.LIGHT_GREEN : '#A6E3A1',
        Color.LIGHT_TEAL :  '#74C7EC',
        Color.LIGHT_BLUE :  '#89DCEB',
        Color.LIGHT_PURPLE :'#B4BEFE',

        Color.RED :         '#F38BA8',
        Color.ORANGE :      '#FAB387',
        Color.GREEN :       '#A6E3A1',
        Color.TEAL :        '#94E2D5',
        Color.BLUE :        '#89B4FA',
        Color.PURPLE :      '#CBA6F7',
        Color.PINK :        '#F5E0DC',

        Color.TEXT :        '#CDD6F4',
        Color.TEXT_DARKER : '#BAC2DE',
        Color.TEXT_DARK :   '#A6ADC8',

        Color.BACKGROUND_8 :'#9399B2',
        Color.BACKGROUND_7 :'#7F849C',
        Color.BACKGROUND_6 :'#6C7086',
        Color.BACKGROUND_5 :'#585B70',
        Color.BACKGROUND_4 :'#45475A',
        Color.BACKGROUND_3 :'#313244',
        Color.BACKGROUND_2 :'#1E1E2E',
        Color.BACKGROUND_1 :'#181825',
        Color.BACKGROUND_0 :'#11111B',

        Color.ACCENT :      '#89DCEB',
    },
    "debug" : {
        Color.LIGHT_RED :   '#FF0000',
        Color.YELLOW :      '#FF6571',
        Color.LIGHT_GREEN : '#00FF00',
        Color.LIGHT_TEAL :  '#00FFFF',
        Color.LIGHT_BLUE :  '#0000FF',
        Color.LIGHT_PURPLE :'#7700FF',

        Color.RED :         '#770000',
        Color.ORANGE :      '#770077',
        Color.GREEN :       '#007700',
        Color.TEAL :        '#007777',
        Color.BLUE :        '#000077',
        Color.PURPLE :      '#770077',
        Color.PINK :        '#FF00FF',

        Color.TEXT :        '#FFFFFF',
        Color.TEXT_DARKER : '#777777',
        Color.TEXT_DARK :   '#000000',

        Color.BACKGROUND_8 :'#FFFFFF',
        Color.BACKGROUND_7 :'#EEEEEE',
        Color.BACKGROUND_6 :'#CCCCCC',
        Color.BACKGROUND_5 :'#AAAAAA',
        Color.BACKGROUND_4 :'#888888',
        Color.BACKGROUND_3 :'#666666',
        Color.BACKGROUND_2 :'#444444',
        Color.BACKGROUND_1 :'#222222',
        Color.BACKGROUND_0 :'#000000',

        Color.ACCENT :      '#ff0000',
    },
}

