from classes.Text import Text

class ETName(Text):
    
    def __init__(self, x=0, y=0, text=''):
        super().__init__(x, y, text, 'etname')
        
    def update(self, x=None, y=None, text=None):
        super().update(x, y, text)