from manim import *
from config import *

class FrisbeeBaseScene(MovingCameraScene):
    """飞盘基础场景，包含所有共享功能"""
    
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
        number_text = MathTex(str(number),font_size=24,color=text_color)
        number_text.move_to(circle.get_center())
        return VGroup(circle, number_text)
        pass
    
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
        pass
    
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
        pass
    
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
        pass
        
    
    def high_light_player(self, target_player):
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
        pass
    
    def fly_frisbee(self, frisbee, handler, target_player, direction, defender=None, 
               flight_type="straight", run_time=1.5, arc_angle=PI/2, 
               target_player_movement=None, handler_movement=None, defender_movement=None,
               additional_players=None, is_camera_move=True, vertical_only=True, 
                target_camera_pos=None, highlight_player=True, is_relative=False):
        """
        飞盘飞行时相机跟随目标玩家，可同时移动攻击者、持盘人、防守者和其他任意多个玩家
        
        @param frisbee: 飞盘对象
        @param handler: handler对象
        @param target_player: 目标玩家对象
        @param direction: 飞盘相对于目标玩家的方向（LEFT、RIGHT等）
        @param defender: 防守者对象(可选)
        @param flight_type: 飞行类型：'left'(左弧线)、'right'(右弧线)或'straight'(直线)
        @param run_time: 动画时长
        @param arc_angle: 弧线角度大小(仅用于弧线飞行)
        @param target_player_movement: 目标玩家的移动向量或目标位置
        @param handler_movement: handler的移动向量或目标位置
        @param defender_movement: 防守者的移动向量或目标位置
        @param additional_players: 额外需要移动的玩家列表，每项为 (player, position, player_is_relative) 元组
        @param is_camera_move: 是否移动相机（默认True）
        @param vertical_only: 是否只在垂直方向跟随（默认True）
        @param target_camera_pos: 目标相机位置（可选）
        @param highlight_player: 是否高亮显示目标玩家（默认True）
        @param is_relative: 玩家移动是相对位移(True)还是绝对位置(False)，默认False
        """
        # 获取起点
        start_point = frisbee.get_center()
        
        # 计算终点和路径
        if target_player_movement is not None:
            # 如果玩家同时移动，计算移动后的位置
            future_player = target_player.copy()
            
            # 根据is_relative确定如何移动未来玩家位置
            if is_relative:
                future_player.shift(target_player_movement)
            else:
                future_player.move_to(target_player_movement)
                
            end_point = self.get_frisbee_position(future_player, direction, frisbee)
            future_position = future_player.get_center()
        else:
            # 玩家不移动
            end_point = self.get_frisbee_position(target_player, direction, frisbee)
            future_position = target_player.get_center()

        # 创建飞盘路径
        if flight_type == "left":
            path = ArcBetweenPoints(start_point, end_point, angle=-arc_angle)
        elif flight_type == "right":
            path = ArcBetweenPoints(start_point, end_point, angle=arc_angle)
        else:
            path = Line(start_point, end_point)
        
        # 准备动画列表
        animations = []
        
        # 添加飞盘动画
        animations.append(MoveAlongPath(frisbee, path))
        
        # 添加目标玩家动画
        if target_player_movement is not None:
            if is_relative:
                animations.append(target_player.animate.shift(target_player_movement))
            else:
                animations.append(target_player.animate.move_to(target_player_movement))
        
        # 添加handler动画
        if handler_movement is not None:
            if is_relative:
                animations.append(handler.animate.shift(handler_movement))
            else:
                animations.append(handler.animate.move_to(handler_movement))
        
        # 添加defender动画
        if defender is not None and defender_movement is not None:
            if is_relative:
                animations.append(defender.animate.shift(defender_movement))
            else:
                animations.append(defender.animate.move_to(defender_movement))
        
        # 添加额外玩家的移动动画
        if additional_players:
            for player, position, player_is_relative in additional_players:
                if player_is_relative:
                    animations.append(player.animate.shift(position))
                else:
                    animations.append(player.animate.move_to(position))
        
        # 添加相机动画
        if is_camera_move:
            if target_camera_pos is not None:
                target_camera_pos = target_camera_pos
            else:
                current_camera_pos = self.camera.frame.get_center()
                if vertical_only:
                    target_camera_pos = np.array([
                        current_camera_pos[0], 
                        future_position[1], 
                        current_camera_pos[2]
                    ])
                else:
                    target_camera_pos = future_position
                    
            animations.append(self.camera.frame.animate.move_to(target_camera_pos))
        
        # 执行所有动画
        self.play(
            *animations,
            run_time=run_time,
            rate_func=smooth
        )
        
        # 将飞盘移动到精确位置
        frisbee.move_to(end_point)
        
        # 高亮显示接球的球员
        if highlight_player:
            self.high_light_player(target_player)
        
        return end_point
        pass
    
    def move_player(self, player, target_position, path_type="straight", run_time=1.0, 
               arc_angle=PI/2, highlight=False, is_camera_follow=False, 
               vertical_only=True, target_camera_pos=None, is_relative=True, 
               return_animations=False):
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
        is_relative - 是否为相对位移（True）或绝对位置（False），默认True
        return_animations - 是否返回动画对象而不是立即执行动画，默认False
        
        返回值:
        如果return_animations为True, 返回 (animations列表, 终点位置)
        否则，直接执行动画并返回None
        """
        # 获取起点
        start_point = player.get_center()

        # 计算终点位置
        if is_relative:
            end_point = start_point + target_position
        else:
            # 如果不是相对位移，直接使用目标位置
            end_point = target_position
        
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
        
        # 创建动画列表
        animations = [MoveAlongPath(player, path)]
        
        # 添加相机动画
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
            
            animations.append(self.camera.frame.animate.move_to(target_camera_pos))
        
        # 根据return_animations参数决定是返回动画还是执行动画
        if return_animations:
            return animations, end_point
        else:
            # 直接执行动画
            self.play(
                *animations,
                run_time=run_time,
                rate_func=smooth
            )
            
            # 确保玩家移动到精确位置
            player.move_to(end_point)
            
            # 可选：移动结束后高亮显示
            if highlight:
                self.high_light_player(player)
            
            return None
        pass

    def move_multiple_players(self, players_and_positions, run_time=1.0, path_type="straight", 
                         arc_angle=PI/2, is_camera_follow=False, camera_follow_index=0, 
                         vertical_only=True, target_camera_pos=None):
        """
        同时移动多个玩家
        
        参数:
        players_and_positions - 列表，每项为 (player, position, is_relative) 元组
        run_time - 动画时长
        path_type - 路径类型：'left'(左弧线)、'right'(右弧线)或'straight'(直线)
        arc_angle - 弧线角度大小(仅用于弧线移动)
        is_camera_follow - 是否让摄像机跟随某个玩家
        camera_follow_index - 跟随玩家列表中的第几个玩家(索引)
        vertical_only - 是否只在垂直方向跟随(保持X坐标不变)
        target_camera_pos - 自定义相机目标位置，如果提供则忽略camera_follow_index
        """
        all_animations = []
        end_points = []
        
        # 首先计算所有玩家的终点位置
        for player, position, is_relative in players_and_positions:
            if is_relative:
                end_point = player.get_center() + position
            else:
                end_point = position
            end_points.append(end_point)
        
        # 确定相机目标位置
        if is_camera_follow:
            if target_camera_pos is not None:
                camera_target = target_camera_pos
            else:
                # 使用跟随玩家的终点位置
                player_end_point = end_points[camera_follow_index]
                current_camera_pos = self.camera.frame.get_center()
                
                if vertical_only:
                    camera_target = np.array([
                        current_camera_pos[0],
                        player_end_point[1],
                        current_camera_pos[2]
                    ])
                else:
                    camera_target = player_end_point
                    
            # 添加相机动画
            camera_anim = self.camera.frame.animate.move_to(camera_target)
            all_animations.append(camera_anim)
        
        # 收集所有玩家的移动动画
        for i, (player, position, is_relative) in enumerate(players_and_positions):
            # 创建路径
            start_point = player.get_center()
            end_point = end_points[i]
            
            if path_type == "left":
                path = ArcBetweenPoints(start_point, end_point, angle=-arc_angle)
            elif path_type == "right":
                path = ArcBetweenPoints(start_point, end_point, angle=arc_angle)
            else:  # "straight"
                path = Line(start_point, end_point)
                
            # 添加移动动画
            all_animations.append(MoveAlongPath(player, path))
        
        # 同时执行所有动画
        self.play(
            *all_animations,
            run_time=run_time,
            rate_func=smooth
        )
        
        # 确保所有玩家都准确到位
        for i, (player, position, is_relative) in enumerate(players_and_positions):
            player.move_to(end_points[i])
        pass

    def double_arrow(self, start, end, color=BLUE, stroke_width=2, tip_length=0.15, buff=0):
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
            color=color,
            stroke_width=2,
            tip_length=0.15,
            buff=0  # 尖端刚好接触砖块圆边缘
        )

        arrow_group=VGroup(arrow1,arrow2)
        return arrow_group
        pass