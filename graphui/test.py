import pygame
from App import App
from Widget import Widget

def test():
    a = App()
    w = Widget()
    
    w.text = 'moshe'
    w.font_size.final=50
    
    a.add_widget(w)
    
    a.run()

if __name__=='__main__':
    test()
