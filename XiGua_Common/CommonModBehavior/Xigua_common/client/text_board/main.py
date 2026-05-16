# -*- coding: utf-8 -*-
from ..utils.ClientSystem_utils import *


class TextBoard(BaseSystem):
    def __init__(self, namespace, systemName):
        super(TextBoard, self).__init__(namespace, systemName)
        self.textBoardComp = textBoardComp
        self.all_text_board = {}
        self.image_board = {}

    @Listen(event_name="textBoard", event_type=Listen.server)
    def handleTextBoard(self, args):
        """服务端文字面板事件监听"""
        action = args.get("action")
        if action == "init":
            self._destroy_all()
            return

        board_key = args.get("boardId")
        if not board_key:
            return

        if action == "create":
            self._handle_create(board_key, args)
            return

        board_data = self.all_text_board.get(board_key)
        if not board_data:
            return

        if action == "update":
            self._update(board_data, args)
        elif action == "delete":
            self._delete_board(board_key)

    def _handle_create(self, board_key, args):
        if args.get("image"):
            self._handle_create_image(board_key, args)
            return
        old_board = self.all_text_board.get(board_key)
        if old_board:
            self._remove_client_board(old_board.get("clientBoardId"))

        board_data = self._create(args)
        if board_data:
            self.all_text_board[board_key] = board_data

    def _handle_create_image(self, board_key, args):
        image = args.get("image")
        frameEntityId = self.image_board.pop(board_key, None)
        if frameEntityId:
            self.DestroyEntity(frameEntityId)

        json_file = "effects/" + scoreboard_title_image_dict.get(image) + ".json"
        frameEntityId = self.CreateEngineSfxFromEditor(json_file)
        if frameEntityId:
            frameAniTransComp = clientApi.GetEngineCompFactory().CreateFrameAniTrans(frameEntityId)
            frameAniTransComp.SetPos(self._get_pos(args))
            frameAniTransComp.SetRot(self._get_rot(args))
            scale_x, scale_y = self._get_scale(args)
            frameAniTransComp.SetScale((scale_x, scale_y, 0))
            frameAniControlComp = clientApi.GetEngineCompFactory().CreateFrameAniControl(frameEntityId)
            frameAniControlComp.SetFaceCamera(args.get("faceCamera", True))
            frameAniControlComp.SetDeepTest(args.get("depthTest", True))
            frameAniControlComp.Play()
            self.image_board[board_key] = frameEntityId
        else:
            self._handle_create(board_key, args)

    def _create(self, args):
        """创建文字面板"""
        bind_type = args.get("bindType", "WORLD")
        text = args.get("text", "")
        text_color = self._color_to_float(self._get_color(args, "textColor", (255, 255, 255, 255)))
        board_color = self._color_to_float(self._get_color(args, "boardColor", (0, 0, 0, 100)))
        face_camera = args.get("faceCamera", True)
        client_board_id = self.textBoardComp.CreateTextBoardInWorld(text, text_color, board_color, face_camera)
        if not client_board_id:
            return None

        board_data = {
            "clientBoardId": client_board_id,
            "bindType": bind_type,
            "bindEntityId": args.get("bindEntityId"),
            "pos": self._get_pos(args),
            "offset": self._get_offset(args),
            "rot": self._get_rot(args),
            "scale": self._get_scale(args),
        }

        if bind_type == "ENTITY":
            bind_entity_id = board_data.get("bindEntityId")
            if bind_entity_id is None:
                self._remove_client_board(client_board_id)
                return None
            self.textBoardComp.SetBoardBindEntity(
                client_board_id,
                bind_entity_id,
                board_data["offset"],
                board_data["rot"]
            )
        else:
            self.textBoardComp.SetBoardPos(client_board_id, board_data["pos"])
            self.textBoardComp.SetBoardRot(client_board_id, board_data["rot"])

        self.textBoardComp.SetBoardScale(client_board_id, board_data["scale"])
        self.textBoardComp.SetBoardDepthTest(client_board_id, args.get("depthTest", True))
        return board_data

    def _update(self, board_data, args):
        """更新文字面板"""
        client_board_id = board_data.get("clientBoardId")
        if not client_board_id:
            return

        if "text" in args:
            self.textBoardComp.SetText(client_board_id, args.get("text", ""))

        if "textColor" in args:
            color = self._color_to_float(self._get_color(args, "textColor"))
            self.textBoardComp.SetBoardTextColor(client_board_id, color)

        if "boardColor" in args:
            color = self._color_to_float(self._get_color(args, "boardColor"))
            self.textBoardComp.SetBoardBackgroundColor(client_board_id, color)

        if "faceCamera" in args:
            self.textBoardComp.SetBoardFaceCamera(client_board_id, args.get("faceCamera", True))

        if "depthTest" in args:
            self.textBoardComp.SetBoardDepthTest(client_board_id, args.get("depthTest", True))

        bind_type = board_data.get("bindType", "WORLD")
        if bind_type == "ENTITY":
            if "offset" in args:
                board_data["offset"] = self._get_offset(args)
            if "rot" in args:
                board_data["rot"] = self._get_rot(args)

            if "offset" in args or "rot" in args:
                self.textBoardComp.SetBoardBindEntity(
                    client_board_id,
                    board_data.get("bindEntityId"),
                    board_data.get("offset", (0, 0, 0)),
                    board_data.get("rot", (0, 0, 0))
                )
        else:
            if "pos" in args:
                board_data["pos"] = self._get_pos(args)
                self.textBoardComp.SetBoardPos(client_board_id, board_data["pos"])

            if "rot" in args:
                board_data["rot"] = self._get_rot(args)
                self.textBoardComp.SetBoardRot(client_board_id, board_data["rot"])

        if "scale" in args:
            board_data["scale"] = self._get_scale(args)
            self.textBoardComp.SetBoardScale(client_board_id, board_data["scale"])

    def _delete_board(self, board_key):
        board_data = self.all_text_board.pop(board_key, None)
        if board_data:
            self._remove_client_board(board_data.get("clientBoardId"))
        else:
            frameEntityId = self.image_board.pop(board_key, None)
            if frameEntityId:
                self.DestroyEntity(frameEntityId)

    def _remove_client_board(self, client_board_id):
        if client_board_id:
            self.textBoardComp.RemoveTextBoard(client_board_id)

    def _destroy_all(self):
        """销毁所有文字面板"""
        for board_data in self.all_text_board.values():
            self._remove_client_board(board_data.get("clientBoardId"))
        self.all_text_board.clear()

    def _color_to_float(self, color_tuple):
        """将 0-255 颜色转换为 0-1 浮点颜色"""
        r, g, b, a = color_tuple
        return r / 255.0, g / 255.0, b / 255.0, a / 255.0

    def _get_color(self, args, key, default=(255, 255, 255, 255)):
        color_dict = args.get(key, {})
        return (
            color_dict.get("r", default[0]),
            color_dict.get("g", default[1]),
            color_dict.get("b", default[2]),
            color_dict.get("a", default[3])
        )

    def _get_offset(self, args):
        offset_dict = args.get("offset", {})
        return offset_dict.get("x", 0), offset_dict.get("y", 0), offset_dict.get("z", 0)

    def _get_pos(self, args):
        pos_dict = args.get("pos", {})
        return pos_dict.get("x", 0), pos_dict.get("y", 0), pos_dict.get("z", 0)

    def _get_rot(self, args):
        rot_dict = args.get("rot", {})
        return rot_dict.get("x", 0), rot_dict.get("y", 0), rot_dict.get("z", 0)

    def _get_scale(self, args):
        scale_dict = args.get("scale", {})
        return scale_dict.get("x", 1.0), scale_dict.get("y", 1.0)
