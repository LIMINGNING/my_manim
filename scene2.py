from manim import *
from config import *
from frisbee_base import FrisbeeBaseScene
from custom_mobjects import DashedArrow 
# Text.set_default(font="Kaiti") windows
Text.set_default(font="STKaiti")
class scene2(FrisbeeBaseScene):
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
        
        #scene2
        direction_of_attack = DashedArrow(
            start = np.array([-3.5, 2.2, 0]),
            end = np.array([-3.5, 3.2, 0]),
            color=WHITE,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        )
        direction_of_attack_label = MathTex("Direction of attack", font_size=32).next_to(direction_of_attack, RIGHT)
        direction_of_attack_label_chinese=Text("进攻方向", font_size=24).next_to(direction_of_attack_label, RIGHT)
        # play direction of attack
        self.play(Create(direction_of_attack))
        self.play(Write(direction_of_attack_label))
        self.play(Write(direction_of_attack_label_chinese))

        tuli_attackers = Circle(radius=PLAER_RADIUS,color=RED) 
        tuli_attackers.set_fill(color=RED,opacity=1)
        tuli_attackers.set_stroke(color=WHITE, width=2)

        tuli_defender = Circle(radius=PLAER_RADIUS,color=BLUE) 
        tuli_defender.set_fill(color=BLUE,opacity=1)
        tuli_defender.set_stroke(color=WHITE, width=2)

        tuli_attackers.next_to(direction_of_attack, DOWN)
        tuli_defender.next_to(tuli_attackers, DOWN)
        attackers_label = MathTex("Attackers", font_size=32).next_to(tuli_attackers, RIGHT)
        attackers_label_chinese=Text("进攻方", font_size=24).next_to(attackers_label, RIGHT)
        defenders_label = MathTex("Defenders", font_size=32).next_to(tuli_defender, RIGHT)
        defenders_label_chinese=Text("防守方", font_size=24).next_to(defenders_label, RIGHT)

        # play attackers and defenders label
        self.play(Create(tuli_attackers))
        self.play(Write(attackers_label))
        self.play(Write(attackers_label_chinese))
        self.play(Create(tuli_defender))
        self.play(Write(defenders_label))
        self.play(Write(defenders_label_chinese))
        self.wait(2)

        self.play(FadeOut(direction_of_attack_label_chinese),FadeOut(attackers_label_chinese),FadeOut(defenders_label_chinese))

        # fadeout chinese and transform
        tuli_attackers_label_suoxie= MathTex("A", font_size=32).next_to(tuli_attackers, RIGHT)
        tuli_defender_label_suoxie= MathTex("D", font_size=32).next_to(tuli_defender, RIGHT)
        direction_of_attack_label_suoxie= MathTex("DOA", font_size=32).next_to(direction_of_attack, RIGHT)
        self.play(Transform(direction_of_attack_label, direction_of_attack_label_suoxie))
        self.play(Transform(attackers_label, tuli_attackers_label_suoxie))
        self.play(Transform(defenders_label, tuli_defender_label_suoxie))

        legend_group = VGroup(
            direction_of_attack,
            direction_of_attack_label, 
            tuli_attackers,
            attackers_label,
            tuli_defender,
            defenders_label
        )

        legend_bg = SurroundingRectangle(legend_group, color=GREY, fill_opacity=0.1, buff=0.1)
        self.play(Create(legend_bg))
        legend_with_bg = VGroup(legend_bg, legend_group)

        # shift right 1.8
        self.play(legend_with_bg.animate.shift(np.array([-1.8, 0, 0])))

        legend_with_bg_position=legend_with_bg.get_center()
        def update_rewind_position(mob):
            camera_center = self.camera.frame.get_center()
            offset=np.array([legend_with_bg_position[0],legend_with_bg_position[1],0])
            mob.move_to(camera_center + offset)

        # 添加updater
        legend_with_bg.add_updater(update_rewind_position)
        self.wait(2)

        handler=Circle(radius=PLAER_RADIUS,color=YELLOW)
        handler.set_fill(color=YELLOW,opacity=1)
        self.play(Create(handler))
        self.move_player(handler, np.array([-4, 5.5, 0]), is_camera_follow=True, vertical_only=True)
        self.wait(2)
