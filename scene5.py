from manim import *
from config import *
from frisbee_base import FrisbeeBaseScene
from custom_mobjects import DashedArrow 
# Text.set_default(font="Kaiti") windows
Text.set_default(font="STKaiti")
class scene5(FrisbeeBaseScene):
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

        # scene2: frisbee and handler
        attackers = {}
        for i in range(2,8):
            attackers[i] = self.create_player(i,RED,WHITE)

        defender = {}
        for i in range(1,8):
            defender[i] = self.create_player(i,BLUE,WHITE)
        
        attackers_group = VGroup()
        for i in range(3,8):
            attackers_group.add(attackers[i])

        defenders_group = VGroup()
        for i in range(3, 8):
            defenders_group.add(defender[i])
        
        frisbee = Circle(radius=FRISBEE_RADIUS,color=WHITE)
        handler = self.create_player(1,RED,WHITE)

        handler.shift(np.array([0, -2.2, 0]))
        frisbee_position = self.get_frisbee_position(handler, RIGHT, frisbee)
        frisbee.move_to(frisbee_position)
        defender[1].next_to(handler,UL, buff=0.02)
        self.play(FadeIn(handler),FadeIn(frisbee),FadeIn(defender[1]))
        self.wait(0.5)

        # scene3
        direction_of_attack = DashedArrow(
            start = np.array([-3.5, 2.2, 0]),
            end = np.array([-3.5, 3.2, 0]),
            color=WHITE,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        )
        direction_of_attack_label = MathTex("Direction\ of\ attack", font_size=32).next_to(direction_of_attack, RIGHT)
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
        def update_position(mob):
            camera_center = self.camera.frame.get_center()
            offset=np.array([legend_with_bg_position[0],legend_with_bg_position[1],0])
            mob.move_to(camera_center + offset)
        # 添加updater
        legend_with_bg.add_updater(update_position)

        self.wait(2)

        # scene4: attackers and defenders
        self.wait(0.5)

        # 将2号攻击者移动到handler左边
        attackers[2].shift(np.array([-2.5,-1.4,0]))
        defender[2].next_to(attackers[2], UR,buff=0.02)

        # 显示2号攻击者
        self.play(FadeIn(attackers[2]))
        self.play(FadeIn(defender[2]))

        # 将攻击者排成一竖排，2号距离handler约8-10m，间隔2m
        self.position_attackers(handler, attackers, base_distance=1.7, interval=0.6)      
        self.position_defenders(attackers, defender,offset_x=0.5, offset_y=-0.4, interval=0.8)

        self.play(FadeIn(attackers_group))
        self.play(FadeIn(defenders_group))

        origin_pos_attacker = {}
        origin_pos_defender = {}
        for i in range(2, 8):
            origin_pos_attacker[i] = attackers[i].get_center()
            origin_pos_defender[i] = defender[i].get_center()
        origin_pos_attacker[1] = handler.get_center()
        origin_pos_defender[1] = defender[1].get_center()

        arr1=Arrow(
            start=origin_pos_attacker[6],
            end=np.array([1,1.2,0]),
            color=BLUE,
            buff=0,
            stroke_width=2,
            tip_length=0.2
        )
        label_arr1=MathTex("fake",font_size=32)
        label_arr1.next_to(arr1, RIGHT)
        self.play(Create(arr1))
        self.play(Write(label_arr1))
        self.wait(0.5)
        self.play(FadeOut(label_arr1),FadeOut(arr1))

        self.move_multiple_players([
            (attackers[6], np.array([1,1.2,0]), False),  # 第1个玩家
            (defender[6], np.array([1.4,1.2,0]), False)    # 第2个玩家
        ],
        run_time=1.5,
        path_type="straight",
        is_camera_follow=False 
        )
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

        pos2=attackers[6].get_center()
        arr2=Arrow(
            start=pos2,
            end=np.array([-2,1,0]),
            color=BLUE,
            buff=0,
            stroke_width=2,
            tip_length=0.2
        )
        pos3=frisbee.get_center()
        frisbee_arr=Arrow(
            start=pos3,
            end=np.array([-2,1,0]),
            color=ORANGE,
            buff=0,
            stroke_width=2,
            tip_length=0.2
        )
        around_break_label=MathTex("Around\ break",font_size=32)
        around_break_label.next_to(frisbee, LEFT)
        around_break_label_chinese=Text("反手跨步出盘",font_size=24)
        around_break_label_chinese.next_to(around_break_label, DOWN)
        self.play(Create(arr2))
        self.play(Create(frisbee_arr))
        self.play(Write(around_break_label))
        self.play(Write(around_break_label_chinese))
        self.wait(0.5)
        self.play(FadeOut(arr2),FadeOut(frisbee_arr),FadeOut(around_break_label),FadeOut(around_break_label_chinese))
        self.fly_frisbee(
            frisbee=frisbee,
            handler=handler,
            target_player=attackers[6],
            direction=DR,
            defender=defender[6],
            target_player_movement=np.array([-2,1,0]),
            defender_movement=np.array([-1.8,1.3,0]),
            is_camera_move=False,
            flight_type="straight",
            is_relative=False,
            run_time=1.5
        )

        line1=DashedLine(
            start=np.array([-2,1,0]),
            end=np.array([-1, 1,0]),
            color=BLUE,
            buff=0,
            stroke_width=2,
            tip_length=0.15
        )
        line2=DashedLine(
            start=np.array([0,-2.2,0]),
            end=np.array([-1, -2.2,0]),
            color=BLUE,
            buff=0,
            stroke_width=2,
            tip_length=0.15
        )
        double_arrow=self.double_arrow(
            start=np.array([-1, 1,0]),
            end=np.array([-1, -2.2,0]),
            color=BLUE,
            buff=0,
            stroke_width=2,
            tip_length=0.2
        )
        self.play(Create(line1),Create(line2))
        self.play(Create(double_arrow))
        self.wait(0.5)
        self.play(FadeOut(line1),FadeOut(line2),FadeOut(double_arrow))

        self.fly_frisbee(
            frisbee=frisbee,
            handler=attackers[6],
            target_player=handler,
            direction=LEFT,
            defender=defender[6],
            handler_movement=origin_pos_attacker[6],
            defender_movement=origin_pos_defender[6],
            is_camera_move=False,
            flight_type="straight",
            is_relative=False,
            run_time=1.5,
            highlight_player=False
        )

        handler_center  = handler.get_center()
        self.play(
            Rotate(
                frisbee,
                angle=PI,
                about_point=handler_center,
                run_time=1,
                rate_func=smooth
            )
        )
        posa3=attackers[3].get_center()
        arrow1=Arrow(
            start=attackers[3],
            end=posa3+LEFT,
            color=BLUE,
            buff=0,
            stroke_width=2,
            tip_length=0.2
        )
        arrow2=Arrow(
            start=frisbee,
            end=posa3+LEFT,
            color=ORANGE,
            buff=0,
            stroke_width=2,
            tip_length=0.2
        )
        forehand_inside=MathTex("Forehand\ inside",font_size=32)
        forehand_inside_chinese=Text("正手内侧",font_size=24)
        forehand_inside.next_to(frisbee,RIGHT)
        forehand_inside_chinese.next_to(forehand_inside,DOWN)
        self.play(Create(arrow1))
        self.play(Create(arrow2))
        self.play(Write(forehand_inside))
        self.play(Write(forehand_inside_chinese))
        self.wait(0.5)
        self.play(FadeOut(arrow1),FadeOut(arrow2),FadeOut(forehand_inside),FadeOut(forehand_inside_chinese))

        self.fly_frisbee(
            frisbee=frisbee,
            handler=handler,
            target_player=attackers[3],
            direction=DR,
            defender=defender[3],
            target_player_movement=posa3+LEFT,
            defender_movement=posa3+LEFT*0.5,
            is_camera_move=False,
            flight_type="straight",
            is_relative=False,
            run_time=1.5
        )

        self.wait(2)