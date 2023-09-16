from color import Color

class Theme:
    
    def __init__(self, light_bg, dark_bg, light_trace, dark_trace) -> None:
        self.bg = Color(light_bg, dark_bg)
        self.trace = Color(light_trace, dark_trace)