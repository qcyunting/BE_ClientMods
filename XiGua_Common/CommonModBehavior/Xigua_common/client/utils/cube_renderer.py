# -*- encoding: utf-8 -*-
import mod.client.extraClientApi as clientApi


class CubeRenderer:
    def __init__(self, parent):
        self.parent = parent  # 持有父对象引用，用于调用API
        self.cubes = {}  # 存储每个立方体的所有面ID {cube_id: [face_ids]}
        self.next_id = 1

    def renderCube(self, start_pos, end_pos):
        """
        渲染一个立方体
        start_pos: 起始坐标 (x, y, z)
        end_pos: 结束坐标 (x, y, z)
        返回: cube_id 用于后续删除
        """
        # 计算立方体的最小和最大坐标
        x1, y1, z1 = start_pos
        x2, y2, z2 = end_pos

        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        min_z, max_z = min(z1, z2), max(z1, z2)

        # 计算中心点和尺寸
        center_x = (min_x + max_x) / 2.0
        center_y = (min_y + max_y) / 2.0
        center_z = (min_z + max_z) / 2.0
        size_x = max_x - min_x
        size_y = max_y - min_y
        size_z = max_z - min_z

        center = (center_x, center_y, center_z)

        # 6个面的配置
        faces = [
            {"pos": (center_x, center_y, center_z + size_z / 2), "rot": (0, 0, 0), "scale": (size_x, size_y, 1)},  # 前
            {"pos": (center_x, center_y, center_z - size_z / 2), "rot": (0, 180, 0), "scale": (size_x, size_y, 1)},  # 后
            {"pos": (center_x + size_x / 2, center_y, center_z), "rot": (0, 90, 0), "scale": (size_z, size_y, 1)},  # 右
            {"pos": (center_x - size_x / 2, center_y, center_z), "rot": (0, -90, 0), "scale": (size_z, size_y, 1)},  # 左
            {"pos": (center_x, center_y + size_y / 2, center_z), "rot": (90, 0, 0), "scale": (size_x, size_z, 1)},  # 上
            {"pos": (center_x, center_y - size_y / 2, center_z), "rot": (-90, 0, 0), "scale": (size_x, size_z, 1)},  # 下
        ]

        cube_id = self.next_id
        self.next_id += 1
        face_ids = []

        for face in faces:
            frameEntityId = self.parent.CreateEngineSfxFromEditor("effects/block_selected.json")
            frameAniTransComp = clientApi.GetEngineCompFactory().CreateFrameAniTrans(frameEntityId)
            frameAniTransComp.SetPos(face["pos"])
            frameAniTransComp.SetRot(face["rot"])
            frameAniTransComp.SetScale(face["scale"])
            frameAniControlComp = clientApi.GetEngineCompFactory().CreateFrameAniControl(frameEntityId)
            frameAniControlComp.Play()
            face_ids.append(frameEntityId)

        self.cubes[cube_id] = face_ids
        return cube_id

    def removeCube(self, cube_id):
        """
        删除指定的立方体
        cube_id: renderCube返回的ID
        """
        if cube_id in self.cubes:
            for face_id in self.cubes[cube_id]:
                self.parent.DestroyEntity(face_id)
            del self.cubes[cube_id]
            return True
        return False

    def removeAllCubes(self):
        """删除所有立方体"""
        for cube_id in list(self.cubes.keys()):
            self.removeCube(cube_id)