from pgu import gui

class TimestepControl(gui.Table):


    def __init__(self, **params):
        gui.Table.__init__(self,**params)
    
        self.slider_year = 2012
        self.new_dataset = False

        def sliding(slider):
            self.new_dataset = True
            self.slider_year = slider.value

        fg = (0,0,0)

        self.tr()
        self.td(gui.Label("Year: ",color=fg),align=1)
        e = gui.HSlider(100,2012,2027,size=50,width=700,height=16,name='year ')
        e.connect(gui.CHANGE, sliding, e)
        self.td(e)

