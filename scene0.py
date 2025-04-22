from manim import *
from config import *
from frisbee_base import FrisbeeBaseScene

Text.set_default(font="STKaiti")

class scene0(FrisbeeBaseScene):
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
        '''
        # 添加网格作为参考
        grid1 = NumberPlane(x_range=[-6, 6], y_range=[-4, 4])
        self.add(grid1)
        
        # scene0
        # 中央大标题
        center_text = Text(
            "飞盘战术分析",
            font_size=60)
        UD_text = Text(
            "李明柠",
            font_size=45)
        UD_text.shift(DOWN * 2 + RIGHT * 3)
        # 先显示中央标题
        self.play(Write(center_text),Write(UD_text))
        self.wait(1)
        self.play(FadeOut(center_text),FadeOut(UD_text))

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

        central_zone=MathTex("Central Zone",font_size=36)
        central_zone_chinese=Text("中场区域",font_size=34).next_to(central_zone, DOWN)
        end_zone=MathTex("End Zone",font_size=36).next_to(dashed_line_Left,LEFT)
        end_zone_chinese=Text("底线区域",font_size=34).next_to(end_zone, DOWN)
        end_zone1=MathTex("End Zone",font_size=36).next_to(dashed_line_Right,RIGHT)
        end_zone1_chinese=Text("底线区域",font_size=34).next_to(end_zone1, DOWN)

        self.play(Write(central_zone))
        self.play(Write(central_zone_chinese))
        self.play(Write(end_zone))
        self.play(Write(end_zone_chinese))
        self.play(Write(end_zone1))
        self.play(Write(end_zone1_chinese))
        self.wait(1)

        self.play(FadeOut(central_zone),FadeOut(central_zone_chinese),FadeOut(end_zone),FadeOut(end_zone_chinese),FadeOut(end_zone1),FadeOut(end_zone1_chinese))

        
        double_arrow_ground_width=self.double_arrow(
            start = dashed_line_Left.get_start() + LEFT * 0.3,
            end = dashed_line_Left.get_end() + LEFT * 0.3,
            color=BLUE,
            stroke_width=2,
            tip_length=0.15,
            buff=0
        )
        self.play(FadeIn(double_arrow_ground_width))
        width_label = MathTex("37m",font_size = 36).next_to(double_arrow_ground_width[0], LEFT)  # 在上方标记长度
        self.play(Create(width_label))

        double_arrow_ground_length=self.double_arrow(
            start = dashed_line_Left.get_end() + DOWN * 0.3,
            end = dashed_line_Right.get_end() + DOWN * 0.3,
            color=BLUE,
            stroke_width=2,
            tip_length=0.15,
            buff=0
        )
        self.play(FadeIn(double_arrow_ground_length))
        length_label = MathTex("64m",font_size = 36).next_to(double_arrow_ground_length[0],DOWN)
        self.play(Create(length_label))

        double_arrow_ground_depth=self.double_arrow(
            start=GROUND_RATIO * GROUND_LENGTH * LEFT/2 + GROUND_RATIO * DOWN * GROUND_WIDTH/2 + DOWN * 0.3,
            end=dashed_line_Left.get_end() + DOWN * 0.3,
            color=BLUE,
            stroke_width=2,
            tip_length=0.15,
            buff=0
        )
        self.play(FadeIn(double_arrow_ground_depth))
        depth_label = MathTex("18m",font_size = 36).next_to(double_arrow_ground_depth[0],DOWN)
        self.play(Create(depth_label))


        heng_ground = VGroup(rectangle1,dashed_line_Left,dashed_line_Right)

        self.wait(2)

        brick_mark_left = Cross(stroke_color=BLUE, stroke_width=2,scale_factor=0.1)
        brick_mark_left.shift(np.array([-GROUND_RATIO * GROUND_LENGTH*14/100, 0, 0]))
        brick_mark_right = Cross(stroke_color=BLUE, stroke_width=2,scale_factor=0.1)
        brick_mark_right.shift(np.array([GROUND_RATIO * GROUND_LENGTH*14/100, 0, 0]))
        self.play(Create(brick_mark_left))
        self.play(Create(brick_mark_right))

        brick_mark_name=MathTex("Brick Mark",font_size=36).next_to(brick_mark_left, DOWN)
        brick_mark_name_chinese=Text("砖头点",font_size=34).next_to(brick_mark_name, DOWN)
        self.play(Write(brick_mark_name))
        self.play(Write(brick_mark_name_chinese))

        dashed_line_pos = GROUND_RATIO * LEFT * GROUND_LENGTH*32/100
        # 砖块左边位置
        brick_left_pos = brick_mark_left.get_center()
        double_arrow_brick_left_length = self.double_arrow(
            start = dashed_line_pos,
            end = brick_left_pos,
            color=BLUE,
            stroke_width=2,
            tip_length=0.15,
            buff=0
        )
        self.play(FadeIn(double_arrow_brick_left_length))

        brick_label = MathTex("18m",font_size=36)
        brick_label.next_to(double_arrow_brick_left_length[0], UP)
        self.play(Write(brick_label))

        self.wait()
 
        self.play(FadeOut(width_label), FadeOut(length_label), FadeOut(depth_label),FadeOut(brick_label)
                ,FadeOut(double_arrow_ground_width[0]), FadeOut(double_arrow_ground_width[1]), FadeOut(double_arrow_ground_length[0]), FadeOut(double_arrow_ground_length[1]), FadeOut(double_arrow_ground_depth[0]), FadeOut(double_arrow_ground_depth[1]),FadeOut(double_arrow_brick_left_length[0]), FadeOut(double_arrow_brick_left_length[1]),FadeOut(brick_mark_name), FadeOut(brick_mark_name_chinese))
        self.play(FadeOut(brick_mark_left), FadeOut(brick_mark_right))
        self.play(heng_ground.animate.rotate(-PI/2))
        self.play(heng_ground.animate.shift(DOWN * 2))
        self.play(heng_ground.animate.scale(2))  # 放大两倍

        self.wait(2)