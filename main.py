from manim import *
from config import *
# 设置默认分辨率

GROUND_WIDTH = (config.frame_height - 0.1)*37/100
GROUND_LENGTH = config.frame_height - 0.1
BIGGER_GROUND = 1.5

class RectangleAroundScene(MovingCameraScene):
    # 将attackers按顺序排在handler前方的竖排
    def position_attackers(self, handler, attackers, base_distance=4, interval=1):
        """
        将攻击者排列在handler前方的竖排
        handler: handler对象
        attackers: 攻击者字典 {2:attacker2, 3:attacker3, ...}
        base_distance: 第一个攻击者(2号)与handler的距离，单位是场景单位
        interval: 攻击者之间的间距，单位是场景单位
        """
        handler_center = handler.get_center()
    
        # 排列攻击者(从2到6)
        for i in range(3, 8):
            # 计算距离: 2号距离base_distance, 3号距离base_distance+interval, 以此类推
            distance = base_distance + (i-3) * interval
            
            # 计算位置: handler的正前方(上方)
            position = handler_center + UP * distance
            
            # 移动攻击者到该位置
            attackers[i].move_to(position)

    def position_defenders(self, attackers, defenders, offset_x=0.5, offset_y=-0.5, interval=0.8):
        """
        将防守者排列在攻击者的右下方
        attackers: 攻击者字典 {3:attacker3, 4:attacker4, ...}
        defenders: 防守者字典 {3:defender3, 4:defender4, ...}
        offset_x: 水平偏移量(正值为右移)
        offset_y: 垂直偏移量(负值为下移)
        interval: 防守者之间的间距，与攻击者间距相同
        """
        attacker_pos = attackers[3].get_center()
        defender_start_pos = attacker_pos + RIGHT * offset_x + DOWN * (-offset_y)
        # 对每个编号从3到7的防守者进行处理
        for i in range(3, 8):
            distance = (i-3) * interval

            positon = UP * distance + defender_start_pos

            # 移动防守者到该位置
            defenders[i].move_to(positon)

    def create_circle(self,number,color,text_color=WHITE):
        circle = Circle(radius=0.15,color=color)
        circle.set_fill(color=color,opacity=1)
        number_text = Text(str(number),font_size=24,color=text_color)
        number_text.move_to(circle.get_center())
        return VGroup(circle, number_text)
    
    def construct(self):
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

        # scene2
        jingongfangxiang = DashedArrow(
            start = np.array([-3.5, 2.2, 0]),
            end = np.array([-3.5, 3.2, 0]),
            color=WHITE,
            buff=0,
            stroke_width=3,
            tip_length=0.2
        )
        jingongfangxiang_label = Tex("Direction of attack", font_size=32).next_to(jingongfangxiang, RIGHT)
        self.play(Create(jingongfangxiang))
        self.play(Write(jingongfangxiang_label))

        # frisbee and handler
        frisbee = Circle(radius=0.1,color=WHITE)
        handler = self.create_circle(1,RED,WHITE)

        handler.shift(np.array([0, -2.8, 0]))
        frisbee.next_to(handler,direction=UR,buff=-0.05)  
        self.play(FadeIn(handler))
        self.play(FadeIn(frisbee))
        handler_center  = handler.get_center()

        self.wait(2)

        self.play(
            Rotate(
                frisbee,
                angle=PI/2,
                about_point=handler_center,
                run_time=1,
                rate_func=smooth
            )
        )

        # attackers and defenders
        attackers = {}
        for i in range(2,8):
            attackers[i] = self.create_circle(i,RED,WHITE)

        defender = {}
        for i in range(1,8):
            defender[i] = self.create_circle(i,BLUE,WHITE)
        
        attackers_group = VGroup()
        for i in range(3,8):
            attackers_group.add(attackers[i])

        defenders_group = VGroup()
        for i in range(3, 8):
            defenders_group.add(defender[i])

        # 将2号攻击者移动到handler左下方位置(向左1个单位，向下1个单位)
        attackers[2].move_to(handler.get_center() + LEFT)

        # 显示2号攻击者
        self.play(FadeIn(attackers[2]))

        # 将攻击者排成一竖排，2号距离handler约8-10m，间隔2m
        self.position_attackers(handler, attackers, base_distance=1.8, interval=0.6)      
        self.position_defenders(attackers, defender,offset_x=0.5, offset_y=-0.4, interval=0.8)

        # 显示所有defenders
        self.play(FadeIn(defenders_group),FadeIn(attackers_group))
        
        self.wait(2)

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

        # 现在任何attackers[7]的移动都会被相机跟随
        self.play(attackers[7].animate.shift(UP * 2))
        self.wait(1)
        # 当你想停止相机跟随时
        self.camera.frame.clear_updaters()
        # 现在attackers[7]移动不会再被跟随
        self.play(attackers[7].animate.shift(RIGHT * 2))

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
class CreateDashedArrow(Animation):
    def __init__(self, dashedarrow, **kwargs):
        self.line_animation = Create(dashedarrow.dashed_line)
        self.tip_animation = Create(dashedarrow.arrow_tip)
        super().__init__(dashedarrow, **kwargs)
        
    def begin(self):
        self.line_animation.begin()
        self.tip_animation.suspend_updating()  # 先暂停箭头尖端的动画
        
    def interpolate_mobject(self, alpha):
        self.line_animation.interpolate_mobject(alpha)
        
        # 当虚线创建到一定程度时(例如70%)，开始创建箭头尖端
        if alpha >= 0.7:
            # 将箭头尖端的动画进度映射到0-1的范围
            tip_alpha = (alpha - 0.7) / 0.3  
            self.tip_animation.interpolate_mobject(tip_alpha)
            self.tip_animation.resume_updating()
        else:
            # 箭头尖端还不可见
            self.mobject.arrow_tip.set_opacity(0)

