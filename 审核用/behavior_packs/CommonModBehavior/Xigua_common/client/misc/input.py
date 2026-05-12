# -*- coding: utf-8 -*-
from ..utils.ClientSystem_utils import *


def handle_alt_camera_key(args):
    key = args.get("key")
    is_down = args.get("isDown")
    if is_down == "1":
        if key == "18":
            CF.CreateCamera(levelId).DepartCamera()
    else:
        if key == "18":
            CF.CreateCamera(levelId).UnDepartCamera()
