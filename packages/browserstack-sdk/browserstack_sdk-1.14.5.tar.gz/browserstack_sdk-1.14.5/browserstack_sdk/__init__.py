# coding: UTF-8
import sys
bstack1l1lll1ll_opy_ = sys.version_info [0] == 2
bstack111l1ll1l_opy_ = 2048
bstack11llllll_opy_ = 7
def bstack1lllllll1_opy_ (bstack11lll1ll1_opy_):
    global bstack1l11l111_opy_
    stringNr = ord (bstack11lll1ll1_opy_ [-1])
    bstack1111lll_opy_ = bstack11lll1ll1_opy_ [:-1]
    bstack111l1ll1_opy_ = stringNr % len (bstack1111lll_opy_)
    bstack11lll111_opy_ = bstack1111lll_opy_ [:bstack111l1ll1_opy_] + bstack1111lll_opy_ [bstack111l1ll1_opy_:]
    if bstack1l1lll1ll_opy_:
        bstack111lll1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1ll1l_opy_ - (bstack11ll1111l_opy_ + stringNr) % bstack11llllll_opy_) for bstack11ll1111l_opy_, char in enumerate (bstack11lll111_opy_)])
    else:
        bstack111lll1ll_opy_ = str () .join ([chr (ord (char) - bstack111l1ll1l_opy_ - (bstack11ll1111l_opy_ + stringNr) % bstack11llllll_opy_) for bstack11ll1111l_opy_, char in enumerate (bstack11lll111_opy_)])
    return eval (bstack111lll1ll_opy_)
import atexit
import os
import signal
import sys
import time
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
from multiprocessing import Pool
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
bstack1ll1llll1_opy_ = {
	bstack1lllllll1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࠀ"): bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࠩࠁ"),
  bstack1lllllll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩࠂ"): bstack1lllllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡫ࡦࡻࠪࠃ"),
  bstack1lllllll1_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫࠄ"): bstack1lllllll1_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ࠅ"),
  bstack1lllllll1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪࠆ"): bstack1lllllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫࡟ࡸ࠵ࡦࠫࠇ"),
  bstack1lllllll1_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪࠈ"): bstack1lllllll1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࠧࠉ"),
  bstack1lllllll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪࠊ"): bstack1lllllll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧࠋ"),
  bstack1lllllll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࠌ"): bstack1lllllll1_opy_ (u"ࠪࡲࡦࡳࡥࠨࠍ"),
  bstack1lllllll1_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪࠎ"): bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩࠪࠏ"),
  bstack1lllllll1_opy_ (u"࠭ࡣࡰࡰࡶࡳࡱ࡫ࡌࡰࡩࡶࠫࠐ"): bstack1lllllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰࡰࡶࡳࡱ࡫ࠧࠑ"),
  bstack1lllllll1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭ࠒ"): bstack1lllllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭ࠓ"),
  bstack1lllllll1_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧࠔ"): bstack1lllllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧࠕ"),
  bstack1lllllll1_opy_ (u"ࠬࡼࡩࡥࡧࡲࠫࠖ"): bstack1lllllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡼࡩࡥࡧࡲࠫࠗ"),
  bstack1lllllll1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭࠘"): bstack1lllllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭࠙"),
  bstack1lllllll1_opy_ (u"ࠩࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩࠚ"): bstack1lllllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩࠛ"),
  bstack1lllllll1_opy_ (u"ࠫ࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩࠜ"): bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩࠝ"),
  bstack1lllllll1_opy_ (u"࠭ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨࠞ"): bstack1lllllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨࠟ"),
  bstack1lllllll1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࠠ"): bstack1lllllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫࠡ"),
  bstack1lllllll1_opy_ (u"ࠪࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩࠢ"): bstack1lllllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩࠣ"),
  bstack1lllllll1_opy_ (u"ࠬ࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪࠤ"): bstack1lllllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪࠥ"),
  bstack1lllllll1_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧࠦ"): bstack1lllllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧࠧ"),
  bstack1lllllll1_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡶࠫࠨ"): bstack1lllllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡳࡪࡋࡦࡻࡶࠫࠩ"),
  bstack1lllllll1_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭ࠪ"): bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭ࠫ"),
  bstack1lllllll1_opy_ (u"࠭ࡨࡰࡵࡷࡷࠬࠬ"): bstack1lllllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡨࡰࡵࡷࡷࠬ࠭"),
  bstack1lllllll1_opy_ (u"ࠨࡤࡩࡧࡦࡩࡨࡦࠩ࠮"): bstack1lllllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡩࡧࡦࡩࡨࡦࠩ࠯"),
  bstack1lllllll1_opy_ (u"ࠪࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫ࠰"): bstack1lllllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫ࠱"),
  bstack1lllllll1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ࠲"): bstack1lllllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ࠳"),
  bstack1lllllll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ࠴"): bstack1lllllll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ࠵"),
  bstack1lllllll1_opy_ (u"ࠩࡵࡩࡦࡲࡍࡰࡤ࡬ࡰࡪ࠭࠶"): bstack1lllllll1_opy_ (u"ࠪࡶࡪࡧ࡬ࡠ࡯ࡲࡦ࡮ࡲࡥࠨ࠷"),
  bstack1lllllll1_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ࠸"): bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ࠹"),
  bstack1lllllll1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭࠺"): bstack1lllllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭࠻"),
  bstack1lllllll1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩ࠼"): bstack1lllllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩ࠽"),
  bstack1lllllll1_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩ࠾"): bstack1lllllll1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࡷࠬ࠿"),
  bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧࡀ"): bstack1lllllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧࡁ"),
  bstack1lllllll1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧࡂ"): bstack1lllllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡱࡸࡶࡨ࡫ࠧࡃ"),
  bstack1lllllll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࡄ"): bstack1lllllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࡅ"),
  bstack1lllllll1_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ࡆ"): bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ࡇ"),
}
bstack1llllll1_opy_ = [
  bstack1lllllll1_opy_ (u"࠭࡯ࡴࠩࡈ"),
  bstack1lllllll1_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪࡉ"),
  bstack1lllllll1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࡊ"),
  bstack1lllllll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࡋ"),
  bstack1lllllll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧࡌ"),
  bstack1lllllll1_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨࡍ"),
  bstack1lllllll1_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬࡎ"),
]
bstack1l111111_opy_ = {
  bstack1lllllll1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࡏ"): [bstack1lllllll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨࡐ"), bstack1lllllll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡤࡔࡁࡎࡇࠪࡑ")],
  bstack1lllllll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬࡒ"): bstack1lllllll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ࡓ"),
  bstack1lllllll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࡔ"): bstack1lllllll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠨࡕ"),
  bstack1lllllll1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫࡖ"): bstack1lllllll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡏࡃࡐࡉࠬࡗ"),
  bstack1lllllll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࡘ"): bstack1lllllll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕ࡙ࠫ"),
  bstack1lllllll1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯࡚ࠪ"): bstack1lllllll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡆࡘࡁࡍࡎࡈࡐࡘࡥࡐࡆࡔࡢࡔࡑࡇࡔࡇࡑࡕࡑ࡛ࠬ"),
  bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ࡜"): bstack1lllllll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࠫ࡝"),
  bstack1lllllll1_opy_ (u"ࠧࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫ࡞"): bstack1lllllll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠬ࡟"),
  bstack1lllllll1_opy_ (u"ࠩࡤࡴࡵ࠭ࡠ"): [bstack1lllllll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡔࡕࡥࡉࡅࠩࡡ"), bstack1lllllll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡕࡖࠧࡢ")],
  bstack1lllllll1_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧࡣ"): bstack1lllllll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࡤࡊࡅࡃࡗࡊࠫࡤ"),
  bstack1lllllll1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫࡥ"): bstack1lllllll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫࡦ")
}
bstack11l1l111l_opy_ = {
  bstack1lllllll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࡧ"): [bstack1lllllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸ࡟࡯ࡣࡰࡩࠬࡨ"), bstack1lllllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࡩ")],
  bstack1lllllll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࡪ"): [bstack1lllllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡤࡱࡥࡺࠩ࡫"), bstack1lllllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ࡬")],
  bstack1lllllll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡭"): bstack1lllllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡮"),
  bstack1lllllll1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ࡯"): bstack1lllllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨࡰ"),
  bstack1lllllll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡱ"): bstack1lllllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡲ"),
  bstack1lllllll1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧࡳ"): [bstack1lllllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡲࡳࠫࡴ"), bstack1lllllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࡵ")],
  bstack1lllllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࡶ"): bstack1lllllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩࡷ"),
  bstack1lllllll1_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡸ"): bstack1lllllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡹ"),
  bstack1lllllll1_opy_ (u"ࠧࡢࡲࡳࠫࡺ"): bstack1lllllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳࠫࡻ"),
  bstack1lllllll1_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡼ"): bstack1lllllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡽ"),
  bstack1lllllll1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡾ"): bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡿ")
}
bstack1l11lll11_opy_ = {
  bstack1lllllll1_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩࢀ"): bstack1lllllll1_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫࢁ"),
  bstack1lllllll1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࢂ"): [bstack1lllllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫࢃ"), bstack1lllllll1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ࢄ")],
  bstack1lllllll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢅ"): bstack1lllllll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢆ"),
  bstack1lllllll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪࢇ"): bstack1lllllll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ࢈"),
  bstack1lllllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ࢉ"): [bstack1lllllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪࢊ"), bstack1lllllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩࢋ")],
  bstack1lllllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢌ"): bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࢍ"),
  bstack1lllllll1_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪࢎ"): bstack1lllllll1_opy_ (u"ࠧࡳࡧࡤࡰࡤࡳ࡯ࡣ࡫࡯ࡩࠬ࢏"),
  bstack1lllllll1_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࢐"): [bstack1lllllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ࢑"), bstack1lllllll1_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫ࢒")],
  bstack1lllllll1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࢓"): [bstack1lllllll1_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭࢔"), bstack1lllllll1_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹ࠭࢕")]
}
bstack1ll1l11l_opy_ = [
  bstack1lllllll1_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭࢖"),
  bstack1lllllll1_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫࢗ"),
  bstack1lllllll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ࢘"),
  bstack1lllllll1_opy_ (u"ࠪࡷࡪࡺࡗࡪࡰࡧࡳࡼࡘࡥࡤࡶ࢙ࠪ"),
  bstack1lllllll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࢚࠭"),
  bstack1lllllll1_opy_ (u"ࠬࡹࡴࡳ࡫ࡦࡸࡋ࡯࡬ࡦࡋࡱࡸࡪࡸࡡࡤࡶࡤࡦ࡮ࡲࡩࡵࡻ࢛ࠪ"),
  bstack1lllllll1_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩ࢜"),
  bstack1lllllll1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ࢝"),
  bstack1lllllll1_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭࢞"),
  bstack1lllllll1_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ࢟"),
  bstack1lllllll1_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢠ"),
  bstack1lllllll1_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬࢡ"),
]
bstack111l111l_opy_ = [
  bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࢢ"),
  bstack1lllllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢣ"),
  bstack1lllllll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢤ"),
  bstack1lllllll1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࢥ"),
  bstack1lllllll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢦ"),
  bstack1lllllll1_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬࢧ"),
  bstack1lllllll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧࢨ"),
  bstack1lllllll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩࢩ"),
  bstack1lllllll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩࢪ"),
  bstack1lllllll1_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬࢫ")
]
bstack11l1l1lll_opy_ = [
  bstack1lllllll1_opy_ (u"ࠨࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭ࢬ"),
  bstack1lllllll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࢭ"),
  bstack1lllllll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࢮ"),
  bstack1lllllll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢯ"),
  bstack1lllllll1_opy_ (u"ࠬࡺࡥࡴࡶࡓࡶ࡮ࡵࡲࡪࡶࡼࠫࢰ"),
  bstack1lllllll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩࢱ"),
  bstack1lllllll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚ࡡࡨࠩࢲ"),
  bstack1lllllll1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ࢳ"),
  bstack1lllllll1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࢴ"),
  bstack1lllllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࢵ"),
  bstack1lllllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢶ"),
  bstack1lllllll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫࢷ"),
  bstack1lllllll1_opy_ (u"࠭࡯ࡴࠩࢸ"),
  bstack1lllllll1_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪࢹ"),
  bstack1lllllll1_opy_ (u"ࠨࡪࡲࡷࡹࡹࠧࢺ"),
  bstack1lllllll1_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷࠫࢻ"),
  bstack1lllllll1_opy_ (u"ࠪࡶࡪ࡭ࡩࡰࡰࠪࢼ"),
  bstack1lllllll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭ࢽ"),
  bstack1lllllll1_opy_ (u"ࠬࡳࡡࡤࡪ࡬ࡲࡪ࠭ࢾ"),
  bstack1lllllll1_opy_ (u"࠭ࡲࡦࡵࡲࡰࡺࡺࡩࡰࡰࠪࢿ"),
  bstack1lllllll1_opy_ (u"ࠧࡪࡦ࡯ࡩ࡙࡯࡭ࡦࡱࡸࡸࠬࣀ"),
  bstack1lllllll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬࣁ"),
  bstack1lllllll1_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࠨࣂ"),
  bstack1lllllll1_opy_ (u"ࠪࡲࡴࡖࡡࡨࡧࡏࡳࡦࡪࡔࡪ࡯ࡨࡳࡺࡺࠧࣃ"),
  bstack1lllllll1_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬࣄ"),
  bstack1lllllll1_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࣅ"),
  bstack1lllllll1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪࣆ"),
  bstack1lllllll1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡦࡰࡧࡏࡪࡿࡳࠨࣇ"),
  bstack1lllllll1_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬࣈ"),
  bstack1lllllll1_opy_ (u"ࠩࡱࡳࡕ࡯ࡰࡦ࡮࡬ࡲࡪ࠭ࣉ"),
  bstack1lllllll1_opy_ (u"ࠪࡧ࡭࡫ࡣ࡬ࡗࡕࡐࠬ࣊"),
  bstack1lllllll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣋"),
  bstack1lllllll1_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡈࡵ࡯࡬࡫ࡨࡷࠬ࣌"),
  bstack1lllllll1_opy_ (u"࠭ࡣࡢࡲࡷࡹࡷ࡫ࡃࡳࡣࡶ࡬ࠬ࣍"),
  bstack1lllllll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ࣎"),
  bstack1lllllll1_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࣏"),
  bstack1lllllll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࡜ࡥࡳࡵ࡬ࡳࡳ࣐࠭"),
  bstack1lllllll1_opy_ (u"ࠪࡲࡴࡈ࡬ࡢࡰ࡮ࡔࡴࡲ࡬ࡪࡰࡪ࣑ࠫ"),
  bstack1lllllll1_opy_ (u"ࠫࡲࡧࡳ࡬ࡕࡨࡲࡩࡑࡥࡺࡵ࣒ࠪ"),
  bstack1lllllll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡑࡵࡧࡴ࣓ࠩ"),
  bstack1lllllll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡏࡤࠨࣔ"),
  bstack1lllllll1_opy_ (u"ࠧࡥࡧࡧ࡭ࡨࡧࡴࡦࡦࡇࡩࡻ࡯ࡣࡦࠩࣕ"),
  bstack1lllllll1_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡑࡣࡵࡥࡲࡹࠧࣖ"),
  bstack1lllllll1_opy_ (u"ࠩࡳ࡬ࡴࡴࡥࡏࡷࡰࡦࡪࡸࠧࣗ"),
  bstack1lllllll1_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࠨࣘ"),
  bstack1lllllll1_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣙ"),
  bstack1lllllll1_opy_ (u"ࠬࡩ࡯࡯ࡵࡲࡰࡪࡒ࡯ࡨࡵࠪࣚ"),
  bstack1lllllll1_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ࣛ"),
  bstack1lllllll1_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫࣜ"),
  bstack1lllllll1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡃ࡫ࡲࡱࡪࡺࡲࡪࡥࠪࣝ"),
  bstack1lllllll1_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࡗ࠴ࠪࣞ"),
  bstack1lllllll1_opy_ (u"ࠪࡱ࡮ࡪࡓࡦࡵࡶ࡭ࡴࡴࡉ࡯ࡵࡷࡥࡱࡲࡁࡱࡲࡶࠫࣟ"),
  bstack1lllllll1_opy_ (u"ࠫࡪࡹࡰࡳࡧࡶࡷࡴ࡙ࡥࡳࡸࡨࡶࠬ࣠"),
  bstack1lllllll1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫ࣡"),
  bstack1lllllll1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡄࡦࡳࠫ࣢"),
  bstack1lllllll1_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࣣࠧ"),
  bstack1lllllll1_opy_ (u"ࠨࡵࡼࡲࡨ࡚ࡩ࡮ࡧ࡚࡭ࡹ࡮ࡎࡕࡒࠪࣤ"),
  bstack1lllllll1_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧࣥ"),
  bstack1lllllll1_opy_ (u"ࠪ࡫ࡵࡹࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨࣦ"),
  bstack1lllllll1_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬࣧ"),
  bstack1lllllll1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬࣨ"),
  bstack1lllllll1_opy_ (u"࠭ࡦࡰࡴࡦࡩࡈ࡮ࡡ࡯ࡩࡨࡎࡦࡸࣩࠧ"),
  bstack1lllllll1_opy_ (u"ࠧࡹ࡯ࡶࡎࡦࡸࠧ࣪"),
  bstack1lllllll1_opy_ (u"ࠨࡺࡰࡼࡏࡧࡲࠨ࣫"),
  bstack1lllllll1_opy_ (u"ࠩࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨ࣬"),
  bstack1lllllll1_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪ࣭ࠪ"),
  bstack1lllllll1_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸ࣮ࠬ"),
  bstack1lllllll1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ࣯"),
  bstack1lllllll1_opy_ (u"࠭ࡡࡱࡲ࡙ࡩࡷࡹࡩࡰࡰࣰࠪ"),
  bstack1lllllll1_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸࣱ࠭"),
  bstack1lllllll1_opy_ (u"ࠨࡴࡨࡷ࡮࡭࡮ࡂࡲࡳࣲࠫ"),
  bstack1lllllll1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࡸ࠭ࣳ"),
  bstack1lllllll1_opy_ (u"ࠪࡧࡦࡴࡡࡳࡻࠪࣴ"),
  bstack1lllllll1_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬࣵ"),
  bstack1lllllll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࣶࠬ"),
  bstack1lllllll1_opy_ (u"࠭ࡩࡦࠩࣷ"),
  bstack1lllllll1_opy_ (u"ࠧࡦࡦࡪࡩࠬࣸ"),
  bstack1lllllll1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨࣹ"),
  bstack1lllllll1_opy_ (u"ࠩࡴࡹࡪࡻࡥࠨࣺ"),
  bstack1lllllll1_opy_ (u"ࠪ࡭ࡳࡺࡥࡳࡰࡤࡰࠬࣻ"),
  bstack1lllllll1_opy_ (u"ࠫࡦࡶࡰࡔࡶࡲࡶࡪࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠬࣼ"),
  bstack1lllllll1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡈࡧ࡭ࡦࡴࡤࡍࡲࡧࡧࡦࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫࣽ"),
  bstack1lllllll1_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡉࡽࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩࣾ"),
  bstack1lllllll1_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡎࡴࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪࣿ"),
  bstack1lllllll1_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷࠬऀ"),
  bstack1lllllll1_opy_ (u"ࠩࡵࡩࡸ࡫ࡲࡷࡧࡇࡩࡻ࡯ࡣࡦࠩँ"),
  bstack1lllllll1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪं"),
  bstack1lllllll1_opy_ (u"ࠫࡸ࡫࡮ࡥࡍࡨࡽࡸ࠭ः"),
  bstack1lllllll1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡕࡧࡳࡴࡥࡲࡨࡪ࠭ऄ"),
  bstack1lllllll1_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡏ࡯ࡴࡆࡨࡺ࡮ࡩࡥࡔࡧࡷࡸ࡮ࡴࡧࡴࠩअ"),
  bstack1lllllll1_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡶࡦ࡬ࡳࡎࡴࡪࡦࡥࡷ࡭ࡴࡴࠧआ"),
  bstack1lllllll1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡲࡳࡰࡪࡖࡡࡺࠩइ"),
  bstack1lllllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪई"),
  bstack1lllllll1_opy_ (u"ࠪࡻࡩ࡯࡯ࡔࡧࡵࡺ࡮ࡩࡥࠨउ"),
  bstack1lllllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ऊ"),
  bstack1lllllll1_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹࡉࡲࡰࡵࡶࡗ࡮ࡺࡥࡕࡴࡤࡧࡰ࡯࡮ࡨࠩऋ"),
  bstack1lllllll1_opy_ (u"࠭ࡨࡪࡩ࡫ࡇࡴࡴࡴࡳࡣࡶࡸࠬऌ"),
  bstack1lllllll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡐࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࡶࠫऍ"),
  bstack1lllllll1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡔ࡫ࡰࠫऎ"),
  bstack1lllllll1_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ए"),
  bstack1lllllll1_opy_ (u"ࠪࡶࡪࡳ࡯ࡷࡧࡌࡓࡘࡇࡰࡱࡕࡨࡸࡹ࡯࡮ࡨࡵࡏࡳࡨࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨऐ"),
  bstack1lllllll1_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ऑ"),
  bstack1lllllll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ"),
  bstack1lllllll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨओ"),
  bstack1lllllll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭औ"),
  bstack1lllllll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪक"),
  bstack1lllllll1_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬख"),
  bstack1lllllll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩग"),
  bstack1lllllll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࠭घ"),
  bstack1lllllll1_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨङ")
]
bstack1ll1ll11l_opy_ = {
  bstack1lllllll1_opy_ (u"࠭ࡶࠨच"): bstack1lllllll1_opy_ (u"ࠧࡷࠩछ"),
  bstack1lllllll1_opy_ (u"ࠨࡨࠪज"): bstack1lllllll1_opy_ (u"ࠩࡩࠫझ"),
  bstack1lllllll1_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩञ"): bstack1lllllll1_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪट"),
  bstack1lllllll1_opy_ (u"ࠬࡵ࡮࡭ࡻࡤࡹࡹࡵ࡭ࡢࡶࡨࠫठ"): bstack1lllllll1_opy_ (u"࠭࡯࡯࡮ࡼࡅࡺࡺ࡯࡮ࡣࡷࡩࠬड"),
  bstack1lllllll1_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫढ"): bstack1lllllll1_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬण"),
  bstack1lllllll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬत"): bstack1lllllll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭थ"),
  bstack1lllllll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧद"): bstack1lllllll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨध"),
  bstack1lllllll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩन"): bstack1lllllll1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऩ"),
  bstack1lllllll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫप"): bstack1lllllll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬफ"),
  bstack1lllllll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫब"): bstack1lllllll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡉࡱࡶࡸࠬभ"),
  bstack1lllllll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭म"): bstack1lllllll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧय"),
  bstack1lllllll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨर"): bstack1lllllll1_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऱ"),
  bstack1lllllll1_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫल"): bstack1lllllll1_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬळ"),
  bstack1lllllll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬऴ"): bstack1lllllll1_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡥࡸࡹࠧव"),
  bstack1lllllll1_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨश"): bstack1lllllll1_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩष"),
  bstack1lllllll1_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬस"): bstack1lllllll1_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ह"),
  bstack1lllllll1_opy_ (u"ࠪࡴࡦࡩࡦࡪ࡮ࡨࠫऺ"): bstack1lllllll1_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧऻ"),
  bstack1lllllll1_opy_ (u"ࠬࡶࡡࡤ࠯ࡩ࡭ࡱ࡫़ࠧ"): bstack1lllllll1_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩऽ"),
  bstack1lllllll1_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪा"): bstack1lllllll1_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫि"),
  bstack1lllllll1_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪी"): bstack1lllllll1_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫु"),
  bstack1lllllll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ू"): bstack1lllllll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧृ"),
}
bstack111111ll_opy_ = bstack1lllllll1_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡸࡦ࠲࡬ࡺࡨࠧॄ")
bstack1l1ll1l11_opy_ = bstack1lllllll1_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠪॅ")
bstack1l11111l1_opy_ = bstack1lllllll1_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠬॆ")
bstack111lll1l_opy_ = {
  bstack1lllllll1_opy_ (u"ࠩࡦࡶ࡮ࡺࡩࡤࡣ࡯ࠫे"): 50,
  bstack1lllllll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩै"): 40,
  bstack1lllllll1_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬॉ"): 30,
  bstack1lllllll1_opy_ (u"ࠬ࡯࡮ࡧࡱࠪॊ"): 20,
  bstack1lllllll1_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬो"): 10
}
bstack11lll1l1_opy_ = bstack111lll1l_opy_[bstack1lllllll1_opy_ (u"ࠧࡪࡰࡩࡳࠬौ")]
bstack1ll11111_opy_ = bstack1lllllll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵्ࠧ")
bstack1ll111lll_opy_ = bstack1lllllll1_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧॎ")
bstack1l1l1llll_opy_ = bstack1lllllll1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩॏ")
bstack1llll11_opy_ = bstack1lllllll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪॐ")
bstack1lll11ll_opy_ = [bstack1lllllll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭॑"), bstack1lllllll1_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ॒࠭")]
bstack11l_opy_ = [bstack1lllllll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॓"), bstack1lllllll1_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॔")]
bstack1ll1l1l11_opy_ = [
  bstack1lllllll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡔࡡ࡮ࡧࠪॕ"),
  bstack1lllllll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬॖ"),
  bstack1lllllll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨॗ"),
  bstack1lllllll1_opy_ (u"ࠬࡴࡥࡸࡅࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࠩक़"),
  bstack1lllllll1_opy_ (u"࠭ࡡࡱࡲࠪख़"),
  bstack1lllllll1_opy_ (u"ࠧࡶࡦ࡬ࡨࠬग़"),
  bstack1lllllll1_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪज़"),
  bstack1lllllll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡦࠩड़"),
  bstack1lllllll1_opy_ (u"ࠪࡳࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨढ़"),
  bstack1lllllll1_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡨࡦࡻ࡯ࡥࡸࠩफ़"),
  bstack1lllllll1_opy_ (u"ࠬࡴ࡯ࡓࡧࡶࡩࡹ࠭य़"), bstack1lllllll1_opy_ (u"࠭ࡦࡶ࡮࡯ࡖࡪࡹࡥࡵࠩॠ"),
  bstack1lllllll1_opy_ (u"ࠧࡤ࡮ࡨࡥࡷ࡙ࡹࡴࡶࡨࡱࡋ࡯࡬ࡦࡵࠪॡ"),
  bstack1lllllll1_opy_ (u"ࠨࡧࡹࡩࡳࡺࡔࡪ࡯࡬ࡲ࡬ࡹࠧॢ"),
  bstack1lllllll1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡨࡶ࡫ࡵࡲ࡮ࡣࡱࡧࡪࡒ࡯ࡨࡩ࡬ࡲ࡬࠭ॣ"),
  bstack1lllllll1_opy_ (u"ࠪࡳࡹ࡮ࡥࡳࡃࡳࡴࡸ࠭।"),
  bstack1lllllll1_opy_ (u"ࠫࡵࡸࡩ࡯ࡶࡓࡥ࡬࡫ࡓࡰࡷࡵࡧࡪࡕ࡮ࡇ࡫ࡱࡨࡋࡧࡩ࡭ࡷࡵࡩࠬ॥"),
  bstack1lllllll1_opy_ (u"ࠬࡧࡰࡱࡃࡦࡸ࡮ࡼࡩࡵࡻࠪ०"), bstack1lllllll1_opy_ (u"࠭ࡡࡱࡲࡓࡥࡨࡱࡡࡨࡧࠪ१"), bstack1lllllll1_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩ२"), bstack1lllllll1_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡒࡤࡧࡰࡧࡧࡦࠩ३"), bstack1lllllll1_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡇࡹࡷࡧࡴࡪࡱࡱࠫ४"),
  bstack1lllllll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨ५"),
  bstack1lllllll1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡩࡸࡺࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠨ६"),
  bstack1lllllll1_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࠧ७"), bstack1lllllll1_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࡆࡰࡧࡍࡳࡺࡥ࡯ࡶࠪ८"),
  bstack1lllllll1_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡒࡦࡣࡧࡽ࡙࡯࡭ࡦࡱࡸࡸࠬ९"),
  bstack1lllllll1_opy_ (u"ࠨࡣࡧࡦࡕࡵࡲࡵࠩ॰"),
  bstack1lllllll1_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡕࡲࡧࡰ࡫ࡴࠨॱ"),
  bstack1lllllll1_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡘ࡮ࡳࡥࡰࡷࡷࠫॲ"),
  bstack1lllllll1_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡴࡩࠩॳ"),
  bstack1lllllll1_opy_ (u"ࠬࡧࡶࡥࠩॴ"), bstack1lllllll1_opy_ (u"࠭ࡡࡷࡦࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩॵ"), bstack1lllllll1_opy_ (u"ࠧࡢࡸࡧࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩॶ"), bstack1lllllll1_opy_ (u"ࠨࡣࡹࡨࡆࡸࡧࡴࠩॷ"),
  bstack1lllllll1_opy_ (u"ࠩࡸࡷࡪࡑࡥࡺࡵࡷࡳࡷ࡫ࠧॸ"), bstack1lllllll1_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡴࡩࠩॹ"), bstack1lllllll1_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡴࡵࡺࡳࡷࡪࠧॺ"),
  bstack1lllllll1_opy_ (u"ࠬࡱࡥࡺࡃ࡯࡭ࡦࡹࠧॻ"), bstack1lllllll1_opy_ (u"࠭࡫ࡦࡻࡓࡥࡸࡹࡷࡰࡴࡧࠫॼ"),
  bstack1lllllll1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩॽ"), bstack1lllllll1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡁࡳࡩࡶࠫॾ"), bstack1lllllll1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࡈ࡮ࡸࠧॿ"), bstack1lllllll1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡅ࡫ࡶࡴࡳࡥࡎࡣࡳࡴ࡮ࡴࡧࡇ࡫࡯ࡩࠬঀ"), bstack1lllllll1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡘࡷࡪ࡙ࡹࡴࡶࡨࡱࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨঁ"),
  bstack1lllllll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࠨং"), bstack1lllllll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࡵࠪঃ"),
  bstack1lllllll1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡊࡩࡴࡣࡥࡰࡪࡈࡵࡪ࡮ࡧࡇ࡭࡫ࡣ࡬ࠩ঄"),
  bstack1lllllll1_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡥࡣࡸ࡬ࡩࡼ࡚ࡩ࡮ࡧࡲࡹࡹ࠭অ"),
  bstack1lllllll1_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡃࡦࡸ࡮ࡵ࡮ࠨআ"), bstack1lllllll1_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡆࡥࡹ࡫ࡧࡰࡴࡼࠫই"), bstack1lllllll1_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡊࡱࡧࡧࡴࠩঈ"), bstack1lllllll1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡦࡲࡉ࡯ࡶࡨࡲࡹࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨউ"),
  bstack1lllllll1_opy_ (u"࠭ࡤࡰࡰࡷࡗࡹࡵࡰࡂࡲࡳࡓࡳࡘࡥࡴࡧࡷࠫঊ"),
  bstack1lllllll1_opy_ (u"ࠧࡶࡰ࡬ࡧࡴࡪࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩঋ"), bstack1lllllll1_opy_ (u"ࠨࡴࡨࡷࡪࡺࡋࡦࡻࡥࡳࡦࡸࡤࠨঌ"),
  bstack1lllllll1_opy_ (u"ࠩࡱࡳࡘ࡯ࡧ࡯ࠩ঍"),
  bstack1lllllll1_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࡘࡲ࡮ࡳࡰࡰࡴࡷࡥࡳࡺࡖࡪࡧࡺࡷࠬ঎"),
  bstack1lllllll1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡴࡤࡳࡱ࡬ࡨ࡜ࡧࡴࡤࡪࡨࡶࡸ࠭এ"),
  bstack1lllllll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬঐ"),
  bstack1lllllll1_opy_ (u"࠭ࡲࡦࡥࡵࡩࡦࡺࡥࡄࡪࡵࡳࡲ࡫ࡄࡳ࡫ࡹࡩࡷ࡙ࡥࡴࡵ࡬ࡳࡳࡹࠧ঑"),
  bstack1lllllll1_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭঒"),
  bstack1lllllll1_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡕࡧࡴࡩࠩও"),
  bstack1lllllll1_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡖࡴࡪ࡫ࡤࠨঔ"),
  bstack1lllllll1_opy_ (u"ࠪ࡫ࡵࡹࡅ࡯ࡣࡥࡰࡪࡪࠧক"),
  bstack1lllllll1_opy_ (u"ࠫ࡮ࡹࡈࡦࡣࡧࡰࡪࡹࡳࠨখ"),
  bstack1lllllll1_opy_ (u"ࠬࡧࡤࡣࡇࡻࡩࡨ࡚ࡩ࡮ࡧࡲࡹࡹ࠭গ"),
  bstack1lllllll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡪ࡙ࡣࡳ࡫ࡳࡸࠬঘ"),
  bstack1lllllll1_opy_ (u"ࠧࡴ࡭࡬ࡴࡉ࡫ࡶࡪࡥࡨࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫঙ"),
  bstack1lllllll1_opy_ (u"ࠨࡣࡸࡸࡴࡍࡲࡢࡰࡷࡔࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠨচ"),
  bstack1lllllll1_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡑࡥࡹࡻࡲࡢ࡮ࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧছ"),
  bstack1lllllll1_opy_ (u"ࠪࡷࡾࡹࡴࡦ࡯ࡓࡳࡷࡺࠧজ"),
  bstack1lllllll1_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡩࡨࡈࡰࡵࡷࠫঝ"),
  bstack1lllllll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡘࡲࡱࡵࡣ࡬ࠩঞ"), bstack1lllllll1_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰ࡚ࡹࡱࡧࠪট"), bstack1lllllll1_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡋࡦࡻࠪঠ"),
  bstack1lllllll1_opy_ (u"ࠨࡣࡸࡸࡴࡒࡡࡶࡰࡦ࡬ࠬড"),
  bstack1lllllll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡌࡰࡩࡦࡥࡹࡉࡡࡱࡶࡸࡶࡪ࠭ঢ"),
  bstack1lllllll1_opy_ (u"ࠪࡹࡳ࡯࡮ࡴࡶࡤࡰࡱࡕࡴࡩࡧࡵࡔࡦࡩ࡫ࡢࡩࡨࡷࠬণ"),
  bstack1lllllll1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩ࡜࡯࡮ࡥࡱࡺࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳ࠭ত"),
  bstack1lllllll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡘࡴࡵ࡬ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩথ"),
  bstack1lllllll1_opy_ (u"࠭ࡥ࡯ࡨࡲࡶࡨ࡫ࡁࡱࡲࡌࡲࡸࡺࡡ࡭࡮ࠪদ"),
  bstack1lllllll1_opy_ (u"ࠧࡦࡰࡶࡹࡷ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡳࡉࡣࡹࡩࡕࡧࡧࡦࡵࠪধ"), bstack1lllllll1_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡆࡨࡺࡹࡵ࡯࡭ࡵࡓࡳࡷࡺࠧন"), bstack1lllllll1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡆࡨࡸࡦ࡯࡬ࡴࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠬ঩"),
  bstack1lllllll1_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡴࡵࡹࡃࡢࡥ࡫ࡩࡑ࡯࡭ࡪࡶࠪপ"),
  bstack1lllllll1_opy_ (u"ࠫࡨࡧ࡬ࡦࡰࡧࡥࡷࡌ࡯ࡳ࡯ࡤࡸࠬফ"),
  bstack1lllllll1_opy_ (u"ࠬࡨࡵ࡯ࡦ࡯ࡩࡎࡪࠧব"),
  bstack1lllllll1_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ভ"),
  bstack1lllllll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡈࡲࡦࡨ࡬ࡦࡦࠪম"), bstack1lllllll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡅࡺࡺࡨࡰࡴ࡬ࡾࡪࡪࠧয"),
  bstack1lllllll1_opy_ (u"ࠩࡤࡹࡹࡵࡁࡤࡥࡨࡴࡹࡇ࡬ࡦࡴࡷࡷࠬর"), bstack1lllllll1_opy_ (u"ࠪࡥࡺࡺ࡯ࡅ࡫ࡶࡱ࡮ࡹࡳࡂ࡮ࡨࡶࡹࡹࠧ঱"),
  bstack1lllllll1_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨࡍࡳࡹࡴࡳࡷࡰࡩࡳࡺࡳࡍ࡫ࡥࠫল"),
  bstack1lllllll1_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡕࡣࡳࠫ঳"),
  bstack1lllllll1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏ࡮ࡪࡶ࡬ࡥࡱ࡛ࡲ࡭ࠩ঴"), bstack1lllllll1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡁ࡭࡮ࡲࡻࡕࡵࡰࡶࡲࡶࠫ঵"), bstack1lllllll1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡩࡱࡳࡷ࡫ࡆࡳࡣࡸࡨ࡜ࡧࡲ࡯࡫ࡱ࡫ࠬশ"), bstack1lllllll1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡑࡳࡩࡳࡒࡩ࡯࡭ࡶࡍࡳࡈࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥࠩষ"),
  bstack1lllllll1_opy_ (u"ࠪ࡯ࡪ࡫ࡰࡌࡧࡼࡇ࡭ࡧࡩ࡯ࡵࠪস"),
  bstack1lllllll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡾࡦࡨ࡬ࡦࡕࡷࡶ࡮ࡴࡧࡴࡆ࡬ࡶࠬহ"),
  bstack1lllllll1_opy_ (u"ࠬࡶࡲࡰࡥࡨࡷࡸࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨ঺"),
  bstack1lllllll1_opy_ (u"࠭ࡩ࡯ࡶࡨࡶࡐ࡫ࡹࡅࡧ࡯ࡥࡾ࠭঻"),
  bstack1lllllll1_opy_ (u"ࠧࡴࡪࡲࡻࡎࡕࡓࡍࡱࡪ়ࠫ"),
  bstack1lllllll1_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡕࡷࡶࡦࡺࡥࡨࡻࠪঽ"),
  bstack1lllllll1_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡔࡨࡷࡵࡵ࡮ࡴࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪা"), bstack1lllllll1_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡗࡢ࡫ࡷࡘ࡮ࡳࡥࡰࡷࡷࠫি"),
  bstack1lllllll1_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡈࡪࡨࡵࡨࡒࡵࡳࡽࡿࠧী"),
  bstack1lllllll1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡹࡹ࡯ࡥࡈࡼࡪࡩࡵࡵࡧࡉࡶࡴࡳࡈࡵࡶࡳࡷࠬু"),
  bstack1lllllll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡐࡴ࡭ࡃࡢࡲࡷࡹࡷ࡫ࠧূ"),
  bstack1lllllll1_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡄࡦࡤࡸ࡫ࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧৃ"),
  bstack1lllllll1_opy_ (u"ࠨࡨࡸࡰࡱࡉ࡯࡯ࡶࡨࡼࡹࡒࡩࡴࡶࠪৄ"),
  bstack1lllllll1_opy_ (u"ࠩࡺࡥ࡮ࡺࡆࡰࡴࡄࡴࡵ࡙ࡣࡳ࡫ࡳࡸࠬ৅"),
  bstack1lllllll1_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡇࡴࡴ࡮ࡦࡥࡷࡖࡪࡺࡲࡪࡧࡶࠫ৆"),
  bstack1lllllll1_opy_ (u"ࠫࡦࡶࡰࡏࡣࡰࡩࠬে"),
  bstack1lllllll1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘ࡙ࡌࡄࡧࡵࡸࠬৈ"),
  bstack1lllllll1_opy_ (u"࠭ࡴࡢࡲ࡚࡭ࡹ࡮ࡓࡩࡱࡵࡸࡕࡸࡥࡴࡵࡇࡹࡷࡧࡴࡪࡱࡱࠫ৉"),
  bstack1lllllll1_opy_ (u"ࠧࡴࡥࡤࡰࡪࡌࡡࡤࡶࡲࡶࠬ৊"),
  bstack1lllllll1_opy_ (u"ࠨࡹࡧࡥࡑࡵࡣࡢ࡮ࡓࡳࡷࡺࠧো"),
  bstack1lllllll1_opy_ (u"ࠩࡶ࡬ࡴࡽࡘࡤࡱࡧࡩࡑࡵࡧࠨৌ"),
  bstack1lllllll1_opy_ (u"ࠪ࡭ࡴࡹࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡷࡶࡩ্ࠬ"),
  bstack1lllllll1_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡆࡳࡳ࡬ࡩࡨࡈ࡬ࡰࡪ࠭ৎ"),
  bstack1lllllll1_opy_ (u"ࠬࡱࡥࡺࡥ࡫ࡥ࡮ࡴࡐࡢࡵࡶࡻࡴࡸࡤࠨ৏"),
  bstack1lllllll1_opy_ (u"࠭ࡵࡴࡧࡓࡶࡪࡨࡵࡪ࡮ࡷ࡛ࡉࡇࠧ৐"),
  bstack1lllllll1_opy_ (u"ࠧࡱࡴࡨࡺࡪࡴࡴࡘࡆࡄࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠨ৑"),
  bstack1lllllll1_opy_ (u"ࠨࡹࡨࡦࡉࡸࡩࡷࡧࡵࡅ࡬࡫࡮ࡵࡗࡵࡰࠬ৒"),
  bstack1lllllll1_opy_ (u"ࠩ࡮ࡩࡾࡩࡨࡢ࡫ࡱࡔࡦࡺࡨࠨ৓"),
  bstack1lllllll1_opy_ (u"ࠪࡹࡸ࡫ࡎࡦࡹ࡚ࡈࡆ࠭৔"),
  bstack1lllllll1_opy_ (u"ࠫࡼࡪࡡࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧ৕"), bstack1lllllll1_opy_ (u"ࠬࡽࡤࡢࡅࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲ࡙࡯࡭ࡦࡱࡸࡸࠬ৖"),
  bstack1lllllll1_opy_ (u"࠭ࡸࡤࡱࡧࡩࡔࡸࡧࡊࡦࠪৗ"), bstack1lllllll1_opy_ (u"ࠧࡹࡥࡲࡨࡪ࡙ࡩࡨࡰ࡬ࡲ࡬ࡏࡤࠨ৘"),
  bstack1lllllll1_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡥ࡙ࡇࡅࡇࡻ࡮ࡥ࡮ࡨࡍࡩ࠭৙"),
  bstack1lllllll1_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡐࡰࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡸࡴࡐࡰ࡯ࡽࠬ৚"),
  bstack1lllllll1_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࡷࠬ৛"),
  bstack1lllllll1_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶ࡮࡫ࡳࠨড়"), bstack1lllllll1_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷࡿࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠨঢ়"),
  bstack1lllllll1_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࡈࡢࡴࡧࡻࡦࡸࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩ৞"),
  bstack1lllllll1_opy_ (u"ࠧ࡮ࡣࡻࡘࡾࡶࡩ࡯ࡩࡉࡶࡪࡷࡵࡦࡰࡦࡽࠬয়"),
  bstack1lllllll1_opy_ (u"ࠨࡵ࡬ࡱࡵࡲࡥࡊࡵ࡙࡭ࡸ࡯ࡢ࡭ࡧࡆ࡬ࡪࡩ࡫ࠨৠ"),
  bstack1lllllll1_opy_ (u"ࠩࡸࡷࡪࡉࡡࡳࡶ࡫ࡥ࡬࡫ࡓࡴ࡮ࠪৡ"),
  bstack1lllllll1_opy_ (u"ࠪࡷ࡭ࡵࡵ࡭ࡦࡘࡷࡪ࡙ࡩ࡯ࡩ࡯ࡩࡹࡵ࡮ࡕࡧࡶࡸࡒࡧ࡮ࡢࡩࡨࡶࠬৢ"),
  bstack1lllllll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡌ࡛ࡉࡖࠧৣ"),
  bstack1lllllll1_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡴࡻࡣࡩࡋࡧࡉࡳࡸ࡯࡭࡮ࠪ৤"),
  bstack1lllllll1_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪࡎࡩࡥࡦࡨࡲࡆࡶࡩࡑࡱ࡯࡭ࡨࡿࡅࡳࡴࡲࡶࠬ৥"),
  bstack1lllllll1_opy_ (u"ࠧ࡮ࡱࡦ࡯ࡑࡵࡣࡢࡶ࡬ࡳࡳࡇࡰࡱࠩ০"),
  bstack1lllllll1_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇࡱࡵࡱࡦࡺࠧ১"), bstack1lllllll1_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈ࡬ࡰࡹ࡫ࡲࡔࡲࡨࡧࡸ࠭২"),
  bstack1lllllll1_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡆࡨࡰࡦࡿࡁࡥࡤࠪ৩")
]
bstack1ll11l1l1_opy_ = bstack1lllllll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡹࡵࡲ࡯ࡢࡦࠪ৪")
bstack111lll_opy_ = [bstack1lllllll1_opy_ (u"ࠬ࠴ࡡࡱ࡭ࠪ৫"), bstack1lllllll1_opy_ (u"࠭࠮ࡢࡣࡥࠫ৬"), bstack1lllllll1_opy_ (u"ࠧ࠯࡫ࡳࡥࠬ৭")]
bstack11ll11l11_opy_ = [bstack1lllllll1_opy_ (u"ࠨ࡫ࡧࠫ৮"), bstack1lllllll1_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ৯"), bstack1lllllll1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ৰ"), bstack1lllllll1_opy_ (u"ࠫࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦࠪৱ")]
bstack1llll_opy_ = {
  bstack1lllllll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ৲"): bstack1lllllll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৳"),
  bstack1lllllll1_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ৴"): bstack1lllllll1_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭৵"),
  bstack1lllllll1_opy_ (u"ࠩࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৶"): bstack1lllllll1_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৷"),
  bstack1lllllll1_opy_ (u"ࠫ࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৸"): bstack1lllllll1_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৹"),
  bstack1lllllll1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡵ࡫ࡲࡲࡸ࠭৺"): bstack1lllllll1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ৻")
}
bstack1ll11l11_opy_ = [
  bstack1lllllll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ৼ"),
  bstack1lllllll1_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ৽"),
  bstack1lllllll1_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৾"),
  bstack1lllllll1_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ৿"),
  bstack1lllllll1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭਀"),
]
bstack111llll1l_opy_ = bstack111l111l_opy_ + bstack11l1l1lll_opy_ + bstack1ll1l1l11_opy_
bstack1ll111ll_opy_ = [
  bstack1lllllll1_opy_ (u"࠭࡞࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶࠧࠫਁ"),
  bstack1lllllll1_opy_ (u"ࠧ࡟ࡤࡶ࠱ࡱࡵࡣࡢ࡮࠱ࡧࡴࡳࠤࠨਂ"),
  bstack1lllllll1_opy_ (u"ࠨࡠ࠴࠶࠼࠴ࠧਃ"),
  bstack1lllllll1_opy_ (u"ࠩࡡ࠵࠵࠴ࠧ਄"),
  bstack1lllllll1_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠳࡞࠺࠲࠿࡝࠯ࠩਅ"),
  bstack1lllllll1_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠵࡟࠵࠳࠹࡞࠰ࠪਆ"),
  bstack1lllllll1_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠷ࡠ࠶࠭࠲࡟࠱ࠫਇ"),
  bstack1lllllll1_opy_ (u"࠭࡞࠲࠻࠵࠲࠶࠼࠸࠯ࠩਈ")
]
bstack1l11llll1_opy_ = bstack1lllllll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀࠫਉ")
bstack11l1ll1ll_opy_ = bstack1lllllll1_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡧࡹࡩࡳࡺࠧਊ")
bstack11ll1lll1_opy_ = [ bstack1lllllll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ਋") ]
bstack11l1l1ll_opy_ = [ bstack1lllllll1_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ਌") ]
bstack1l1lllll1_opy_ = [ bstack1lllllll1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ਍") ]
bstack1ll1111l1_opy_ = bstack1lllllll1_opy_ (u"࡙ࠬࡄࡌࡕࡨࡸࡺࡶࠧ਎")
bstack1111ll_opy_ = bstack1lllllll1_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠩਏ")
bstack11ll1llll_opy_ = bstack1lllllll1_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠫਐ")
bstack1lllll1_opy_ = bstack1lllllll1_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࠧ਑")
bstack1l11l1ll_opy_ = [
  bstack1lllllll1_opy_ (u"ࠩࡈࡖࡗࡥࡆࡂࡋࡏࡉࡉ࠭਒"),
  bstack1lllllll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪਓ"),
  bstack1lllllll1_opy_ (u"ࠫࡊࡘࡒࡠࡄࡏࡓࡈࡑࡅࡅࡡࡅ࡝ࡤࡉࡌࡊࡇࡑࡘࠬਔ"),
  bstack1lllllll1_opy_ (u"ࠬࡋࡒࡓࡡࡑࡉ࡙࡝ࡏࡓࡍࡢࡇࡍࡇࡎࡈࡇࡇࠫਕ"),
  bstack1lllllll1_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡆࡖࡢࡒࡔ࡚࡟ࡄࡑࡑࡒࡊࡉࡔࡆࡆࠪਖ"),
  bstack1lllllll1_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡅࡏࡓࡘࡋࡄࠨਗ"),
  bstack1lllllll1_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡕࡉࡘࡋࡔࠨਘ"),
  bstack1lllllll1_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊࡌࡕࡔࡇࡇࠫਙ"),
  bstack1lllllll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡆࡈࡏࡓࡖࡈࡈࠬਚ"),
  bstack1lllllll1_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਛ"),
  bstack1lllllll1_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡏࡑࡗࡣࡗࡋࡓࡐࡎ࡙ࡉࡉ࠭ਜ"),
  bstack1lllllll1_opy_ (u"࠭ࡅࡓࡔࡢࡅࡉࡊࡒࡆࡕࡖࡣࡎࡔࡖࡂࡎࡌࡈࠬਝ"),
  bstack1lllllll1_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪਞ"),
  bstack1lllllll1_opy_ (u"ࠨࡇࡕࡖࡤ࡚ࡕࡏࡐࡈࡐࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩਟ"),
  bstack1lllllll1_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭ਠ"),
  bstack1lllllll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡘࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪਡ"),
  bstack1lllllll1_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡍࡕࡓࡕࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧਢ"),
  bstack1lllllll1_opy_ (u"ࠬࡋࡒࡓࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਣ"),
  bstack1lllllll1_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧਤ"),
  bstack1lllllll1_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡕࡉࡘࡕࡌࡖࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ਥ"),
  bstack1lllllll1_opy_ (u"ࠨࡇࡕࡖࡤࡓࡁࡏࡆࡄࡘࡔࡘ࡙ࡠࡒࡕࡓ࡝࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧਦ"),
]
bstack1llll1l1_opy_ = bstack1lllllll1_opy_ (u"ࠩ࠱࠳ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡥࡷࡺࡩࡧࡣࡦࡸࡸ࠵ࠧਧ")
def bstack111l1l111_opy_():
  global CONFIG
  headers = {
        bstack1lllllll1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩਨ"): bstack1lllllll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ਩"),
      }
  proxies = bstack1l11l111l_opy_(CONFIG, bstack1l11111l1_opy_)
  try:
    response = requests.get(bstack1l11111l1_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack111l111_opy_ = response.json()[bstack1lllllll1_opy_ (u"ࠬ࡮ࡵࡣࡵࠪਪ")]
      logger.debug(bstack1l1ll1lll_opy_.format(response.json()))
      return bstack111l111_opy_
    else:
      logger.debug(bstack11111l_opy_.format(bstack1lllllll1_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧਫ")))
  except Exception as e:
    logger.debug(bstack11111l_opy_.format(e))
def bstack11l1l11l_opy_(hub_url):
  global CONFIG
  url = bstack1lllllll1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤਬ")+  hub_url + bstack1lllllll1_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣਭ")
  headers = {
        bstack1lllllll1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨਮ"): bstack1lllllll1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ਯ"),
      }
  proxies = bstack1l11l111l_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack11llll_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1lll111_opy_.format(hub_url, e))
def bstack111llll1_opy_():
  try:
    global bstack1ll111l11_opy_
    bstack111l111_opy_ = bstack111l1l111_opy_()
    bstack1l1l111l1_opy_ = []
    results = []
    for bstack11l1l11_opy_ in bstack111l111_opy_:
      bstack1l1l111l1_opy_.append(bstack11lll11ll_opy_(target=bstack11l1l11l_opy_,args=(bstack11l1l11_opy_,)))
    for t in bstack1l1l111l1_opy_:
      t.start()
    for t in bstack1l1l111l1_opy_:
      results.append(t.join())
    bstack111lll111_opy_ = {}
    for item in results:
      hub_url = item[bstack1lllllll1_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬਰ")]
      latency = item[bstack1lllllll1_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭਱")]
      bstack111lll111_opy_[hub_url] = latency
    bstack1l1ll11_opy_ = min(bstack111lll111_opy_, key= lambda x: bstack111lll111_opy_[x])
    bstack1ll111l11_opy_ = bstack1l1ll11_opy_
    logger.debug(bstack111llllll_opy_.format(bstack1l1ll11_opy_))
  except Exception as e:
    logger.debug(bstack11ll1ll1l_opy_.format(e))
bstack1lll1llll_opy_ = bstack1lllllll1_opy_ (u"࠭ࡓࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡲࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠼ࠣࡿࢂ࠭ਲ")
bstack1l111_opy_ = bstack1lllllll1_opy_ (u"ࠧࡄࡱࡰࡴࡱ࡫ࡴࡦࡦࠣࡷࡪࡺࡵࡱࠣࠪਲ਼")
bstack1ll1lll11_opy_ = bstack1lllllll1_opy_ (u"ࠨࡒࡤࡶࡸ࡫ࡤࠡࡥࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࡀࠠࡼࡿࠪ਴")
bstack1l111l11l_opy_ = bstack1lllllll1_opy_ (u"ࠩࡖࡥࡳ࡯ࡴࡪࡼࡨࡨࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠧਵ")
bstack11ll1lll_opy_ = bstack1lllllll1_opy_ (u"࡙ࠪࡸ࡯࡮ࡨࠢ࡫ࡹࡧࠦࡵࡳ࡮࠽ࠤࢀࢃࠧਸ਼")
bstack1ll11l_opy_ = bstack1lllllll1_opy_ (u"ࠫࡘ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡴࡷࡩࡩࠦࡷࡪࡶ࡫ࠤ࡮ࡪ࠺ࠡࡽࢀࠫ਷")
bstack111ll111_opy_ = bstack1lllllll1_opy_ (u"ࠬࡘࡥࡤࡧ࡬ࡺࡪࡪࠠࡪࡰࡷࡩࡷࡸࡵࡱࡶ࠯ࠤࡪࡾࡩࡵ࡫ࡱ࡫ࠬਸ")
bstack1111_opy_ = bstack1lllllll1_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࡣࠫਹ")
bstack11l111111_opy_ = bstack1lllllll1_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴࠡࡣࡱࡨࠥࡶࡹࡵࡧࡶࡸ࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡱࡣࡦ࡯ࡦ࡭ࡥࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡶࡩࡱ࡫࡮ࡪࡷࡰࡤࠬ਺")
bstack1l11l11_opy_ = bstack1lllllll1_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡄࡴࡵ࡯ࡵ࡮ࡎ࡬ࡦࡷࡧࡲࡺࠢࡳࡥࡨࡱࡡࡨࡧ࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡶࡴࡨ࡯ࡵࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠱ࡦࡶࡰࡪࡷࡰࡰ࡮ࡨࡲࡢࡴࡼࡤࠬ਻")
bstack1lll1l1ll_opy_ = bstack1lllllll1_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡶࡴࡨ࡯ࡵ࠮ࠣࡴࡦࡨ࡯ࡵࠢࡤࡲࡩࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࡭࡫ࡥࡶࡦࡸࡹࠡࡲࡤࡧࡰࡧࡧࡦࡵࠣࡸࡴࠦࡲࡶࡰࠣࡶࡴࡨ࡯ࡵࠢࡷࡩࡸࡺࡳࠡ࡫ࡱࠤࡵࡧࡲࡢ࡮࡯ࡩࡱ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡲࡰࡤࡲࡸ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡳࡱࡥࡳࡹ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠮ࡲࡤࡦࡴࡺࠠࡳࡱࡥࡳࡹ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠮ࡵࡨࡰࡪࡴࡩࡶ࡯࡯࡭ࡧࡸࡡࡳࡻࡣ਼ࠫ")
bstack11l1l1ll1_opy_ = bstack1lllllll1_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡧ࡫ࡨࡢࡸࡨࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵ࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡦࡪ࡮ࡡࡷࡧࡣࠫ਽")
bstack1ll1111ll_opy_ = bstack1lllllll1_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡧࡰࡱ࡫ࡸࡱ࠲ࡩ࡬ࡪࡧࡱࡸࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶ࠲ࠥࡦࡰࡪࡲࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡆࡶࡰࡪࡷࡰ࠱ࡕࡿࡴࡩࡱࡱ࠱ࡈࡲࡩࡦࡰࡷࡤࠬਾ")
bstack1l111ll_opy_ = bstack1lllllll1_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡦࠧਿ")
bstack11l1ll1_opy_ = bstack1lllllll1_opy_ (u"࠭ࡃࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡩ࡭ࡳࡪࠠࡦ࡫ࡷ࡬ࡪࡸࠠࡔࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡲࡶࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳ࠯ࠢࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡹࡧ࡬࡭ࠢࡷ࡬ࡪࠦࡲࡦ࡮ࡨࡺࡦࡴࡴࠡࡲࡤࡧࡰࡧࡧࡦࡵࠣࡹࡸ࡯࡮ࡨࠢࡳ࡭ࡵࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷ࠳࠭ੀ")
bstack111l11l1l_opy_ = bstack1lllllll1_opy_ (u"ࠧࡉࡣࡱࡨࡱ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡱࡵࡳࡦࠩੁ")
bstack11llll111_opy_ = bstack1lllllll1_opy_ (u"ࠨࡃ࡯ࡰࠥࡪ࡯࡯ࡧࠤࠫੂ")
bstack1l111l1l_opy_ = bstack1lllllll1_opy_ (u"ࠩࡆࡳࡳ࡬ࡩࡨࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴࠡࡣࡷࠤࡦࡴࡹࠡࡲࡤࡶࡪࡴࡴࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡴ࡬ࠠࠣࡽࢀࠦ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡥ࡯ࡹࡩ࡫ࠠࡢࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰ࠴ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡧ࡭࡭ࠢࡩ࡭ࡱ࡫ࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࡹ࠮ࠨ੃")
bstack1ll11l1_opy_ = bstack1lllllll1_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡶࡪࡪࡥ࡯ࡶ࡬ࡥࡱࡹࠠ࡯ࡱࡷࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡢࡦࡧࠤࡹ࡮ࡥ࡮ࠢ࡬ࡲࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠡࡥࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࠦࡡࡴࠢࠥࡹࡸ࡫ࡲࡏࡣࡰࡩࠧࠦࡡ࡯ࡦࠣࠦࡦࡩࡣࡦࡵࡶࡏࡪࡿࠢࠡࡱࡵࠤࡸ࡫ࡴࠡࡶ࡫ࡩࡲࠦࡡࡴࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࡵ࠽ࠤࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊࠨࠠࡢࡰࡧࠤࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠣࠩ੄")
bstack1111lllll_opy_ = bstack1lllllll1_opy_ (u"ࠫࡒࡧ࡬ࡧࡱࡵࡱࡪࡪࠠࡤࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩ࠿ࠨࡻࡾࠤࠪ੅")
bstack1lll1l1l_opy_ = bstack1lllllll1_opy_ (u"ࠬࡋ࡮ࡤࡱࡸࡲࡹ࡫ࡲࡦࡦࠣࡩࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡸࡴࠥ࠳ࠠࡼࡿࠪ੆")
bstack11l1lll_opy_ = bstack1lllllll1_opy_ (u"࠭ࡓࡵࡣࡵࡸ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡍࡱࡦࡥࡱ࠭ੇ")
bstack1l1l1l11_opy_ = bstack1lllllll1_opy_ (u"ࠧࡔࡶࡲࡴࡵ࡯࡮ࡨࠢࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡎࡲࡧࡦࡲࠧੈ")
bstack11lll1l_opy_ = bstack1lllllll1_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡍࡱࡦࡥࡱࠦࡩࡴࠢࡱࡳࡼࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠡࠨ੉")
bstack1111l1l_opy_ = bstack1lllllll1_opy_ (u"ࠩࡆࡳࡺࡲࡤࠡࡰࡲࡸࠥࡹࡴࡢࡴࡷࠤࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡐࡴࡩࡡ࡭࠼ࠣࡿࢂ࠭੊")
bstack11l11ll_opy_ = bstack1lllllll1_opy_ (u"ࠪࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡲ࡯ࡤࡣ࡯ࠤࡧ࡯࡮ࡢࡴࡼࠤࡼ࡯ࡴࡩࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࢀࢃࠧੋ")
bstack1lll1l11l_opy_ = bstack1lllllll1_opy_ (u"࡚ࠫࡶࡤࡢࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡥࡧࡷࡥ࡮ࡲࡳ࠻ࠢࡾࢁࠬੌ")
bstack1ll11111l_opy_ = bstack1lllllll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡷࡳࡨࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳࠡࡽࢀ੍ࠫ")
bstack1l1111111_opy_ = bstack1lllllll1_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡰࡳࡱࡹ࡭ࡩ࡫ࠠࡢࡰࠣࡥࡵࡶࡲࡰࡲࡵ࡭ࡦࡺࡥࠡࡈ࡚ࠤ࠭ࡸ࡯ࡣࡱࡷ࠳ࡵࡧࡢࡰࡶࠬࠤ࡮ࡴࠠࡤࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩ࠱ࠦࡳ࡬࡫ࡳࠤࡹ࡮ࡥࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡰ࡫ࡹࠡ࡫ࡱࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡮࡬ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡵ࡬ࡱࡵࡲࡥࠡࡲࡼࡸ࡭ࡵ࡮ࠡࡵࡦࡶ࡮ࡶࡴࠡࡹ࡬ࡸ࡭ࡵࡵࡵࠢࡤࡲࡾࠦࡆࡘ࠰ࠪ੎")
bstack1ll111_opy_ = bstack1lllllll1_opy_ (u"ࠧࡔࡧࡷࡸ࡮ࡴࡧࠡࡪࡷࡸࡵࡖࡲࡰࡺࡼ࠳࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠡ࡫ࡶࠤࡳࡵࡴࠡࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤࡴࡴࠠࡤࡷࡵࡶࡪࡴࡴ࡭ࡻࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡰࡨࠣࡷࡪࡲࡥ࡯࡫ࡸࡱࠥ࠮ࡻࡾࠫ࠯ࠤࡵࡲࡥࡢࡵࡨࠤࡺࡶࡧࡳࡣࡧࡩࠥࡺ࡯ࠡࡕࡨࡰࡪࡴࡩࡶ࡯ࡁࡁ࠹࠴࠰࠯࠲ࠣࡳࡷࠦࡲࡦࡨࡨࡶࠥࡺ࡯ࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡺࡻࡼ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡳࡨࡹ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡶࡩࡱ࡫࡮ࡪࡷࡰ࠳ࡷࡻ࡮࠮ࡶࡨࡷࡹࡹ࠭ࡣࡧ࡫࡭ࡳࡪ࠭ࡱࡴࡲࡼࡾࠩࡰࡺࡶ࡫ࡳࡳࠦࡦࡰࡴࠣࡥࠥࡽ࡯ࡳ࡭ࡤࡶࡴࡻ࡮ࡥ࠰ࠪ੏")
bstack1ll1llll_opy_ = bstack1lllllll1_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡾࡳ࡬ࠡࡨ࡬ࡰࡪ࠴࠮ࠨ੐")
bstack1lll1ll_opy_ = bstack1lllllll1_opy_ (u"ࠩࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡩࡨࡲࡪࡸࡡࡵࡧࡧࠤࡹ࡮ࡥࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨ࡬ࡰࡪࠧࠧੑ")
bstack1l111l1_opy_ = bstack1lllllll1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡶ࡫ࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫࡯࡬ࡦ࠰ࠣࡿࢂ࠭੒")
bstack11l1l11l1_opy_ = bstack1lllllll1_opy_ (u"ࠫࡊࡾࡰࡦࡥࡷࡩࡩࠦࡡࡵࠢ࡯ࡩࡦࡹࡴࠡ࠳ࠣ࡭ࡳࡶࡵࡵ࠮ࠣࡶࡪࡩࡥࡪࡸࡨࡨࠥ࠶ࠧ੓")
bstack11lllll1_opy_ = bstack1lllllll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡩࡻࡲࡪࡰࡪࠤࡆࡶࡰࠡࡷࡳࡰࡴࡧࡤ࠯ࠢࡾࢁࠬ੔")
bstack11l1_opy_ = bstack1lllllll1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡸࡴࡱࡵࡡࡥࠢࡄࡴࡵ࠴ࠠࡊࡰࡹࡥࡱ࡯ࡤࠡࡨ࡬ࡰࡪࠦࡰࡢࡶ࡫ࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡻࡾ࠰ࠪ੕")
bstack111_opy_ = bstack1lllllll1_opy_ (u"ࠧࡌࡧࡼࡷࠥࡩࡡ࡯ࡰࡲࡸࠥࡩ࡯࠮ࡧࡻ࡭ࡸࡺࠠࡢࡵࠣࡥࡵࡶࠠࡷࡣ࡯ࡹࡪࡹࠬࠡࡷࡶࡩࠥࡧ࡮ࡺࠢࡲࡲࡪࠦࡰࡳࡱࡳࡩࡷࡺࡹࠡࡨࡵࡳࡲࠦࡻࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡶࡡࡵࡪ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡩࡵࡴࡶࡲࡱࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡷ࡭ࡧࡲࡦࡣࡥࡰࡪࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀࢀ࠰ࠥࡵ࡮࡭ࡻࠣࠦࡵࡧࡴࡩࠤࠣࡥࡳࡪࠠࠣࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠦࠥࡩࡡ࡯ࠢࡦࡳ࠲࡫ࡸࡪࡵࡷࠤࡹࡵࡧࡦࡶ࡫ࡩࡷ࠴ࠧ੖")
bstack11l1l_opy_ = bstack1lllllll1_opy_ (u"ࠨ࡝ࡌࡲࡻࡧ࡬ࡪࡦࠣࡥࡵࡶࠠࡱࡴࡲࡴࡪࡸࡴࡺ࡟ࠣࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠣࡥࡷ࡫ࠠࡼ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡰࡢࡶ࡫ࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡣࡶࡵࡷࡳࡲࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁࢁ࠳ࠦࡆࡰࡴࠣࡱࡴࡸࡥࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡳࡰࡪࡧࡳࡦࠢࡹ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡺࡻࡼ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡳࡨࡹ࠯ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱࡲ࡬ࡹࡲ࠵ࡳࡦࡶ࠰ࡹࡵ࠳ࡴࡦࡵࡷࡷ࠴ࡹࡰࡦࡥ࡬ࡪࡾ࠳ࡡࡱࡲࠪ੗")
bstack1l1l111_opy_ = bstack1lllllll1_opy_ (u"ࠩ࡞ࡍࡳࡼࡡ࡭࡫ࡧࠤࡦࡶࡰࠡࡲࡵࡳࡵ࡫ࡲࡵࡻࡠࠤࡘࡻࡰࡱࡱࡵࡸࡪࡪࠠࡷࡣ࡯ࡹࡪࡹࠠࡰࡨࠣࡥࡵࡶࠠࡢࡴࡨࠤࡴ࡬ࠠࡼ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡰࡢࡶ࡫ࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡣࡶࡵࡷࡳࡲࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁࢁ࠳ࠦࡆࡰࡴࠣࡱࡴࡸࡥࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡳࡰࡪࡧࡳࡦࠢࡹ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡺࡻࡼ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡳࡨࡹ࠯ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱࡲ࡬ࡹࡲ࠵ࡳࡦࡶ࠰ࡹࡵ࠳ࡴࡦࡵࡷࡷ࠴ࡹࡰࡦࡥ࡬ࡪࡾ࠳ࡡࡱࡲࠪ੘")
bstack1ll1l1_opy_ = bstack1lllllll1_opy_ (u"࡙ࠪࡸ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡦࡶࡰࠡ࡫ࡧࠤࢀࢃࠠࡧࡱࡵࠤ࡭ࡧࡳࡩࠢ࠽ࠤࢀࢃ࠮ࠨਖ਼")
bstack11l11l1l1_opy_ = bstack1lllllll1_opy_ (u"ࠫࡆࡶࡰࠡࡗࡳࡰࡴࡧࡤࡦࡦࠣࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺ࠰ࠣࡍࡉࠦ࠺ࠡࡽࢀࠫਗ਼")
bstack1l1111ll_opy_ = bstack1lllllll1_opy_ (u"࡛ࠬࡳࡪࡰࡪࠤࡆࡶࡰࠡ࠼ࠣࡿࢂ࠴ࠧਜ਼")
bstack11l1l1l1_opy_ = bstack1lllllll1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲࠦࡩࡴࠢࡱࡳࡹࠦࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡳࡷࠦࡶࡢࡰ࡬ࡰࡱࡧࠠࡱࡻࡷ࡬ࡴࡴࠠࡵࡧࡶࡸࡸ࠲ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡹ࡬ࡸ࡭ࠦࡰࡢࡴࡤࡰࡱ࡫࡬ࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠥࡃࠠ࠲ࠩੜ")
bstack1l1l1ll1l_opy_ = bstack1lllllll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࡀࠠࡼࡿࠪ੝")
bstack1llllll1l_opy_ = bstack1lllllll1_opy_ (u"ࠨࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡨࡲ࡯ࡴࡧࠣࡦࡷࡵࡷࡴࡧࡵ࠾ࠥࢁࡽࠨਫ਼")
bstack11l1ll1l_opy_ = bstack1lllllll1_opy_ (u"ࠩࡆࡳࡺࡲࡤࠡࡰࡲࡸࠥ࡭ࡥࡵࠢࡵࡩࡦࡹ࡯࡯ࠢࡩࡳࡷࠦࡢࡦࡪࡤࡺࡪࠦࡦࡦࡣࡷࡹࡷ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥ࠯ࠢࡾࢁࠬ੟")
bstack11l1111l1_opy_ = bstack1lllllll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠤ࡫ࡸ࡯࡮ࠢࡤࡴ࡮ࠦࡣࡢ࡮࡯࠲ࠥࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠨ੠")
bstack1l111ll11_opy_ = bstack1lllllll1_opy_ (u"࡚ࠫࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡪࡲࡻࠥࡨࡵࡪ࡮ࡧࠤ࡚ࡘࡌ࠭ࠢࡤࡷࠥࡨࡵࡪ࡮ࡧࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠡ࡫ࡶࠤࡳࡵࡴࠡࡷࡶࡩࡩ࠴ࠧ੡")
bstack1l1llllll_opy_ = bstack1lllllll1_opy_ (u"࡙ࠬࡥࡳࡸࡨࡶࠥࡹࡩࡥࡧࠣࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠮ࡻࡾࠫࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡷࡦࡳࡥࠡࡣࡶࠤࡨࡲࡩࡦࡰࡷࠤࡸ࡯ࡤࡦࠢࡥࡹ࡮ࡲࡤࡏࡣࡰࡩ࠭ࢁࡽࠪࠩ੢")
bstack1l1ll111l_opy_ = bstack1lllllll1_opy_ (u"࠭ࡖࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡳࡳࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡪࡡࡴࡪࡥࡳࡦࡸࡤ࠻ࠢࡾࢁࠬ੣")
bstack111lllll_opy_ = bstack1lllllll1_opy_ (u"ࠧࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡥࡨࡩࡥࡴࡵࠣࡥࠥࡶࡲࡪࡸࡤࡸࡪࠦࡤࡰ࡯ࡤ࡭ࡳࡀࠠࡼࡿࠣ࠲࡙ࠥࡥࡵࠢࡷ࡬ࡪࠦࡦࡰ࡮࡯ࡳࡼ࡯࡮ࡨࠢࡦࡳࡳ࡬ࡩࡨࠢ࡬ࡲࠥࡿ࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨ࠾ࠥࡢ࡮࠮࠯࠰࠱࠲࠳࠭࠮࠯࠰࠱ࠥࡢ࡮ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰ࠿ࠦࡴࡳࡷࡨࠤࡡࡴ࠭࠮࠯࠰࠱࠲࠳࠭࠮࠯࠰ࠫ੤")
bstack11ll1ll_opy_ = bstack1lllllll1_opy_ (u"ࠨࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣ࡫ࡪࡺ࡟࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࡤ࡫ࡲࡳࡱࡵࠤ࠿ࠦࡻࡾࠩ੥")
bstack1l111lll_opy_ = bstack1lllllll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫࡮ࡥࡡࡤࡱࡵࡲࡩࡵࡷࡧࡩࡤ࡫ࡶࡦࡰࡷࠤ࡫ࡵࡲࠡࡕࡇࡏࡘ࡫ࡴࡶࡲࠣࡿࢂࠨ੦")
bstack11111l1_opy_ = bstack1lllllll1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥ࡯ࡦࡢࡥࡲࡶ࡬ࡪࡶࡸࡨࡪࡥࡥࡷࡧࡱࡸࠥ࡬࡯ࡳࠢࡖࡈࡐ࡚ࡥࡴࡶࡄࡸࡹ࡫࡭ࡱࡶࡨࡨࠥࢁࡽࠣ੧")
bstack111ll1l1_opy_ = bstack1lllllll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡰࡧࡣࡦࡳࡰ࡭࡫ࡷࡹࡩ࡫࡟ࡦࡸࡨࡲࡹࠦࡦࡰࡴࠣࡗࡉࡑࡔࡦࡵࡷࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠠࡼࡿࠥ੨")
bstack11ll111l1_opy_ = bstack1lllllll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧ࡫ࡵࡩࡤࡸࡥࡲࡷࡨࡷࡹࠦࡻࡾࠤ੩")
bstack111l1l11_opy_ = bstack1lllllll1_opy_ (u"ࠨࡐࡐࡕࡗࠤࡊࡼࡥ࡯ࡶࠣࡿࢂࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡ࠼ࠣࡿࢂࠨ੪")
bstack11lll111l_opy_ = bstack1lllllll1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࠦࡰࡳࡱࡻࡽࠥࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫ੫")
bstack1l1ll1lll_opy_ = bstack1lllllll1_opy_ (u"ࠨࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡪࡷࡵ࡭ࠡ࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠥࢁࡽࠨ੬")
bstack11111l_opy_ = bstack1lllllll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠠࡧࡴࡲࡱࠥ࠵࡮ࡦࡺࡷࡣ࡭ࡻࡢࡴ࠼ࠣࡿࢂ࠭੭")
bstack111llllll_opy_ = bstack1lllllll1_opy_ (u"ࠪࡒࡪࡧࡲࡦࡵࡷࠤ࡭ࡻࡢࠡࡣ࡯ࡰࡴࡩࡡࡵࡧࡧࠤ࡮ࡹ࠺ࠡࡽࢀࠫ੮")
bstack11ll1ll1l_opy_ = bstack1lllllll1_opy_ (u"ࠫࡊࡘࡒࡐࡔࠣࡍࡓࠦࡁࡍࡎࡒࡇࡆ࡚ࡅࠡࡊࡘࡆࠥࢁࡽࠨ੯")
bstack11llll_opy_ = bstack1lllllll1_opy_ (u"ࠬࡒࡡࡵࡧࡱࡧࡾࠦ࡯ࡧࠢ࡫ࡹࡧࡀࠠࡼࡿࠣ࡭ࡸࡀࠠࡼࡿࠪੰ")
bstack1lll111_opy_ = bstack1lllllll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢ࡯ࡥࡹ࡫࡮ࡤࡻࠣࡪࡴࡸࠠࡼࡿࠣ࡬ࡺࡨ࠺ࠡࡽࢀࠫੱ")
bstack11l111lll_opy_ = bstack1lllllll1_opy_ (u"ࠧࡉࡷࡥࠤࡺࡸ࡬ࠡࡥ࡫ࡥࡳ࡭ࡥࡥࠢࡷࡳࠥࡺࡨࡦࠢࡲࡴࡹ࡯࡭ࡢ࡮ࠣ࡬ࡺࡨ࠺ࠡࡽࢀࠫੲ")
bstack1l1ll11ll_opy_ = bstack1lllllll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡴࡶࡴࡪ࡯ࡤࡰࠥ࡮ࡵࡣࠢࡸࡶࡱࡀࠠࡼࡿࠪੳ")
bstack111ll11l_opy_ = bstack1lllllll1_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡰ࡮ࡹࡴࡴ࠼ࠣࡿࢂ࠭ੴ")
bstack1l1l11l_opy_ = bstack1lllllll1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡣࡷ࡬ࡰࡩࠦࡡࡳࡶ࡬ࡪࡦࡩࡴࡴ࠼ࠣࡿࢂ࠭ੵ")
bstack111l1ll11_opy_ = bstack1lllllll1_opy_ (u"࡚ࠫࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡰࡢࡥࠣࡪ࡮ࡲࡥࠡࡽࢀ࠲ࠥࡋࡲࡳࡱࡵࠤ࠲ࠦࡻࡾࠩ੶")
bstack1l111l1l1_opy_ = bstack1lllllll1_opy_ (u"ࠬࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠥࠦࡩࡧࠪࡳࡥ࡬࡫ࠠ࠾࠿ࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠥࢁ࡜࡯ࠢࠣࠤࡹࡸࡹࡼ࡞ࡱࠤࡨࡵ࡮ࡴࡶࠣࡪࡸࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪ࡟ࠫ࡫ࡹ࡜ࠨࠫ࠾ࡠࡳࠦࠠࠡࠢࠣࡪࡸ࠴ࡡࡱࡲࡨࡲࡩࡌࡩ࡭ࡧࡖࡽࡳࡩࠨࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷ࡬࠱ࠦࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡱࡡ࡬ࡲࡩ࡫ࡸࠪࠢ࠮ࠤࠧࡀࠢࠡ࠭ࠣࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࠪࡤࡻࡦ࡯ࡴࠡࡰࡨࡻࡕࡧࡧࡦ࠴࠱ࡩࡻࡧ࡬ࡶࡣࡷࡩ࠭ࠨࠨࠪࠢࡀࡂࠥࢁࡽࠣ࠮ࠣࡠࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠤࢀࡠࠬ࠯ࠩࠪ࡝ࠥ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩࠨ࡝ࠪࠢ࠮ࠤࠧ࠲࡜࡝ࡰࠥ࠭ࡡࡴࠠࠡࠢࠣࢁࡨࡧࡴࡤࡪࠫࡩࡽ࠯ࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࢂࡢ࡮ࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠬ੷")
bstack111ll1l_opy_ = bstack1lllllll1_opy_ (u"࠭࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸ࡣ࡜࡯ࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࡟ࡲࡨࡵ࡮ࡴࡶࠣࡴࡤ࡯࡮ࡥࡧࡻࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠲࡞࡞ࡱࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳ࠪ࡞ࡱࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࡠࡳ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬ࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨ࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࡢ࡮࡭ࡧࡷࠤࡨࡧࡰࡴ࠽࡟ࡲࡹࡸࡹࠡࡽ࡟ࡲࡨࡧࡰࡴࠢࡀࠤࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸ࠯࡜࡯ࠢࠣࢁࠥࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࠡࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻ࡝ࡰࠣࠤࠥࠦࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ࠽ࠤࡥࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠤࡼࡧࡱࡧࡴࡪࡥࡖࡔࡌࡇࡴࡳࡰࡰࡰࡨࡲࡹ࠮ࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡤࡣࡳࡷ࠮࠯ࡽࡡ࠮࡟ࡲࠥࠦࠠࠡ࠰࠱࠲ࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶࡠࡳࠦࠠࡾࠫ࡟ࡲࢂࡢ࡮࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠬ੸")
from ._version import __version__
bstack11l11l11l_opy_ = None
CONFIG = {}
bstack11l111l1l_opy_ = {}
bstack111111l_opy_ = {}
bstack11lllllll_opy_ = None
bstack11111l11_opy_ = None
bstack1l1l1l1l1_opy_ = None
bstack111l11l_opy_ = -1
bstack1l1l1l1l_opy_ = bstack11lll1l1_opy_
bstack1ll111l_opy_ = 1
bstack1ll1l1ll_opy_ = False
bstack11l11l1l_opy_ = False
bstack111111l1_opy_ = bstack1lllllll1_opy_ (u"ࠧࠨ੹")
bstack1lll11l1l_opy_ = bstack1lllllll1_opy_ (u"ࠨࠩ੺")
bstack1l11ll1l_opy_ = False
bstack1l1111l11_opy_ = True
bstack111l11l11_opy_ = bstack1lllllll1_opy_ (u"ࠩࠪ੻")
bstack1l111l111_opy_ = []
bstack1ll111l11_opy_ = bstack1lllllll1_opy_ (u"ࠪࠫ੼")
bstack111l1l_opy_ = False
bstack1lll1_opy_ = None
bstack1l11l11l1_opy_ = None
bstack11ll1l111_opy_ = -1
bstack11ll11l_opy_ = os.path.join(os.path.expanduser(bstack1lllllll1_opy_ (u"ࠫࢃ࠭੽")), bstack1lllllll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ੾"), bstack1lllllll1_opy_ (u"࠭࠮ࡳࡱࡥࡳࡹ࠳ࡲࡦࡲࡲࡶࡹ࠳ࡨࡦ࡮ࡳࡩࡷ࠴ࡪࡴࡱࡱࠫ੿"))
bstack1lllll1ll_opy_ = []
bstack1llll1lll_opy_ = False
bstack11l1l1l11_opy_ = False
bstack11l1llll1_opy_ = None
bstack1l11l1l1l_opy_ = None
bstack111ll11ll_opy_ = None
bstack111llll11_opy_ = None
bstack1lll1ll1_opy_ = None
bstack1l1l11ll_opy_ = None
bstack1111l11l_opy_ = None
bstack1_opy_ = None
bstack11l11lll_opy_ = None
bstack1l1lll111_opy_ = None
bstack11ll111ll_opy_ = None
bstack1l1l111l_opy_ = None
bstack111l11ll1_opy_ = None
bstack1l1ll1l1_opy_ = None
bstack11ll1ll11_opy_ = None
bstack1lll11lll_opy_ = None
bstack1l1ll1l_opy_ = None
bstack11ll1l1ll_opy_ = None
bstack1ll1l_opy_ = bstack1lllllll1_opy_ (u"ࠢࠣ઀")
class bstack11lll11ll_opy_(threading.Thread):
  def run(self):
    self.exc = None
    try:
      self.ret = self._target(*self._args, **self._kwargs)
    except Exception as e:
      self.exc = e
  def join(self, timeout=None):
    super(bstack11lll11ll_opy_, self).join(timeout)
    if self.exc:
      raise self.exc
    return self.ret
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1l1l1l1l_opy_,
                    format=bstack1lllllll1_opy_ (u"ࠨ࡞ࡱࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ઁ"),
                    datefmt=bstack1lllllll1_opy_ (u"ࠩࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫં"))
def bstack1llll1l1l_opy_():
  global CONFIG
  global bstack1l1l1l1l_opy_
  if bstack1lllllll1_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬઃ") in CONFIG:
    bstack1l1l1l1l_opy_ = bstack111lll1l_opy_[CONFIG[bstack1lllllll1_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭઄")]]
    logging.getLogger().setLevel(bstack1l1l1l1l_opy_)
def bstack1l11l11l_opy_():
  global CONFIG
  global bstack1llll1lll_opy_
  bstack1l1l11ll1_opy_ = bstack1l1l1ll_opy_(CONFIG)
  if(bstack1lllllll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧઅ") in bstack1l1l11ll1_opy_ and str(bstack1l1l11ll1_opy_[bstack1lllllll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨઆ")]).lower() == bstack1lllllll1_opy_ (u"ࠧࡵࡴࡸࡩࠬઇ")):
    bstack1llll1lll_opy_ = True
def bstack1l11_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1ll11l1l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1111ll11_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1lllllll1_opy_ (u"ࠣ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡥࡲࡲ࡫࡯ࡧࡧ࡫࡯ࡩࠧઈ") == args[i].lower() or bstack1lllllll1_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡦࡪࡩࠥઉ") == args[i].lower():
      path = args[i+1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack111l11l11_opy_
      bstack111l11l11_opy_ += bstack1lllllll1_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠠࠨઊ") + path
      return path
  return None
def bstack1l1ll11l_opy_():
  bstack11lll1lll_opy_ = bstack1111ll11_opy_()
  if bstack11lll1lll_opy_ and os.path.exists(os.path.abspath(bstack11lll1lll_opy_)):
    fileName = bstack11lll1lll_opy_
  if bstack1lllllll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨઋ") in os.environ and os.path.exists(os.path.abspath(os.environ[bstack1lllllll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆࠩઌ")])) and not bstack1lllllll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨઍ") in locals():
    fileName = os.environ[bstack1lllllll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ઎")]
  if bstack1lllllll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪએ") in locals():
    bstack1ll1ll1l1_opy_ = os.path.abspath(fileName)
  else:
    bstack1ll1ll1l1_opy_ = bstack1lllllll1_opy_ (u"ࠩࠪઐ")
  bstack1ll1lllll_opy_ = os.getcwd()
  bstack1lll1lll_opy_ = bstack1lllllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ઑ")
  bstack11l111l11_opy_ = bstack1lllllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠨ઒")
  while (not os.path.exists(bstack1ll1ll1l1_opy_)) and bstack1ll1lllll_opy_ != bstack1lllllll1_opy_ (u"ࠧࠨઓ"):
    bstack1ll1ll1l1_opy_ = os.path.join(bstack1ll1lllll_opy_, bstack1lll1lll_opy_)
    if not os.path.exists(bstack1ll1ll1l1_opy_):
      bstack1ll1ll1l1_opy_ = os.path.join(bstack1ll1lllll_opy_, bstack11l111l11_opy_)
    if bstack1ll1lllll_opy_ != os.path.dirname(bstack1ll1lllll_opy_):
      bstack1ll1lllll_opy_ = os.path.dirname(bstack1ll1lllll_opy_)
    else:
      bstack1ll1lllll_opy_ = bstack1lllllll1_opy_ (u"ࠨࠢઔ")
  if not os.path.exists(bstack1ll1ll1l1_opy_):
    bstack11l11_opy_(
      bstack1l111l1l_opy_.format(os.getcwd()))
  with open(bstack1ll1ll1l1_opy_, bstack1lllllll1_opy_ (u"ࠧࡳࠩક")) as stream:
    try:
      config = yaml.safe_load(stream)
      return config
    except yaml.YAMLError as exc:
      bstack11l11_opy_(bstack1111lllll_opy_.format(str(exc)))
def bstack1l1ll1111_opy_(config):
  bstack1l11l1l11_opy_ = bstack1lllllll_opy_(config)
  for option in list(bstack1l11l1l11_opy_):
    if option.lower() in bstack1ll1ll11l_opy_ and option != bstack1ll1ll11l_opy_[option.lower()]:
      bstack1l11l1l11_opy_[bstack1ll1ll11l_opy_[option.lower()]] = bstack1l11l1l11_opy_[option]
      del bstack1l11l1l11_opy_[option]
  return config
def bstack1l1l1111l_opy_():
  global bstack111111l_opy_
  for key, bstack11ll11l1_opy_ in bstack1l111111_opy_.items():
    if isinstance(bstack11ll11l1_opy_, list):
      for var in bstack11ll11l1_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack111111l_opy_[key] = os.environ[var]
          break
    elif bstack11ll11l1_opy_ in os.environ and os.environ[bstack11ll11l1_opy_] and str(os.environ[bstack11ll11l1_opy_]).strip():
      bstack111111l_opy_[key] = os.environ[bstack11ll11l1_opy_]
  if bstack1lllllll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪખ") in os.environ:
    bstack111111l_opy_[bstack1lllllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ગ")] = {}
    bstack111111l_opy_[bstack1lllllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧઘ")][bstack1lllllll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ઙ")] = os.environ[bstack1lllllll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧચ")]
def bstack1l11ll1_opy_():
  global bstack11l111l1l_opy_
  global bstack111l11l11_opy_
  for idx, val in enumerate(sys.argv):
    if idx<len(sys.argv) and bstack1lllllll1_opy_ (u"࠭࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩછ").lower() == val.lower():
      bstack11l111l1l_opy_[bstack1lllllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫજ")] = {}
      bstack11l111l1l_opy_[bstack1lllllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬઝ")][bstack1lllllll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫઞ")] = sys.argv[idx+1]
      del sys.argv[idx:idx+2]
      break
  for key, bstack1ll1l1lll_opy_ in bstack11l1l111l_opy_.items():
    if isinstance(bstack1ll1l1lll_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1ll1l1lll_opy_:
          if idx<len(sys.argv) and bstack1lllllll1_opy_ (u"ࠪ࠱࠲࠭ટ") + var.lower() == val.lower() and not key in bstack11l111l1l_opy_:
            bstack11l111l1l_opy_[key] = sys.argv[idx+1]
            bstack111l11l11_opy_ += bstack1lllllll1_opy_ (u"ࠫࠥ࠳࠭ࠨઠ") + var + bstack1lllllll1_opy_ (u"ࠬࠦࠧડ") + sys.argv[idx+1]
            del sys.argv[idx:idx+2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx<len(sys.argv) and bstack1lllllll1_opy_ (u"࠭࠭࠮ࠩઢ") + bstack1ll1l1lll_opy_.lower() == val.lower() and not key in bstack11l111l1l_opy_:
          bstack11l111l1l_opy_[key] = sys.argv[idx+1]
          bstack111l11l11_opy_ += bstack1lllllll1_opy_ (u"ࠧࠡ࠯࠰ࠫણ") + bstack1ll1l1lll_opy_ + bstack1lllllll1_opy_ (u"ࠨࠢࠪત") + sys.argv[idx+1]
          del sys.argv[idx:idx+2]
def bstack1l1l11l1_opy_(config):
  bstack1l11l1111_opy_ = config.keys()
  for bstack1ll1l11ll_opy_, bstack1ll1l111l_opy_ in bstack1ll1llll1_opy_.items():
    if bstack1ll1l111l_opy_ in bstack1l11l1111_opy_:
      config[bstack1ll1l11ll_opy_] = config[bstack1ll1l111l_opy_]
      del config[bstack1ll1l111l_opy_]
  for bstack1ll1l11ll_opy_, bstack1ll1l111l_opy_ in bstack1l11lll11_opy_.items():
    if isinstance(bstack1ll1l111l_opy_, list):
      for bstack1l11ll11l_opy_ in bstack1ll1l111l_opy_:
        if bstack1l11ll11l_opy_ in bstack1l11l1111_opy_:
          config[bstack1ll1l11ll_opy_] = config[bstack1l11ll11l_opy_]
          del config[bstack1l11ll11l_opy_]
          break
    elif bstack1ll1l111l_opy_ in bstack1l11l1111_opy_:
        config[bstack1ll1l11ll_opy_] = config[bstack1ll1l111l_opy_]
        del config[bstack1ll1l111l_opy_]
  for bstack1l11ll11l_opy_ in list(config):
    for bstack1ll1_opy_ in bstack111llll1l_opy_:
      if bstack1l11ll11l_opy_.lower() == bstack1ll1_opy_.lower() and bstack1l11ll11l_opy_ != bstack1ll1_opy_:
        config[bstack1ll1_opy_] = config[bstack1l11ll11l_opy_]
        del config[bstack1l11ll11l_opy_]
  bstack1llll1ll1_opy_ = []
  if bstack1lllllll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬથ") in config:
    bstack1llll1ll1_opy_ = config[bstack1lllllll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭દ")]
  for platform in bstack1llll1ll1_opy_:
    for bstack1l11ll11l_opy_ in list(platform):
      for bstack1ll1_opy_ in bstack111llll1l_opy_:
        if bstack1l11ll11l_opy_.lower() == bstack1ll1_opy_.lower() and bstack1l11ll11l_opy_ != bstack1ll1_opy_:
          platform[bstack1ll1_opy_] = platform[bstack1l11ll11l_opy_]
          del platform[bstack1l11ll11l_opy_]
  for bstack1ll1l11ll_opy_, bstack1ll1l111l_opy_ in bstack1l11lll11_opy_.items():
    for platform in bstack1llll1ll1_opy_:
      if isinstance(bstack1ll1l111l_opy_, list):
        for bstack1l11ll11l_opy_ in bstack1ll1l111l_opy_:
          if bstack1l11ll11l_opy_ in platform:
            platform[bstack1ll1l11ll_opy_] = platform[bstack1l11ll11l_opy_]
            del platform[bstack1l11ll11l_opy_]
            break
      elif bstack1ll1l111l_opy_ in platform:
        platform[bstack1ll1l11ll_opy_] = platform[bstack1ll1l111l_opy_]
        del platform[bstack1ll1l111l_opy_]
  for bstack11l1l1l1l_opy_ in bstack1llll_opy_:
    if bstack11l1l1l1l_opy_ in config:
      if not bstack1llll_opy_[bstack11l1l1l1l_opy_] in config:
        config[bstack1llll_opy_[bstack11l1l1l1l_opy_]] = {}
      config[bstack1llll_opy_[bstack11l1l1l1l_opy_]].update(config[bstack11l1l1l1l_opy_])
      del config[bstack11l1l1l1l_opy_]
  for platform in bstack1llll1ll1_opy_:
    for bstack11l1l1l1l_opy_ in bstack1llll_opy_:
      if bstack11l1l1l1l_opy_ in list(platform):
        if not bstack1llll_opy_[bstack11l1l1l1l_opy_] in platform:
          platform[bstack1llll_opy_[bstack11l1l1l1l_opy_]] = {}
        platform[bstack1llll_opy_[bstack11l1l1l1l_opy_]].update(platform[bstack11l1l1l1l_opy_])
        del platform[bstack11l1l1l1l_opy_]
  config = bstack1l1ll1111_opy_(config)
  return config
def bstack1l1llll_opy_(config):
  global bstack1lll11l1l_opy_
  if bstack1lllllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨધ") in config and str(config[bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩન")]).lower() != bstack1lllllll1_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ઩"):
    if not bstack1lllllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫપ") in config:
      config[bstack1lllllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬફ")] = {}
    if not bstack1lllllll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫબ") in config[bstack1lllllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧભ")]:
      bstack11l11l111_opy_ = datetime.datetime.now()
      bstack1l11ll11_opy_ = bstack11l11l111_opy_.strftime(bstack1lllllll1_opy_ (u"ࠫࠪࡪ࡟ࠦࡤࡢࠩࡍࠫࡍࠨમ"))
      hostname = socket.gethostname()
      bstack1ll11ll1_opy_ = bstack1lllllll1_opy_ (u"ࠬ࠭ય").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1lllllll1_opy_ (u"࠭ࡻࡾࡡࡾࢁࡤࢁࡽࠨર").format(bstack1l11ll11_opy_, hostname, bstack1ll11ll1_opy_)
      config[bstack1lllllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ઱")][bstack1lllllll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪલ")] = identifier
    bstack1lll11l1l_opy_ = config[bstack1lllllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ળ")][bstack1lllllll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ઴")]
  return config
def bstack11ll11111_opy_():
  if (
    isinstance(os.getenv(bstack1lllllll1_opy_ (u"ࠫࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠩવ")), str) and len(os.getenv(bstack1lllllll1_opy_ (u"ࠬࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠪશ"))) > 0
  ) or (
    isinstance(os.getenv(bstack1lllllll1_opy_ (u"࠭ࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠬષ")), str) and len(os.getenv(bstack1lllllll1_opy_ (u"ࠧࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊ࠭સ"))) > 0
  ):
    return os.getenv(bstack1lllllll1_opy_ (u"ࠨࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠧહ"), 0)
  if str(os.getenv(bstack1lllllll1_opy_ (u"ࠩࡆࡍࠬ઺"))).lower() == bstack1lllllll1_opy_ (u"ࠪࡸࡷࡻࡥࠨ઻") and str(os.getenv(bstack1lllllll1_opy_ (u"ࠫࡈࡏࡒࡄࡎࡈࡇࡎ઼࠭"))).lower() == bstack1lllllll1_opy_ (u"ࠬࡺࡲࡶࡧࠪઽ"):
    return os.getenv(bstack1lllllll1_opy_ (u"࠭ࡃࡊࡔࡆࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࠩા"), 0)
  if str(os.getenv(bstack1lllllll1_opy_ (u"ࠧࡄࡋࠪિ"))).lower() == bstack1lllllll1_opy_ (u"ࠨࡶࡵࡹࡪ࠭ી") and str(os.getenv(bstack1lllllll1_opy_ (u"ࠩࡗࡖࡆ࡜ࡉࡔࠩુ"))).lower() == bstack1lllllll1_opy_ (u"ࠪࡸࡷࡻࡥࠨૂ"):
    return os.getenv(bstack1lllllll1_opy_ (u"࡙ࠫࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠪૃ"), 0)
  if str(os.getenv(bstack1lllllll1_opy_ (u"ࠬࡉࡉࠨૄ"))).lower() == bstack1lllllll1_opy_ (u"࠭ࡴࡳࡷࡨࠫૅ") and str(os.getenv(bstack1lllllll1_opy_ (u"ࠧࡄࡋࡢࡒࡆࡓࡅࠨ૆"))).lower() == bstack1lllllll1_opy_ (u"ࠨࡥࡲࡨࡪࡹࡨࡪࡲࠪે"):
    return 0 # bstack1111ll1_opy_ bstack1l111ll1l_opy_ not set build number env
  if os.getenv(bstack1lllllll1_opy_ (u"ࠩࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡒࡂࡐࡆࡌࠬૈ")) and os.getenv(bstack1lllllll1_opy_ (u"ࠪࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡃࡐࡏࡐࡍ࡙࠭ૉ")):
    return os.getenv(bstack1lllllll1_opy_ (u"ࠫࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗ࠭૊"), 0)
  if str(os.getenv(bstack1lllllll1_opy_ (u"ࠬࡉࡉࠨો"))).lower() == bstack1lllllll1_opy_ (u"࠭ࡴࡳࡷࡨࠫૌ") and str(os.getenv(bstack1lllllll1_opy_ (u"ࠧࡅࡔࡒࡒࡊ્࠭"))).lower() == bstack1lllllll1_opy_ (u"ࠨࡶࡵࡹࡪ࠭૎"):
    return os.getenv(bstack1lllllll1_opy_ (u"ࠩࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠧ૏"), 0)
  if str(os.getenv(bstack1lllllll1_opy_ (u"ࠪࡇࡎ࠭ૐ"))).lower() == bstack1lllllll1_opy_ (u"ࠫࡹࡸࡵࡦࠩ૑") and str(os.getenv(bstack1lllllll1_opy_ (u"࡙ࠬࡅࡎࡃࡓࡌࡔࡘࡅࠨ૒"))).lower() == bstack1lllllll1_opy_ (u"࠭ࡴࡳࡷࡨࠫ૓"):
    return os.getenv(bstack1lllllll1_opy_ (u"ࠧࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡊࡆࠪ૔"), 0)
  if str(os.getenv(bstack1lllllll1_opy_ (u"ࠨࡅࡌࠫ૕"))).lower() == bstack1lllllll1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ૖") and str(os.getenv(bstack1lllllll1_opy_ (u"ࠪࡋࡎ࡚ࡌࡂࡄࡢࡇࡎ࠭૗"))).lower() == bstack1lllllll1_opy_ (u"ࠫࡹࡸࡵࡦࠩ૘"):
    return os.getenv(bstack1lllllll1_opy_ (u"ࠬࡉࡉࡠࡌࡒࡆࡤࡏࡄࠨ૙"), 0)
  if str(os.getenv(bstack1lllllll1_opy_ (u"࠭ࡃࡊࠩ૚"))).lower() == bstack1lllllll1_opy_ (u"ࠧࡵࡴࡸࡩࠬ૛") and str(os.getenv(bstack1lllllll1_opy_ (u"ࠨࡄࡘࡍࡑࡊࡋࡊࡖࡈࠫ૜"))).lower() == bstack1lllllll1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ૝"):
    return os.getenv(bstack1lllllll1_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠬ૞"), 0)
  if str(os.getenv(bstack1lllllll1_opy_ (u"࡙ࠫࡌ࡟ࡃࡗࡌࡐࡉ࠭૟"))).lower() == bstack1lllllll1_opy_ (u"ࠬࡺࡲࡶࡧࠪૠ"):
    return os.getenv(bstack1lllllll1_opy_ (u"࠭ࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉ࠭ૡ"), 0)
  return -1
def bstack1l11llll_opy_(bstack1l1lll1l1_opy_):
  global CONFIG
  if not bstack1lllllll1_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩૢ") in CONFIG[bstack1lllllll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪૣ")]:
    return
  CONFIG[bstack1lllllll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૤")] = CONFIG[bstack1lllllll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૥")].replace(
    bstack1lllllll1_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭૦"),
    str(bstack1l1lll1l1_opy_)
  )
def bstack111ll11_opy_():
  global CONFIG
  if not bstack1lllllll1_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫ૧") in CONFIG[bstack1lllllll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૨")]:
    return
  bstack11l11l111_opy_ = datetime.datetime.now()
  bstack1l11ll11_opy_ = bstack11l11l111_opy_.strftime(bstack1lllllll1_opy_ (u"ࠧࠦࡦ࠰ࠩࡧ࠳ࠥࡉ࠼ࠨࡑࠬ૩"))
  CONFIG[bstack1lllllll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૪")] = CONFIG[bstack1lllllll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૫")].replace(
    bstack1lllllll1_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩ૬"),
    bstack1l11ll11_opy_
  )
def bstack111ll1111_opy_():
  global CONFIG
  if bstack1lllllll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૭") in CONFIG and not bool(CONFIG[bstack1lllllll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૮")]):
    del CONFIG[bstack1lllllll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૯")]
    return
  if not bstack1lllllll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૰") in CONFIG:
    CONFIG[bstack1lllllll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૱")] = bstack1lllllll1_opy_ (u"ࠩࠦࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬ૲")
  if bstack1lllllll1_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩ૳") in CONFIG[bstack1lllllll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૴")]:
    bstack111ll11_opy_()
    os.environ[bstack1lllllll1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ૵")] = CONFIG[bstack1lllllll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૶")]
  if not bstack1lllllll1_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩ૷") in CONFIG[bstack1lllllll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૸")]:
    return
  bstack1l1lll1l1_opy_ = bstack1lllllll1_opy_ (u"ࠩࠪૹ")
  bstack1llllll_opy_ = bstack11ll11111_opy_()
  if bstack1llllll_opy_ != -1:
    bstack1l1lll1l1_opy_ = bstack1lllllll1_opy_ (u"ࠪࡇࡎࠦࠧૺ") + str(bstack1llllll_opy_)
  if bstack1l1lll1l1_opy_ == bstack1lllllll1_opy_ (u"ࠫࠬૻ"):
    bstack11ll1ll1_opy_ = bstack111l11_opy_(CONFIG[bstack1lllllll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨૼ")])
    if bstack11ll1ll1_opy_ != -1:
      bstack1l1lll1l1_opy_ = str(bstack11ll1ll1_opy_)
  if bstack1l1lll1l1_opy_:
    bstack1l11llll_opy_(bstack1l1lll1l1_opy_)
    os.environ[bstack1lllllll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ૽")] = CONFIG[bstack1lllllll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૾")]
def bstack1llll11l_opy_(bstack1l1llll1l_opy_, bstack1l1l111ll_opy_, path):
  bstack111lll1l1_opy_ = {
    bstack1lllllll1_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૿"): bstack1l1l111ll_opy_
  }
  if os.path.exists(path):
    bstack11lllll_opy_ = json.load(open(path, bstack1lllllll1_opy_ (u"ࠩࡵࡦࠬ଀")))
  else:
    bstack11lllll_opy_ = {}
  bstack11lllll_opy_[bstack1l1llll1l_opy_] = bstack111lll1l1_opy_
  with open(path, bstack1lllllll1_opy_ (u"ࠥࡻ࠰ࠨଁ")) as outfile:
    json.dump(bstack11lllll_opy_, outfile)
def bstack111l11_opy_(bstack1l1llll1l_opy_):
  bstack1l1llll1l_opy_ = str(bstack1l1llll1l_opy_)
  bstack111l1lll_opy_ = os.path.join(os.path.expanduser(bstack1lllllll1_opy_ (u"ࠫࢃ࠭ଂ")), bstack1lllllll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬଃ"))
  try:
    if not os.path.exists(bstack111l1lll_opy_):
      os.makedirs(bstack111l1lll_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1lllllll1_opy_ (u"࠭ࡾࠨ଄")), bstack1lllllll1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧଅ"), bstack1lllllll1_opy_ (u"ࠨ࠰ࡥࡹ࡮ࡲࡤ࠮ࡰࡤࡱࡪ࠳ࡣࡢࡥ࡫ࡩ࠳ࡰࡳࡰࡰࠪଆ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1lllllll1_opy_ (u"ࠩࡺࠫଇ")):
        pass
      with open(file_path, bstack1lllllll1_opy_ (u"ࠥࡻ࠰ࠨଈ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1lllllll1_opy_ (u"ࠫࡷ࠭ଉ")) as bstack111ll1ll1_opy_:
      bstack1l1ll1ll1_opy_ = json.load(bstack111ll1ll1_opy_)
    if bstack1l1llll1l_opy_ in bstack1l1ll1ll1_opy_:
      bstack1llll1111_opy_ = bstack1l1ll1ll1_opy_[bstack1l1llll1l_opy_][bstack1lllllll1_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩଊ")]
      bstack1l1l1l_opy_ = int(bstack1llll1111_opy_) + 1
      bstack1llll11l_opy_(bstack1l1llll1l_opy_, bstack1l1l1l_opy_, file_path)
      return bstack1l1l1l_opy_
    else:
      bstack1llll11l_opy_(bstack1l1llll1l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1l1l1ll1l_opy_.format(str(e)))
    return -1
def bstack11l1ll1l1_opy_(config):
  if not config[bstack1lllllll1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨଋ")] or not config[bstack1lllllll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪଌ")]:
    return True
  else:
    return False
def bstack1ll1ll111_opy_(config):
  if bstack1lllllll1_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧ଍") in config:
    del(config[bstack1lllllll1_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨ଎")])
    return False
  if bstack1ll11l1l_opy_() < version.parse(bstack1lllllll1_opy_ (u"ࠪ࠷࠳࠺࠮࠱ࠩଏ")):
    return False
  if bstack1ll11l1l_opy_() >= version.parse(bstack1lllllll1_opy_ (u"ࠫ࠹࠴࠱࠯࠷ࠪଐ")):
    return True
  if bstack1lllllll1_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ଑") in config and config[bstack1lllllll1_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭଒")] == False:
    return False
  else:
    return True
def bstack1lll1l_opy_(config, index = 0):
  global bstack1l11ll1l_opy_
  bstack1l1llll11_opy_ = {}
  caps = bstack111l111l_opy_ + bstack1ll1l11l_opy_
  if bstack1l11ll1l_opy_:
    caps += bstack1ll1l1l11_opy_
  for key in config:
    if key in caps + [bstack1lllllll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଓ")]:
      continue
    bstack1l1llll11_opy_[key] = config[key]
  if bstack1lllllll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫଔ") in config:
    for bstack1l1l1111_opy_ in config[bstack1lllllll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬକ")][index]:
      if bstack1l1l1111_opy_ in caps + [bstack1lllllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨଖ"), bstack1lllllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬଗ")]:
        continue
      bstack1l1llll11_opy_[bstack1l1l1111_opy_] = config[bstack1lllllll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଘ")][index][bstack1l1l1111_opy_]
  bstack1l1llll11_opy_[bstack1lllllll1_opy_ (u"࠭ࡨࡰࡵࡷࡒࡦࡳࡥࠨଙ")] = socket.gethostname()
  if bstack1lllllll1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨଚ") in bstack1l1llll11_opy_:
    del(bstack1l1llll11_opy_[bstack1lllllll1_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩଛ")])
  return bstack1l1llll11_opy_
def bstack1llll1ll_opy_(config):
  global bstack1l11ll1l_opy_
  bstack1ll111111_opy_ = {}
  caps = bstack1ll1l11l_opy_
  if bstack1l11ll1l_opy_:
    caps+= bstack1ll1l1l11_opy_
  for key in caps:
    if key in config:
      bstack1ll111111_opy_[key] = config[key]
  return bstack1ll111111_opy_
def bstack11ll1l_opy_(bstack1l1llll11_opy_, bstack1ll111111_opy_):
  bstack1ll1l1ll1_opy_ = {}
  for key in bstack1l1llll11_opy_.keys():
    if key in bstack1ll1llll1_opy_:
      bstack1ll1l1ll1_opy_[bstack1ll1llll1_opy_[key]] = bstack1l1llll11_opy_[key]
    else:
      bstack1ll1l1ll1_opy_[key] = bstack1l1llll11_opy_[key]
  for key in bstack1ll111111_opy_:
    if key in bstack1ll1llll1_opy_:
      bstack1ll1l1ll1_opy_[bstack1ll1llll1_opy_[key]] = bstack1ll111111_opy_[key]
    else:
      bstack1ll1l1ll1_opy_[key] = bstack1ll111111_opy_[key]
  return bstack1ll1l1ll1_opy_
def bstack1ll11lll1_opy_(config, index = 0):
  global bstack1l11ll1l_opy_
  config = copy.deepcopy(config)
  caps = {}
  bstack1ll111111_opy_ = bstack1llll1ll_opy_(config)
  bstack11l1l1l_opy_ = bstack1ll1l11l_opy_
  bstack11l1l1l_opy_ += bstack1ll11l11_opy_
  if bstack1l11ll1l_opy_:
    bstack11l1l1l_opy_ += bstack1ll1l1l11_opy_
  if bstack1lllllll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬଜ") in config:
    if bstack1lllllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨଝ") in config[bstack1lllllll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଞ")][index]:
      caps[bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪଟ")] = config[bstack1lllllll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଠ")][index][bstack1lllllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬଡ")]
    if bstack1lllllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩଢ") in config[bstack1lllllll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬଣ")][index]:
      caps[bstack1lllllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫତ")] = str(config[bstack1lllllll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଥ")][index][bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ଦ")])
    bstack11l1l111_opy_ = {}
    for bstack1l1l1ll11_opy_ in bstack11l1l1l_opy_:
      if bstack1l1l1ll11_opy_ in config[bstack1lllllll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଧ")][index]:
        if bstack1l1l1ll11_opy_ == bstack1lllllll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩନ"):
          bstack11l1l111_opy_[bstack1l1l1ll11_opy_] = str(config[bstack1lllllll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ଩")][index][bstack1l1l1ll11_opy_] * 1.0)
        else:
          bstack11l1l111_opy_[bstack1l1l1ll11_opy_] = config[bstack1lllllll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬପ")][index][bstack1l1l1ll11_opy_]
        del(config[bstack1lllllll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଫ")][index][bstack1l1l1ll11_opy_])
    bstack1ll111111_opy_ = update(bstack1ll111111_opy_, bstack11l1l111_opy_)
  bstack1l1llll11_opy_ = bstack1lll1l_opy_(config, index)
  for bstack1l11ll11l_opy_ in bstack1ll1l11l_opy_ + [bstack1lllllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩବ"), bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ଭ")]:
    if bstack1l11ll11l_opy_ in bstack1l1llll11_opy_:
      bstack1ll111111_opy_[bstack1l11ll11l_opy_] = bstack1l1llll11_opy_[bstack1l11ll11l_opy_]
      del(bstack1l1llll11_opy_[bstack1l11ll11l_opy_])
  if bstack1ll1ll111_opy_(config):
    bstack1l1llll11_opy_[bstack1lllllll1_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ମ")] = True
    caps.update(bstack1ll111111_opy_)
    caps[bstack1lllllll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨଯ")] = bstack1l1llll11_opy_
  else:
    bstack1l1llll11_opy_[bstack1lllllll1_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨର")] = False
    caps.update(bstack11ll1l_opy_(bstack1l1llll11_opy_, bstack1ll111111_opy_))
    if bstack1lllllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ଱") in caps:
      caps[bstack1lllllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫଲ")] = caps[bstack1lllllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩଳ")]
      del(caps[bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ଴")])
    if bstack1lllllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧଵ") in caps:
      caps[bstack1lllllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩଶ")] = caps[bstack1lllllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩଷ")]
      del(caps[bstack1lllllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪସ")])
  return caps
def bstack1111lll1_opy_():
  global bstack1ll111l11_opy_
  if bstack1ll11l1l_opy_() <= version.parse(bstack1lllllll1_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪହ")):
    if bstack1ll111l11_opy_ != bstack1lllllll1_opy_ (u"ࠫࠬ଺"):
      return bstack1lllllll1_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ଻") + bstack1ll111l11_opy_ + bstack1lllllll1_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤ଼ࠥ")
    return bstack1l1ll1l11_opy_
  if  bstack1ll111l11_opy_ != bstack1lllllll1_opy_ (u"ࠧࠨଽ"):
    return bstack1lllllll1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥା") + bstack1ll111l11_opy_ + bstack1lllllll1_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥି")
  return bstack111111ll_opy_
def bstack1ll1l11l1_opy_(options):
  return hasattr(options, bstack1lllllll1_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫୀ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l1111ll1_opy_(options, bstack1l1llll1_opy_):
  for bstack1ll11l11l_opy_ in bstack1l1llll1_opy_:
    if bstack1ll11l11l_opy_ in [bstack1lllllll1_opy_ (u"ࠫࡦࡸࡧࡴࠩୁ"), bstack1lllllll1_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩୂ")]:
      next
    if bstack1ll11l11l_opy_ in options._experimental_options:
      options._experimental_options[bstack1ll11l11l_opy_]= update(options._experimental_options[bstack1ll11l11l_opy_], bstack1l1llll1_opy_[bstack1ll11l11l_opy_])
    else:
      options.add_experimental_option(bstack1ll11l11l_opy_, bstack1l1llll1_opy_[bstack1ll11l11l_opy_])
  if bstack1lllllll1_opy_ (u"࠭ࡡࡳࡩࡶࠫୃ") in bstack1l1llll1_opy_:
    for arg in bstack1l1llll1_opy_[bstack1lllllll1_opy_ (u"ࠧࡢࡴࡪࡷࠬୄ")]:
      options.add_argument(arg)
    del(bstack1l1llll1_opy_[bstack1lllllll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭୅")])
  if bstack1lllllll1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭୆") in bstack1l1llll1_opy_:
    for ext in bstack1l1llll1_opy_[bstack1lllllll1_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧେ")]:
      options.add_extension(ext)
    del(bstack1l1llll1_opy_[bstack1lllllll1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨୈ")])
def bstackl_opy_(options, bstack1lll111l1_opy_):
  if bstack1lllllll1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ୉") in bstack1lll111l1_opy_:
    for bstack11l11ll1l_opy_ in bstack1lll111l1_opy_[bstack1lllllll1_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ୊")]:
      if bstack11l11ll1l_opy_ in options._preferences:
        options._preferences[bstack11l11ll1l_opy_] = update(options._preferences[bstack11l11ll1l_opy_], bstack1lll111l1_opy_[bstack1lllllll1_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ୋ")][bstack11l11ll1l_opy_])
      else:
        options.set_preference(bstack11l11ll1l_opy_, bstack1lll111l1_opy_[bstack1lllllll1_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧୌ")][bstack11l11ll1l_opy_])
  if bstack1lllllll1_opy_ (u"ࠩࡤࡶ࡬ࡹ୍ࠧ") in bstack1lll111l1_opy_:
    for arg in bstack1lll111l1_opy_[bstack1lllllll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ୎")]:
      options.add_argument(arg)
def bstack1111l111_opy_(options, bstack1l1_opy_):
  if bstack1lllllll1_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬ୏") in bstack1l1_opy_:
    options.use_webview(bool(bstack1l1_opy_[bstack1lllllll1_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭୐")]))
  bstack1l1111ll1_opy_(options, bstack1l1_opy_)
def bstack1l1l1_opy_(options, bstack1l11ll1ll_opy_):
  for bstack1ll1ll_opy_ in bstack1l11ll1ll_opy_:
    if bstack1ll1ll_opy_ in [bstack1lllllll1_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪ୑"), bstack1lllllll1_opy_ (u"ࠧࡢࡴࡪࡷࠬ୒")]:
      next
    options.set_capability(bstack1ll1ll_opy_, bstack1l11ll1ll_opy_[bstack1ll1ll_opy_])
  if bstack1lllllll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭୓") in bstack1l11ll1ll_opy_:
    for arg in bstack1l11ll1ll_opy_[bstack1lllllll1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ୔")]:
      options.add_argument(arg)
  if bstack1lllllll1_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧ୕") in bstack1l11ll1ll_opy_:
    options.use_technology_preview(bool(bstack1l11ll1ll_opy_[bstack1lllllll1_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨୖ")]))
def bstack111lll11l_opy_(options, bstack1l11lll1_opy_):
  for bstack111l1llll_opy_ in bstack1l11lll1_opy_:
    if bstack111l1llll_opy_ in [bstack1lllllll1_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩୗ"), bstack1lllllll1_opy_ (u"࠭ࡡࡳࡩࡶࠫ୘")]:
      next
    options._options[bstack111l1llll_opy_] = bstack1l11lll1_opy_[bstack111l1llll_opy_]
  if bstack1lllllll1_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ୙") in bstack1l11lll1_opy_:
    for bstack111ll1lll_opy_ in bstack1l11lll1_opy_[bstack1lllllll1_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ୚")]:
      options.bstack1l11l11ll_opy_(
          bstack111ll1lll_opy_, bstack1l11lll1_opy_[bstack1lllllll1_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭୛")][bstack111ll1lll_opy_])
  if bstack1lllllll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨଡ଼") in bstack1l11lll1_opy_:
    for arg in bstack1l11lll1_opy_[bstack1lllllll1_opy_ (u"ࠫࡦࡸࡧࡴࠩଢ଼")]:
      options.add_argument(arg)
def bstack11l11111l_opy_(options, caps):
  if not hasattr(options, bstack1lllllll1_opy_ (u"ࠬࡑࡅ࡚ࠩ୞")):
    return
  if options.KEY == bstack1lllllll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫୟ") and options.KEY in caps:
    bstack1l1111ll1_opy_(options, caps[bstack1lllllll1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬୠ")])
  elif options.KEY == bstack1lllllll1_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ୡ") and options.KEY in caps:
    bstackl_opy_(options, caps[bstack1lllllll1_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧୢ")])
  elif options.KEY == bstack1lllllll1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫୣ") and options.KEY in caps:
    bstack1l1l1_opy_(options, caps[bstack1lllllll1_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬ୤")])
  elif options.KEY == bstack1lllllll1_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭୥") and options.KEY in caps:
    bstack1111l111_opy_(options, caps[bstack1lllllll1_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ୦")])
  elif options.KEY == bstack1lllllll1_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭୧") and options.KEY in caps:
    bstack111lll11l_opy_(options, caps[bstack1lllllll1_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ୨")])
def bstack1llll11l1_opy_(caps):
  global bstack1l11ll1l_opy_
  if bstack1l11ll1l_opy_:
    if bstack1l11_opy_() < version.parse(bstack1lllllll1_opy_ (u"ࠩ࠵࠲࠸࠴࠰ࠨ୩")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1lllllll1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ୪")
    if bstack1lllllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ୫") in caps:
      browser = caps[bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ୬")]
    elif bstack1lllllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ୭") in caps:
      browser = caps[bstack1lllllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ୮")]
    browser = str(browser).lower()
    if browser == bstack1lllllll1_opy_ (u"ࠨ࡫ࡳ࡬ࡴࡴࡥࠨ୯") or browser == bstack1lllllll1_opy_ (u"ࠩ࡬ࡴࡦࡪࠧ୰"):
      browser = bstack1lllllll1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪୱ")
    if browser == bstack1lllllll1_opy_ (u"ࠫࡸࡧ࡭ࡴࡷࡱ࡫ࠬ୲"):
      browser = bstack1lllllll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ୳")
    if browser not in [bstack1lllllll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭୴"), bstack1lllllll1_opy_ (u"ࠧࡦࡦࡪࡩࠬ୵"), bstack1lllllll1_opy_ (u"ࠨ࡫ࡨࠫ୶"), bstack1lllllll1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩ୷"), bstack1lllllll1_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫ୸")]:
      return None
    try:
      package = bstack1lllllll1_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡾࢁ࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭୹").format(browser)
      name = bstack1lllllll1_opy_ (u"ࠬࡕࡰࡵ࡫ࡲࡲࡸ࠭୺")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1ll1l11l1_opy_(options):
        return None
      for bstack1l11ll11l_opy_ in caps.keys():
        options.set_capability(bstack1l11ll11l_opy_, caps[bstack1l11ll11l_opy_])
      bstack11l11111l_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l1111_opy_(options, bstack11l111_opy_):
  if not bstack1ll1l11l1_opy_(options):
    return
  for bstack1l11ll11l_opy_ in bstack11l111_opy_.keys():
    if bstack1l11ll11l_opy_ in bstack1ll11l11_opy_:
      next
    if bstack1l11ll11l_opy_ in options._caps and type(options._caps[bstack1l11ll11l_opy_]) in [dict, list]:
      options._caps[bstack1l11ll11l_opy_] = update(options._caps[bstack1l11ll11l_opy_], bstack11l111_opy_[bstack1l11ll11l_opy_])
    else:
      options.set_capability(bstack1l11ll11l_opy_, bstack11l111_opy_[bstack1l11ll11l_opy_])
  bstack11l11111l_opy_(options, bstack11l111_opy_)
  if bstack1lllllll1_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬ୻") in options._caps:
    if options._caps[bstack1lllllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ୼")] and options._caps[bstack1lllllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭୽")].lower() != bstack1lllllll1_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪ୾"):
      del options._caps[bstack1lllllll1_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩ୿")]
def bstack1ll11ll_opy_(proxy_config):
  if bstack1lllllll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ஀") in proxy_config:
    proxy_config[bstack1lllllll1_opy_ (u"ࠬࡹࡳ࡭ࡒࡵࡳࡽࡿࠧ஁")] = proxy_config[bstack1lllllll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪஂ")]
    del(proxy_config[bstack1lllllll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫஃ")])
  if bstack1lllllll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ஄") in proxy_config and proxy_config[bstack1lllllll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬஅ")].lower() != bstack1lllllll1_opy_ (u"ࠪࡨ࡮ࡸࡥࡤࡶࠪஆ"):
    proxy_config[bstack1lllllll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧஇ")] = bstack1lllllll1_opy_ (u"ࠬࡳࡡ࡯ࡷࡤࡰࠬஈ")
  if bstack1lllllll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡆࡻࡴࡰࡥࡲࡲ࡫࡯ࡧࡖࡴ࡯ࠫஉ") in proxy_config:
    proxy_config[bstack1lllllll1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪஊ")] = bstack1lllllll1_opy_ (u"ࠨࡲࡤࡧࠬ஋")
  return proxy_config
def bstack111l11l1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1lllllll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ஌") in config:
    return proxy
  config[bstack1lllllll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ஍")] = bstack1ll11ll_opy_(config[bstack1lllllll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪஎ")])
  if proxy == None:
    proxy = Proxy(config[bstack1lllllll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫஏ")])
  return proxy
def bstack111l1l1ll_opy_(self):
  global CONFIG
  global bstack11ll111ll_opy_
  try:
    proxy = bstack1ll1lll_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1lllllll1_opy_ (u"࠭࠮ࡱࡣࡦࠫஐ")):
        proxies = bstack1llll1l_opy_(proxy, bstack1111lll1_opy_())
        if len(proxies) > 0:
          protocol, bstack111ll1l1l_opy_ = proxies.popitem()
          if bstack1lllllll1_opy_ (u"ࠢ࠻࠱࠲ࠦ஑") in bstack111ll1l1l_opy_:
            return bstack111ll1l1l_opy_
          else:
            return bstack1lllllll1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤஒ") + bstack111ll1l1l_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1lllllll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨஓ").format(str(e)))
  return bstack11ll111ll_opy_(self)
def bstack11ll11ll1_opy_():
  global CONFIG
  return bstack1lllllll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ஔ") in CONFIG or bstack1lllllll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨக") in CONFIG
def bstack1ll1lll_opy_(config):
  if not bstack11ll11ll1_opy_():
    return
  if config.get(bstack1lllllll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ஖")):
    return config.get(bstack1lllllll1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ஗"))
  if config.get(bstack1lllllll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ஘")):
    return config.get(bstack1lllllll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬங"))
def bstack1l1lll1_opy_(url):
  try:
      result = urlparse(url)
      return all([result.scheme, result.netloc])
  except:
      return False
def bstack111l1l1_opy_(bstack1l1111l1l_opy_, bstack1l111llll_opy_):
  from pypac import get_pac
  from pypac import PACSession
  from pypac.parser import PACFile
  import socket
  if os.path.isfile(bstack1l1111l1l_opy_):
    with open(bstack1l1111l1l_opy_) as f:
      pac = PACFile(f.read())
  elif bstack1l1lll1_opy_(bstack1l1111l1l_opy_):
    pac = get_pac(url=bstack1l1111l1l_opy_)
  else:
    raise Exception(bstack1lllllll1_opy_ (u"ࠩࡓࡥࡨࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠩச").format(bstack1l1111l1l_opy_))
  session = PACSession(pac)
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((bstack1lllllll1_opy_ (u"ࠥ࠼࠳࠾࠮࠹࠰࠻ࠦ஛"), 80))
    bstack111l11111_opy_ = s.getsockname()[0]
    s.close()
  except:
    bstack111l11111_opy_ = bstack1lllllll1_opy_ (u"ࠫ࠵࠴࠰࠯࠲࠱࠴ࠬஜ")
  proxy_url = session.get_pac().find_proxy_for_url(bstack1l111llll_opy_, bstack111l11111_opy_)
  return proxy_url
def bstack1llll1l_opy_(bstack1l1111l1l_opy_, bstack1l111llll_opy_):
  proxies = {}
  global bstack1lll11l11_opy_
  if bstack1lllllll1_opy_ (u"ࠬࡖࡁࡄࡡࡓࡖࡔ࡞࡙ࠨ஝") in globals():
    return bstack1lll11l11_opy_
  try:
    proxy = bstack111l1l1_opy_(bstack1l1111l1l_opy_,bstack1l111llll_opy_)
    if bstack1lllllll1_opy_ (u"ࠨࡄࡊࡔࡈࡇ࡙ࠨஞ") in proxy:
      proxies = {}
    elif bstack1lllllll1_opy_ (u"ࠢࡉࡖࡗࡔࠧட") in proxy or bstack1lllllll1_opy_ (u"ࠣࡊࡗࡘࡕ࡙ࠢ஠") in proxy or bstack1lllllll1_opy_ (u"ࠤࡖࡓࡈࡑࡓࠣ஡") in proxy:
      bstack1ll1l1l_opy_ = proxy.split(bstack1lllllll1_opy_ (u"ࠥࠤࠧ஢"))
      if bstack1lllllll1_opy_ (u"ࠦ࠿࠵࠯ࠣண") in bstack1lllllll1_opy_ (u"ࠧࠨத").join(bstack1ll1l1l_opy_[1:]):
        proxies = {
          bstack1lllllll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ஥"): bstack1lllllll1_opy_ (u"ࠢࠣ஦").join(bstack1ll1l1l_opy_[1:])
        }
      else:
        proxies = {
          bstack1lllllll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ஧") : str(bstack1ll1l1l_opy_[0]).lower()+ bstack1lllllll1_opy_ (u"ࠤ࠽࠳࠴ࠨந") + bstack1lllllll1_opy_ (u"ࠥࠦன").join(bstack1ll1l1l_opy_[1:])
        }
    elif bstack1lllllll1_opy_ (u"ࠦࡕࡘࡏ࡙࡛ࠥப") in proxy:
      bstack1ll1l1l_opy_ = proxy.split(bstack1lllllll1_opy_ (u"ࠧࠦࠢ஫"))
      if bstack1lllllll1_opy_ (u"ࠨ࠺࠰࠱ࠥ஬") in bstack1lllllll1_opy_ (u"ࠢࠣ஭").join(bstack1ll1l1l_opy_[1:]):
        proxies = {
          bstack1lllllll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧம"): bstack1lllllll1_opy_ (u"ࠤࠥய").join(bstack1ll1l1l_opy_[1:])
        }
      else:
        proxies = {
          bstack1lllllll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩர"): bstack1lllllll1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧற") + bstack1lllllll1_opy_ (u"ࠧࠨல").join(bstack1ll1l1l_opy_[1:])
        }
    else:
      proxies = {
        bstack1lllllll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬள"): proxy
      }
  except Exception as e:
    logger.error(bstack111l1ll11_opy_.format(bstack1l1111l1l_opy_, str(e)))
  bstack1lll11l11_opy_ = proxies
  return proxies
def bstack1l11l111l_opy_(config, bstack1l111llll_opy_):
  proxy = bstack1ll1lll_opy_(config)
  proxies = {}
  if config.get(bstack1lllllll1_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪழ")) or config.get(bstack1lllllll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬவ")):
    if proxy.endswith(bstack1lllllll1_opy_ (u"ࠩ࠱ࡴࡦࡩࠧஶ")):
      proxies = bstack1llll1l_opy_(proxy,bstack1l111llll_opy_)
    else:
      proxies = {
        bstack1lllllll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩஷ"): proxy
      }
  return proxies
def bstack1l11ll111_opy_():
  return bstack11ll11ll1_opy_() and bstack1ll11l1l_opy_() >= version.parse(bstack1lllll1_opy_)
def bstack1lllllll_opy_(config):
  bstack1l11l1l11_opy_ = {}
  if bstack1lllllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨஸ") in config:
    bstack1l11l1l11_opy_ =  config[bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩஹ")]
  if bstack1lllllll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ஺") in config:
    bstack1l11l1l11_opy_ = config[bstack1lllllll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭஻")]
  proxy = bstack1ll1lll_opy_(config)
  if proxy:
    if proxy.endswith(bstack1lllllll1_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭஼")) and os.path.isfile(proxy):
      bstack1l11l1l11_opy_[bstack1lllllll1_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬ஽")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1lllllll1_opy_ (u"ࠪ࠲ࡵࡧࡣࠨா")):
        proxies = bstack1l11l111l_opy_(config, bstack1111lll1_opy_())
        if len(proxies) > 0:
          protocol, bstack111ll1l1l_opy_ = proxies.popitem()
          if bstack1lllllll1_opy_ (u"ࠦ࠿࠵࠯ࠣி") in bstack111ll1l1l_opy_:
            parsed_url = urlparse(bstack111ll1l1l_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1lllllll1_opy_ (u"ࠧࡀ࠯࠰ࠤீ") + bstack111ll1l1l_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1l11l1l11_opy_[bstack1lllllll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡍࡵࡳࡵࠩு")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1l11l1l11_opy_[bstack1lllllll1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪூ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1l11l1l11_opy_[bstack1lllllll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫ௃")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1l11l1l11_opy_[bstack1lllllll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬ௄")] = str(parsed_url.password)
  return bstack1l11l1l11_opy_
def bstack1l1l1ll_opy_(config):
  if bstack1lllllll1_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨ௅") in config:
    return config[bstack1lllllll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩெ")]
  return {}
def bstack11111_opy_(caps):
  global bstack1lll11l1l_opy_
  if bstack1lllllll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ே") in caps:
    caps[bstack1lllllll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧை")][bstack1lllllll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭௉")] = True
    if bstack1lll11l1l_opy_:
      caps[bstack1lllllll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩொ")][bstack1lllllll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫோ")] = bstack1lll11l1l_opy_
  else:
    caps[bstack1lllllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨௌ")] = True
    if bstack1lll11l1l_opy_:
      caps[bstack1lllllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ்ࠬ")] = bstack1lll11l1l_opy_
def bstack1l11lll1l_opy_():
  global CONFIG
  if bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ௎") in CONFIG and CONFIG[bstack1lllllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ௏")]:
    bstack1l11l1l11_opy_ = bstack1lllllll_opy_(CONFIG)
    bstack111ll1ll_opy_(CONFIG[bstack1lllllll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪௐ")], bstack1l11l1l11_opy_)
def bstack111ll1ll_opy_(key, bstack1l11l1l11_opy_):
  global bstack11l11l11l_opy_
  logger.info(bstack11l1lll_opy_)
  try:
    bstack11l11l11l_opy_ = Local()
    bstack1l111111l_opy_ = {bstack1lllllll1_opy_ (u"ࠨ࡭ࡨࡽࠬ௑"): key}
    bstack1l111111l_opy_.update(bstack1l11l1l11_opy_)
    logger.debug(bstack11l11ll_opy_.format(str(bstack1l111111l_opy_)))
    bstack11l11l11l_opy_.start(**bstack1l111111l_opy_)
    if bstack11l11l11l_opy_.isRunning():
      logger.info(bstack11lll1l_opy_)
  except Exception as e:
    bstack11l11_opy_(bstack1111l1l_opy_.format(str(e)))
def bstack1lllll11l_opy_():
  global bstack11l11l11l_opy_
  if bstack11l11l11l_opy_.isRunning():
    logger.info(bstack1l1l1l11_opy_)
    bstack11l11l11l_opy_.stop()
  bstack11l11l11l_opy_ = None
def bstack1l11l1l_opy_(bstack1l1l1l111_opy_=[]):
  global CONFIG
  bstack1l1ll1ll_opy_ = []
  bstack1lllll1l1_opy_ = [bstack1lllllll1_opy_ (u"ࠩࡲࡷࠬ௒"), bstack1lllllll1_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭௓"), bstack1lllllll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ௔"), bstack1lllllll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ௕"), bstack1lllllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ௖"), bstack1lllllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨௗ")]
  try:
    for err in bstack1l1l1l111_opy_:
      bstack11lll1ll_opy_ = {}
      for k in bstack1lllll1l1_opy_:
        val = CONFIG[bstack1lllllll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௘")][int(err[bstack1lllllll1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ௙")])].get(k)
        if val:
          bstack11lll1ll_opy_[k] = val
      bstack11lll1ll_opy_[bstack1lllllll1_opy_ (u"ࠪࡸࡪࡹࡴࡴࠩ௚")] = {
        err[bstack1lllllll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ௛")]: err[bstack1lllllll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ௜")]
      }
      bstack1l1ll1ll_opy_.append(bstack11lll1ll_opy_)
  except Exception as e:
    logger.debug(bstack1lllllll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨࡲࡶࡲࡧࡴࡵ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡀࠠࠨ௝") +str(e))
  finally:
    return bstack1l1ll1ll_opy_
def bstack11llll11_opy_():
  global bstack1ll1l_opy_
  global bstack1l111l111_opy_
  global bstack1lllll1ll_opy_
  if bstack1ll1l_opy_:
    logger.warning(bstack111lllll_opy_.format(str(bstack1ll1l_opy_)))
  logger.info(bstack111l11l1l_opy_)
  global bstack11l11l11l_opy_
  if bstack11l11l11l_opy_:
    bstack1lllll11l_opy_()
  try:
    for driver in bstack1l111l111_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack11llll111_opy_)
  bstack1l11lllll_opy_()
  if len(bstack1lllll1ll_opy_) > 0:
    message = bstack1l11l1l_opy_(bstack1lllll1ll_opy_)
    bstack1l11lllll_opy_(message)
  else:
    bstack1l11lllll_opy_()
def bstack11l1l11ll_opy_(self, *args):
  logger.error(bstack111ll111_opy_)
  bstack11llll11_opy_()
  sys.exit(1)
def bstack11l11_opy_(err):
  logger.critical(bstack1lll1l1l_opy_.format(str(err)))
  bstack1l11lllll_opy_(bstack1lll1l1l_opy_.format(str(err)))
  atexit.unregister(bstack11llll11_opy_)
  sys.exit(1)
def bstack1111111l_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1l11lllll_opy_(message)
  atexit.unregister(bstack11llll11_opy_)
  sys.exit(1)
def bstack1l1l1l1ll_opy_():
  global CONFIG
  global bstack11l111l1l_opy_
  global bstack111111l_opy_
  global bstack1l1111l11_opy_
  CONFIG = bstack1l1ll11l_opy_()
  bstack1l1l1111l_opy_()
  bstack1l11ll1_opy_()
  CONFIG = bstack1l1l11l1_opy_(CONFIG)
  update(CONFIG, bstack111111l_opy_)
  update(CONFIG, bstack11l111l1l_opy_)
  CONFIG = bstack1l1llll_opy_(CONFIG)
  if bstack1lllllll1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ௞") in CONFIG and str(CONFIG[bstack1lllllll1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ௟")]).lower() == bstack1lllllll1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ௠"):
    bstack1l1111l11_opy_ = False
  if (bstack1lllllll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭௡") in CONFIG and bstack1lllllll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ௢") in bstack11l111l1l_opy_) or (bstack1lllllll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ௣") in CONFIG and bstack1lllllll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ௤") not in bstack111111l_opy_):
    if os.getenv(bstack1lllllll1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫ௥")):
      CONFIG[bstack1lllllll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ௦")] = os.getenv(bstack1lllllll1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭௧"))
    else:
      bstack111ll1111_opy_()
  elif (bstack1lllllll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭௨") not in CONFIG and bstack1lllllll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭௩") in CONFIG) or (bstack1lllllll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ௪") in bstack111111l_opy_ and bstack1lllllll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ௫") not in bstack11l111l1l_opy_):
    del(CONFIG[bstack1lllllll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ௬")])
  if bstack11l1ll1l1_opy_(CONFIG):
    bstack11l11_opy_(bstack1ll11l1_opy_)
  bstack11llll1ll_opy_()
  bstack111l1lll1_opy_()
  if bstack1l11ll1l_opy_:
    CONFIG[bstack1lllllll1_opy_ (u"ࠨࡣࡳࡴࠬ௭")] = bstack1l11ll_opy_(CONFIG)
    logger.info(bstack1l1111ll_opy_.format(CONFIG[bstack1lllllll1_opy_ (u"ࠩࡤࡴࡵ࠭௮")]))
def bstack111l1lll1_opy_():
  global CONFIG
  global bstack1l11ll1l_opy_
  if bstack1lllllll1_opy_ (u"ࠪࡥࡵࡶࠧ௯") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1111111l_opy_(e, bstack1ll1111ll_opy_)
    bstack1l11ll1l_opy_ = True
def bstack1l11ll_opy_(config):
  bstack11lll1111_opy_ = bstack1lllllll1_opy_ (u"ࠫࠬ௰")
  app = config[bstack1lllllll1_opy_ (u"ࠬࡧࡰࡱࠩ௱")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack111lll_opy_:
      if os.path.exists(app):
        bstack11lll1111_opy_ = bstack1ll1l1111_opy_(config, app)
      elif bstack11lll11l_opy_(app):
        bstack11lll1111_opy_ = app
      else:
        bstack11l11_opy_(bstack11l1_opy_.format(app))
    else:
      if bstack11lll11l_opy_(app):
        bstack11lll1111_opy_ = app
      elif os.path.exists(app):
        bstack11lll1111_opy_ = bstack1ll1l1111_opy_(app)
      else:
        bstack11l11_opy_(bstack1l1l111_opy_)
  else:
    if len(app) > 2:
      bstack11l11_opy_(bstack111_opy_)
    elif len(app) == 2:
      if bstack1lllllll1_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ௲") in app and bstack1lllllll1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ௳") in app:
        if os.path.exists(app[bstack1lllllll1_opy_ (u"ࠨࡲࡤࡸ࡭࠭௴")]):
          bstack11lll1111_opy_ = bstack1ll1l1111_opy_(config, app[bstack1lllllll1_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ௵")], app[bstack1lllllll1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭௶")])
        else:
          bstack11l11_opy_(bstack11l1_opy_.format(app))
      else:
        bstack11l11_opy_(bstack111_opy_)
    else:
      for key in app:
        if key in bstack11ll11l11_opy_:
          if key == bstack1lllllll1_opy_ (u"ࠫࡵࡧࡴࡩࠩ௷"):
            if os.path.exists(app[key]):
              bstack11lll1111_opy_ = bstack1ll1l1111_opy_(config, app[key])
            else:
              bstack11l11_opy_(bstack11l1_opy_.format(app))
          else:
            bstack11lll1111_opy_ = app[key]
        else:
          bstack11l11_opy_(bstack11l1l_opy_)
  return bstack11lll1111_opy_
def bstack11lll11l_opy_(bstack11lll1111_opy_):
  import re
  bstack1l1111l1_opy_ = re.compile(bstack1lllllll1_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧ௸"))
  bstack11111lll_opy_ = re.compile(bstack1lllllll1_opy_ (u"ࡸࠢ࡟࡝ࡤ࠱ࡿࡇ࡛࠭࠲࠰࠽ࡡࡥ࠮࡝࠯ࡠ࠮࠴ࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥ௹"))
  if bstack1lllllll1_opy_ (u"ࠧࡣࡵ࠽࠳࠴࠭௺") in bstack11lll1111_opy_ or re.fullmatch(bstack1l1111l1_opy_, bstack11lll1111_opy_) or re.fullmatch(bstack11111lll_opy_, bstack11lll1111_opy_):
    return True
  else:
    return False
def bstack1ll1l1111_opy_(config, path, bstack111l1_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1lllllll1_opy_ (u"ࠨࡴࡥࠫ௻")).read()).hexdigest()
  bstack11ll1111_opy_ = bstack1l1l11lll_opy_(md5_hash)
  bstack11lll1111_opy_ = None
  if bstack11ll1111_opy_:
    logger.info(bstack1ll1l1_opy_.format(bstack11ll1111_opy_, md5_hash))
    return bstack11ll1111_opy_
  bstack1ll11l111_opy_ = MultipartEncoder(
    fields={
        bstack1lllllll1_opy_ (u"ࠩࡩ࡭ࡱ࡫ࠧ௼"): (os.path.basename(path), open(os.path.abspath(path), bstack1lllllll1_opy_ (u"ࠪࡶࡧ࠭௽")), bstack1lllllll1_opy_ (u"ࠫࡹ࡫ࡸࡵ࠱ࡳࡰࡦ࡯࡮ࠨ௾")),
        bstack1lllllll1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ௿"): bstack111l1_opy_
    }
  )
  response = requests.post(bstack1ll11l1l1_opy_, data=bstack1ll11l111_opy_,
                         headers={bstack1lllllll1_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬఀ"): bstack1ll11l111_opy_.content_type}, auth=(config[bstack1lllllll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩఁ")], config[bstack1lllllll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫం")]))
  try:
    res = json.loads(response.text)
    bstack11lll1111_opy_ = res[bstack1lllllll1_opy_ (u"ࠩࡤࡴࡵࡥࡵࡳ࡮ࠪః")]
    logger.info(bstack11l11l1l1_opy_.format(bstack11lll1111_opy_))
    bstack11lll11_opy_(md5_hash, bstack11lll1111_opy_)
  except ValueError as err:
    bstack11l11_opy_(bstack11lllll1_opy_.format(str(err)))
  return bstack11lll1111_opy_
def bstack11llll1ll_opy_():
  global CONFIG
  global bstack1ll111l_opy_
  bstack1111l11_opy_ = 0
  bstack1ll1l1l1l_opy_ = 1
  if bstack1lllllll1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪఄ") in CONFIG:
    bstack1ll1l1l1l_opy_ = CONFIG[bstack1lllllll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫఅ")]
  if bstack1lllllll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨఆ") in CONFIG:
    bstack1111l11_opy_ = len(CONFIG[bstack1lllllll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩఇ")])
  bstack1ll111l_opy_ = int(bstack1ll1l1l1l_opy_) * int(bstack1111l11_opy_)
def bstack1l1l11lll_opy_(md5_hash):
  bstack111l_opy_ = os.path.join(os.path.expanduser(bstack1lllllll1_opy_ (u"ࠧࡿࠩఈ")), bstack1lllllll1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨఉ"), bstack1lllllll1_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪఊ"))
  if os.path.exists(bstack111l_opy_):
    bstack11ll111_opy_ = json.load(open(bstack111l_opy_,bstack1lllllll1_opy_ (u"ࠪࡶࡧ࠭ఋ")))
    if md5_hash in bstack11ll111_opy_:
      bstack1lll1ll1l_opy_ = bstack11ll111_opy_[md5_hash]
      bstack1l1111l_opy_ = datetime.datetime.now()
      bstack1l11111ll_opy_ = datetime.datetime.strptime(bstack1lll1ll1l_opy_[bstack1lllllll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧఌ")], bstack1lllllll1_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ఍"))
      if (bstack1l1111l_opy_ - bstack1l11111ll_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1lll1ll1l_opy_[bstack1lllllll1_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫఎ")]):
        return None
      return bstack1lll1ll1l_opy_[bstack1lllllll1_opy_ (u"ࠧࡪࡦࠪఏ")]
  else:
    return None
def bstack11lll11_opy_(md5_hash, bstack11lll1111_opy_):
  bstack111l1lll_opy_ = os.path.join(os.path.expanduser(bstack1lllllll1_opy_ (u"ࠨࢀࠪఐ")), bstack1lllllll1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ఑"))
  if not os.path.exists(bstack111l1lll_opy_):
    os.makedirs(bstack111l1lll_opy_)
  bstack111l_opy_ = os.path.join(os.path.expanduser(bstack1lllllll1_opy_ (u"ࠪࢂࠬఒ")), bstack1lllllll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫఓ"), bstack1lllllll1_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭ఔ"))
  bstack1ll1ll11_opy_ = {
    bstack1lllllll1_opy_ (u"࠭ࡩࡥࠩక"): bstack11lll1111_opy_,
    bstack1lllllll1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪఖ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1lllllll1_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬగ")),
    bstack1lllllll1_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧఘ"): str(__version__)
  }
  if os.path.exists(bstack111l_opy_):
    bstack11ll111_opy_ = json.load(open(bstack111l_opy_,bstack1lllllll1_opy_ (u"ࠪࡶࡧ࠭ఙ")))
  else:
    bstack11ll111_opy_ = {}
  bstack11ll111_opy_[md5_hash] = bstack1ll1ll11_opy_
  with open(bstack111l_opy_, bstack1lllllll1_opy_ (u"ࠦࡼ࠱ࠢచ")) as outfile:
    json.dump(bstack11ll111_opy_, outfile)
def bstack1l1ll1_opy_(self):
  return
def bstack11ll1l1_opy_(self):
  return
def bstack11l111l1_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack11l1l1_opy_(self):
  global bstack111111l1_opy_
  global bstack11lllllll_opy_
  global bstack1l11l1l1l_opy_
  try:
    if bstack1lllllll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬఛ") in bstack111111l1_opy_ and self.session_id != None:
      bstack11l1lllll_opy_ = bstack1lllllll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭జ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1lllllll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧఝ")
      bstack11llll1_opy_ = bstack1111l1l1_opy_(bstack1lllllll1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫఞ"), bstack1lllllll1_opy_ (u"ࠩࠪట"), bstack11l1lllll_opy_, bstack1lllllll1_opy_ (u"ࠪ࠰ࠥ࠭ఠ").join(threading.current_thread().bstackTestErrorMessages), bstack1lllllll1_opy_ (u"ࠫࠬడ"), bstack1lllllll1_opy_ (u"ࠬ࠭ఢ"))
      if self != None:
        self.execute_script(bstack11llll1_opy_)
  except Exception as e:
    logger.info(bstack1lllllll1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࠢణ") + str(e))
  bstack1l11l1l1l_opy_(self)
  self.session_id = None
def bstack1l1l11l1l_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack11lllllll_opy_
  global bstack111l11l_opy_
  global bstack1l1l1l1l1_opy_
  global bstack1ll1l1ll_opy_
  global bstack11l11l1l_opy_
  global bstack111111l1_opy_
  global bstack11l1llll1_opy_
  global bstack1l111l111_opy_
  global bstack11ll1l111_opy_
  CONFIG[bstack1lllllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩత")] = str(bstack111111l1_opy_) + str(__version__)
  command_executor = bstack1111lll1_opy_()
  logger.debug(bstack11ll1lll_opy_.format(command_executor))
  proxy = bstack111l11l1_opy_(CONFIG, proxy)
  bstack111l1ll_opy_ = 0 if bstack111l11l_opy_ < 0 else bstack111l11l_opy_
  try:
    if bstack1ll1l1ll_opy_ is True:
      bstack111l1ll_opy_ = int(multiprocessing.current_process().name)
    elif bstack11l11l1l_opy_ is True:
      bstack111l1ll_opy_ = int(threading.current_thread().name)
  except:
    bstack111l1ll_opy_ = 0
  bstack11l111_opy_ = bstack1ll11lll1_opy_(CONFIG, bstack111l1ll_opy_)
  logger.debug(bstack1ll1lll11_opy_.format(str(bstack11l111_opy_)))
  if bstack1lllllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬథ") in CONFIG and CONFIG[bstack1lllllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ద")]:
    bstack11111_opy_(bstack11l111_opy_)
  if desired_capabilities:
    bstack11lll1_opy_ = bstack1l1l11l1_opy_(desired_capabilities)
    bstack11lll1_opy_[bstack1lllllll1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪధ")] = bstack1ll1ll111_opy_(CONFIG)
    bstack1l11lll_opy_ = bstack1ll11lll1_opy_(bstack11lll1_opy_)
    if bstack1l11lll_opy_:
      bstack11l111_opy_ = update(bstack1l11lll_opy_, bstack11l111_opy_)
    desired_capabilities = None
  if options:
    bstack1l1111_opy_(options, bstack11l111_opy_)
  if not options:
    options = bstack1llll11l1_opy_(bstack11l111_opy_)
  if proxy and bstack1ll11l1l_opy_() >= version.parse(bstack1lllllll1_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫన")):
    options.proxy(proxy)
  if options and bstack1ll11l1l_opy_() >= version.parse(bstack1lllllll1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ఩")):
    desired_capabilities = None
  if (
      not options and not desired_capabilities
  ) or (
      bstack1ll11l1l_opy_() < version.parse(bstack1lllllll1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬప")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11l111_opy_)
  logger.info(bstack1l111_opy_)
  if bstack1ll11l1l_opy_() >= version.parse(bstack1lllllll1_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧఫ")):
    bstack11l1llll1_opy_(self, command_executor=command_executor,
          options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1ll11l1l_opy_() >= version.parse(bstack1lllllll1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧబ")):
    bstack11l1llll1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1ll11l1l_opy_() >= version.parse(bstack1lllllll1_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩభ")):
    bstack11l1llll1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack11l1llll1_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  try:
    bstack1ll1ll1ll_opy_ = bstack1lllllll1_opy_ (u"ࠪࠫమ")
    if bstack1ll11l1l_opy_() >= version.parse(bstack1lllllll1_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬయ")):
      bstack1ll1ll1ll_opy_ = self.caps.get(bstack1lllllll1_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧర"))
    else:
      bstack1ll1ll1ll_opy_ = self.capabilities.get(bstack1lllllll1_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨఱ"))
    if bstack1ll1ll1ll_opy_:
      if bstack1ll11l1l_opy_() <= version.parse(bstack1lllllll1_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧల")):
        self.command_executor._url = bstack1lllllll1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤళ") + bstack1ll111l11_opy_ + bstack1lllllll1_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨఴ")
      else:
        self.command_executor._url = bstack1lllllll1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧవ") + bstack1ll1ll1ll_opy_ + bstack1lllllll1_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧశ")
      logger.debug(bstack11l111lll_opy_.format(bstack1ll1ll1ll_opy_))
    else:
      logger.debug(bstack1l1ll11ll_opy_.format(bstack1lllllll1_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨష")))
  except Exception as e:
    logger.debug(bstack1l1ll11ll_opy_.format(e))
  if bstack1lllllll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬస") in bstack111111l1_opy_:
    bstack1l111l11_opy_(bstack111l11l_opy_, bstack11ll1l111_opy_)
  bstack11lllllll_opy_ = self.session_id
  if bstack1lllllll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧహ") in bstack111111l1_opy_:
    threading.current_thread().bstack1111111_opy_ = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1l111l111_opy_.append(self)
  if bstack1lllllll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ఺") in CONFIG and bstack1lllllll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ఻") in CONFIG[bstack1lllllll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ఼࠭")][bstack111l1ll_opy_]:
    bstack1l1l1l1l1_opy_ = CONFIG[bstack1lllllll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧఽ")][bstack111l1ll_opy_][bstack1lllllll1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪా")]
  logger.debug(bstack1ll11l_opy_.format(bstack11lllllll_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack111lllll1_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack111l1l_opy_
      if(bstack1lllllll1_opy_ (u"ࠨࡩ࡯ࡦࡨࡼ࠳ࡰࡳࠣి") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1lllllll1_opy_ (u"ࠧࡿࠩీ")), bstack1lllllll1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨు"), bstack1lllllll1_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫూ")), bstack1lllllll1_opy_ (u"ࠪࡻࠬృ")) as fp:
          fp.write(bstack1lllllll1_opy_ (u"ࠦࠧౄ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1lllllll1_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢ౅")))):
          with open(args[1], bstack1lllllll1_opy_ (u"࠭ࡲࠨె")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1lllllll1_opy_ (u"ࠧࡢࡵࡼࡲࡨࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡡࡱࡩࡼࡖࡡࡨࡧࠫࡧࡴࡴࡴࡦࡺࡷ࠰ࠥࡶࡡࡨࡧࠣࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮࠭ే") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l111l1l1_opy_)
            lines.insert(1, bstack111ll1l_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1lllllll1_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥై")), bstack1lllllll1_opy_ (u"ࠩࡺࠫ౉")) as bstack1l111l_opy_:
              bstack1l111l_opy_.writelines(lines)
        CONFIG[bstack1lllllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬొ")] = str(bstack111111l1_opy_) + str(__version__)
        bstack111l1ll_opy_ = 0 if bstack111l11l_opy_ < 0 else bstack111l11l_opy_
        if bstack1ll1l1ll_opy_ is True:
          bstack111l1ll_opy_ = int(threading.current_thread().getName())
        CONFIG[bstack1lllllll1_opy_ (u"ࠦࡺࡹࡥࡘ࠵ࡆࠦో")] = False
        CONFIG[bstack1lllllll1_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦౌ")] = True
        bstack11l111_opy_ = bstack1ll11lll1_opy_(CONFIG, bstack111l1ll_opy_)
        logger.debug(bstack1ll1lll11_opy_.format(str(bstack11l111_opy_)))
        if CONFIG[bstack1lllllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮్ࠪ")]:
          bstack11111_opy_(bstack11l111_opy_)
        if bstack1lllllll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ౎") in CONFIG and bstack1lllllll1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭౏") in CONFIG[bstack1lllllll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౐")][bstack111l1ll_opy_]:
          bstack1l1l1l1l1_opy_ = CONFIG[bstack1lllllll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭౑")][bstack111l1ll_opy_][bstack1lllllll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ౒")]
        args.append(os.path.join(os.path.expanduser(bstack1lllllll1_opy_ (u"ࠬࢄࠧ౓")), bstack1lllllll1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭౔"), bstack1lllllll1_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵౕࠩ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11l111_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1lllllll1_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵౖࠥ"))
      bstack111l1l_opy_ = True
      return bstack1l1ll1l1_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1lll11_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack11lllllll_opy_
    global bstack111l11l_opy_
    global bstack1l1l1l1l1_opy_
    global bstack1ll1l1ll_opy_
    global bstack111111l1_opy_
    global bstack11l1llll1_opy_
    CONFIG[bstack1lllllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ౗")] = str(bstack111111l1_opy_) + str(__version__)
    bstack111l1ll_opy_ = 0 if bstack111l11l_opy_ < 0 else bstack111l11l_opy_
    if bstack1ll1l1ll_opy_ is True:
      bstack111l1ll_opy_ = int(threading.current_thread().getName())
    CONFIG[bstack1lllllll1_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤౘ")] = True
    bstack11l111_opy_ = bstack1ll11lll1_opy_(CONFIG, bstack111l1ll_opy_)
    logger.debug(bstack1ll1lll11_opy_.format(str(bstack11l111_opy_)))
    if CONFIG[bstack1lllllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨౙ")]:
      bstack11111_opy_(bstack11l111_opy_)
    if bstack1lllllll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨౚ") in CONFIG and bstack1lllllll1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ౛") in CONFIG[bstack1lllllll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ౜")][bstack111l1ll_opy_]:
      bstack1l1l1l1l1_opy_ = CONFIG[bstack1lllllll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫౝ")][bstack111l1ll_opy_][bstack1lllllll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ౞")]
    import urllib
    import json
    bstack11llll11l_opy_ = bstack1lllllll1_opy_ (u"ࠪࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠬ౟") + urllib.parse.quote(json.dumps(bstack11l111_opy_))
    browser = self.connect(bstack11llll11l_opy_)
    return browser
except Exception as e:
    pass
def bstack11l1lll1_opy_():
    global bstack111l1l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1lll11_opy_
        bstack111l1l_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack111lllll1_opy_
      bstack111l1l_opy_ = True
    except Exception as e:
      pass
def bstack111l1l1l_opy_(context, bstack1ll1111_opy_):
  try:
    context.page.evaluate(bstack1lllllll1_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧౠ"), bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠩౡ")+ json.dumps(bstack1ll1111_opy_) + bstack1lllllll1_opy_ (u"ࠨࡽࡾࠤౢ"))
  except Exception as e:
    logger.debug(bstack1lllllll1_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧౣ"), e)
def bstack1111ll1l_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1lllllll1_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ౤"), bstack1lllllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ౥") + json.dumps(message) + bstack1lllllll1_opy_ (u"ࠪ࠰ࠧࡲࡥࡷࡧ࡯ࠦ࠿࠭౦") + json.dumps(level) + bstack1lllllll1_opy_ (u"ࠫࢂࢃࠧ౧"))
  except Exception as e:
    logger.debug(bstack1lllllll1_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࢁࡽࠣ౨"), e)
def bstack1ll1lll1l_opy_(context, status, message = bstack1lllllll1_opy_ (u"ࠨࠢ౩")):
  try:
    if(status == bstack1lllllll1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ౪")):
      context.page.evaluate(bstack1lllllll1_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ౫"), bstack1lllllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡴࡨࡥࡸࡵ࡮ࠣ࠼ࠪ౬") + json.dumps(bstack1lllllll1_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࠧ౭") + str(message)) + bstack1lllllll1_opy_ (u"ࠫ࠱ࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠨ౮") + json.dumps(status) + bstack1lllllll1_opy_ (u"ࠧࢃࡽࠣ౯"))
    else:
      context.page.evaluate(bstack1lllllll1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ౰"), bstack1lllllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠨ౱") + json.dumps(status) + bstack1lllllll1_opy_ (u"ࠣࡿࢀࠦ౲"))
  except Exception as e:
    logger.debug(bstack1lllllll1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡿࢂࠨ౳"), e)
def bstack111lll11_opy_(self, url):
  global bstack111l11ll1_opy_
  try:
    bstack1l1l1lll1_opy_(url)
  except Exception as err:
    logger.debug(bstack11ll1ll_opy_.format(str(err)))
  try:
    bstack111l11ll1_opy_(self, url)
  except Exception as e:
    try:
      bstack11lll1l1l_opy_ = str(e)
      if any(err_msg in bstack11lll1l1l_opy_ for err_msg in bstack1l11l1ll_opy_):
        bstack1l1l1lll1_opy_(url, True)
    except Exception as err:
      logger.debug(bstack11ll1ll_opy_.format(str(err)))
    raise e
def bstack1l11l1lll_opy_(self):
  global bstack1l11l11l1_opy_
  bstack1l11l11l1_opy_ = self
  return
def bstack11lllll11_opy_(self):
  global bstack1lll1_opy_
  bstack1lll1_opy_ = self
  return
def bstack1lll11111_opy_(self, test):
  global CONFIG
  global bstack1lll1_opy_
  global bstack1l11l11l1_opy_
  global bstack11lllllll_opy_
  global bstack11111l11_opy_
  global bstack1l1l1l1l1_opy_
  global bstack111ll11ll_opy_
  global bstack111llll11_opy_
  global bstack1lll1ll1_opy_
  global bstack1l111l111_opy_
  try:
    if not bstack11lllllll_opy_:
      with open(os.path.join(os.path.expanduser(bstack1lllllll1_opy_ (u"ࠪࢂࠬ౴")), bstack1lllllll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ౵"), bstack1lllllll1_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧ౶"))) as f:
        bstack1l1111lll_opy_ = json.loads(bstack1lllllll1_opy_ (u"ࠨࡻࠣ౷") + f.read().strip() + bstack1lllllll1_opy_ (u"ࠧࠣࡺࠥ࠾ࠥࠨࡹࠣࠩ౸") + bstack1lllllll1_opy_ (u"ࠣࡿࠥ౹"))
        bstack11lllllll_opy_ = bstack1l1111lll_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1l111l111_opy_:
    for driver in bstack1l111l111_opy_:
      if bstack11lllllll_opy_ == driver.session_id:
        if test:
          bstack1111l1_opy_ = str(test.data)
        if not bstack1llll1lll_opy_ and bstack1111l1_opy_:
          bstack11llll1l_opy_ = {
            bstack1lllllll1_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩ౺"): bstack1lllllll1_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ౻"),
            bstack1lllllll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ౼"): {
              bstack1lllllll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ౽"): bstack1111l1_opy_
            }
          }
          bstack1lll1l111_opy_ = bstack1lllllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ౾").format(json.dumps(bstack11llll1l_opy_))
          driver.execute_script(bstack1lll1l111_opy_)
        if bstack11111l11_opy_:
          bstack111ll1_opy_ = {
            bstack1lllllll1_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧ౿"): bstack1lllllll1_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪಀ"),
            bstack1lllllll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬಁ"): {
              bstack1lllllll1_opy_ (u"ࠪࡨࡦࡺࡡࠨಂ"): bstack1111l1_opy_ + bstack1lllllll1_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭ಃ"),
              bstack1lllllll1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ಄"): bstack1lllllll1_opy_ (u"࠭ࡩ࡯ࡨࡲࠫಅ")
            }
          }
          bstack11llll1l_opy_ = {
            bstack1lllllll1_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧಆ"): bstack1lllllll1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫಇ"),
            bstack1lllllll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬಈ"): {
              bstack1lllllll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪಉ"): bstack1lllllll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫಊ")
            }
          }
          if bstack11111l11_opy_.status == bstack1lllllll1_opy_ (u"ࠬࡖࡁࡔࡕࠪಋ"):
            bstack1ll1lll1_opy_ = bstack1lllllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫಌ").format(json.dumps(bstack111ll1_opy_))
            driver.execute_script(bstack1ll1lll1_opy_)
            bstack1lll1l111_opy_ = bstack1lllllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ಍").format(json.dumps(bstack11llll1l_opy_))
            driver.execute_script(bstack1lll1l111_opy_)
          elif bstack11111l11_opy_.status == bstack1lllllll1_opy_ (u"ࠨࡈࡄࡍࡑ࠭ಎ"):
            reason = bstack1lllllll1_opy_ (u"ࠤࠥಏ")
            bstack1l1ll111_opy_ = bstack1111l1_opy_ + bstack1lllllll1_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠫಐ")
            if bstack11111l11_opy_.message:
              reason = str(bstack11111l11_opy_.message)
              bstack1l1ll111_opy_ = bstack1l1ll111_opy_ + bstack1lllllll1_opy_ (u"ࠫࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠫ಑") + reason
            bstack111ll1_opy_[bstack1lllllll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨಒ")] = {
              bstack1lllllll1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬಓ"): bstack1lllllll1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ಔ"),
              bstack1lllllll1_opy_ (u"ࠨࡦࡤࡸࡦ࠭ಕ"): bstack1l1ll111_opy_
            }
            bstack11llll1l_opy_[bstack1lllllll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬಖ")] = {
              bstack1lllllll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪಗ"): bstack1lllllll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫಘ"),
              bstack1lllllll1_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬಙ"): reason
            }
            bstack1ll1lll1_opy_ = bstack1lllllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫಚ").format(json.dumps(bstack111ll1_opy_))
            driver.execute_script(bstack1ll1lll1_opy_)
            bstack1lll1l111_opy_ = bstack1lllllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬಛ").format(json.dumps(bstack11llll1l_opy_))
            driver.execute_script(bstack1lll1l111_opy_)
  elif bstack11lllllll_opy_:
    try:
      data = {}
      bstack1111l1_opy_ = None
      if test:
        bstack1111l1_opy_ = str(test.data)
      if not bstack1llll1lll_opy_ and bstack1111l1_opy_:
        data[bstack1lllllll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ಜ")] = bstack1111l1_opy_
      if bstack11111l11_opy_:
        if bstack11111l11_opy_.status == bstack1lllllll1_opy_ (u"ࠩࡓࡅࡘ࡙ࠧಝ"):
          data[bstack1lllllll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪಞ")] = bstack1lllllll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫಟ")
        elif bstack11111l11_opy_.status == bstack1lllllll1_opy_ (u"ࠬࡌࡁࡊࡎࠪಠ"):
          data[bstack1lllllll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ಡ")] = bstack1lllllll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧಢ")
          if bstack11111l11_opy_.message:
            data[bstack1lllllll1_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨಣ")] = str(bstack11111l11_opy_.message)
      user = CONFIG[bstack1lllllll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫತ")]
      key = CONFIG[bstack1lllllll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ಥ")]
      url = bstack1lllllll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠰ࡽࢀ࠲࡯ࡹ࡯࡯ࠩದ").format(user, key, bstack11lllllll_opy_)
      headers = {
        bstack1lllllll1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫಧ"): bstack1lllllll1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩನ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1ll11111l_opy_.format(str(e)))
  if bstack1lll1_opy_:
    bstack111llll11_opy_(bstack1lll1_opy_)
  if bstack1l11l11l1_opy_:
    bstack1lll1ll1_opy_(bstack1l11l11l1_opy_)
  bstack111ll11ll_opy_(self, test)
def bstack11l11111_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1l1l11ll_opy_
  bstack1l1l11ll_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11111l11_opy_
  bstack11111l11_opy_ = self._test
def bstack1ll1ll1l_opy_():
  global bstack11ll11l_opy_
  try:
    if os.path.exists(bstack11ll11l_opy_):
      os.remove(bstack11ll11l_opy_)
  except Exception as e:
    logger.debug(bstack1lllllll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪ಩") + str(e))
def bstack11l1ll111_opy_():
  global bstack11ll11l_opy_
  bstack11lllll_opy_ = {}
  try:
    if not os.path.isfile(bstack11ll11l_opy_):
      with open(bstack11ll11l_opy_, bstack1lllllll1_opy_ (u"ࠨࡹࠪಪ")):
        pass
      with open(bstack11ll11l_opy_, bstack1lllllll1_opy_ (u"ࠤࡺ࠯ࠧಫ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack11ll11l_opy_):
      bstack11lllll_opy_ = json.load(open(bstack11ll11l_opy_, bstack1lllllll1_opy_ (u"ࠪࡶࡧ࠭ಬ")))
  except Exception as e:
    logger.debug(bstack1lllllll1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ಭ") + str(e))
  finally:
    return bstack11lllll_opy_
def bstack1l111l11_opy_(platform_index, item_index):
  global bstack11ll11l_opy_
  try:
    bstack11lllll_opy_ = bstack11l1ll111_opy_()
    bstack11lllll_opy_[item_index] = platform_index
    with open(bstack11ll11l_opy_, bstack1lllllll1_opy_ (u"ࠧࡽࠫࠣಮ")) as outfile:
      json.dump(bstack11lllll_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1lllllll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡹࡵ࡭ࡹ࡯࡮ࡨࠢࡷࡳࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫಯ") + str(e))
def bstack11ll11ll_opy_(bstack1l1l11l11_opy_):
  global CONFIG
  bstack111l11lll_opy_ = bstack1lllllll1_opy_ (u"ࠧࠨರ")
  if not bstack1lllllll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫಱ") in CONFIG:
    logger.info(bstack1lllllll1_opy_ (u"ࠩࡑࡳࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠡࡲࡤࡷࡸ࡫ࡤࠡࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡲࡦࡲࡲࡶࡹࠦࡦࡰࡴࠣࡖࡴࡨ࡯ࡵࠢࡵࡹࡳ࠭ಲ"))
  try:
    platform = CONFIG[bstack1lllllll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ಳ")][bstack1l1l11l11_opy_]
    if bstack1lllllll1_opy_ (u"ࠫࡴࡹࠧ಴") in platform:
      bstack111l11lll_opy_ += str(platform[bstack1lllllll1_opy_ (u"ࠬࡵࡳࠨವ")]) + bstack1lllllll1_opy_ (u"࠭ࠬࠡࠩಶ")
    if bstack1lllllll1_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪಷ") in platform:
      bstack111l11lll_opy_ += str(platform[bstack1lllllll1_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫಸ")]) + bstack1lllllll1_opy_ (u"ࠩ࠯ࠤࠬಹ")
    if bstack1lllllll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ಺") in platform:
      bstack111l11lll_opy_ += str(platform[bstack1lllllll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ಻")]) + bstack1lllllll1_opy_ (u"ࠬ࠲ࠠࠨ಼")
    if bstack1lllllll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨಽ") in platform:
      bstack111l11lll_opy_ += str(platform[bstack1lllllll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩಾ")]) + bstack1lllllll1_opy_ (u"ࠨ࠮ࠣࠫಿ")
    if bstack1lllllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧೀ") in platform:
      bstack111l11lll_opy_ += str(platform[bstack1lllllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨು")]) + bstack1lllllll1_opy_ (u"ࠫ࠱ࠦࠧೂ")
    if bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ೃ") in platform:
      bstack111l11lll_opy_ += str(platform[bstack1lllllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧೄ")]) + bstack1lllllll1_opy_ (u"ࠧ࠭ࠢࠪ೅")
  except Exception as e:
    logger.debug(bstack1lllllll1_opy_ (u"ࠨࡕࡲࡱࡪࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡷ࡫ࡰࡰࡴࡷࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡵ࡮ࠨೆ") + str(e))
  finally:
    if bstack111l11lll_opy_[len(bstack111l11lll_opy_) - 2:] == bstack1lllllll1_opy_ (u"ࠩ࠯ࠤࠬೇ"):
      bstack111l11lll_opy_ = bstack111l11lll_opy_[:-2]
    return bstack111l11lll_opy_
def bstack11l11l_opy_(path, bstack111l11lll_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1111l_opy_ = ET.parse(path)
    bstack11l11l1_opy_ = bstack1111l_opy_.getroot()
    bstack1llllllll_opy_ = None
    for suite in bstack11l11l1_opy_.iter(bstack1lllllll1_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩೈ")):
      if bstack1lllllll1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ೉") in suite.attrib:
        suite.attrib[bstack1lllllll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪೊ")] += bstack1lllllll1_opy_ (u"࠭ࠠࠨೋ") + bstack111l11lll_opy_
        bstack1llllllll_opy_ = suite
    bstack1l11l_opy_ = None
    for robot in bstack11l11l1_opy_.iter(bstack1lllllll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ೌ")):
      bstack1l11l_opy_ = robot
    bstack1l1lllll_opy_ = len(bstack1l11l_opy_.findall(bstack1lllllll1_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫್ࠧ")))
    if bstack1l1lllll_opy_ == 1:
      bstack1l11l_opy_.remove(bstack1l11l_opy_.findall(bstack1lllllll1_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ೎"))[0])
      bstack1ll1l11_opy_ = ET.Element(bstack1lllllll1_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩ೏"), attrib={bstack1lllllll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ೐"):bstack1lllllll1_opy_ (u"࡙ࠬࡵࡪࡶࡨࡷࠬ೑"), bstack1lllllll1_opy_ (u"࠭ࡩࡥࠩ೒"):bstack1lllllll1_opy_ (u"ࠧࡴ࠲ࠪ೓")})
      bstack1l11l_opy_.insert(1, bstack1ll1l11_opy_)
      bstack11l1lll1l_opy_ = None
      for suite in bstack1l11l_opy_.iter(bstack1lllllll1_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ೔")):
        bstack11l1lll1l_opy_ = suite
      bstack11l1lll1l_opy_.append(bstack1llllllll_opy_)
      bstack11l1llll_opy_ = None
      for status in bstack1llllllll_opy_.iter(bstack1lllllll1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩೕ")):
        bstack11l1llll_opy_ = status
      bstack11l1lll1l_opy_.append(bstack11l1llll_opy_)
    bstack1111l_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1lllllll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡳࡵ࡬ࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠨೖ") + str(e))
def bstack11l111ll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l1ll1l_opy_
  global CONFIG
  if bstack1lllllll1_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣ೗") in options:
    del options[bstack1lllllll1_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤ೘")]
  bstack111lll1l1_opy_ = bstack11l1ll111_opy_()
  for bstack1lllll_opy_ in bstack111lll1l1_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1lllllll1_opy_ (u"࠭ࡰࡢࡤࡲࡸࡤࡸࡥࡴࡷ࡯ࡸࡸ࠭೙"), str(bstack1lllll_opy_), bstack1lllllll1_opy_ (u"ࠧࡰࡷࡷࡴࡺࡺ࠮ࡹ࡯࡯ࠫ೚"))
    bstack11l11l_opy_(path, bstack11ll11ll_opy_(bstack111lll1l1_opy_[bstack1lllll_opy_]))
  bstack1ll1ll1l_opy_()
  return bstack1l1ll1l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack11l111ll_opy_(self, ff_profile_dir):
  global bstack1111l11l_opy_
  if not ff_profile_dir:
    return None
  return bstack1111l11l_opy_(self, ff_profile_dir)
def bstack1lll_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1lll11l1l_opy_
  bstack111ll11l1_opy_ = []
  if bstack1lllllll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ೛") in CONFIG:
    bstack111ll11l1_opy_ = CONFIG[bstack1lllllll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ೜")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1lllllll1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦೝ")],
      pabot_args[bstack1lllllll1_opy_ (u"ࠦࡻ࡫ࡲࡣࡱࡶࡩࠧೞ")],
      argfile,
      pabot_args.get(bstack1lllllll1_opy_ (u"ࠧ࡮ࡩࡷࡧࠥ೟")),
      pabot_args[bstack1lllllll1_opy_ (u"ࠨࡰࡳࡱࡦࡩࡸࡹࡥࡴࠤೠ")],
      platform[0],
      bstack1lll11l1l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1lllllll1_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡨ࡬ࡰࡪࡹࠢೡ")] or [(bstack1lllllll1_opy_ (u"ࠣࠤೢ"), None)]
    for platform in enumerate(bstack111ll11l1_opy_)
  ]
def bstack1lll1111l_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack11l11ll11_opy_=bstack1lllllll1_opy_ (u"ࠩࠪೣ")):
  global bstack11l11lll_opy_
  self.platform_index = platform_index
  self.bstack11_opy_ = bstack11l11ll11_opy_
  bstack11l11lll_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack111l1111_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l1lll111_opy_
  global bstack111l11l11_opy_
  if not bstack1lllllll1_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ೤") in item.options:
    item.options[bstack1lllllll1_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭೥")] = []
  for v in item.options[bstack1lllllll1_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ೦")]:
    if bstack1lllllll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬ೧") in v:
      item.options[bstack1lllllll1_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ೨")].remove(v)
    if bstack1lllllll1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨ೩") in v:
      item.options[bstack1lllllll1_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ೪")].remove(v)
  item.options[bstack1lllllll1_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ೫")].insert(0, bstack1lllllll1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚࠽ࡿࢂ࠭೬").format(item.platform_index))
  item.options[bstack1lllllll1_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ೭")].insert(0, bstack1lllllll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔ࠽ࡿࢂ࠭೮").format(item.bstack11_opy_))
  if bstack111l11l11_opy_:
    item.options[bstack1lllllll1_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ೯")].insert(0, bstack1lllllll1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓ࠻ࡽࢀࠫ೰").format(bstack111l11l11_opy_))
  return bstack1l1lll111_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1lll11l1_opy_(command, item_index):
  global bstack111l11l11_opy_
  if bstack111l11l11_opy_:
    command[0] = command[0].replace(bstack1lllllll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨೱ"), bstack1lllllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽࠦࠧೲ") + str(item_index) + bstack1lllllll1_opy_ (u"ࠫࠥ࠭ೳ") + bstack111l11l11_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1lllllll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ೴"), bstack1lllllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠣ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠪ೵") + str(item_index), 1)
def bstack1l1l1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1_opy_
  bstack1lll11l1_opy_(command, item_index)
  return bstack1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack11l11l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1_opy_
  bstack1lll11l1_opy_(command, item_index)
  return bstack1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1lll1111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1_opy_
  bstack1lll11l1_opy_(command, item_index)
  return bstack1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1lll111l_opy_(self, runner, quiet=False, capture=True):
  global bstack1l11111_opy_
  bstack11l1111l_opy_ = bstack1l11111_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack1lllllll1_opy_ (u"ࠧࡦࡺࡦࡩࡵࡺࡩࡰࡰࡢࡥࡷࡸࠧ೶")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1lllllll1_opy_ (u"ࠨࡧࡻࡧࡤࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࡠࡣࡵࡶࠬ೷")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack11l1111l_opy_
def bstack11l11ll1_opy_(self, name, context, *args):
  global bstack1ll1111l_opy_
  if name in [bstack1lllllll1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠪ೸"), bstack1lllllll1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ೹")]:
    bstack1ll1111l_opy_(self, name, context, *args)
  if name == bstack1lllllll1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ೺"):
    try:
      if(not bstack1llll1lll_opy_):
        bstack1ll1111_opy_ = str(self.feature.name)
        bstack111l1l1l_opy_(context, bstack1ll1111_opy_)
        context.browser.execute_script(bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ೻") + json.dumps(bstack1ll1111_opy_) + bstack1lllllll1_opy_ (u"࠭ࡽࡾࠩ೼"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack1lllllll1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ೽").format(str(e)))
  if name == bstack1lllllll1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ೾"):
    try:
      if not hasattr(self, bstack1lllllll1_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ೿")):
        self.driver_before_scenario = True
      if(not bstack1llll1lll_opy_):
        scenario_name = args[0].name
        feature_name = bstack1ll1111_opy_ = str(self.feature.name)
        bstack1ll1111_opy_ = feature_name + bstack1lllllll1_opy_ (u"ࠪࠤ࠲ࠦࠧഀ") + scenario_name
        if self.driver_before_scenario:
          bstack111l1l1l_opy_(context, bstack1ll1111_opy_)
          context.browser.execute_script(bstack1lllllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩഁ") + json.dumps(bstack1ll1111_opy_) + bstack1lllllll1_opy_ (u"ࠬࢃࡽࠨം"))
    except Exception as e:
      logger.debug(bstack1lllllll1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧഃ").format(str(e)))
  if name == bstack1lllllll1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨഄ"):
    try:
      bstack1ll11ll1l_opy_ = args[0].status.name
      if str(bstack1ll11ll1l_opy_).lower() == bstack1lllllll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨഅ"):
        bstack1l1l11111_opy_ = bstack1lllllll1_opy_ (u"ࠩࠪആ")
        bstack1l111l1ll_opy_ = bstack1lllllll1_opy_ (u"ࠪࠫഇ")
        bstack1ll11l1ll_opy_ = bstack1lllllll1_opy_ (u"ࠫࠬഈ")
        try:
          import traceback
          bstack1l1l11111_opy_ = self.exception.__class__.__name__
          bstack1l1lll1l_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1l111l1ll_opy_ = bstack1lllllll1_opy_ (u"ࠬࠦࠧഉ").join(bstack1l1lll1l_opy_)
          bstack1ll11l1ll_opy_ = bstack1l1lll1l_opy_[-1]
        except Exception as e:
          logger.debug(bstack11l1ll1l_opy_.format(str(e)))
        bstack1l1l11111_opy_ += bstack1ll11l1ll_opy_
        bstack1111ll1l_opy_(context, json.dumps(str(args[0].name) + bstack1lllllll1_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧഊ") + str(bstack1l111l1ll_opy_)), bstack1lllllll1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨഋ"))
        if self.driver_before_scenario:
          bstack1ll1lll1l_opy_(context, bstack1lllllll1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣഌ"), bstack1l1l11111_opy_)
        context.browser.execute_script(bstack1lllllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ഍") + json.dumps(str(args[0].name) + bstack1lllllll1_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤഎ") + str(bstack1l111l1ll_opy_)) + bstack1lllllll1_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫഏ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡸࡺࡡࡵࡷࡶࠦ࠿ࠨࡦࡢ࡫࡯ࡩࡩࠨࠬࠡࠤࡵࡩࡦࡹ࡯࡯ࠤ࠽ࠤࠬഐ") + json.dumps(bstack1lllllll1_opy_ (u"ࠨࡓࡤࡧࡱࡥࡷ࡯࡯ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥ഑") + str(bstack1l1l11111_opy_)) + bstack1lllllll1_opy_ (u"ࠧࡾࡿࠪഒ"))
      else:
        bstack1111ll1l_opy_(context, bstack1lllllll1_opy_ (u"ࠣࡒࡤࡷࡸ࡫ࡤࠢࠤഓ"), bstack1lllllll1_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢഔ"))
        if self.driver_before_scenario:
          bstack1ll1lll1l_opy_(context, bstack1lllllll1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥക"))
        context.browser.execute_script(bstack1lllllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩഖ") + json.dumps(str(args[0].name) + bstack1lllllll1_opy_ (u"ࠧࠦ࠭ࠡࡒࡤࡷࡸ࡫ࡤࠢࠤഗ")) + bstack1lllllll1_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬഘ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1lllllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠣࡲࡤࡷࡸ࡫ࡤࠣࡿࢀࠫങ"))
    except Exception as e:
      logger.debug(bstack1lllllll1_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪച").format(str(e)))
  if name == bstack1lllllll1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩഛ"):
    try:
      if context.failed is True:
        bstack11ll_opy_ = []
        bstack1lllll111_opy_ = []
        bstack11lllll1l_opy_ = []
        bstack11lll1l11_opy_ = bstack1lllllll1_opy_ (u"ࠪࠫജ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack11ll_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1l1lll1l_opy_ = traceback.format_tb(exc_tb)
            bstack111ll111l_opy_ = bstack1lllllll1_opy_ (u"ࠫࠥ࠭ഝ").join(bstack1l1lll1l_opy_)
            bstack1lllll111_opy_.append(bstack111ll111l_opy_)
            bstack11lllll1l_opy_.append(bstack1l1lll1l_opy_[-1])
        except Exception as e:
          logger.debug(bstack11l1ll1l_opy_.format(str(e)))
        bstack1l1l11111_opy_ = bstack1lllllll1_opy_ (u"ࠬ࠭ഞ")
        for i in range(len(bstack11ll_opy_)):
          bstack1l1l11111_opy_ += bstack11ll_opy_[i] + bstack11lllll1l_opy_[i] + bstack1lllllll1_opy_ (u"࠭࡜࡯ࠩട")
        bstack11lll1l11_opy_ = bstack1lllllll1_opy_ (u"ࠧࠡࠩഠ").join(bstack1lllll111_opy_)
        if not self.driver_before_scenario:
          bstack1111ll1l_opy_(context, bstack11lll1l11_opy_, bstack1lllllll1_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢഡ"))
          bstack1ll1lll1l_opy_(context, bstack1lllllll1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤഢ"), bstack1l1l11111_opy_)
          context.browser.execute_script(bstack1lllllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨണ") + json.dumps(bstack11lll1l11_opy_) + bstack1lllllll1_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫത"))
          context.browser.execute_script(bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡸࡺࡡࡵࡷࡶࠦ࠿ࠨࡦࡢ࡫࡯ࡩࡩࠨࠬࠡࠤࡵࡩࡦࡹ࡯࡯ࠤ࠽ࠤࠬഥ") + json.dumps(bstack1lllllll1_opy_ (u"ࠨࡓࡰ࡯ࡨࠤࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡹࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡ࡞ࡱࠦദ") + str(bstack1l1l11111_opy_)) + bstack1lllllll1_opy_ (u"ࠧࡾࡿࠪധ"))
      else:
        if not self.driver_before_scenario:
          bstack1111ll1l_opy_(context, bstack1lllllll1_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦന") + str(self.feature.name) + bstack1lllllll1_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦഩ"), bstack1lllllll1_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣപ"))
          bstack1ll1lll1l_opy_(context, bstack1lllllll1_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦഫ"))
          context.browser.execute_script(bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪബ") + json.dumps(bstack1lllllll1_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤഭ") + str(self.feature.name) + bstack1lllllll1_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤമ")) + bstack1lllllll1_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧയ"))
          context.browser.execute_script(bstack1lllllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡴࡦࡹࡳࡦࡦࠥࢁࢂ࠭ര"))
    except Exception as e:
      logger.debug(bstack1lllllll1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬറ").format(str(e)))
  if name in [bstack1lllllll1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫല"), bstack1lllllll1_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ള")]:
    bstack1ll1111l_opy_(self, name, context, *args)
    if (name == bstack1lllllll1_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧഴ") and self.driver_before_scenario) or (name == bstack1lllllll1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧവ") and not self.driver_before_scenario):
      try:
        context.browser.quit()
      except Exception:
        pass
def bstack1ll1ll1_opy_(config, startdir):
  return bstack1lllllll1_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾ࠴ࢂࠨശ").format(bstack1lllllll1_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣഷ"))
class Notset:
  def __repr__(self):
    return bstack1lllllll1_opy_ (u"ࠥࡀࡓࡕࡔࡔࡇࡗࡂࠧസ")
notset = Notset()
def bstack1lllll1l_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack11ll1ll11_opy_
  if str(name).lower() == bstack1lllllll1_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫഹ"):
    return bstack1lllllll1_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦഺ")
  else:
    return bstack11ll1ll11_opy_(self, name, default, skip)
def bstack1l1l11_opy_(item, when):
  global bstack1lll11lll_opy_
  try:
    bstack1lll11lll_opy_(item, when)
  except Exception as e:
    pass
def bstack111l111ll_opy_():
  return
def bstack1111l1l1_opy_(type, name, status, reason, bstack1ll_opy_, bstack1l1ll11l1_opy_):
  bstack11llll1l_opy_ = {
    bstack1lllllll1_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ഻࠭"): type,
    bstack1lllllll1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ഼ࠪ"): {}
  }
  if type == bstack1lllllll1_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪഽ"):
    bstack11llll1l_opy_[bstack1lllllll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬാ")][bstack1lllllll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩി")] = bstack1ll_opy_
    bstack11llll1l_opy_[bstack1lllllll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧീ")][bstack1lllllll1_opy_ (u"ࠬࡪࡡࡵࡣࠪു")] = json.dumps(str(bstack1l1ll11l1_opy_))
  if type == bstack1lllllll1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧൂ"):
    bstack11llll1l_opy_[bstack1lllllll1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪൃ")][bstack1lllllll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ൄ")] = name
  if type == bstack1lllllll1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ൅"):
    bstack11llll1l_opy_[bstack1lllllll1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭െ")][bstack1lllllll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫേ")] = status
    if status == bstack1lllllll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬൈ"):
      bstack11llll1l_opy_[bstack1lllllll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ൉")][bstack1lllllll1_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧൊ")] = json.dumps(str(reason))
  bstack1lll1l111_opy_ = bstack1lllllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ോ").format(json.dumps(bstack11llll1l_opy_))
  return bstack1lll1l111_opy_
def bstack1l1ll_opy_(item, call, rep):
  global bstack11ll1l1ll_opy_
  global bstack1l111l111_opy_
  name = bstack1lllllll1_opy_ (u"ࠩࠪൌ")
  try:
    if rep.when == bstack1lllllll1_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ്"):
      bstack11lllllll_opy_ = threading.current_thread().bstack1111111_opy_
      try:
        name = str(rep.nodeid)
        bstack11llll1_opy_ = bstack1111l1l1_opy_(bstack1lllllll1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬൎ"), name, bstack1lllllll1_opy_ (u"ࠬ࠭൏"), bstack1lllllll1_opy_ (u"࠭ࠧ൐"), bstack1lllllll1_opy_ (u"ࠧࠨ൑"), bstack1lllllll1_opy_ (u"ࠨࠩ൒"))
        for driver in bstack1l111l111_opy_:
          if bstack11lllllll_opy_ == driver.session_id:
            driver.execute_script(bstack11llll1_opy_)
      except Exception as e:
        logger.debug(bstack1lllllll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ൓").format(str(e)))
      try:
        status = bstack1lllllll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪൔ") if rep.outcome.lower() == bstack1lllllll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫൕ") else bstack1lllllll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬൖ")
        reason = bstack1lllllll1_opy_ (u"࠭ࠧൗ")
        if (reason != bstack1lllllll1_opy_ (u"ࠢࠣ൘")):
          try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
          except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
          threading.current_thread().bstackTestErrorMessages.append(str(reason))
        if status == bstack1lllllll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ൙"):
          reason = rep.longrepr.reprcrash.message
          if (not threading.current_thread().bstackTestErrorMessages):
            threading.current_thread().bstackTestErrorMessages = []
          threading.current_thread().bstackTestErrorMessages.append(reason)
        level = bstack1lllllll1_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ൚") if status == bstack1lllllll1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ൛") else bstack1lllllll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ൜")
        data = name + bstack1lllllll1_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧ൝") if status == bstack1lllllll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭൞") else name + bstack1lllllll1_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠢࠢࠪൟ") + reason
        bstack1lll11l_opy_ = bstack1111l1l1_opy_(bstack1lllllll1_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪൠ"), bstack1lllllll1_opy_ (u"ࠩࠪൡ"), bstack1lllllll1_opy_ (u"ࠪࠫൢ"), bstack1lllllll1_opy_ (u"ࠫࠬൣ"), level, data)
        for driver in bstack1l111l111_opy_:
          if bstack11lllllll_opy_ == driver.session_id:
            driver.execute_script(bstack1lll11l_opy_)
      except Exception as e:
        logger.debug(bstack1lllllll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡦࡳࡳࡺࡥࡹࡶࠣࡪࡴࡸࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠩ൤").format(str(e)))
  except Exception as e:
    logger.debug(bstack1lllllll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡶࡸࡦࡺࡥࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼࡿࠪ൥").format(str(e)))
  bstack11ll1l1ll_opy_(item, call, rep)
def bstack1ll11llll_opy_(framework_name):
  global bstack111111l1_opy_
  global bstack111l1l_opy_
  global bstack11l1l1l11_opy_
  bstack111111l1_opy_ = framework_name
  logger.info(bstack1lll1llll_opy_.format(bstack111111l1_opy_.split(bstack1lllllll1_opy_ (u"ࠧ࠮ࠩ൦"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    Service.start = bstack1l1ll1_opy_
    Service.stop = bstack11ll1l1_opy_
    webdriver.Remote.__init__ = bstack1l1l11l1l_opy_
    webdriver.Remote.get = bstack111lll11_opy_
    WebDriver.close = bstack11l111l1_opy_
    WebDriver.quit = bstack11l1l1_opy_
    bstack111l1l_opy_ = True
  except Exception as e:
    pass
  bstack11l1lll1_opy_()
  if not bstack111l1l_opy_:
    bstack1111111l_opy_(bstack1lllllll1_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥ൧"), bstack11l1ll1_opy_)
  if bstack1l11ll111_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack111l1l1ll_opy_
    except Exception as e:
      logger.error(bstack11lll111l_opy_.format(str(e)))
  if (bstack1lllllll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ൨") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack11l111ll_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack11lllll11_opy_
      except Exception as e:
        logger.warn(bstack1lll1l1ll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1l11l1lll_opy_
      except Exception as e:
        logger.debug(bstack1l11l11_opy_ + str(e))
    except Exception as e:
      bstack1111111l_opy_(e, bstack1lll1l1ll_opy_)
    Output.end_test = bstack1lll11111_opy_
    TestStatus.__init__ = bstack11l11111_opy_
    QueueItem.__init__ = bstack1lll1111l_opy_
    pabot._create_items = bstack1lll_opy_
    try:
      from pabot import __version__ as bstack11111ll_opy_
      if version.parse(bstack11111ll_opy_) >= version.parse(bstack1lllllll1_opy_ (u"ࠪ࠶࠳࠷࠵࠯࠲ࠪ൩")):
        pabot._run = bstack1lll1111_opy_
      elif version.parse(bstack11111ll_opy_) >= version.parse(bstack1lllllll1_opy_ (u"ࠫ࠷࠴࠱࠴࠰࠳ࠫ൪")):
        pabot._run = bstack11l11l11_opy_
      else:
        pabot._run = bstack1l1l1l1_opy_
    except Exception as e:
      pabot._run = bstack1l1l1l1_opy_
    pabot._create_command_for_execution = bstack111l1111_opy_
    pabot._report_results = bstack11l111ll1_opy_
  if bstack1lllllll1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ൫") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1111111l_opy_(e, bstack11l1l1ll1_opy_)
    Runner.run_hook = bstack11l11ll1_opy_
    Step.run = bstack1lll111l_opy_
  if bstack1lllllll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭൬") in str(framework_name).lower():
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      from _pytest import runner
      pytest_selenium.pytest_report_header = bstack1ll1ll1_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack111l111ll_opy_
      Config.getoption = bstack1lllll1l_opy_
      runner._update_current_test_var = bstack1l1l11_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1l1ll_opy_
    except Exception as e:
      pass
def bstack1ll11lll_opy_():
  global CONFIG
  if bstack1lllllll1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ൭") in CONFIG and int(CONFIG[bstack1lllllll1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ൮")]) > 1:
    logger.warn(bstack11l1l1l1_opy_)
def bstack1ll111ll1_opy_(arg):
  arg.append(bstack1lllllll1_opy_ (u"ࠤ࠰࠱ࡨࡧࡰࡵࡷࡵࡩࡂࡹࡹࡴࠤ൯"))
  arg.append(bstack1lllllll1_opy_ (u"ࠥ࠱࡜ࠨ൰"))
  arg.append(bstack1lllllll1_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨ࠾ࡒࡵࡤࡶ࡮ࡨࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡯࡭ࡱࡱࡵࡸࡪࡪ࠺ࡱࡻࡷࡩࡸࡺ࠮ࡑࡻࡷࡩࡸࡺࡗࡢࡴࡱ࡭ࡳ࡭ࠢ൱"))
  global CONFIG
  bstack1ll11llll_opy_(bstack1llll11_opy_)
  os.environ[bstack1lllllll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭൲")] = CONFIG[bstack1lllllll1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ൳")]
  os.environ[bstack1lllllll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ൴")] = CONFIG[bstack1lllllll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ൵")]
  from _pytest.config import main as bstack1l1lll_opy_
  bstack1l1lll_opy_(arg)
def bstack1lll1lll1_opy_(arg):
  bstack1ll11llll_opy_(bstack1l1l1llll_opy_)
  from behave.__main__ import main as bstack1l1lll11_opy_
  bstack1l1lll11_opy_(arg)
def bstack1ll1l1l1_opy_():
  logger.info(bstack1ll1llll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1lllllll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ൶"), help=bstack1lllllll1_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࠫ൷"))
  parser.add_argument(bstack1lllllll1_opy_ (u"ࠫ࠲ࡻࠧ൸"), bstack1lllllll1_opy_ (u"ࠬ࠳࠭ࡶࡵࡨࡶࡳࡧ࡭ࡦࠩ൹"), help=bstack1lllllll1_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬൺ"))
  parser.add_argument(bstack1lllllll1_opy_ (u"ࠧ࠮࡭ࠪൻ"), bstack1lllllll1_opy_ (u"ࠨ࠯࠰࡯ࡪࡿࠧർ"), help=bstack1lllllll1_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡡࡤࡥࡨࡷࡸࠦ࡫ࡦࡻࠪൽ"))
  parser.add_argument(bstack1lllllll1_opy_ (u"ࠪ࠱࡫࠭ൾ"), bstack1lllllll1_opy_ (u"ࠫ࠲࠳ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩൿ"), help=bstack1lllllll1_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ඀"))
  bstack111l11ll_opy_ = parser.parse_args()
  try:
    bstack1llll111l_opy_ = bstack1lllllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥ࡯ࡧࡵ࡭ࡨ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪඁ")
    if bstack111l11ll_opy_.framework and bstack111l11ll_opy_.framework not in (bstack1lllllll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧං"), bstack1lllllll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩඃ")):
      bstack1llll111l_opy_ = bstack1lllllll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨ඄")
    bstack1l11ll1l1_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1llll111l_opy_)
    bstack1lll1ll11_opy_ = open(bstack1l11ll1l1_opy_, bstack1lllllll1_opy_ (u"ࠪࡶࠬඅ"))
    bstack11l1l1111_opy_ = bstack1lll1ll11_opy_.read()
    bstack1lll1ll11_opy_.close()
    if bstack111l11ll_opy_.username:
      bstack11l1l1111_opy_ = bstack11l1l1111_opy_.replace(bstack1lllllll1_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫආ"), bstack111l11ll_opy_.username)
    if bstack111l11ll_opy_.key:
      bstack11l1l1111_opy_ = bstack11l1l1111_opy_.replace(bstack1lllllll1_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧඇ"), bstack111l11ll_opy_.key)
    if bstack111l11ll_opy_.framework:
      bstack11l1l1111_opy_ = bstack11l1l1111_opy_.replace(bstack1lllllll1_opy_ (u"࡙࠭ࡐࡗࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧඈ"), bstack111l11ll_opy_.framework)
    file_name = bstack1lllllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪඉ")
    file_path = os.path.abspath(file_name)
    bstack1l1l1l11l_opy_ = open(file_path, bstack1lllllll1_opy_ (u"ࠨࡹࠪඊ"))
    bstack1l1l1l11l_opy_.write(bstack11l1l1111_opy_)
    bstack1l1l1l11l_opy_.close()
    logger.info(bstack1lll1ll_opy_)
    try:
      os.environ[bstack1lllllll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫඋ")] = bstack111l11ll_opy_.framework if bstack111l11ll_opy_.framework != None else bstack1lllllll1_opy_ (u"ࠥࠦඌ")
      config = yaml.safe_load(bstack11l1l1111_opy_)
      config[bstack1lllllll1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫඍ")] = bstack1lllllll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡹࡥࡵࡷࡳࠫඎ")
      bstack11l1111_opy_(bstack1ll1111l1_opy_, config)
    except Exception as e:
      logger.debug(bstack1l111lll_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1l111l1_opy_.format(str(e)))
def bstack11l1111_opy_(bstack11ll1l1l_opy_, config, bstack1llll1l11_opy_ = {}):
  global bstack1l1111l11_opy_
  if not config:
    return
  bstack1ll111l1_opy_ = bstack1l1lllll1_opy_ if not bstack1l1111l11_opy_ else ( bstack11l1l1ll_opy_ if bstack1lllllll1_opy_ (u"࠭ࡡࡱࡲࠪඏ") in config else bstack11ll1lll1_opy_ )
  data = {
    bstack1lllllll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩඐ"): config[bstack1lllllll1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪඑ")],
    bstack1lllllll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬඒ"): config[bstack1lllllll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ඓ")],
    bstack1lllllll1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨඔ"): bstack11ll1l1l_opy_,
    bstack1lllllll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨඕ"): {
      bstack1lllllll1_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫඖ"): str(config[bstack1lllllll1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ඗")]) if bstack1lllllll1_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ඘") in config else bstack1lllllll1_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥ඙"),
      bstack1lllllll1_opy_ (u"ࠪࡶࡪ࡬ࡥࡳࡴࡨࡶࠬක"): bstack1llll111_opy_(os.getenv(bstack1lllllll1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࠨඛ"), bstack1lllllll1_opy_ (u"ࠧࠨග"))),
      bstack1lllllll1_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨඝ"): bstack1lllllll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧඞ"),
      bstack1lllllll1_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩඟ"): bstack1ll111l1_opy_,
      bstack1lllllll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬච"): config[bstack1lllllll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ඡ")]if config[bstack1lllllll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧජ")] else bstack1lllllll1_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨඣ"),
      bstack1lllllll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨඤ"): str(config[bstack1lllllll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩඥ")]) if bstack1lllllll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪඦ") in config else bstack1lllllll1_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥට"),
      bstack1lllllll1_opy_ (u"ࠪࡳࡸ࠭ඨ"): sys.platform,
      bstack1lllllll1_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ඩ"): socket.gethostname()
    }
  }
  update(data[bstack1lllllll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨඪ")], bstack1llll1l11_opy_)
  try:
    response = bstack1l11l1l1_opy_(bstack1lllllll1_opy_ (u"࠭ࡐࡐࡕࡗࠫණ"), bstack11l1ll1ll_opy_, data, config)
    if response:
      logger.debug(bstack111l1l11_opy_.format(bstack11ll1l1l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack11ll111l1_opy_.format(str(e)))
def bstack1l11l1l1_opy_(type, url, data, config):
  bstack11l11l1ll_opy_ = bstack1l11llll1_opy_.format(url)
  proxies = bstack1l11l111l_opy_(config, bstack11l11l1ll_opy_)
  if type == bstack1lllllll1_opy_ (u"ࠧࡑࡑࡖࡘࠬඬ"):
    response = requests.post(bstack11l11l1ll_opy_, json=data,
                    headers={bstack1lllllll1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧත"): bstack1lllllll1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬථ")}, auth=(config[bstack1lllllll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬද")], config[bstack1lllllll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧධ")]), proxies=proxies)
  return response
def bstack1llll111_opy_(framework):
  return bstack1lllllll1_opy_ (u"ࠧࢁࡽ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤන").format(str(framework), __version__) if framework else bstack1lllllll1_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢ඲").format(__version__)
def bstack1ll11_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack1l1l1l1ll_opy_()
    logger.debug(bstack1l111l11l_opy_.format(str(CONFIG)))
    bstack1llll1l1l_opy_()
    bstack1l11l11l_opy_()
  except Exception as e:
    logger.error(bstack1lllllll1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠦඳ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack111lll1_opy_
  atexit.register(bstack11llll11_opy_)
  signal.signal(signal.SIGINT, bstack11l1l11ll_opy_)
  signal.signal(signal.SIGTERM, bstack11l1l11ll_opy_)
def bstack111lll1_opy_(exctype, value, traceback):
  global bstack1l111l111_opy_
  try:
    for driver in bstack1l111l111_opy_:
      driver.execute_script(
        bstack1lllllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠤࡩࡥ࡮ࡲࡥࡥࠤ࠯ࠤࠧࡸࡥࡢࡵࡲࡲࠧࡀࠠࠨප") + json.dumps(bstack1lllllll1_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧඵ") + str(value)) + bstack1lllllll1_opy_ (u"ࠪࢁࢂ࠭බ"))
  except Exception:
    pass
  bstack1l11lllll_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1l11lllll_opy_(message = bstack1lllllll1_opy_ (u"ࠫࠬභ")):
  global CONFIG
  try:
    if message:
      bstack1llll1l11_opy_ = {
        bstack1lllllll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫම"): str(message)
      }
      bstack11l1111_opy_(bstack11ll1llll_opy_, CONFIG, bstack1llll1l11_opy_)
    else:
      bstack11l1111_opy_(bstack11ll1llll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack111ll1l1_opy_.format(str(e)))
def bstack1l11l1ll1_opy_(bstack111111_opy_, size):
  bstack111ll_opy_ = []
  while len(bstack111111_opy_) > size:
    bstack11ll11_opy_ = bstack111111_opy_[:size]
    bstack111ll_opy_.append(bstack11ll11_opy_)
    bstack111111_opy_   = bstack111111_opy_[size:]
  bstack111ll_opy_.append(bstack111111_opy_)
  return bstack111ll_opy_
def bstack1l_opy_(args):
  if bstack1lllllll1_opy_ (u"࠭࠭࡮ࠩඹ") in args and bstack1lllllll1_opy_ (u"ࠧࡱࡦࡥࠫය") in args:
    return True
  return False
def run_on_browserstack(bstack11111111_opy_=None, bstack111l1l1l1_opy_=None, bstack1ll11ll11_opy_=False):
  global CONFIG
  global bstack1ll111l11_opy_
  global bstack1l11ll1l_opy_
  bstack1lll111ll_opy_ = bstack1lllllll1_opy_ (u"ࠨࠩර")
  if bstack11111111_opy_ and isinstance(bstack11111111_opy_, str):
    bstack11111111_opy_ = eval(bstack11111111_opy_)
  if bstack11111111_opy_:
    CONFIG = bstack11111111_opy_[bstack1lllllll1_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩ඼")]
    bstack1ll111l11_opy_ = bstack11111111_opy_[bstack1lllllll1_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫල")]
    bstack1l11ll1l_opy_ = bstack11111111_opy_[bstack1lllllll1_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭඾")]
    bstack1lll111ll_opy_ = bstack1lllllll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ඿")
  if not bstack1ll11ll11_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack11l1l11l1_opy_)
      return
    if sys.argv[1] == bstack1lllllll1_opy_ (u"࠭࠭࠮ࡸࡨࡶࡸ࡯࡯࡯ࠩව")  or sys.argv[1] == bstack1lllllll1_opy_ (u"ࠧ࠮ࡸࠪශ"):
      logger.info(bstack1lllllll1_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡑࡻࡷ࡬ࡴࡴࠠࡔࡆࡎࠤࡻࢁࡽࠨෂ").format(__version__))
      return
    if sys.argv[1] == bstack1lllllll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨස"):
      bstack1ll1l1l1_opy_()
      return
  args = sys.argv
  bstack1ll11_opy_()
  global bstack1ll111l_opy_
  global bstack1ll1l1ll_opy_
  global bstack11l11l1l_opy_
  global bstack111l11l_opy_
  global bstack1lll11l1l_opy_
  global bstack111l11l11_opy_
  global bstack1lllll1ll_opy_
  global bstack11l1l1l11_opy_
  if not bstack1lll111ll_opy_:
    if args[1] == bstack1lllllll1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪහ") or args[1] == bstack1lllllll1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬළ"):
      bstack1lll111ll_opy_ = bstack1lllllll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬෆ")
      args = args[2:]
    elif args[1] == bstack1lllllll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ෇"):
      bstack1lll111ll_opy_ = bstack1lllllll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭෈")
      args = args[2:]
    elif args[1] == bstack1lllllll1_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ෉"):
      bstack1lll111ll_opy_ = bstack1lllllll1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ්")
      args = args[2:]
    elif args[1] == bstack1lllllll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ෋"):
      bstack1lll111ll_opy_ = bstack1lllllll1_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ෌")
      args = args[2:]
    elif args[1] == bstack1lllllll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ෍"):
      bstack1lll111ll_opy_ = bstack1lllllll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭෎")
      args = args[2:]
    elif args[1] == bstack1lllllll1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧා"):
      bstack1lll111ll_opy_ = bstack1lllllll1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨැ")
      args = args[2:]
    else:
      if not bstack1lllllll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬෑ") in CONFIG or str(CONFIG[bstack1lllllll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ි")]).lower() in [bstack1lllllll1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫී"), bstack1lllllll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭ු")]:
        bstack1lll111ll_opy_ = bstack1lllllll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭෕")
        args = args[1:]
      elif str(CONFIG[bstack1lllllll1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪූ")]).lower() == bstack1lllllll1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ෗"):
        bstack1lll111ll_opy_ = bstack1lllllll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨෘ")
        args = args[1:]
      elif str(CONFIG[bstack1lllllll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ෙ")]).lower() == bstack1lllllll1_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪේ"):
        bstack1lll111ll_opy_ = bstack1lllllll1_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫෛ")
        args = args[1:]
      elif str(CONFIG[bstack1lllllll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩො")]).lower() == bstack1lllllll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧෝ"):
        bstack1lll111ll_opy_ = bstack1lllllll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨෞ")
        args = args[1:]
      elif str(CONFIG[bstack1lllllll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬෟ")]).lower() == bstack1lllllll1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ෠"):
        bstack1lll111ll_opy_ = bstack1lllllll1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ෡")
        args = args[1:]
      else:
        os.environ[bstack1lllllll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ෢")] = bstack1lll111ll_opy_
        bstack11l11_opy_(bstack1l1111111_opy_)
  global bstack1l1ll1l1_opy_
  if bstack11111111_opy_:
    try:
      os.environ[bstack1lllllll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ෣")] = bstack1lll111ll_opy_
      bstack11l1111_opy_(bstack1111ll_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack111ll1l1_opy_.format(str(e)))
  global bstack11l1llll1_opy_
  global bstack1l11l1l1l_opy_
  global bstack111ll11ll_opy_
  global bstack1lll1ll1_opy_
  global bstack111llll11_opy_
  global bstack1l1l11ll_opy_
  global bstack1111l11l_opy_
  global bstack1_opy_
  global bstack11l11lll_opy_
  global bstack1l1lll111_opy_
  global bstack1l1l111l_opy_
  global bstack1ll1111l_opy_
  global bstack1l11111_opy_
  global bstack111l11ll1_opy_
  global bstack11ll111ll_opy_
  global bstack11ll1ll11_opy_
  global bstack1lll11lll_opy_
  global bstack1l1ll1l_opy_
  global bstack11ll1l1ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11l1llll1_opy_ = webdriver.Remote.__init__
    bstack1l11l1l1l_opy_ = WebDriver.quit
    bstack1l1l111l_opy_ = WebDriver.close
    bstack111l11ll1_opy_ = WebDriver.get
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1ll1l1_opy_ = Popen.__init__
  except Exception as e:
    pass
  if bstack11ll11ll1_opy_():
    if bstack1ll11l1l_opy_() < version.parse(bstack1lllll1_opy_):
      logger.error(bstack1ll111_opy_.format(bstack1ll11l1l_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack11ll111ll_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack11lll111l_opy_.format(str(e)))
  if bstack1lll111ll_opy_ != bstack1lllllll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ෤") or (bstack1lll111ll_opy_ == bstack1lllllll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ෥") and not bstack11111111_opy_):
    bstack111llll1_opy_()
  if (bstack1lll111ll_opy_ in [bstack1lllllll1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ෦"), bstack1lllllll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ෧"), bstack1lllllll1_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ෨")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack11l111ll_opy_
        bstack111llll11_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1lll1l1ll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1lll1ll1_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1l11l11_opy_ + str(e))
    except Exception as e:
      bstack1111111l_opy_(e, bstack1lll1l1ll_opy_)
    if bstack1lll111ll_opy_ != bstack1lllllll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭෩"):
      bstack1ll1ll1l_opy_()
    bstack111ll11ll_opy_ = Output.end_test
    bstack1l1l11ll_opy_ = TestStatus.__init__
    bstack1_opy_ = pabot._run
    bstack11l11lll_opy_ = QueueItem.__init__
    bstack1l1lll111_opy_ = pabot._create_command_for_execution
    bstack1l1ll1l_opy_ = pabot._report_results
  if bstack1lll111ll_opy_ == bstack1lllllll1_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭෪"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1111111l_opy_(e, bstack11l1l1ll1_opy_)
    bstack1ll1111l_opy_ = Runner.run_hook
    bstack1l11111_opy_ = Step.run
  if bstack1lll111ll_opy_ == bstack1lllllll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ෫"):
    try:
      from _pytest.config import Config
      bstack11ll1ll11_opy_ = Config.getoption
      from _pytest import runner
      bstack1lll11lll_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack11l111111_opy_)
    try:
      from pytest_bdd import reporting
      bstack11ll1l1ll_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1lllllll1_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩ෬"))
  if bstack1lll111ll_opy_ == bstack1lllllll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ෭"):
    bstack1ll1l1ll_opy_ = True
    if bstack11111111_opy_ and bstack1ll11ll11_opy_:
      bstack1lll11l1l_opy_ = CONFIG.get(bstack1lllllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ෮"), {}).get(bstack1lllllll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭෯"))
      bstack1ll11llll_opy_(bstack1ll11111_opy_)
    elif bstack11111111_opy_:
      bstack1lll11l1l_opy_ = CONFIG.get(bstack1lllllll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ෰"), {}).get(bstack1lllllll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ෱"))
      global bstack1l111l111_opy_
      try:
        if bstack1l_opy_(bstack11111111_opy_[bstack1lllllll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪෲ")]) and multiprocessing.current_process().name == bstack1lllllll1_opy_ (u"ࠨ࠲ࠪෳ"):
          bstack11111111_opy_[bstack1lllllll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ෴")].remove(bstack1lllllll1_opy_ (u"ࠪ࠱ࡲ࠭෵"))
          bstack11111111_opy_[bstack1lllllll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ෶")].remove(bstack1lllllll1_opy_ (u"ࠬࡶࡤࡣࠩ෷"))
          bstack11111111_opy_[bstack1lllllll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ෸")] = bstack11111111_opy_[bstack1lllllll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ෹")][0]
          with open(bstack11111111_opy_[bstack1lllllll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ෺")], bstack1lllllll1_opy_ (u"ࠩࡵࠫ෻")) as f:
            bstack111ll1l11_opy_ = f.read()
          bstack111l111l1_opy_ = bstack1lllllll1_opy_ (u"ࠥࠦࠧ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡨࡰࠦࡩ࡮ࡲࡲࡶࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦ࠽ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪ࠮ࡻࡾࠫ࠾ࠤ࡫ࡸ࡯࡮ࠢࡳࡨࡧࠦࡩ࡮ࡲࡲࡶࡹࠦࡐࡥࡤ࠾ࠤࡴ࡭࡟ࡥࡤࠣࡁࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮࠿ࠏࡪࡥࡧࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯࠭ࡹࡥ࡭ࡨ࠯ࠤࡦࡸࡧ࠭ࠢࡷࡩࡲࡶ࡯ࡳࡣࡵࡽࠥࡃࠠ࠱ࠫ࠽ࠎࠥࠦࡴࡳࡻ࠽ࠎࠥࠦࠠࠡࡣࡵ࡫ࠥࡃࠠࡴࡶࡵࠬ࡮ࡴࡴࠩࡣࡵ࡫࠮࠱࠱࠱ࠫࠍࠤࠥ࡫ࡸࡤࡧࡳࡸࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡣࡶࠤࡪࡀࠊࠡࠢࠣࠤࡵࡧࡳࡴࠌࠣࠤࡴ࡭࡟ࡥࡤࠫࡷࡪࡲࡦ࠭ࡣࡵ࡫࠱ࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠪࠌࡓࡨࡧ࠴ࡤࡰࡡࡥࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࡓࡨࡧ࠴ࡤࡰࡡࡥࡶࡪࡧ࡫ࠡ࠿ࠣࡱࡴࡪ࡟ࡣࡴࡨࡥࡰࠐࡐࡥࡤࠫ࠭࠳ࡹࡥࡵࡡࡷࡶࡦࡩࡥࠩࠫ࡟ࡲࠧࠨࠢ෼").format(str(bstack11111111_opy_))
          bstack1l1l_opy_ = bstack111l111l1_opy_ + bstack111ll1l11_opy_
          bstack11l1ll_opy_ = bstack11111111_opy_[bstack1lllllll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ෽")] + bstack1lllllll1_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡴࡦ࡯ࡳ࠲ࡵࡿࠧ෾")
          with open(bstack11l1ll_opy_, bstack1lllllll1_opy_ (u"࠭ࡷࠨ෿")):
            pass
          with open(bstack11l1ll_opy_, bstack1lllllll1_opy_ (u"ࠢࡸ࠭ࠥ฀")) as f:
            f.write(bstack1l1l_opy_)
          import subprocess
          bstack1llllll11_opy_ = subprocess.run([bstack1lllllll1_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣก"), bstack11l1ll_opy_])
          if os.path.exists(bstack11l1ll_opy_):
            os.unlink(bstack11l1ll_opy_)
          os._exit(bstack1llllll11_opy_.returncode)
        else:
          if bstack1l_opy_(bstack11111111_opy_[bstack1lllllll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬข")]):
            bstack11111111_opy_[bstack1lllllll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ฃ")].remove(bstack1lllllll1_opy_ (u"ࠫ࠲ࡳࠧค"))
            bstack11111111_opy_[bstack1lllllll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨฅ")].remove(bstack1lllllll1_opy_ (u"࠭ࡰࡥࡤࠪฆ"))
            bstack11111111_opy_[bstack1lllllll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪง")] = bstack11111111_opy_[bstack1lllllll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫจ")][0]
          bstack1ll11llll_opy_(bstack1ll11111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11111111_opy_[bstack1lllllll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬฉ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1lllllll1_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬช")] = bstack1lllllll1_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭ซ")
          mod_globals[bstack1lllllll1_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧฌ")] = os.path.abspath(bstack11111111_opy_[bstack1lllllll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩญ")])
          exec(open(bstack11111111_opy_[bstack1lllllll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪฎ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1lllllll1_opy_ (u"ࠨࡅࡤࡹ࡬࡮ࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠨฏ").format(str(e)))
          for driver in bstack1l111l111_opy_:
            bstack111l1l1l1_opy_.append({
              bstack1lllllll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧฐ"): bstack11111111_opy_[bstack1lllllll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ฑ")],
              bstack1lllllll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪฒ"): str(e),
              bstack1lllllll1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫณ"): multiprocessing.current_process().name
            })
            driver.execute_script(
              bstack1lllllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡧࡣ࡬ࡰࡪࡪࠢ࠭ࠢࠥࡶࡪࡧࡳࡰࡰࠥ࠾ࠥ࠭ด") + json.dumps(bstack1lllllll1_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥต") + str(e)) + bstack1lllllll1_opy_ (u"ࠨࡿࢀࠫถ"))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1l111l111_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      bstack1l11lll1l_opy_()
      bstack1ll11lll_opy_()
      bstack1111llll_opy_ = {
        bstack1lllllll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬท"): args[0],
        bstack1lllllll1_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪธ"): CONFIG,
        bstack1lllllll1_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬน"): bstack1ll111l11_opy_,
        bstack1lllllll1_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧบ"): bstack1l11ll1l_opy_
      }
      if bstack1lllllll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩป") in CONFIG:
        bstack11ll11l1l_opy_ = []
        manager = multiprocessing.Manager()
        bstack11l11lll1_opy_ = manager.list()
        if bstack1l_opy_(args):
          for index, platform in enumerate(CONFIG[bstack1lllllll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪผ")]):
            if index == 0:
              bstack1111llll_opy_[bstack1lllllll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫฝ")] = args
            bstack11ll11l1l_opy_.append(multiprocessing.Process(name=str(index),
                                          target=run_on_browserstack, args=(bstack1111llll_opy_, bstack11l11lll1_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack1lllllll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬพ")]):
            bstack11ll11l1l_opy_.append(multiprocessing.Process(name=str(index),
                                          target=run_on_browserstack, args=(bstack1111llll_opy_, bstack11l11lll1_opy_)))
        for t in bstack11ll11l1l_opy_:
          t.start()
        for t in bstack11ll11l1l_opy_:
          t.join()
        bstack1lllll1ll_opy_ = list(bstack11l11lll1_opy_)
      else:
        if bstack1l_opy_(args):
          bstack1111llll_opy_[bstack1lllllll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ฟ")] = args
          test = multiprocessing.Process(name=str(0),
                                        target=run_on_browserstack, args=(bstack1111llll_opy_,))
          test.start()
          test.join()
        else:
          bstack1ll11llll_opy_(bstack1ll11111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1lllllll1_opy_ (u"ࠫࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠭ภ")] = bstack1lllllll1_opy_ (u"ࠬࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠧม")
          mod_globals[bstack1lllllll1_opy_ (u"࠭࡟ࡠࡨ࡬ࡰࡪࡥ࡟ࠨย")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1lll111ll_opy_ == bstack1lllllll1_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ร") or bstack1lll111ll_opy_ == bstack1lllllll1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧฤ"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack1111111l_opy_(e, bstack1lll1l1ll_opy_)
    bstack1l11lll1l_opy_()
    bstack1ll11llll_opy_(bstack1ll111lll_opy_)
    if bstack1lllllll1_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧล") in args:
      i = args.index(bstack1lllllll1_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨฦ"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1ll111l_opy_))
    args.insert(0, str(bstack1lllllll1_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩว")))
    pabot.main(args)
  elif bstack1lll111ll_opy_ == bstack1lllllll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ศ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1111111l_opy_(e, bstack1lll1l1ll_opy_)
    for a in args:
      if bstack1lllllll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬษ") in a:
        bstack111l11l_opy_ = int(a.split(bstack1lllllll1_opy_ (u"ࠧ࠻ࠩส"))[1])
      if bstack1lllllll1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬห") in a:
        bstack1lll11l1l_opy_ = str(a.split(bstack1lllllll1_opy_ (u"ࠩ࠽ࠫฬ"))[1])
      if bstack1lllllll1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕࠪอ") in a:
        bstack111l11l11_opy_ = str(a.split(bstack1lllllll1_opy_ (u"ࠫ࠿࠭ฮ"))[1])
    bstack11l1ll11l_opy_ = None
    if bstack1lllllll1_opy_ (u"ࠬ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠫฯ") in args:
      i = args.index(bstack1lllllll1_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠬะ"))
      args.pop(i)
      bstack11l1ll11l_opy_ = args.pop(i)
    if bstack11l1ll11l_opy_ is not None:
      global bstack11ll1l111_opy_
      bstack11ll1l111_opy_ = bstack11l1ll11l_opy_
    bstack1ll11llll_opy_(bstack1ll111lll_opy_)
    run_cli(args)
  elif bstack1lll111ll_opy_ == bstack1lllllll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧั"):
    try:
      from _pytest.config import _prepareconfig
      from _pytest.config import Config
      from _pytest import runner
      import importlib
      bstack11lll_opy_ = importlib.find_loader(bstack1lllllll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠪา"))
    except Exception as e:
      logger.warn(e, bstack11l111111_opy_)
    bstack1l11lll1l_opy_()
    try:
      if bstack1lllllll1_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫำ") in args:
        i = args.index(bstack1lllllll1_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬิ"))
        args.pop(i+1)
        args.pop(i)
      if bstack1lllllll1_opy_ (u"ࠫ࠲࠳ࡰ࡭ࡷࡪ࡭ࡳࡹࠧี") in args:
        i = args.index(bstack1lllllll1_opy_ (u"ࠬ࠳࠭ࡱ࡮ࡸ࡫࡮ࡴࡳࠨึ"))
        args.pop(i+1)
        args.pop(i)
      if bstack1lllllll1_opy_ (u"࠭࠭ࡱࠩื") in args:
        i = args.index(bstack1lllllll1_opy_ (u"ࠧ࠮ࡲุࠪ"))
        args.pop(i+1)
        args.pop(i)
      if bstack1lllllll1_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴูࠩ") in args:
        i = args.index(bstack1lllllll1_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵฺࠪ"))
        args.pop(i+1)
        args.pop(i)
      if bstack1lllllll1_opy_ (u"ࠪ࠱ࡳ࠭฻") in args:
        i = args.index(bstack1lllllll1_opy_ (u"ࠫ࠲ࡴࠧ฼"))
        args.pop(i+1)
        args.pop(i)
    except Exception as exc:
      logger.error(str(exc))
    config = _prepareconfig(args)
    bstack11ll1_opy_ = config.args
    bstack11l1ll11_opy_ = config.invocation_params.args
    bstack11l1ll11_opy_ = list(bstack11l1ll11_opy_)
    bstack1lll11ll1_opy_ = [os.path.normpath(item) for item in bstack11ll1_opy_]
    bstack1llll11ll_opy_ = [os.path.normpath(item) for item in bstack11l1ll11_opy_]
    bstack11111l1l_opy_ = [item for item in bstack1llll11ll_opy_ if item not in bstack1lll11ll1_opy_]
    if bstack1lllllll1_opy_ (u"ࠬ࠳࠭ࡤࡣࡦ࡬ࡪ࠳ࡣ࡭ࡧࡤࡶࠬ฽") not in bstack11111l1l_opy_:
      bstack11111l1l_opy_.append(bstack1lllllll1_opy_ (u"࠭࠭࠮ࡥࡤࡧ࡭࡫࠭ࡤ࡮ࡨࡥࡷ࠭฾"))
    import platform as pf
    if pf.system().lower() == bstack1lllllll1_opy_ (u"ࠧࡸ࡫ࡱࡨࡴࡽࡳࠨ฿"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11ll1_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11ll1l1l1_opy_)))
                    for bstack11ll1l1l1_opy_ in bstack11ll1_opy_]
    if (bstack1llll1lll_opy_):
      bstack11111l1l_opy_.append(bstack1lllllll1_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬเ"))
      bstack11111l1l_opy_.append(bstack1lllllll1_opy_ (u"ࠩࡗࡶࡺ࡫ࠧแ"))
    try:
      from pytest_bdd import reporting
      bstack11l1l1l11_opy_ = True
    except Exception as e:
      pass
    if (not bstack11l1l1l11_opy_):
      bstack11111l1l_opy_.append(bstack1lllllll1_opy_ (u"ࠪ࠱ࡵ࠭โ"))
      bstack11111l1l_opy_.append(bstack1lllllll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠩใ"))
    bstack11111l1l_opy_.append(bstack1lllllll1_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧไ"))
    bstack11111l1l_opy_.append(bstack1lllllll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ๅ"))
    bstack1l111ll1_opy_ = []
    for spec in bstack11ll1_opy_:
      bstack11l11llll_opy_ = []
      bstack11l11llll_opy_.append(spec)
      bstack11l11llll_opy_ += bstack11111l1l_opy_
      bstack1l111ll1_opy_.append(bstack11l11llll_opy_)
    bstack11l11l1l_opy_ = True
    bstack1lllll11_opy_ = 1
    if bstack1lllllll1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧๆ") in CONFIG:
      bstack1lllll11_opy_ = CONFIG[bstack1lllllll1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ็")]
    bstack1lll1l1l1_opy_ = int(bstack1lllll11_opy_)*int(len(CONFIG[bstack1lllllll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷ่ࠬ")]))
    execution_items = []
    for bstack11l11llll_opy_ in bstack1l111ll1_opy_:
      for index, _ in enumerate(CONFIG[bstack1lllllll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ้࠭")]):
        item = {}
        item[bstack1lllllll1_opy_ (u"ࠫࡦࡸࡧࠨ๊")] = bstack11l11llll_opy_
        item[bstack1lllllll1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻ๋ࠫ")] = index
        execution_items.append(item)
    bstack111l1l11l_opy_ = bstack1l11l1ll1_opy_(execution_items, bstack1lll1l1l1_opy_)
    for execution_item in bstack111l1l11l_opy_:
      bstack11ll11l1l_opy_ = []
      for item in execution_item:
        bstack11ll11l1l_opy_.append(bstack11lll11ll_opy_(name=str(item[bstack1lllllll1_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ์")]),
                                            target=bstack1ll111ll1_opy_,
                                            args=(item[bstack1lllllll1_opy_ (u"ࠧࡢࡴࡪࠫํ")],)))
      for t in bstack11ll11l1l_opy_:
        t.start()
      for t in bstack11ll11l1l_opy_:
        t.join()
  elif bstack1lll111ll_opy_ == bstack1lllllll1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ๎"):
    try:
      from behave.__main__ import main as bstack1l1lll11_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1111111l_opy_(e, bstack11l1l1ll1_opy_)
    bstack1l11lll1l_opy_()
    bstack11l11l1l_opy_ = True
    bstack1lllll11_opy_ = 1
    if bstack1lllllll1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ๏") in CONFIG:
      bstack1lllll11_opy_ = CONFIG[bstack1lllllll1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ๐")]
    bstack1lll1l1l1_opy_ = int(bstack1lllll11_opy_)*int(len(CONFIG[bstack1lllllll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ๑")]))
    config = Configuration(args)
    bstack111l1111l_opy_ = config.paths
    if len(bstack111l1111l_opy_) == 0:
      import glob
      pattern = bstack1lllllll1_opy_ (u"ࠬ࠰ࠪ࠰ࠬ࠱ࡪࡪࡧࡴࡶࡴࡨࠫ๒")
      bstack11l1lll11_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack11l1lll11_opy_)
      config = Configuration(args)
      bstack111l1111l_opy_ = config.paths
    bstack11ll1_opy_ = [os.path.normpath(item) for item in bstack111l1111l_opy_]
    bstack11111ll1_opy_ = [os.path.normpath(item) for item in args]
    bstack1l1ll1l1l_opy_ = [item for item in bstack11111ll1_opy_ if item not in bstack11ll1_opy_]
    import platform as pf
    if pf.system().lower() == bstack1lllllll1_opy_ (u"࠭ࡷࡪࡰࡧࡳࡼࡹࠧ๓"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11ll1_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11ll1l1l1_opy_)))
                    for bstack11ll1l1l1_opy_ in bstack11ll1_opy_]
    bstack1l111ll1_opy_ = []
    for spec in bstack11ll1_opy_:
      bstack11l11llll_opy_ = []
      bstack11l11llll_opy_ += bstack1l1ll1l1l_opy_
      bstack11l11llll_opy_.append(spec)
      bstack1l111ll1_opy_.append(bstack11l11llll_opy_)
    execution_items = []
    for bstack11l11llll_opy_ in bstack1l111ll1_opy_:
      for index, _ in enumerate(CONFIG[bstack1lllllll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ๔")]):
        item = {}
        item[bstack1lllllll1_opy_ (u"ࠨࡣࡵ࡫ࠬ๕")] = bstack1lllllll1_opy_ (u"ࠩࠣࠫ๖").join(bstack11l11llll_opy_)
        item[bstack1lllllll1_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ๗")] = index
        execution_items.append(item)
    bstack111l1l11l_opy_ = bstack1l11l1ll1_opy_(execution_items, bstack1lll1l1l1_opy_)
    for execution_item in bstack111l1l11l_opy_:
      bstack11ll11l1l_opy_ = []
      for item in execution_item:
        bstack11ll11l1l_opy_.append(bstack11lll11ll_opy_(name=str(item[bstack1lllllll1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ๘")]),
                                            target=bstack1lll1lll1_opy_,
                                            args=(item[bstack1lllllll1_opy_ (u"ࠬࡧࡲࡨࠩ๙")],)))
      for t in bstack11ll11l1l_opy_:
        t.start()
      for t in bstack11ll11l1l_opy_:
        t.join()
  else:
    bstack11l11_opy_(bstack1l1111111_opy_)
  if not bstack11111111_opy_:
    bstack1l1lll11l_opy_()
def browserstack_initialize(bstack1l111lll1_opy_=None):
  run_on_browserstack(bstack1l111lll1_opy_, None, True)
def bstack1l1lll11l_opy_():
  [bstack11ll11lll_opy_, bstack1l1l1lll_opy_] = bstack1l11111l_opy_()
  if bstack11ll11lll_opy_ is not None and bstack11ll11111_opy_() != -1:
    sessions = bstack1111l1ll_opy_(bstack11ll11lll_opy_)
    bstack11ll1l11l_opy_(sessions, bstack1l1l1lll_opy_)
def bstack1l1l1ll1_opy_(bstack11llllll1_opy_):
    if bstack11llllll1_opy_:
        return bstack11llllll1_opy_.capitalize()
    else:
        return bstack11llllll1_opy_
def bstack1ll1l111_opy_(bstack1llll1_opy_):
    if bstack1lllllll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ๚") in bstack1llll1_opy_ and bstack1llll1_opy_[bstack1lllllll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ๛")] != bstack1lllllll1_opy_ (u"ࠨࠩ๜"):
        return bstack1llll1_opy_[bstack1lllllll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ๝")]
    else:
        bstack1111l1_opy_ = bstack1lllllll1_opy_ (u"ࠥࠦ๞")
        if bstack1lllllll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ๟") in bstack1llll1_opy_ and bstack1llll1_opy_[bstack1lllllll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ๠")] != None:
            bstack1111l1_opy_ += bstack1llll1_opy_[bstack1lllllll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭๡")] + bstack1lllllll1_opy_ (u"ࠢ࠭ࠢࠥ๢")
            if bstack1llll1_opy_[bstack1lllllll1_opy_ (u"ࠨࡱࡶࠫ๣")] == bstack1lllllll1_opy_ (u"ࠤ࡬ࡳࡸࠨ๤"):
                bstack1111l1_opy_ += bstack1lllllll1_opy_ (u"ࠥ࡭ࡔ࡙ࠠࠣ๥")
            bstack1111l1_opy_ += (bstack1llll1_opy_[bstack1lllllll1_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ๦")] or bstack1lllllll1_opy_ (u"ࠬ࠭๧"))
            return bstack1111l1_opy_
        else:
            bstack1111l1_opy_ += bstack1l1l1ll1_opy_(bstack1llll1_opy_[bstack1lllllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ๨")]) + bstack1lllllll1_opy_ (u"ࠢࠡࠤ๩") + (bstack1llll1_opy_[bstack1lllllll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ๪")] or bstack1lllllll1_opy_ (u"ࠩࠪ๫")) + bstack1lllllll1_opy_ (u"ࠥ࠰ࠥࠨ๬")
            if bstack1llll1_opy_[bstack1lllllll1_opy_ (u"ࠫࡴࡹࠧ๭")] == bstack1lllllll1_opy_ (u"ࠧ࡝ࡩ࡯ࡦࡲࡻࡸࠨ๮"):
                bstack1111l1_opy_ += bstack1lllllll1_opy_ (u"ࠨࡗࡪࡰࠣࠦ๯")
            bstack1111l1_opy_ += bstack1llll1_opy_[bstack1lllllll1_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫ๰")] or bstack1lllllll1_opy_ (u"ࠨࠩ๱")
            return bstack1111l1_opy_
def bstack1lll1l11_opy_(bstack1ll111l1l_opy_):
    if bstack1ll111l1l_opy_ == bstack1lllllll1_opy_ (u"ࠤࡧࡳࡳ࡫ࠢ๲"):
        return bstack1lllllll1_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿࡭ࡲࡦࡧࡱ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧ࡭ࡲࡦࡧࡱࠦࡃࡉ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭๳")
    elif bstack1ll111l1l_opy_ == bstack1lllllll1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ๴"):
        return bstack1lllllll1_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡳࡧࡧ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡸࡥࡥࠤࡁࡊࡦ࡯࡬ࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ๵")
    elif bstack1ll111l1l_opy_ == bstack1lllllll1_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ๶"):
        return bstack1lllllll1_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡪࡶࡪ࡫࡮࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡪࡶࡪ࡫࡮ࠣࡀࡓࡥࡸࡹࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ๷")
    elif bstack1ll111l1l_opy_ == bstack1lllllll1_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ๸"):
        return bstack1lllllll1_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡷ࡫ࡤ࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡵࡩࡩࠨ࠾ࡆࡴࡵࡳࡷࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ๹")
    elif bstack1ll111l1l_opy_ == bstack1lllllll1_opy_ (u"ࠥࡸ࡮ࡳࡥࡰࡷࡷࠦ๺"):
        return bstack1lllllll1_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࠣࡦࡧࡤ࠷࠷࠼࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࠥࡨࡩࡦ࠹࠲࠷ࠤࡁࡘ࡮ࡳࡥࡰࡷࡷࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ๻")
    elif bstack1ll111l1l_opy_ == bstack1lllllll1_opy_ (u"ࠧࡸࡵ࡯ࡰ࡬ࡲ࡬ࠨ๼"):
        return bstack1lllllll1_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡤ࡯ࡥࡨࡱ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡤ࡯ࡥࡨࡱࠢ࠿ࡔࡸࡲࡳ࡯࡮ࡨ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ๽")
    else:
        return bstack1lllllll1_opy_ (u"ࠧ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡦࡱࡧࡣ࡬࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡦࡱࡧࡣ࡬ࠤࡁࠫ๾")+bstack1l1l1ll1_opy_(bstack1ll111l1l_opy_)+bstack1lllllll1_opy_ (u"ࠨ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ๿")
def bstack11ll111l_opy_(session):
    return bstack1lllllll1_opy_ (u"ࠩ࠿ࡸࡷࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡲࡰࡹࠥࡂࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠦࡳࡦࡵࡶ࡭ࡴࡴ࠭࡯ࡣࡰࡩࠧࡄ࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࡽࢀࠦࠥࡺࡡࡳࡩࡨࡸࡂࠨ࡟ࡣ࡮ࡤࡲࡰࠨ࠾ࡼࡿ࠿࠳ࡦࡄ࠼࠰ࡶࡧࡂࢀࢃࡻࡾ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀ࠴ࡺࡲ࠿ࠩ຀").format(session[bstack1lllllll1_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧກ")],bstack1ll1l111_opy_(session), bstack1lll1l11_opy_(session[bstack1lllllll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡹࡧࡴࡶࡵࠪຂ")]), bstack1lll1l11_opy_(session[bstack1lllllll1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ຃")]), bstack1l1l1ll1_opy_(session[bstack1lllllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧຄ")] or session[bstack1lllllll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ຅")] or bstack1lllllll1_opy_ (u"ࠨࠩຆ")) + bstack1lllllll1_opy_ (u"ࠤࠣࠦງ") + (session[bstack1lllllll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬຈ")] or bstack1lllllll1_opy_ (u"ࠫࠬຉ")), session[bstack1lllllll1_opy_ (u"ࠬࡵࡳࠨຊ")] + bstack1lllllll1_opy_ (u"ࠨࠠࠣ຋") + session[bstack1lllllll1_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫຌ")], session[bstack1lllllll1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪຍ")] or bstack1lllllll1_opy_ (u"ࠩࠪຎ"), session[bstack1lllllll1_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺࠧຏ")] if session[bstack1lllllll1_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨຐ")] else bstack1lllllll1_opy_ (u"ࠬ࠭ຑ"))
def bstack11ll1l11l_opy_(sessions, bstack1l1l1lll_opy_):
  try:
    bstack11l111l_opy_ = bstack1lllllll1_opy_ (u"ࠨࠢຒ")
    if not os.path.exists(bstack1llll1l1_opy_):
      os.mkdir(bstack1llll1l1_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lllllll1_opy_ (u"ࠧࡢࡵࡶࡩࡹࡹ࠯ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰࠬຓ")), bstack1lllllll1_opy_ (u"ࠨࡴࠪດ")) as f:
      bstack11l111l_opy_ = f.read()
    bstack11l111l_opy_ = bstack11l111l_opy_.replace(bstack1lllllll1_opy_ (u"ࠩࡾࠩࡗࡋࡓࡖࡎࡗࡗࡤࡉࡏࡖࡐࡗࠩࢂ࠭ຕ"), str(len(sessions)))
    bstack11l111l_opy_ = bstack11l111l_opy_.replace(bstack1lllllll1_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠦࡿࠪຖ"), bstack1l1l1lll_opy_)
    bstack11l111l_opy_ = bstack11l111l_opy_.replace(bstack1lllllll1_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤࡔࡁࡎࡇࠨࢁࠬທ"), sessions[0].get(bstack1lllllll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡳࡧ࡭ࡦࠩຘ")) if sessions[0] else bstack1lllllll1_opy_ (u"࠭ࠧນ"))
    with open(os.path.join(bstack1llll1l1_opy_, bstack1lllllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫບ")), bstack1lllllll1_opy_ (u"ࠨࡹࠪປ")) as stream:
      stream.write(bstack11l111l_opy_.split(bstack1lllllll1_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ࠭ຜ"))[0])
      for session in sessions:
        stream.write(bstack11ll111l_opy_(session))
      stream.write(bstack11l111l_opy_.split(bstack1lllllll1_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃࠧຝ"))[1])
    logger.info(bstack1lllllll1_opy_ (u"ࠫࡌ࡫࡮ࡦࡴࡤࡸࡪࡪࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡢࡶ࡫࡯ࡨࠥࡧࡲࡵ࡫ࡩࡥࡨࡺࡳࠡࡣࡷࠤࢀࢃࠧພ").format(bstack1llll1l1_opy_));
  except Exception as e:
    logger.debug(bstack1l1l11l_opy_.format(str(e)))
def bstack1111l1ll_opy_(bstack11ll11lll_opy_):
  global CONFIG
  try:
    host = bstack1lllllll1_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨຟ") if bstack1lllllll1_opy_ (u"࠭ࡡࡱࡲࠪຠ") in CONFIG else bstack1lllllll1_opy_ (u"ࠧࡢࡲ࡬ࠫມ")
    user = CONFIG[bstack1lllllll1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪຢ")]
    key = CONFIG[bstack1lllllll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬຣ")]
    bstack111llll_opy_ = bstack1lllllll1_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ຤") if bstack1lllllll1_opy_ (u"ࠫࡦࡶࡰࠨລ") in CONFIG else bstack1lllllll1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ຦")
    url = bstack1lllllll1_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠴ࡪࡴࡱࡱࠫວ").format(user, key, host, bstack111llll_opy_, bstack11ll11lll_opy_)
    headers = {
      bstack1lllllll1_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭ຨ"): bstack1lllllll1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫຩ"),
    }
    proxies = bstack1l11l111l_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack1lllllll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠧສ")], response.json()))
  except Exception as e:
    logger.debug(bstack111ll11l_opy_.format(str(e)))
def bstack1l11111l_opy_():
  global CONFIG
  try:
    if bstack1lllllll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ຫ") in CONFIG:
      host = bstack1lllllll1_opy_ (u"ࠫࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪࠧຬ") if bstack1lllllll1_opy_ (u"ࠬࡧࡰࡱࠩອ") in CONFIG else bstack1lllllll1_opy_ (u"࠭ࡡࡱ࡫ࠪຮ")
      user = CONFIG[bstack1lllllll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩຯ")]
      key = CONFIG[bstack1lllllll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫະ")]
      bstack111llll_opy_ = bstack1lllllll1_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨັ") if bstack1lllllll1_opy_ (u"ࠪࡥࡵࡶࠧາ") in CONFIG else bstack1lllllll1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ຳ")
      url = bstack1lllllll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࢁࡽ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠮࡫ࡵࡲࡲࠬິ").format(user, key, host, bstack111llll_opy_)
      headers = {
        bstack1lllllll1_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬີ"): bstack1lllllll1_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪຶ"),
      }
      if bstack1lllllll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪື") in CONFIG:
        params = {bstack1lllllll1_opy_ (u"ࠩࡱࡥࡲ࡫ຸࠧ"):CONFIG[bstack1lllllll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪູ࠭")], bstack1lllllll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ຺ࠧ"):CONFIG[bstack1lllllll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧົ")]}
      else:
        params = {bstack1lllllll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫຼ"):CONFIG[bstack1lllllll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪຽ")]}
      proxies = bstack1l11l111l_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack11l1111ll_opy_ = response.json()[0][bstack1lllllll1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡨࡵࡪ࡮ࡧࠫ຾")]
        if bstack11l1111ll_opy_:
          bstack1l1l1lll_opy_ = bstack11l1111ll_opy_[bstack1lllllll1_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭຿")].split(bstack1lllllll1_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥ࠰ࡦࡺ࡯࡬ࡥࠩເ"))[0] + bstack1lllllll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡶ࠳ࠬແ") + bstack11l1111ll_opy_[bstack1lllllll1_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨໂ")]
          logger.info(bstack1l1ll111l_opy_.format(bstack1l1l1lll_opy_))
          bstack1lll1l1_opy_ = CONFIG[bstack1lllllll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩໃ")]
          if bstack1lllllll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩໄ") in CONFIG:
            bstack1lll1l1_opy_ += bstack1lllllll1_opy_ (u"ࠨࠢࠪ໅") + CONFIG[bstack1lllllll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫໆ")]
          if bstack1lll1l1_opy_!= bstack11l1111ll_opy_[bstack1lllllll1_opy_ (u"ࠪࡲࡦࡳࡥࠨ໇")]:
            logger.debug(bstack1l1llllll_opy_.format(bstack11l1111ll_opy_[bstack1lllllll1_opy_ (u"ࠫࡳࡧ࡭ࡦ່ࠩ")], bstack1lll1l1_opy_))
          return [bstack11l1111ll_opy_[bstack1lllllll1_opy_ (u"ࠬ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ້")], bstack1l1l1lll_opy_]
    else:
      logger.warn(bstack1l111ll11_opy_)
  except Exception as e:
    logger.debug(bstack11l1111l1_opy_.format(str(e)))
  return [None, None]
def bstack1l1l1lll1_opy_(url, bstack11llll1l1_opy_=False):
  global CONFIG
  global bstack1ll1l_opy_
  if not bstack1ll1l_opy_:
    hostname = bstack11lll11l1_opy_(url)
    is_private = bstack1l11l1_opy_(hostname)
    if (bstack1lllllll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮໊ࠪ") in CONFIG and not CONFIG[bstack1lllllll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯໋ࠫ")]) and (is_private or bstack11llll1l1_opy_):
      bstack1ll1l_opy_ = hostname
def bstack11lll11l1_opy_(url):
  return urlparse(url).hostname
def bstack1l11l1_opy_(hostname):
  for bstack11ll1l11_opy_ in bstack1ll111ll_opy_:
    regex = re.compile(bstack11ll1l11_opy_)
    if regex.match(hostname):
      return True
  return False