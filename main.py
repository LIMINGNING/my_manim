from manim import *
from config import *
from frisbee_base import FrisbeeBaseScene
from custom_mobjects import DashedArrow 
# Text.set_default(font="Kaiti") windows
Text.set_default(font="STKaiti")
class RectangleAroundScene(FrisbeeBaseScene):
    def move_player_and_fly_frisbee(self, frisbee, handler, target_player, defender_to_move, 
                               attacker_target_pos, defender_target_pos, direction=RIGHT,
                               flight_type="straight", run_time=1.5, is_relative=False, arc_angle=PI/2):
            """同时执行飞盘飞行和防守者移动的动画"""
            
            # 计算飞盘路径
            start_point = frisbee.get_center()
            
            # 计算终点和路径
            future_player = target_player.copy()
            if is_relative:
                future_player.shift(attacker_target_pos)
            else:
                future_player.move_to(attacker_target_pos)
            
            end_point = self.get_frisbee_position(future_player, direction, frisbee)
            
            # 创建飞盘路径
            if flight_type == "left":
                frisbee_path = ArcBetweenPoints(start_point, end_point, angle=-arc_angle)
            elif flight_type == "right":
                frisbee_path = ArcBetweenPoints(start_point, end_point, angle=arc_angle)
            else:
                frisbee_path = Line(start_point, end_point)
            
            # 创建防守者路径
            defender_start = defender_to_move.get_center()
            defender_end = defender_target_pos
            defender_path = Line(defender_start, defender_end)
            
            # 执行所有动画
            self.play(
                MoveAlongPath(frisbee, frisbee_path),
                target_player.animate.move_to(attacker_target_pos),
                MoveAlongPath(defender_to_move, defender_path),
                run_time=run_time,
                rate_func=smooth
            )
            
            # 确保对象在正确位置
            frisbee.move_to(end_point)
            target_player.move_to(attacker_target_pos)
            defender_to_move.move_to(defender_end)
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
        self.position_attackers(handler, attackers, base_distance=1.7, interval=0.6)      
        self.position_defenders(attackers, defender,offset_x=0.5, offset_y=-0.4, interval=0.8)

        origin_pos_attacker = {}
        origin_pos_defender = {}
        for i in range(2, 8):
            origin_pos_attacker[i] = attackers[i].get_center()
            origin_pos_defender[i] = defender[i].get_center()
        origin_pos_attacker[1] = handler.get_center()
        origin_pos_defender[1] = defender[1].get_center()


        # 显示所有defenders
        self.play(Create(attackers[3]))

        arrow_8_10=self.double_arrow(
            start=attackers[3].get_center(),
            end=handler.get_center(),
            color=BLUE
        )
        self.play(Create(arrow_8_10))
        label_8_10=MathTex("8\sim 10m",font_size=32).next_to(arrow_8_10[0],RIGHT)

        self.play(Write(label_8_10))
        self.wait(0.5)
        self.play(FadeOut(arrow_8_10),FadeOut(label_8_10))

        stack=MathTex("STACK!!",font_size=32)
        stack.next_to(attackers[3],RIGHT)
        self.play(Write(stack))
        self.wait(1)
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

        # scene5
        # 玩家同时移动，相机跟随

        self.wait(1)
        '''
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
        

        # 移除updater并淡出
        group_rewind.clear_updaters()
        self.play(FadeOut(group_rewind), run_time=1.5)
        '''

        openside=Circle(radius=1,color=YELLOW)
        openside.move_to(np.array([2.2, -0.5, 0]))
        openside_label=MathTex("Open\ Side",font_size=32).move_to(np.array([2.2, -0.5, 0]))
        self.play(Create(openside),Create(openside_label))
        self.wait(0.5)

        arrow_connot_go=Arrow(
            start=attackers[7].get_center(),
            end=np.array([2.2, -0.5, 0]),
            color=RED,
            buff=0,
            stroke_width=2,
            tip_length=0.15
        )
        arrow_frisbee_go=Arrow(
            start=handler.get_center(),
            end=np.array([2.2, -0.5, 0]),
            color=ORANGE,
            buff=0,
            stroke_width=2,
            tip_length=0.15
        )
        label_connot_go=MathTex("Hard\ to\ go",font_size=32).next_to(arrow_connot_go,RIGHT)
        self.play(Create(arrow_connot_go))
        self.play(Create(arrow_frisbee_go))
        self.wait(1)
        self.play(Write(label_connot_go))
        self.wait(1)
        self.play(FadeOut(arrow_connot_go),FadeOut(arrow_frisbee_go),FadeOut(label_connot_go),FadeOut(openside),FadeOut(openside_label))

        arrow1=Arrow(
            start=attackers[7].get_center(),
            end=np.array([1.5, 2.2, 0]),
            color=BLUE,
            buff=0,
            stroke_width=2,
            tip_length=0.15
        )
        self.play(Create(arrow1))
        self.wait(0.5)
        self.play(FadeOut(arrow1))

        # 1. 计算attackers[7]移动后的位置
        attacker_target_pos = np.array([1.5, 2.2, 0])
        # 2. 创建临时对象并移动到目标位置
        temp_attacker = attackers[7].copy()
        temp_attacker.move_to(attacker_target_pos)
        # 3. 使用临时对象计算defender位置
        temp_defender = defender[7].copy()
        temp_defender.next_to(temp_attacker, UP, buff=0.1)
        defender_target_pos = temp_defender.get_center()
        # 示例：同时移动攻击者和防守者
        # 4. 同时移动两个对象到计算好的位置
        self.move_multiple_players([
            (attackers[7], attacker_target_pos, False),
            (defender[7], defender_target_pos, False)
        ], run_time=1.5)

        self.wait(0.5)
        arrow2=Arrow(
            start=attackers[7].get_center(),
            end=np.array([2.5, 0.5, 0]),
            color=BLUE,
            buff=0,
            stroke_width=2,
            tip_length=0.15
        )

        arrow3=Arrow(
            start=handler.get_center(),
            end=np.array([2.5, 0.5, 0]),
            color=ORANGE,
            buff=0,
            stroke_width=2,
            tip_length=0.15
        )
        self.play(Create(arrow2),Create(arrow3))
        self.wait(0.5)
        self.play(FadeOut(arrow2),FadeOut(arrow3))

        pos1=np.array([2.5, 0.5, 0])
        temp_attacker.move_to(pos1)
        temp_defender.next_to(temp_attacker, UL, buff=0.01)
        defender_target_pos = temp_defender.get_center()

        self.fly_frisbee(
            frisbee=frisbee,
            handler=handler,
            target_player=attackers[7],
            direction=RIGHT,
            defender=defender[7],
            target_player_movement=pos1,
            defender_movement=defender_target_pos,
            is_camera_move=False,
            flight_type="straight",
            is_relative=False,
            run_time=1.5
        )

        self.wait(0.5)

        self.fly_frisbee(
            frisbee=frisbee,
            handler=attackers[7],
            target_player=attackers[6],
            direction=RIGHT,
            defender=defender[6],
            target_player_movement=np.array([1, 6, 0]),
            defender_movement=np.array([1, 5, 0]),
            is_camera_move=True,
            flight_type="right",
            is_relative=False,
            run_time=1.5
        )

        self.wait(0.5)

        self.fly_frisbee(
            frisbee=frisbee,
            handler=attackers[6],
            target_player=attackers[7],
            direction=RIGHT,
            defender=defender[6],
            defender_movement=origin_pos_defender[6],
            handler_movement=origin_pos_attacker[6],
            is_camera_move=True,
            flight_type="left",
            is_relative=False,
            run_time=1.5,
            highlight_player=False,
            target_camera_pos=ORIGIN
        )

        # 示例：同时移动多个玩家，并让摄像机跟随第一个玩家
        self.move_multiple_players([
            (attackers[6], np.array([1,6,0]), False),  # 第1个玩家
            (defender[6], np.array([1.4,5.6,0]), False)    # 第2个玩家
        ], 
        run_time=1.5,
        path_type="straight",      
        is_camera_follow=True, 
        camera_follow_index=0, 
        vertical_only=True    
        )

        self.wait(0.5)

        self.move_multiple_players([
            (attackers[6], origin_pos_attacker[6], False),  # 第1个玩家
            (defender[6], origin_pos_defender[6], False)    # 第2个玩家
        ],
        run_time=1.5,
        path_type="straight",      
        is_camera_follow=True, 
        camera_follow_index=0, 
        vertical_only=True,
        target_camera_pos=ORIGIN
        )

        self.wait(0.5)

        self.fly_frisbee(
            frisbee=frisbee,
            handler=attackers[7],
            target_player=handler,
            direction=RIGHT,
            defender=defender[1],
            target_player_movement=np.array([2, -1, 0]),
            defender_movement=np.array([1.5, -1.5, 0]),
            is_camera_move=False,
            flight_type="straight",
            is_relative=False,
            run_time=1.5,
            highlight_player=False
        )

        da1=self.double_arrow(
            start=np.array([2, -2.2, 0]),
            end=np.array([2, -1,0]),
            color=BLUE,
            buff=0,
            stroke_width=2,
            tip_length=0.15
        )
        line1=DashedLine(
            start=origin_pos_attacker[1],
            end=np.array([2, -2.2,0]),
            color=BLUE,
            buff=0,
            stroke_width=2,
            tip_length=0.15
        )
        han_copy=Circle(radius=PLAER_RADIUS,color=YELLOW)
        han_copy.move_to(origin_pos_attacker[1])
        label_1=MathTex("Movement!!",font_size=32).next_to(da1[0],RIGHT)
        self.play(Create(han_copy))
        self.play(Create(line1))
        self.play(FadeIn(da1))
        self.play(Write(label_1))

        self.wait(0.5)
        self.play(FadeOut(da1),FadeOut(label_1),FadeOut(han_copy),FadeOut(line1))

        '''
        # 或者直接使用原函数的返回值
        animations1, _ = self.move_player(attackers[7], np.array([2.5, 0.5, 0]), is_relative=False, return_animations=True)
        animations2, _ = self.move_player(defender[7], np.array([2.5, 1.0, 0]), is_relative=False, return_animations=True)

        self.play(
            *animations1,
            *animations2,
            run_time=1.5
        )
        '''

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