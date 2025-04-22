from manim import *
from config import *
from frisbee_base import FrisbeeBaseScene
from custom_mobjects import DashedArrow 
# Text.set_default(font="Kaiti") windows
Text.set_default(font="STKaiti")
class scene1(FrisbeeBaseScene):
    def construct(self):
        '''
        # 使用方法
        camera_grid = create_camera_grid(self)
        self.add(camera_grid)
        '''
        # 创建一个长方形，宽度为场景宽度，高度为场景高度
        '''
        rectangle = Rectangle(width=GROUND_WIDTH, height=GROUND_LENGTH, color=BLUE)
        dashed_line_up = DashedLine(start=LEFT * GROUND_WIDTH/2 + UP * GROUND_LENGTH*32/100,end=RIGHT * GROUND_WIDTH/2 + UP * GROUND_LENGTH*32/100)
        dashed_line_down = DashedLine(start=LEFT * GROUND_WIDTH/2 + DOWN * GROUND_LENGTH*32/100,end=RIGHT * GROUND_WIDTH/2 + DOWN * GROUND_LENGTH*32/100)
        
        Create(rectangle)
        Create(dashed_line_up)
        Create(dashed_line_down)
        shu_ground = VGroup(rectangle,dashed_line_up,dashed_line_down)
        
        # 添加网格作为参考
        grid1 = NumberPlane(x_range=[-6, 6], y_range=[-4, 4])
        self.add(grid1)
        '''
        
        # scene1
        rectangle1 = Rectangle(width=GROUND_RATIO * GROUND_LENGTH,height=GROUND_RATIO * GROUND_WIDTH,color=BLUE)
        
        dashed_line_Left = DashedLine(
            start = GROUND_RATIO * LEFT * GROUND_LENGTH*32/100 + GROUND_RATIO * UP * GROUND_WIDTH/2,
            end = GROUND_RATIO * LEFT * GROUND_LENGTH*32/100 + GROUND_RATIO * DOWN * GROUND_WIDTH/2)
        dashed_line_Right = DashedLine(
            start = GROUND_RATIO * RIGHT * GROUND_LENGTH*32/100 + GROUND_RATIO * UP * GROUND_WIDTH/2,
            end = GROUND_RATIO * RIGHT * GROUND_LENGTH*32/100 + GROUND_RATIO * DOWN * GROUND_WIDTH/2)
        
        self.play(Create(rectangle1))
        self.wait(0.5)
        self.play(Create(dashed_line_Left),run_time = 0.5)
        self.play(Create(dashed_line_Right),run_time = 0.5)

        heng_ground = VGroup(rectangle1,dashed_line_Left,dashed_line_Right)
        
        self.play(heng_ground.animate.rotate(-PI/2))
        self.play(heng_ground.animate.shift(DOWN * 2))
        self.play(heng_ground.animate.scale(2))  # 放大两倍
        
        # scene2: frisbee and handler
        frisbee = Circle(radius=FRISBEE_RADIUS,color=WHITE)
        handler = self.create_player(1,RED,WHITE)

        handler.shift(np.array([0, -2.2, 0]))
        frisbee_position = self.get_frisbee_position(handler, LEFT, frisbee)
        frisbee.move_to(frisbee_position)
        self.play(FadeIn(handler))

        self.wait(0.5)

        handler_label=MathTex("Handler",font_size=32)
        handler_label.next_to(handler,RIGHT)
        handler_label_chinese=Text("持盘者",font_size=24)
        handler_label_chinese.next_to(handler_label,UP)
        self.play(Write(handler_label))
        self.play(Write(handler_label_chinese))
        self.wait(0.5)

        self.play(FadeIn(frisbee))

        frisbee_label=MathTex("Frisbee",font_size=32)
        frisbee_label.next_to(frisbee,LEFT)
        frisbee_label_chinese=Text("飞盘",font_size=24)
        frisbee_label_chinese.next_to(frisbee_label,UP)
        self.play(Write(frisbee_label))
        self.play(Write(frisbee_label_chinese))
        self.wait(0.5)
        self.play(FadeOut(handler_label_chinese),FadeOut(frisbee_label_chinese))
        self.play(FadeOut(handler_label),FadeOut(frisbee_label))

        self.wait(2)

        defender = {}
        for i in range(1,8):
            defender[i] = self.create_player(i,BLUE,WHITE)

        defender[1].next_to(handler,UL, buff=0.02)
        self.play(FadeIn(defender[1]))

        self.wait(0.5)
        force_forehand_defence=MathTex("Force\ Forehand",font_size=32)
        force_forehand_defence_chinese=Text("逼迫正手",font_size=24)
        force_forehand_defence.next_to(defender[1],UP)
        force_forehand_defence_chinese.next_to(force_forehand_defence,RIGHT)
        self.play(Write(force_forehand_defence))
        self.play(Write(force_forehand_defence_chinese))
        self.wait(1)
        self.play(FadeOut(force_forehand_defence),FadeOut(force_forehand_defence_chinese))

        # breakside
        rectangle_breakside = Rectangle(width=GROUND_RATIO * GROUND_WIDTH,height=2.6*2,color=BLUE)
        rectangle_breakside.set_fill(color=RED,opacity=0.5)
        rectangle_breakside.shift(np.array([-GROUND_RATIO * GROUND_WIDTH/2, 0.4, 0]))
        self.play(FadeIn(rectangle_breakside))

        breakside_label = MathTex("Breakside",font_size=32)
        breakside_label_chinese=Text("反手侧",font_size=24)
        breakside_label.move_to(rectangle_breakside.get_center())
        breakside_label_chinese.next_to(breakside_label,DOWN)
        self.play(Write(breakside_label))
        self.play(Write(breakside_label_chinese))
        self.wait(0.5)

        # rotate frisbee
        handler_center  = handler.get_center()
        self.play(
            Rotate(
                frisbee,
                angle=-PI,
                about_point=handler_center,
                run_time=1,
                rate_func=smooth
            )
        )

        self.play(FadeOut(rectangle_breakside),FadeOut(breakside_label),FadeOut(breakside_label_chinese))

        # openside
        rectangle_openside = Rectangle(width=GROUND_RATIO * GROUND_WIDTH,height=2.6*2,color=BLUE)
        rectangle_openside.set_fill(color=BLUE,opacity=0.5)
        rectangle_openside.shift(np.array([GROUND_RATIO * GROUND_WIDTH/2, 0.4, 0]))
        self.play(FadeIn(rectangle_openside))

        openside_label = MathTex("Open side",font_size=32)
        openside_label_chinese=Text("正手侧",font_size=24)
        openside_label.move_to(rectangle_openside.get_center())
        openside_label_chinese.next_to(openside_label,DOWN)
        self.play(Write(openside_label))
        self.play(Write(openside_label_chinese))
        self.wait(0.5)

        self.play(FadeOut(rectangle_openside),FadeOut(openside_label),FadeOut(openside_label_chinese))
        self.wait(2)