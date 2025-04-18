from manim import *
from config import *

class people(Scene):
    def constuct(self):
        frisbee = self.create_circle(WHITE,0)
        handler = self.create_circle(RED,1)
        frisbee.next_to(handler,RIGHT)

        self.play(FadeIn(handler))
        self.play(FadeIn(frisbee))

        self.wait(2)

    def create_circle(self,color,opacity):
        circle = Circle(radius=0.2,color=color)
        circle.set_fill(color=color,opacity=opacity)
        return circle