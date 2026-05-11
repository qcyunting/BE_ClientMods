import math

def calculate_panel_size(player_pos, panel_pos, base_size=1.0, scale_factor=0.5, max_distance=None):
    """
    计算游戏面板的大小，基于玩家与面板距离的指数函数

    参数:
    player_pos: 玩家坐标 (x, y, z)
    panel_pos: 面板坐标 (x, y, z)
    base_size: 基础大小（距离为0时的大小）
    scale_factor: 缩放因子，控制大小随距离变化的敏感度
    max_distance: 可选，最大参考距离（用于归一化）

    返回:
    distance: 距离
    size: 面板的X和Y大小
    """
    # 计算欧几里得距离
    distance = math.sqrt(
        (player_pos[0] - panel_pos[0]) ** 2 +
        (player_pos[1] - panel_pos[1]) ** 2 +
        (player_pos[2] - panel_pos[2]) ** 2
    )

    # 使用指数函数计算大小
    size = base_size * math.exp(scale_factor * distance)

    return distance, size
