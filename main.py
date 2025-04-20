from manim import *
from config import *
# 设置默认分辨率

GROUND_WIDTH = (config.frame_height - 0.1)*37/100
GROUND_LENGTH = config.frame_height - 0.1
BIGGER_GROUND = 1.5
PLAER_RADIUS = 0.15
FRISBEE_RADIUS = 0.1

# 标准化的对角线方向 (长度为1)
UR_UNIT = normalize(UR)
UL_UNIT = normalize(UL)
DR_UNIT = normalize(DR)
DL_UNIT = normalize(DL)

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

    def create_player(self,number,color,text_color=WHITE):
        '''
        @param number: 玩家编号
        @param color: 玩家颜色
        @param text_color: 玩家编号文字颜色
        @return: 返回一个包含圆形和文字的组合对象
        @description: 创建一个玩家对象，包含圆形和编号文字
        @example: player = create_player(1, RED, WHITE)
        @note: 圆形的半径和颜色可以根据需要调整
        @note: 文字的大小和颜色可以根据需要调整
        @note: 该函数可以用于创建不同颜色和编号的玩家对象
        '''
        circle = Circle(radius=PLAER_RADIUS,color=color)
        circle.set_fill(color=color,opacity=1)
        circle.set_stroke(color=WHITE, width=2)
        number_text = Text(str(number),font_size=24,color=text_color)
        number_text.move_to(circle.get_center())
        return VGroup(circle, number_text)
    
    def construct(self):
        def get_frisbee_position(self, player, direction, frisbee, buff=0.05):
            """
            将飞盘精确放置在指定玩家的指定方向位置
            使用直接计算代替next_to，确保所有方向距离一致

            @param player: 玩家对象
            @param direction: 飞盘相对于玩家的方向（LEFT、RIGHT、UP、DOWN等）
            @param frisbee: 飞盘对象
            @param buff: 飞盘与玩家之间的距离偏移量，正值表示远离玩家，负值表示靠近玩家
            @return: 飞盘的最终位置
            @description: 计算飞盘在玩家指定方向上的位置
            @example: get_frisbee_position(player, RIGHT, frisbee)
            @note: 该函数可以用于计算飞盘在不同方向上的位置
            @note: buff参数可以用于调整飞盘与玩家之间的距离
            @note: 该函数假设玩家是一个圆形对象，飞盘也是一个圆形对象
            """
            # 获取玩家中心
            player_center = player.get_center()
            
            # 计算单位方向向量(确保长度为1)
            if isinstance(direction, np.ndarray):
                # 确保方向是单位向量
                dir_unit = direction / np.linalg.norm(direction)
            else:
                dir_unit = direction  # 假设已经是单位向量如RIGHT, UP等
            
            # 计算玩家半径(假设玩家是圆形)
            player_radius = PLAER_RADIUS  # 根据你的创建圆的参数
            
            # 计算飞盘半径
            frisbee_radius = FRISBEE_RADIUS  # 根据你的飞盘半径
            
            # 计算飞盘位置: 玩家中心 + 方向*距离
            distance = player_radius + frisbee_radius + buff  # buff可以为负数表示重叠
            frisbee_position = player_center + dir_unit * distance
            
            return frisbee_position
        

            """
            控制飞盘按指定路径飞行到目标玩家的指定方向
            
            参数:
            frisbee - 飞盘对象
            target_player - 目标玩家对象
            direction - 飞盘最终相对于玩家的方向（LEFT、RIGHT等）
            flight_type - 飞行类型：'left'(左弧线)、'right'(右弧线)或'straight'(直线)
            run_time - 动画时长
            arc_angle - 弧线角度大小(仅用于弧线飞行)
            """
            # 获取起点和终点
            start_point = frisbee.get_center()
            end_point = get_frisbee_position(self, target_player, direction, frisbee)
            
            # 根据飞行类型创建路径
            if flight_type == "left":
                # 左弧线飞行
                path = ArcBetweenPoints(
                    start_point,
                    end_point,
                    angle=-arc_angle  # 负值表示向左弧线
                )
                
            elif flight_type == "right":
                # 右弧线飞行
                path = ArcBetweenPoints(
                    start_point,
                    end_point,
                    angle=arc_angle  # 正值表示向右弧线
                )
                
            else:  # straight
                # 直线飞行
                path = Line(start_point, end_point)
            
            # 飞盘沿路径飞行动画
            self.play(
                MoveAlongPath(frisbee, path),
                run_time=run_time,
                rate_func=smooth
            )
            
            # 将飞盘移动到精确位置
            frisbee.move_to(end_point)
            
            high_light_player(target_player)  # 高亮目标玩家
            return end_point  # 返回飞盘最终位置

        def high_light_player(target_player):
            '''
            @param target_player: 目标玩家对象
            @description: 高亮显示目标玩家
            @example: high_light_player(target_player)
            @note: 该函数将目标玩家的颜色设置为黄色，并在0.3秒后恢复原始颜色
            @note: 该函数假设目标玩家是一个圆形对象
            @note: 该函数假设目标玩家有一个方法get_fill_color()来获取当前颜色
            '''
            # 获取玩家的原始颜色
            original_color = target_player[0].get_fill_color()
            
            # 高亮显示为黄色
            self.play(
                target_player[0].animate.set_fill(color=YELLOW),
                run_time=0.5,
                rate_func=lambda t: smooth(t)
            )
            
            # 保持高亮状态
            self.wait(0.3)
            
            # 颜色逐渐变回原始颜色
            self.play(
                target_player[0].animate.set_fill(color=original_color),  # 恢复原始颜色
                run_time=0.6,
                rate_func=lambda t: smooth(t)
            )

        def fly_frisbee(self, frisbee, handler, target_player, direction, flight_type="left", run_time=1.5, arc_angle=PI/2,target_player_movement=None,handler_movement=None, is_camera_move = True, vertical_only=True, target_camera_pos=None, highlight_player=True):
            """
            飞盘飞行时相机跟随目标玩家，可选择是否只跟随垂直方向
            
            @param frisbee: 飞盘对象
            @param handler: handler对象
            @param target_player: 目标玩家对象
            @param direction: 飞盘相对于目标玩家的方向（LEFT、RIGHT等）
            @param flight_type: 飞行类型：'left'(左弧线)、'right'(右弧线)或'straight'(直线)
            @param run_time: 动画时长
            @param arc_angle: 弧线角度大小(仅用于弧线飞行)
            @param target_player_movement: 目标玩家的移动向量（可选）
            @param handler_movement: handler的移动向量（可选）
            @param is_camera_move: 是否移动相机（默认True）
            @param vertical_only: 是否只在垂直方向跟随（默认True）
            @param target_camera_pos: 目标相机位置（可选）
            @param highlight_player: 是否高亮显示目标玩家（默认True）
            @description: 控制飞盘按指定路径飞行到目标玩家的指定方向
            @example: fly_frisbee(frisbee, handler, target_player, LEFT)
            @note: 该函数将飞盘移动到目标玩家的指定方向，并可选择移动相机
            @note: 飞盘和handler和目标玩家可以同时移动
            """
            # 获取起点
            start_point = frisbee.get_center()
            
            # 计算终点和路径
            if target_player_movement is not None:
                # 如果玩家同时移动，计算移动后的位置
                future_player = target_player.copy()
                future_player.shift(target_player_movement)
                end_point = get_frisbee_position(self, future_player, direction, frisbee)
                future_position = future_player.get_center()
            else:
                # 玩家不移动
                end_point = get_frisbee_position(self, target_player, direction, frisbee)
                future_position = target_player.get_center()

            if handler_movement is not None:
                # 如果handler同时移动，计算移动后的位置
                future_handler = handler.copy()
                future_handler.shift(handler_movement)
                handler_position = future_handler.get_center()
            else:
                # handler不移动
                handler_position = handler.get_center()
            
            # 创建路径
            if flight_type == "left":
                path = ArcBetweenPoints(start_point, end_point, angle=-arc_angle)
            elif flight_type == "right":
                path = ArcBetweenPoints(start_point, end_point, angle=arc_angle)
            else:
                path = Line(start_point, end_point)
            
            if is_camera_move:
                # 计算相机目标位置
                if target_camera_pos is not None:
                    # 如果提供了目标相机位置，使用它
                    target_camera_pos = target_camera_pos
                else:
                # 获取当前相机位置
                    current_camera_pos = self.camera.frame.get_center()
                    if vertical_only:
                        # 只在垂直方向跟随（保持X坐标不变）
                        target_camera_pos = np.array([
                            current_camera_pos[0], 
                            future_position[1], 
                            current_camera_pos[2]
                        ])
                    else:
                        # 完全跟随到目标位置
                        target_camera_pos = future_position
                
                # 执行动画
                animations = [
                    self.camera.frame.animate.move_to(target_camera_pos)
                ]
            
                if target_player_movement is not None:
                    animations.append(target_player.animate.shift(target_player_movement))
                
                if handler_movement is not None:
                    animations.append(handler.animate.shift(handler_movement))
                    
                animations.append(MoveAlongPath(frisbee, path))
                
                self.play(
                    *animations,
                    run_time=run_time,
                    rate_func=smooth
                )
                
                # 将飞盘移动到精确位置
                frisbee.move_to(end_point)
                
                if highlight_player:
                    # 高亮显示接球的球员
                    high_light_player(target_player)
                
                return end_point
            else:
                # 不移动相机
                if target_player_movement is not None:
                    if handler_movement is not None:
                        self.play(
                            target_player.animate.shift(target_player_movement),
                            handler.animate.shift(handler_movement),
                            MoveAlongPath(frisbee, path),
                            run_time=run_time,
                            rate_func=smooth
                        )
                    else:
                        self.play(
                            target_player.animate.shift(target_player_movement),
                            MoveAlongPath(frisbee, path),
                            run_time=run_time,
                            rate_func=smooth
                        )
                else:
                    if handler_movement is not None:
                        self.play(
                            handler.animate.shift(handler_movement),
                            MoveAlongPath(frisbee, path),
                            run_time=run_time,
                            rate_func=smooth
                        )
                    else:
                        self.play(
                            MoveAlongPath(frisbee, path),
                            run_time=run_time,
                            rate_func=smooth
                        )
                
                # 将飞盘移动到精确位置
                frisbee.move_to(end_point)
                
                if highlight_player:
                    # 高亮显示接球的球员
                    high_light_player(target_player)
                
                return end_point
        
        def move_camera_to_player(self, player, vertical_only=True, run_time=1.0, target_camera_pos=None):
            '''
            @param player: 目标玩家对象
            @param vertical_only: 是否只在垂直方向跟随（默认True）
            @param run_time: 动画时长
            @param target_camera_pos: 目标相机位置（可选）
            @description: 控制相机跟随目标玩家
            @example: move_camera_to_player(player)
            @note: 该函数将相机移动到目标玩家的指定位置
            @note: vertical_only参数决定是否只在垂直方向跟随
            '''
            if target_camera_pos is not None:
                # 如果提供了目标相机位置，使用它
                target_camera_pos = target_camera_pos
            else:
                # 获取当前相机位置
                future_position = player.get_center()
                current_camera_pos = self.camera.frame.get_center()
                if vertical_only:
                    # 只在垂直方向跟随（保持X坐标不变）
                    target_camera_pos = np.array([
                    current_camera_pos[0], 
                    future_position[1], 
                    current_camera_pos[2]
                ])
                else:
                    # 完全跟随到目标位置
                    target_camera_pos = future_position
                
                # 执行动画
            animations = [
                self.camera.frame.animate.move_to(target_camera_pos)
            ]

            self.play(
                    *animations,
                    run_time=run_time,
                    rate_func=smooth
                )
                
            return target_camera_pos

        def move_player(self, player, target_position, path_type="straight", run_time=1.0, arc_angle=PI/2, highlight=False, is_camera_follow=False, vertical_only=True, target_camera_pos=None):
            """
            控制玩家按指定路径移动到目标位置，可选择相机跟随
            
            参数:
            player - 要移动的玩家对象
            target_position - 目标位置向量或点坐标
            path_type - 路径类型：'left'(左弧线)、'right'(右弧线)或'straight'(直线)
            run_time - 动画时长
            arc_angle - 弧线角度大小(仅用于弧线移动)
            highlight - 是否在移动结束后高亮显示玩家
            is_camera_follow - 是否让相机跟随玩家移动
            vertical_only - 相机是否只在垂直方向跟随（保持X坐标不变）
            target_camera_pos - 自定义相机目标位置（可选）
            """
            # 获取起点
            start_point = player.get_center()
            
            # 目标位置可以是向量或点坐标
            if isinstance(target_position, np.ndarray) and len(target_position) == 3:
                # 如果是点坐标，计算位移向量
                end_point = target_position
                shift_vector = end_point - start_point
            else:
                # 如果直接提供了位移向量
                shift_vector = target_position
                end_point = start_point + shift_vector
            
            # 根据路径类型创建不同的路径
            if path_type == "left":
                # 左弧线移动
                path = ArcBetweenPoints(
                    start_point,
                    end_point,
                    angle=-arc_angle  # 负值表示向左弧线
                )
            elif path_type == "right":
                # 右弧线移动
                path = ArcBetweenPoints(
                    start_point,
                    end_point,
                    angle=arc_angle  # 正值表示向右弧线
                )
            else:  # straight
                # 直线移动
                path = Line(start_point, end_point)
            
            # 处理相机跟随
            if is_camera_follow:
                if target_camera_pos is not None:
                    # 如果提供了特定的相机位置，使用它
                    target_camera_pos = target_camera_pos
                else:
                    # 获取当前相机位置
                    current_camera_pos = self.camera.frame.get_center()
                    if vertical_only:
                        # 只在垂直方向跟随（保持X坐标不变）
                        target_camera_pos = np.array([
                            current_camera_pos[0], 
                            end_point[1],  # 使用目标点的Y坐标
                            current_camera_pos[2]
                        ])
                    else:
                        # 完全跟随到玩家位置
                        target_camera_pos = end_point
                
                # 执行带相机移动的动画
                self.play(
                    MoveAlongPath(player, path),
                    self.camera.frame.animate.move_to(target_camera_pos),
                    run_time=run_time,
                    rate_func=smooth
                )
            else:
                # 不跟随相机的普通移动
                self.play(
                    MoveAlongPath(player, path),
                    run_time=run_time,
                    rate_func=smooth
                )
            
            # 确保玩家移动到精确位置
            player.move_to(end_point)
            
            # 可选：移动结束后高亮显示
            if highlight:
                high_light_player(player)
            
            return shift_vector  # 返回位移向量以便后续使用

        def create_camera_grid(self, x_range=[-6, 6], y_range=[-4, 4], scale=1):
            """创建跟随相机移动的网格"""
            grid = NumberPlane(
                x_range=x_range,
                y_range=y_range,
                background_line_style={
                    "stroke_opacity": 0.5,
                    "stroke_width": 1
                }
            ).scale(scale)
            
            # 让网格跟随相机移动
            def update_grid(grid):
                grid.move_to(self.camera.frame.get_center())
            
            grid.add_updater(update_grid)
            return grid

        # 使用方法
        camera_grid = create_camera_grid(self)
        self.add(camera_grid)

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
        grid = NumberPlane(x_range=[-6, 6], y_range=[-4, 4])
        self.add(grid)


        # scene1
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

        # scene3: frisbee and handler
        frisbee = Circle(radius=FRISBEE_RADIUS,color=WHITE)
        handler = self.create_player(1,RED,WHITE)

        handler.shift(np.array([0, -2.8, 0]))
        frisbee_position = get_frisbee_position(self, handler, RIGHT, frisbee)
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
        attackers[2].move_to(handler.get_center() + LEFT)

        # 显示2号攻击者
        self.play(FadeIn(attackers[2]))

        # 将攻击者排成一竖排，2号距离handler约8-10m，间隔2m
        self.position_attackers(handler, attackers, base_distance=1.8, interval=0.6)      
        self.position_defenders(attackers, defender,offset_x=0.5, offset_y=-0.4, interval=0.8)

        # 显示所有defenders
        self.play(FadeIn(defenders_group),FadeIn(attackers_group))
        
        self.wait(2)

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
        '''
        # 玩家同时移动，相机跟随
        fly_frisbee(
            self,
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

        fly_frisbee(
            self,
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

        fly_frisbee(
            self,
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
        move_player(self, attackers[6], LEFT, path_type="left", run_time=1.5, 
                    is_camera_follow=True, vertical_only=True)

        # 示例2：移动到场地上的特定位置，相机完全跟随
        target_pos = np.array([2.0, 1.5, 0])
        move_player(self, handler, target_pos, path_type="right", 
                    is_camera_follow=True, vertical_only=False)

        # 示例3：使用向量组合，让防守者向右上方移动，不跟随相机
        move_player(self, defender[5], RIGHT*2 + UP, path_type="straight", 
                    is_camera_follow=False)

        # 示例4：移动并高亮显示，自定义相机位置
        move_player(self, attackers[3], DOWN*3, highlight=True, 
                    is_camera_follow=True, target_camera_pos=np.array([0, -1, 0]))
        target_pos = np.array([-2, 8, 0])
        move_player(self, handler, target_pos, highlight=True, path_type="right", 
                    is_camera_follow=True, vertical_only=False)
        
        move_camera_to_player(self,attackers[7],vertical_only=False,run_time=1.5,target_camera_pos=None)

        fly_frisbee(self,frisbee,attackers[7],handler,LEFT,flight_type="left",run_time=1.5,arc_angle=PI/2,target_player_movement=DOWN * 2,is_camera_move=True,highlight_player=True)

        move_camera_to_player(
            self,
            attackers[7],
            vertical_only=True,
            run_time=1.5,
            target_camera_pos=None
        )

        self.wait(1)
        '''
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