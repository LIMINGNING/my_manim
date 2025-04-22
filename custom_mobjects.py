from manim import *
import numpy as np

class DashedArrow(VGroup):
    def __init__(
        self,
        start=LEFT,
        end=RIGHT,
        color=WHITE,
        dash_length=0.1,
        dashed_ratio=0.5,
        buff=0,
        stroke_width=2,
        tip_length=0.15,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        # 计算方向向量
        direction = end - start
        direction = direction / np.linalg.norm(direction)
        
        # 为箭头尖端预留空间，缩短虚线
        adjusted_end = end - direction * tip_length * 0.8
        
        # 创建虚线
        dashed_line = DashedLine(
            start=start,
            end=adjusted_end,
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
        self.dashed_line = dashed_line
        self.arrow_tip = arrow_tip