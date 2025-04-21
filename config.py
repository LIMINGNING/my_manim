from manim import *

# 设置默认分辨率
config.pixel_height = 1080
config.pixel_width = 1920
config.frame_height = 7.0
config.frame_width = 12.0

GROUND_WIDTH = (config.frame_height - 0.1)*37/100
GROUND_LENGTH = config.frame_height - 0.1
GROUND_RATIO = 1.5
PLAER_RADIUS = 0.15
FRISBEE_RADIUS = 0.1
BIGGER_GROUND_LENGTH = GROUND_RATIO * GROUND_LENGTH
BIGGER_GROUND_WIDTH = GROUND_RATIO * GROUND_WIDTH

# 标准化的对角线方向 (长度为1)
UR_UNIT = normalize(UR)
UL_UNIT = normalize(UL)
DR_UNIT = normalize(DR)
DL_UNIT = normalize(DL)