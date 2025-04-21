from manim import *
from config import *
from frisbee_base import FrisbeeBaseScene
# Text.set_default(font="Kaiti") windows
Text.set_default(font="STKaiti")
class RectangleAroundScene(FrisbeeBaseScene):
    def construct(self):
        def double_arrow(start, end, color=BLUE, stroke_width=2, tip_length=0.15, buff=0):
           # 左箭头，从虚线指向砖块，尖端贴紧虚线
            arrow1 = Arrow(
                start=start,
                end=end,
                color=color,
                stroke_width=2,
                tip_length=0.15,
                buff=0  # 尖端贴紧虚线
            )

            # 右箭头，从砖块指向虚线，尖端与砖块圆刚好相接
            arrow2 = Arrow(
                start=end,
                end=start,
                color=BLUE,
                stroke_width=2,
                tip_length=0.15,
                buff=0  # 尖端刚好接触砖块圆边缘
            )

            self.play(FadeIn(arrow1),FadeIn(arrow2))
            return arrow1, arrow2
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

        central_zone=Text("Central Zone",font_size=36)
        central_zone_chinese=Text("中场区域",font_size=36).next_to(central_zone, DOWN)
        end_zone=Text("End Zone",font_size=36).next_to(dashed_line_Left,LEFT)
        end_zone_chinese=Text("底线区域",font_size=36).next_to(end_zone, DOWN)

        self.play(Write(central_zone))
        self.play(Write(central_zone_chinese))
        self.play(Write(end_zone))
        self.play(Write(end_zone_chinese))
        self.wait(1)

        self.play(FadeOut(central_zone),FadeOut(central_zone_chinese),FadeOut(end_zone),FadeOut(end_zone_chinese))

        
        double_arrow_ground_width=double_arrow(
            start = dashed_line_Left.get_start() + LEFT * 0.3,
            end = dashed_line_Left.get_end() + LEFT * 0.3,
            color=BLUE,
            stroke_width=2,
            tip_length=0.15,
            buff=0
        )
        width_label = MathTex("37m",font_size = 36).next_to(double_arrow_ground_width[0], LEFT)  # 在上方标记长度
        self.play(Create(width_label))

        double_arrow_ground_length=double_arrow(
            start = dashed_line_Left.get_end() + DOWN * 0.3,
            end = dashed_line_Right.get_end() + DOWN * 0.3,
            color=BLUE,
            stroke_width=2,
            tip_length=0.15,
            buff=0
        )
        length_label = MathTex("64m",font_size = 36).next_to(double_arrow_ground_length[0],DOWN)
        self.play(Create(length_label))

        double_arrow_ground_depth=double_arrow(
            start=GROUND_RATIO * GROUND_LENGTH * LEFT/2 + GROUND_RATIO * DOWN * GROUND_WIDTH/2 + DOWN * 0.3,
            end=dashed_line_Left.get_end() + DOWN * 0.3,
            color=BLUE,
            stroke_width=2,
            tip_length=0.15,
            buff=0
        )
        depth_label = MathTex("18m",font_size = 36).next_to(double_arrow_ground_depth[0],DOWN)
        self.play(Create(depth_label))


        heng_ground = VGroup(rectangle1,dashed_line_Left,dashed_line_Right)
        

        brick_mark_left = Circle(radius=FRISBEE_RADIUS,color=BLUE)
        brick_mark_left.set_stroke(color=WHITE, width=2)
        brick_mark_left.shift(np.array([-GROUND_RATIO * GROUND_LENGTH*14/100, 0, 0]))
        brick_mark_right = Circle(radius=FRISBEE_RADIUS,color=BLUE)
        brick_mark_right.set_stroke(color=WHITE, width=2)
        brick_mark_right.shift(np.array([GROUND_RATIO * GROUND_LENGTH*14/100, 0, 0]))
        self.play(Create(brick_mark_left))
        self.play(Create(brick_mark_right))

        dashed_line_pos = GROUND_RATIO * LEFT * GROUND_LENGTH*32/100
        # 砖块左边位置
        brick_left_pos = brick_mark_left.get_center()
        double_arrow_brick_left_length = double_arrow(
            start = dashed_line_pos,
            end = brick_left_pos,
            color=BLUE,
            stroke_width=2,
            tip_length=0.15,
            buff=0
        )

        brick_label = MathTex("18m",font_size=36)
        brick_label.next_to(double_arrow_brick_left_length[0], UP)
        self.play(Write(brick_label))

        self.wait()
 
        self.play(FadeOut(width_label), FadeOut(length_label), FadeOut(depth_label),FadeOut(brick_label)
                ,FadeOut(double_arrow_ground_width[0]), FadeOut(double_arrow_ground_width[1]), FadeOut(double_arrow_ground_length[0]), FadeOut(double_arrow_ground_length[1]), FadeOut(double_arrow_ground_depth[0]), FadeOut(double_arrow_ground_depth[1]),FadeOut(double_arrow_brick_left_length[0]), FadeOut(double_arrow_brick_left_length[1]))
        self.play(FadeOut(brick_mark_left), FadeOut(brick_mark_right))
        self.play(heng_ground.animate.rotate(-PI/2))
        self.play(heng_ground.animate.shift(DOWN * 2))
        self.play(heng_ground.animate.scale(2))  # 放大两倍

        # scene2
        direction_of_attack = DashedArrow(
            start = np.array([-3.5, 2.2, 0]),
            end = np.array([-3.5, 3.2, 0]),
            color=WHITE,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        )
        direction_of_attack_label = Tex("Direction of attack", font_size=32).next_to(direction_of_attack, RIGHT)
        self.play(Create(direction_of_attack))
        self.play(Write(direction_of_attack_label))

        tuli_attackers = Circle(radius=PLAER_RADIUS,color=RED) 
        tuli_attackers.set_fill(color=RED,opacity=1)
        tuli_attackers.set_stroke(color=WHITE, width=2)

        tuli_defender = Circle(radius=PLAER_RADIUS,color=BLUE) 
        tuli_defender.set_fill(color=BLUE,opacity=1)
        tuli_defender.set_stroke(color=WHITE, width=2)

        tuli_attackers.next_to(direction_of_attack, DOWN)
        tuli_defender.next_to(tuli_attackers, DOWN)
        attackers_label = Tex("Attackers", font_size=32).next_to(tuli_attackers, RIGHT)
        defenders_label = Tex("Defenders", font_size=32).next_to(tuli_defender, RIGHT)

        self.play(Create(tuli_attackers))
        self.play(Write(attackers_label))
        self.play(Create(tuli_defender))
        self.play(Write(defenders_label))
        self.wait(2)

        self.play(FadeOut(direction_of_attack), FadeOut(direction_of_attack_label),FadeOut(tuli_attackers), FadeOut(attackers_label),FadeOut(tuli_defender), FadeOut(defenders_label))

        # scene3: frisbee and handler
        frisbee = Circle(radius=FRISBEE_RADIUS,color=WHITE)
        handler = self.create_player(1,RED,WHITE)

        handler.shift(np.array([0, -2.8, 0]))
        frisbee_position = self.get_frisbee_position(handler, RIGHT, frisbee)
        frisbee.move_to(frisbee_position)
        self.play(FadeIn(handler))
        self.play(FadeIn(frisbee))
        handler_center  = handler.get_center()

        self.wait(2)

        self.play(
            Rotate(
                frisbee,
                angle=PI,
                about_point=handler_center,
                run_time=1,
                rate_func=smooth
            )
        )

        rectangle_breakside = Rectangle(width=GROUND_RATIO * GROUND_WIDTH,height=2.8*2,color=BLUE)
        rectangle_breakside.set_fill(color=RED,opacity=0.5)
        rectangle_breakside.shift(np.array([-GROUND_RATIO * GROUND_WIDTH/2, 0, 0]))
        self.play(FadeIn(rectangle_breakside))

        rectangle_openside = Rectangle(width=GROUND_RATIO * GROUND_WIDTH,height=2.8*2,color=BLUE)
        rectangle_openside.set_fill(color=BLUE,opacity=0.5)
        rectangle_openside.shift(np.array([GROUND_RATIO * GROUND_WIDTH/2, 0, 0]))
        self.play(FadeIn(rectangle_openside))
        
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

        # 将2号攻击者移动到handler左边
        attackers[2].shift(np.array([-2.5,-2.0,0]))
        defender[2].next_to(attackers[2], UR,buff=0.02)

        # 显示2号攻击者
        self.play(FadeIn(attackers[2]))
        self.play(FadeIn(defender[2]))

        # 将攻击者排成一竖排，2号距离handler约8-10m，间隔2m
        self.position_attackers(handler, attackers, base_distance=2.3, interval=0.6)      
        self.position_defenders(attackers, defender,offset_x=0.5, offset_y=-0.4, interval=0.8)

        # 显示所有defenders
        self.play(FadeIn(defenders_group),FadeIn(attackers_group))
        
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
            LEFT,
            handler_movement=RIGHT * 2,
            flight_type="left",
            run_time=1.5,
            arc_angle=PI/2,
            is_camera_move=False,
        )
        # 示例1：让攻击者向左移动1个单位，使用左弧线路径，相机垂直跟随
        self.move_player(attackers[6], LEFT, path_type="right", run_time=1.5, is_camera_follow=True, vertical_only=True)

        # 示例2：移动到场地上的特定位置，相机完全跟随
        target_pos = np.array([2.0, 1.5, 0])
        self.move_player(handler, target_pos, path_type="right",is_camera_follow=True, vertical_only=False)

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

class DashedArrow(VGroup):
    def __init__(
        self,
        start=LEFT,
        end=RIGHT,
        color=WHITE,
        dash_length=0.1,
        dashed_ratio=0.5,
        buff=0,
        stroke_width=3,
        tip_length=0.2,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        # 计算方向向量
        direction = end - start
        direction = direction / np.linalg.norm(direction)
        
        # 为箭头尖端预留空间，缩短虚线
        adjusted_end = end - direction * tip_length * 0.8  # 缩短终点位置
        
        # 创建虚线
        dashed_line = DashedLine(
            start=start,
            end=adjusted_end,  # 使用调整后的终点
            dash_length=dash_length,
            dashed_ratio=dashed_ratio,
            color=color,
            stroke_width=stroke_width
        )
        
        # 使用临时箭头来获取正确位置的箭头尖端
        temp_arrow = Arrow(start=start, end=end, color=color, buff=0)
        arrow_tip = temp_arrow.tip.copy()
        
        # 调整箭头尖端大小
        arrow_tip.scale(tip_length / arrow_tip.height)
        
        self.add(dashed_line, arrow_tip)
        self.dashed_line = dashed_line  # 保存引用
        self.arrow_tip = arrow_tip      # 保存引用

# 为DashedArrow创建自定义的Create动画
# 简化版的CreateDashedArrow
# 为DashedArrow创建自定义的Create动画
class CreateDashedArrow(Animation):
    def __init__(self, dashedarrow, **kwargs):
        self.line_animation = Create(dashedarrow.dashed_line)
        super().__init__(dashedarrow, **kwargs)
        
    def begin(self):
        super().begin()  # 确保父类的begin方法被调用
        self.line_animation.begin()
        # 初始时隐藏箭头尖端
        self.mobject.arrow_tip.set_opacity(0)
        
    def interpolate_mobject(self, alpha):
        self.line_animation.interpolate_mobject(alpha)
        
        # 当虚线创建到一定程度时(例如70%)，开始显示箭头尖端
        if alpha >= 0.7:
            # 将箭头尖端的不透明度从0到1平滑过渡
            tip_alpha = (alpha - 0.7) / 0.3
            self.mobject.arrow_tip.set_opacity(tip_alpha)
        else:
            # 确保箭头尖端不可见
            self.mobject.arrow_tip.set_opacity(0)