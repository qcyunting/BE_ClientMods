# -*- coding: utf-8 -*-
from ...utils.ui_utils import *
import math


class Main(BaseCustomScreenProxy):
    def __init__(self, screenName, screenNode):
        super(Main, self).__init__(screenName, screenNode)
        self.ui_create = False
        self.camera_motion = -1
        speed = 0.4
        cameraComp.DepartCamera()
        self.perspective = CF.CreatePlayerView(playerId).GetPerspective()
        if self.perspective != 2:
            CF.CreatePlayerView(playerId).SetPerspective(2)

        # 通过旋转角度获取朝向单位向量
        # rot参数: (俯仰角, 水平角) 单位是角度
        rot_x, rot_y = rotComp.GetRot()
        rotComp.SetRot((0, rot_y))
        dx, dy, dz = self.get_direction_from_z(rot_y, 2)
        if self.perspective == 2:
            target_rot_y = rot_y
        elif rot_y >= 0:
            target_rot_y = rot_y - 180
        else:
            target_rot_y = rot_y + 180
        x, y, z = posComp.GetPos()
        self.camera_pos = (x + dx, y + dy, z + dz)
        self.camera_motion = cameraComp.AddCameraTrackMotion(
            self.camera_pos,
            speed,
            startRot=(0, target_rot_y, 0),
            targetRot=(0, rot_y, 0))
        cameraComp.SetCameraDistanceFixed(True)
        cameraComp.StartCameraMotion(self.camera_motion)
        cameraComp.SetCameraOffset((0, -0.4, -2))
        cameraComp.DepartCamera()

    def OnCreate(self):
        pass

    def OnDestroy(self):
        cameraComp.UnDepartCamera()
        cameraComp.ResetCameraPos()
        cameraComp.SetCameraDistanceFixed(False)
        cameraComp.RemoveCameraMotion(self.camera_motion)
        cameraComp.SetCameraOffset((0, 0, 0))
        CF.CreatePlayerView(playerId).SetPerspective(self.perspective)
        if self.perspective != 2:
            rot_x, rot_y = rotComp.GetRot()
            rotComp.SetRot((0, rot_y + 180))

    def get_direction_from_z(self, angle_deg, length=2.0):
        """
        从Z轴正方向开始，顺时针为正的角度，获取水平方向向量

        参数:
        angle_deg: 角度（度数），范围 -180 到 180
                   Z正=0°, X正=-90°, X负=90°, Z负=±180°
            length: 向量长度，默认2

        返回:
            (x, z): 相对坐标
        """
        # 由于角度定义：0°=Z正，-90°=X正，90°=X负
        # 使用标准三角函数，但注意X和Z的对应关系
        angle_rad = math.radians(angle_deg)

        # 因为标准数学中0°是X正，需要转换
        # 这里：dx = sin(角度), dz = cos(角度)
        x = round(length * math.sin(-angle_rad), 3)
        z = round(length * math.cos(angle_rad), 3)

        return x, 0, z