from manim import *
from config import *
from frisbee_base import FrisbeeBaseScene
from custom_mobjects import DashedArrow 
# Text.set_default(font="Kaiti") windows
Text.set_default(font="STKaiti")
class RectangleAroundScene(FrisbeeBaseScene):
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
        frisbee = Circle(radius=FRISBEE_RADIUS,color=WHITE)
        handler = self.create_player(1,RED,WHITE)

        handler.shift(np.array([0, -2.8, 0]))
        frisbee_position = self.get_frisbee_position(handler, RIGHT, frisbee)
        frisbee.move_to(frisbee_position)
        self.play(FadeIn(handler))
        self.wait(1)
        self.play(FadeIn(frisbee))
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

        defender[1].next_to(handler,UL, buff=0.02)
        self.play(FadeIn(defender[1]))

        self.wait(0.5)

        # 将2号攻击者移动到handler左边
        attackers[2].shift(np.array([-2.5,-2.0,0]))
        defender[2].next_to(attackers[2], UR,buff=0.02)

        # 显示2号攻击者
        self.play(FadeIn(attackers[2]))

        subhandler=MathTex("Sub\ Handler",font_size=32)
        subhandler_chinese=Text("副持盘手",font_size=24)
        subhandler.next_to(attackers[2],DOWN)
        subhandler_chinese.next_to(subhandler,DOWN)
        self.play(Write(subhandler))
        self.play(Write(subhandler_chinese))
        self.wait(0.5)
        self.play(FadeOut(subhandler),FadeOut(subhandler_chinese))

        self.play(FadeIn(defender[2]))

        # 将攻击者排成一竖排，2号距离handler约8-10m，间隔2m
        self.position_attackers(handler, attackers, base_distance=2.3, interval=0.6)      
        self.position_defenders(attackers, defender,offset_x=0.5, offset_y=-0.4, interval=0.8)

        # 显示所有defenders
        self.play(Create(attackers[3]))

        arrow_8_10=self.double_arrow(
            start=attackers[3].get_center(),
            end=handler.get_center(),
            color=BLUE
        )
        self.play(Create(arrow_8_10))
        label_8_10=MathTex("10m",font_size=32).next_to(arrow_8_10[0],RIGHT)

        self.play(Write(label_8_10))
        self.wait(0.5)
        self.play(FadeOut(arrow_8_10),FadeOut(label_8_10))

        stack=MathTex("STACK!!",font_size=32)
        stack.next_to(attackers[3],RIGHT)
        self.play(Write(stack))
        self.wait(0.5)
        self.play(FadeOut(stack))

        for i in range(4, 8):
            self.play(Create(attackers[i]))
        
        arrow_2=self.double_arrow(
            start=attackers[3].get_center(),
            end=attackers[4].get_center(),
            color=BLUE
        )
        self.play(Create(arrow_2))
        label_2=MathTex("2m",font_size=32).next_to(arrow_2[0],RIGHT)
        self.play(Write(label_2))
        self.wait(0.5)
        self.play(FadeOut(arrow_2),FadeOut(label_2))

        self.play(FadeIn(defenders_group))
        
        self.wait(2)
        # 玩家同时移动，相机跟随
        self.fly_frisbee(
            frisbee,
            handler,
            attackers[7],
            LEFT,
            flight_type="left",
            run_time=1.5,
            arc_angle=PI/2,
            target_player_movement=UP * 2,
            vertical_only=True
        )

        self.wait(2)

        rewind_text = Tex("REWIND",font_size=36)
        rewind_re=Rectangle(color=BLUE)
        rewind_re.surround(rewind_text)
        group_rewind=VGroup(rewind_text,rewind_re)
        
        # 添加updater使其始终跟随相机中心
        def update_rewind_position(mob):
            # 获取当前相机中心在场景中的位置
            camera_center = self.camera.frame.get_center()
            # 让REWIND始终位于相机中心
            mob.move_to(camera_center)

        # 添加updater
        group_rewind.add_updater(update_rewind_position)

        # 显示REWIND
        self.play(FadeIn(group_rewind))

        # 执行飞盘动画，REWIND会自动跟随相机
        self.fly_frisbee(
            frisbee,
            attackers[7],
            handler,
            LEFT,
            handler_movement=DOWN * 2,
            flight_type="right",
            run_time=1.5,
            arc_angle=PI/2,
            vertical_only=True,
            target_camera_pos=ORIGIN,
            highlight_player=False
        )

        # 移除updater并淡出
        group_rewind.clear_updaters()
        self.play(FadeOut(group_rewind), run_time=1.5)

        self.fly_frisbee(
            frisbee,
            handler,
            attackers[7],
            RIGHT,
            handler_movement=RIGHT * 2,
            flight_type="left",
            run_time=1.5,
            arc_angle=PI/2,
            is_camera_move=False,
        )
        # 示例1：让攻击者向左移动1个单位，使用左弧线路径，相机垂直跟随
        self.move_player(attackers[6], LEFT, path_type="straight", run_time=1.5, is_camera_follow=True, vertical_only=True)

        # 示例2：移动到场地上的特定位置，相机完全跟随
        target_pos = np.array([2.0, 1.5, 0])
        self.move_player(handler, target_pos, path_type="straight",is_camera_follow=True, vertical_only=False)

        # 示例3：使用向量组合，让防守者向右上方移动，不跟随相机
        self.move_player(defender[5], RIGHT*2 + UP, path_type="straight", is_camera_follow=False)

        # 示例4：移动并高亮显示，自定义相机位置
        self.move_player(attackers[3], DOWN*3, highlight=True, is_camera_follow=True, target_camera_pos=np.array([0, -1, 0]))
        
        target_pos = np.array([-2, 8, 0])
        self.move_player(handler, target_pos, highlight=True, path_type="right", is_camera_follow=True, vertical_only=True)
        
        self.move_camera_to_player(attackers[7],vertical_only=True,run_time=1.5,target_camera_pos=None)

        self.fly_frisbee(frisbee,attackers[7],handler,LEFT,flight_type="left",run_time=1.5,arc_angle=PI/2,target_player_movement=DOWN * 2,is_camera_move=True,highlight_player=True)

        self.move_camera_to_player(
            attackers[7],
            vertical_only=True,
            run_time=1.5,
            target_camera_pos=None
        )

        self.wait(1)
        '''
        # 平滑地将相机中心移动到attackers[7]
        self.play(
            self.camera.frame.animate.move_to(attackers[7].get_center()),
            run_time=1.5  # 控制移动速度，数值越大越慢
        )
        
        # 添加updater让相机持续跟随attackers[7]
        self.camera.frame.add_updater(
            lambda frame, dt: frame.move_to(attackers[7].get_center())
        )


        def smooth_follow(frame, dt):
            # 平滑地跟随目标，interpolate_factor控制平滑程度(0-1之间)
            # 数值越小越平滑但跟随效果越滞后
            interpolate_factor = 0.1
            target_point = attackers[7].get_center()
            current_point = frame.get_center()
            new_point = current_point + (target_point - current_point) * interpolate_factor
            frame.move_to(new_point)

        # 使用平滑跟随函数
        self.camera.frame.add_updater(smooth_follow)
        
        # 当你想停止相机跟随时
        self.camera.frame.clear_updaters()
        # 现在attackers[7]移动不会再被跟随
        
        self.play(attackers[7].animate.shift(RIGHT * 2))
        '''

        # 将相机视角平滑地回到原点
        self.play(
            self.camera.frame.animate.move_to(ORIGIN),
            run_time=1.5  # 控制过渡速度
        )
        '''
        # 如果需要恢复到最初的帧大小
        self.play(
            self.camera.frame.animate.set_width(config.frame_width),
            self.camera.frame.animate.set_height(config.frame_height),
            run_time=1.0
        )
        '''
        self.wait(1)

        self.wait(1)

        self.wait(2)
        self.play(FadeOut(direction_of_attack), FadeOut(direction_of_attack_label),FadeOut(tuli_attackers), FadeOut(attackers_label),FadeOut(tuli_defender), FadeOut(defenders_label))