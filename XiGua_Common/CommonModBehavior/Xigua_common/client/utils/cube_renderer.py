# -*- encoding: utf-8 -*-
import mod.client.extraClientApi as clientApi


class CubeRenderer:
    def __init__(self, parent):
        self.parent = parent  # 持有父对象引用，用于调用API
        self.cubes = {}  # 存储每个立方体的所有面ID {cube_id: [face_ids]}
        self.outlines = {}  # 存储每个立方体的所有描边线对象 {cube_id: [line_objects]}
        self.next_id = 1
        self.levelId = clientApi.GetLevelId()  # 获取当前levelId
        self.drawing_comp = None  # 延迟初始化

    def _get_drawing_comp(self):
        """获取Drawing组件（延迟初始化）"""
        if self.drawing_comp is None:
            self.drawing_comp = clientApi.GetEngineCompFactory().CreateDrawing(self.levelId)
        return self.drawing_comp

    def renderCube(self, start_pos, end_pos, with_outline=True, cube_id=None):
        """
        渲染一个立方体
        start_pos: 起始坐标 (x, y, z)，方块坐标的角点
        end_pos: 结束坐标 (x, y, z)，方块坐标的角点
        with_outline: 是否同时渲染描边，默认为True
        cube_id: 可选的立方体ID，如果指定则使用该ID（重复则删除旧的），不指定则自增
        返回: cube_id 用于后续删除
        """
        # 计算方块坐标的最小和最大坐标（方块坐标）
        x1, y1, z1 = start_pos
        x2, y2, z2 = end_pos

        min_x_block, max_x_block = min(x1, x2), max(x1, x2)
        min_y_block, max_y_block = min(y1, y2), max(y1, y2)
        min_z_block, max_z_block = min(z1, z2), max(z1, z2)

        # 转换为世界坐标（方块坐标的角点需要+1才是实际的世界坐标边界）
        min_x_world = min_x_block + 0.001
        max_x_world = max_x_block + 1.001
        min_y_world = min_y_block + 0.001
        max_y_world = max_y_block + 1.001
        min_z_world = min_z_block + 0.001
        max_z_world = max_z_block + 1.001

        # 计算中心点（世界坐标）
        center_x = (min_x_world + max_x_world) / 2.0
        center_y = (min_y_world + max_y_world) / 2.0
        center_z = (min_z_world + max_z_world) / 2.0

        # 计算尺寸（世界坐标）
        size_x = max_x_world - min_x_world
        size_y = max_y_world - min_y_world
        size_z = max_z_world - min_z_world

        # 因为scale传入1.0实际是2.0，需要除以2
        # 并且尺寸需要转换为scale值（半长）
        scale_x = size_x / 2.0
        scale_y = size_y / 2.0
        scale_z = size_z / 2.0

        # 6个面的配置（位置使用世界坐标，旋转使用欧拉角，缩放使用半长）
        faces = [
            {"pos": (center_x, center_y, center_z + scale_z), "rot": (0, 0, 0), "scale": (scale_x, scale_y, 1)},  # 前
            {"pos": (center_x, center_y, center_z - scale_z), "rot": (0, 180, 0), "scale": (scale_x, scale_y, 1)},  # 后
            {"pos": (center_x + scale_x, center_y, center_z), "rot": (0, 90, 0), "scale": (scale_z, scale_y, 1)},  # 右
            {"pos": (center_x - scale_x, center_y, center_z), "rot": (0, -90, 0), "scale": (scale_z, scale_y, 1)},  # 左
            {"pos": (center_x, center_y + scale_y, center_z), "rot": (90, 0, 0), "scale": (scale_x, scale_z, 1)},  # 上
            {"pos": (center_x, center_y - scale_y, center_z), "rot": (-90, 0, 0), "scale": (scale_x, scale_z, 1)},  # 下
        ]

        # 确定cube_id
        if cube_id is not None:
            # 指定了ID，删除旧的（如果存在）
            if cube_id in self.cubes:
                self.removeCube(cube_id)
            # 检查是否与自增ID冲突（假设自增ID有前缀）
            # 如果不带前缀的自增ID与指定的cube_id相同，则跳过该自增ID
            while "auto_" + str(self.next_id) == str(cube_id) or str(self.next_id) == str(cube_id):
                self.next_id += 1
        else:
            # 不指定ID，使用带前缀的自增ID
            cube_id = "auto_" + str(self.next_id)
            self.next_id += 1
            # 确保生成的自增ID不与任何手动指定的ID冲突
            while cube_id in self.cubes:
                self.next_id += 1
                cube_id = "auto_" + str(self.next_id)

        face_ids = []

        # 渲染立方体面
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

        # 渲染描边
        if with_outline:
            outline_lines = self.renderOutline(
                (min_x_world, min_y_world, min_z_world),
                (max_x_world, max_y_world, max_z_world)
            )
            self.outlines[cube_id] = outline_lines

        return cube_id

    def renderHorizontalFace(self, y, x1, z1, x2, z2, min_point):
        """
        渲染水平方向的一个面
        y: 面的Y坐标
        x1, z1: 起始点
        x2, z2: 结束点
        min_point: 立方体的最小点坐标
        """
        entities = []
        offset = 0.02

        # 4个顶点
        v0 = (x1, y, z1)
        v1 = (x2, y, z1)
        v2 = (x2, y, z2)
        v3 = (x1, y, z2)

        edges = [
            (v0, v1, "x"),  # X轴边
            (v1, v2, "z"),  # Z轴边
            (v2, v3, "x"),  # X轴边
            (v3, v0, "z"),  # Z轴边
        ]

        for start, end, axis in edges:
            center_x = (start[0] + end[0]) / 2.0
            center_y = start[1]
            center_z = (start[2] + end[2]) / 2.0

            length_x = abs(end[0] - start[0])
            length_z = abs(end[2] - start[2])

            # 判断是否连接最小点
            is_min_edge = (start == min_point or end == min_point)

            if axis == "x":
                rot = (90, 0, 0)
                scale = (length_x / 2.0, offset, offset)
                # X轴棱偏移：小的+offset，大的-offset
                if start[0] < end[0]:
                    center_z += offset
                else:
                    center_z -= offset
                # 颜色：连接最小点且是X轴为红色，否则白色
                if is_min_edge and (start[0] != end[0]):  # X轴方向
                    color = (1.0, 0.0, 0.0, 1.0)
                else:
                    color = (1.0, 1.0, 1.0, 1.0)
            else:  # axis == "z"
                rot = (90, 180, 90)
                scale = (length_z / 2.0, offset, offset)
                # Z轴棱偏移：小的+offset，大的-offset
                if start[2] < end[2]:
                    center_x -= offset
                else:
                    center_x += offset
                # 颜色：连接最小点且是Z轴为蓝色，否则白色
                if is_min_edge and (start[2] != end[2]):  # Z轴方向
                    color = (0.0, 0.0, 1.0, 1.0)
                else:
                    color = (1.0, 1.0, 1.0, 1.0)

            entities.append(self._createOutlineEntity((center_x, center_y, center_z), rot, scale, color))

        return entities

    def renderVerticalXFace(self, x, y1, z1, y2, z2, min_point):
        """
        渲染垂直X轴方向的一个面
        x: 面的X坐标
        y1, z1: 起始点
        y2, z2: 结束点
        min_point: 立方体的最小点坐标
        """
        entities = []
        offset = 0.02

        # 4个顶点
        v0 = (x, y1, z1)
        v1 = (x, y1, z2)
        v2 = (x, y2, z2)
        v3 = (x, y2, z1)

        edges = [
            (v0, v1, "z"),  # 底部Z轴边
            (v1, v2, "y"),  # 右边Y轴边
            (v2, v3, "z"),  # 顶部Z轴边
            (v3, v0, "y"),  # 左边Y轴边
        ]

        for start, end, axis in edges:
            center_x = start[0]
            center_y = (start[1] + end[1]) / 2.0
            center_z = (start[2] + end[2]) / 2.0

            length_y = abs(end[1] - start[1])
            length_z = abs(end[2] - start[2])

            # 判断是否连接最小点
            is_min_edge = (start == min_point or end == min_point)

            if axis == "z":
                rot = (0, 90, 0)
                scale = (length_z / 2.0, offset, offset)
                # Z轴棱偏移：小的+offset，大的-offset
                if start[2] < end[2]:
                    center_y += offset
                else:
                    center_y -= offset
                # 颜色：连接最小点且是Z轴为蓝色，否则白色
                if is_min_edge and (start[2] != end[2]):
                    color = (0.0, 0.0, 1.0, 1.0)
                else:
                    color = (1.0, 1.0, 1.0, 1.0)
            else:  # axis == "y"
                rot = (90, 90, 90)
                scale = (offset, length_y / 2.0, offset)
                # Y轴棱偏移：小的+offset，大的-offset
                if start[1] < end[1]:
                    center_z -= offset
                else:
                    center_z += offset
                # 颜色：连接最小点且是Y轴为绿色，否则白色
                if is_min_edge and (start[1] != end[1]):
                    color = (0.0, 1.0, 0.0, 1.0)
                else:
                    color = (1.0, 1.0, 1.0, 1.0)

            entities.append(self._createOutlineEntity((center_x, center_y, center_z), rot, scale, color))

        return entities

    def renderVerticalZFace(self, z, x1, y1, x2, y2, min_point):
        """
        渲染垂直Z轴方向的一个面
        z: 面的Z坐标
        x1, y1: 起始点
        x2, y2: 结束点
        min_point: 立方体的最小点坐标
        """
        entities = []
        offset = 0.02

        # 4个顶点
        v0 = (x1, y1, z)
        v1 = (x2, y1, z)
        v2 = (x2, y2, z)
        v3 = (x1, y2, z)

        edges = [
            (v0, v1, "x"),  # X轴边
            (v1, v2, "y"),  # Y轴边
            (v2, v3, "x"),  # X轴边
            (v3, v0, "y"),  # Y轴边
        ]

        for start, end, axis in edges:
            center_x = (start[0] + end[0]) / 2.0
            center_y = (start[1] + end[1]) / 2.0
            center_z = start[2]

            length_x = abs(end[0] - start[0])
            length_y = abs(end[1] - start[1])

            # 判断是否连接最小点
            is_min_edge = (start == min_point or end == min_point)

            if axis == "x":
                rot = (0, 0, 0)
                scale = (length_x / 2.0, offset, offset)
                # X轴棱偏移：小的+offset，大的-offset
                if start[0] < end[0]:
                    center_y += offset
                else:
                    center_y -= offset
                # 颜色：连接最小点且是X轴为红色，否则白色
                if is_min_edge and (start[0] != end[0]):
                    color = (1.0, 0.0, 0.0, 1.0)
                else:
                    color = (1.0, 1.0, 1.0, 1.0)
            else:  # axis == "y"
                rot = (0, 0, 0)
                scale = (offset, length_y / 2.0, offset)
                # Y轴棱偏移：小的+offset，大的-offset
                if start[1] < end[1]:
                    center_x -= offset
                else:
                    center_x += offset
                # 颜色：连接最小点且是Y轴为绿色，否则白色
                if is_min_edge and (start[1] != end[1]):
                    color = (0.0, 1.0, 0.0, 1.0)
                else:
                    color = (1.0, 1.0, 1.0, 1.0)

            entities.append(self._createOutlineEntity((center_x, center_y, center_z), rot, scale, color))

        return entities

    def _createOutlineEntity(self, pos, rot, scale, color):
        """创建单个边框实体"""
        # 根据颜色选择不同的json文件
        if color == (1.0, 0.0, 0.0, 1.0):  # 红色
            json_file = "effects/block_selected_box_red.json"
        elif color == (0.0, 1.0, 0.0, 1.0):  # 绿色
            json_file = "effects/block_selected_box_green.json"
        elif color == (0.0, 0.0, 1.0, 1.0):  # 蓝色
            json_file = "effects/block_selected_box_blue.json"
        else:  # 白色或其他颜色
            json_file = "effects/block_selected_box.json"

        frameEntityId = self.parent.CreateEngineSfxFromEditor(json_file)
        frameAniTransComp = clientApi.GetEngineCompFactory().CreateFrameAniTrans(frameEntityId)
        frameAniTransComp.SetPos(pos)
        frameAniTransComp.SetRot(rot)
        frameAniTransComp.SetScale(scale)

        frameAniControlComp = clientApi.GetEngineCompFactory().CreateFrameAniControl(frameEntityId)
        frameAniControlComp.Play()

        return frameEntityId

    def renderOutline(self, min_pos, max_pos):
        """完整的立方体边框渲染"""
        x1, y1, z1 = min_pos
        x2, y2, z2 = max_pos

        min_point = (x1, y1, z1)  # 最小点

        outline_entities = []

        # 底面和顶面
        outline_entities.extend(self.renderHorizontalFace(y1, x1, z1, x2, z2, min_point))  # 底面
        outline_entities.extend(self.renderHorizontalFace(y2, x1, z1, x2, z2, min_point))  # 顶面

        # 左面和右面
        outline_entities.extend(self.renderVerticalXFace(x1, y1, z1, y2, z2, min_point))  # 左面
        outline_entities.extend(self.renderVerticalXFace(x2, y1, z1, y2, z2, min_point))  # 右面

        # 前面和后面
        outline_entities.extend(self.renderVerticalZFace(z2, x1, y1, x2, y2, min_point))  # 前面
        outline_entities.extend(self.renderVerticalZFace(z1, x1, y1, x2, y2, min_point))  # 后面

        return outline_entities


    def removeCube(self, cube_id):
        """
        删除指定的立方体（包括其描边）
        cube_id: renderCube返回的ID
        """
        removed = False

        # 删除立方体面
        if cube_id in self.cubes:
            for face_id in self.cubes[cube_id]:
                self.parent.DestroyEntity(face_id)
            del self.cubes[cube_id]
            removed = True

        # 删除描边线条
        if cube_id in self.outlines:
            for line_obj in self.outlines[cube_id]:
                self.parent.DestroyEntity(line_obj)
            del self.outlines[cube_id]
            removed = True

        return removed

    def removeOutline(self, outline_id):
        """
        删除指定的描边
        outline_id: renderOutlineOnly返回的ID
        """
        if outline_id in self.outlines:
            for line_obj in self.outlines[outline_id]:
                line_obj.Remove()
            del self.outlines[outline_id]
            return True
        return False

    def removeAllCubes(self):
        """删除所有立方体（包括描边）"""
        # 删除所有立方体面
        for cube_id in list(self.cubes.keys()):
            for face_id in self.cubes[cube_id]:
                self.parent.DestroyEntity(face_id)
            del self.cubes[cube_id]

        # 删除所有描边线条
        for outline_id in list(self.outlines.keys()):
            for line_obj in self.outlines[outline_id]:
                line_obj.Remove()
            del self.outlines[outline_id]