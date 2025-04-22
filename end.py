from manim import *
from config import *
from frisbee_base import FrisbeeBaseScene
from custom_mobjects import DashedArrow 
# Text.set_default(font="Kaiti") windows
Text.set_default(font="STKaiti")
class end(FrisbeeBaseScene):
    def construct(self):
        center_text = Text(
            "感谢观看！",
            font_size=60)
        center_text_english=MathTex("Thank\ you\ for\ watching!",font_size=36)
        center_text_english.next_to(center_text, DOWN)
        self.play(Write(center_text),Write(center_text_english))
        self.wait(1)
        self.play(FadeOut(center_text),FadeOut(center_text_english))