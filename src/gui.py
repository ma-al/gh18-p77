from pgu import gui

class TimestepControl(gui.Table):


    def __init__(self, **params):
        gui.Table.__init__(self,**params)
    
        self.slider_year = 2012
        self.new_dataset = False
        self.dataset = "aged_pops"
        self.service = False

        def sliding(slider):
            self.new_dataset = True
            self.slider_year = slider.value

        def switch_to_aged(button):
            self.new_dataset = True
            self.dataset = "aged_pops"

        def switch_to_total(button):
            self.new_dataset = True
            self.dataset = "total_pops"

        def toggle_services(button):
            self.new_dataset = True
            self.service = not self.service
            # print("toggled")

        fg = (0,0,0)

        self.tr()
        self.td(gui.Label("Year: ",color=fg),align=1)
        # e = gui.HSlider(100,2012,2015,size=50,width=700,height=16,name='year ')
        e = gui.HSlider(100,2012,2026,size=50,width=700,height=16,name='year ')
        e.connect(gui.CHANGE, sliding, e)
        self.td(e)

        self.tr()
        b = gui.Button("Aged Population", width=50)
        b.connect(gui.CLICK, switch_to_aged, None)
        self.td(b)

        b = gui.Button("Total Population", width=50)
        b.connect(gui.CLICK, switch_to_total, None)
        self.td(b)

        self.tr()

        b = gui.Button("Toggle Services", width=50)
        b.connect(gui.CLICK, toggle_services, None)
        self.td(b)
