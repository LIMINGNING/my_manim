from manim import *
from config import *
# 设置默认分辨率

GROUND_WIDTH = (config.frame_height - 0.1)*37/100
GROUND_LENGTH = config.frame_height - 0.1
BIGGER_GROUND = 1.5

class RectangleAroundScene(Scene):
    def construct(self):
        # 创建一个长方形，宽度为场景宽度，高度为场景高度
        rectangle = Rectangle(width=GROUND_WIDTH, height=GROUND_LENGTH, color=BLUE)
        dashed_line_up = DashedLine(start=LEFT * GROUND_WIDTH/2 + UP * GROUND_LENGTH*32/100,end=RIGHT * GROUND_WIDTH/2 + UP * GROUND_LENGTH*32/100)
        dashed_line_down = DashedLine(start=LEFT * GROUND_WIDTH/2 + DOWN * GROUND_LENGTH*32/100,end=RIGHT * GROUND_WIDTH/2 + DOWN * GROUND_LENGTH*32/100)
        
        Create(rectangle)
        Create(dashed_line_up)
        Create(dashed_line_down)
        shu_ground = VGroup(rectangle,dashed_line_up,dashed_line_down)

        rectangle1 = Rectangle(width=BIGGER_GROUND * GROUND_LENGTH,height=BIGGER_GROUND * GROUND_WIDTH,color=BLUE)
        
        dashed_line_Left = DashedLine(
            start = BIGGER_GROUND * LEFT * GROUND_LENGTH*32/100 + BIGGER_GROUND * UP * GROUND_WIDTH/2,
            end = BIGGER_GROUND * LEFT * GROUND_LENGTH*32/100 + BIGGER_GROUND * DOWN * GROUND_WIDTH/2)
        dashed_line_Right = DashedLine(
            start = BIGGER_GROUND * RIGHT * GROUND_LENGTH*32/100 + BIGGER_GROUND * UP * GROUND_WIDTH/2,
            end = BIGGER_GROUND * RIGHT * GROUND_LENGTH*32/100 + BIGGER_GROUND * DOWN * GROUND_WIDTH/2)
        width_label = MathTex("37m",font_size = 36).next_to(dashed_line_Left, RIGHT)  # 在上方标记长度
        length_label = MathTex("64m",font_size = 36).next_to(rectangle1,DOWN)
        depth_label = MathTex("18m",font_size = 36).next_to(rectangle1,DOWN)
        depth_label.shift(LEFT *  GROUND_LENGTH * 0.6)

        heng_ground = VGroup(rectangle1,dashed_line_Left,dashed_line_Right)


        # 将视角调整为刚好显示该长方形
        self.camera.frame_width = config.frame_width
        self.camera.frame_height = config.frame_height
        self.camera.frame_center = ORIGIN  # 调整相机中心
        
        self.play(Create(rectangle1))
        self.wait(0.5)
        self.play(Create(dashed_line_Left),run_time = 0.5)
        self.play(Create(dashed_line_Right),run_time = 0.5)
        self.play(Create(width_label))
        self.play(Create(length_label))
        self.play(Create(depth_label))
        
        self.wait()
 
        self.play(FadeOut(width_label), FadeOut(length_label), FadeOut(depth_label))
        self.play(heng_ground.animate.rotate(-PI/2))
        self.play(heng_ground.animate.scale(2))  # 放大两倍

        jingongfangxiang = Arrow(
            start = np.array([-3, 2, 0]),
            end = np.array([-3, 3, 0]),
            color=WHITE,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        )
        jingongfangxiang_label = Tex("Direction of attack", font_size=36).next_to(jingongfangxiang, RIGHT)
        self.play(Create(jingongfangxiang))
        self.play(Write(jingongfangxiang_label))

        frisbee = Circle(radius=0.1,color=WHITE)
        handler = self.create_circle(1,RED)
        handler.shift(np.array([0, -2.5, 0]))
        frisbee.next_to(handler,direction=UR,buff=-0.05)
        self.play(FadeIn(handler))
        self.play(FadeIn(frisbee))

        self.wait(2)

    def create_circle(self,number,color,text_color=WHITE):
        circle = Circle(radius=0.2,color=color)
        circle.set_fill(color=color,opacity=1)
        number_text = Text(str(number),font_size=24,color=text_color)
        number_text.move_to(circle.get_center())
        return VGroup(circle, number_text)