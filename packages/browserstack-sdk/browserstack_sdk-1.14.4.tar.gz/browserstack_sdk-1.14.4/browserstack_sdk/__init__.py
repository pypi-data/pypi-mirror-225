# coding: UTF-8
import sys
bstack1lll1l1l_opy_ = sys.version_info [0] == 2
bstack1l11l1l_opy_ = 2048
bstack1l111lll1_opy_ = 7
def bstack11l11lll1_opy_ (bstack1lll11ll1_opy_):
    global bstack11l11llll_opy_
    stringNr = ord (bstack1lll11ll1_opy_ [-1])
    bstack1llll1lll_opy_ = bstack1lll11ll1_opy_ [:-1]
    bstack1l1l1ll11_opy_ = stringNr % len (bstack1llll1lll_opy_)
    bstack1llll111l_opy_ = bstack1llll1lll_opy_ [:bstack1l1l1ll11_opy_] + bstack1llll1lll_opy_ [bstack1l1l1ll11_opy_:]
    if bstack1lll1l1l_opy_:
        bstack1l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11l1l_opy_ - (bstack111ll11l1_opy_ + stringNr) % bstack1l111lll1_opy_) for bstack111ll11l1_opy_, char in enumerate (bstack1llll111l_opy_)])
    else:
        bstack1l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1l11l1l_opy_ - (bstack111ll11l1_opy_ + stringNr) % bstack1l111lll1_opy_) for bstack111ll11l1_opy_, char in enumerate (bstack1llll111l_opy_)])
    return eval (bstack1l1ll1_opy_)
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
bstack1lllllll1_opy_ = {
	bstack11l11lll1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࠀ"): bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡳࠩࠁ"),
  bstack11l11lll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩࠂ"): bstack11l11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡫ࡦࡻࠪࠃ"),
  bstack11l11lll1_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫࠄ"): bstack11l11lll1_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ࠅ"),
  bstack11l11lll1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪࠆ"): bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫࡟ࡸ࠵ࡦࠫࠇ"),
  bstack11l11lll1_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪࠈ"): bstack11l11lll1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࠧࠉ"),
  bstack11l11lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪࠊ"): bstack11l11lll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧࠋ"),
  bstack11l11lll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࠌ"): bstack11l11lll1_opy_ (u"ࠪࡲࡦࡳࡥࠨࠍ"),
  bstack11l11lll1_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪࠎ"): bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩࠪࠏ"),
  bstack11l11lll1_opy_ (u"࠭ࡣࡰࡰࡶࡳࡱ࡫ࡌࡰࡩࡶࠫࠐ"): bstack11l11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰࡰࡶࡳࡱ࡫ࠧࠑ"),
  bstack11l11lll1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭ࠒ"): bstack11l11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸ࠭ࠓ"),
  bstack11l11lll1_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧࠔ"): bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧࠕ"),
  bstack11l11lll1_opy_ (u"ࠬࡼࡩࡥࡧࡲࠫࠖ"): bstack11l11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡼࡩࡥࡧࡲࠫࠗ"),
  bstack11l11lll1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭࠘"): bstack11l11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡎࡲ࡫ࡸ࠭࠙"),
  bstack11l11lll1_opy_ (u"ࠩࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩࠚ"): bstack11l11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡱ࡫࡭ࡦࡶࡵࡽࡑࡵࡧࡴࠩࠛ"),
  bstack11l11lll1_opy_ (u"ࠫ࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩࠜ"): bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡯ࡍࡱࡦࡥࡹ࡯࡯࡯ࠩࠝ"),
  bstack11l11lll1_opy_ (u"࠭ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨࠞ"): bstack11l11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡪ࡯ࡨࡾࡴࡴࡥࠨࠟ"),
  bstack11l11lll1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࠠ"): bstack11l11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫࠡ"),
  bstack11l11lll1_opy_ (u"ࠪࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩࠢ"): bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡱࡦࡹ࡫ࡄࡱࡰࡱࡦࡴࡤࡴࠩࠣ"),
  bstack11l11lll1_opy_ (u"ࠬ࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪࠤ"): bstack11l11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡯ࡤ࡭ࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪࠥ"),
  bstack11l11lll1_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧࠦ"): bstack11l11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧࠧ"),
  bstack11l11lll1_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡶࠫࠨ"): bstack11l11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡶࡩࡳࡪࡋࡦࡻࡶࠫࠩ"),
  bstack11l11lll1_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭ࠪ"): bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡙ࡤ࡭ࡹ࠭ࠫ"),
  bstack11l11lll1_opy_ (u"࠭ࡨࡰࡵࡷࡷࠬࠬ"): bstack11l11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡨࡰࡵࡷࡷࠬ࠭"),
  bstack11l11lll1_opy_ (u"ࠨࡤࡩࡧࡦࡩࡨࡦࠩ࠮"): bstack11l11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡩࡧࡦࡩࡨࡦࠩ࠯"),
  bstack11l11lll1_opy_ (u"ࠪࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫ࠰"): bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡻࡸࡒ࡯ࡤࡣ࡯ࡗࡺࡶࡰࡰࡴࡷࠫ࠱"),
  bstack11l11lll1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ࠲"): bstack11l11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ࠳"),
  bstack11l11lll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ࠴"): bstack11l11lll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ࠵"),
  bstack11l11lll1_opy_ (u"ࠩࡵࡩࡦࡲࡍࡰࡤ࡬ࡰࡪ࠭࠶"): bstack11l11lll1_opy_ (u"ࠪࡶࡪࡧ࡬ࡠ࡯ࡲࡦ࡮ࡲࡥࠨ࠷"),
  bstack11l11lll1_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ࠸"): bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡶࡰࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ࠹"),
  bstack11l11lll1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭࠺"): bstack11l11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡶࡵࡷࡳࡲࡔࡥࡵࡹࡲࡶࡰ࠭࠻"),
  bstack11l11lll1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩ࠼"): bstack11l11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩ࠽"),
  bstack11l11lll1_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩ࠾"): bstack11l11lll1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࡷࠬ࠿"),
  bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧࡀ"): bstack11l11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧࡁ"),
  bstack11l11lll1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧࡂ"): bstack11l11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡱࡸࡶࡨ࡫ࠧࡃ"),
  bstack11l11lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࡄ"): bstack11l11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࡅ"),
  bstack11l11lll1_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ࡆ"): bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ࡇ"),
}
bstack1ll1ll111_opy_ = [
  bstack11l11lll1_opy_ (u"࠭࡯ࡴࠩࡈ"),
  bstack11l11lll1_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪࡉ"),
  bstack11l11lll1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࡊ"),
  bstack11l11lll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࡋ"),
  bstack11l11lll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧࡌ"),
  bstack11l11lll1_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨࡍ"),
  bstack11l11lll1_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬࡎ"),
]
bstack11ll1l1_opy_ = {
  bstack11l11lll1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࡏ"): [bstack11l11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨࡐ"), bstack11l11lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡤࡔࡁࡎࡇࠪࡑ")],
  bstack11l11lll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬࡒ"): bstack11l11lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ࡓ"),
  bstack11l11lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࡔ"): bstack11l11lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠨࡕ"),
  bstack11l11lll1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫࡖ"): bstack11l11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡏࡃࡐࡉࠬࡗ"),
  bstack11l11lll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࡘ"): bstack11l11lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕ࡙ࠫ"),
  bstack11l11lll1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯࡚ࠪ"): bstack11l11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡆࡘࡁࡍࡎࡈࡐࡘࡥࡐࡆࡔࡢࡔࡑࡇࡔࡇࡑࡕࡑ࡛ࠬ"),
  bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ࡜"): bstack11l11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࠫ࡝"),
  bstack11l11lll1_opy_ (u"ࠧࡳࡧࡵࡹࡳ࡚ࡥࡴࡶࡶࠫ࡞"): bstack11l11lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠬ࡟"),
  bstack11l11lll1_opy_ (u"ࠩࡤࡴࡵ࠭ࡠ"): [bstack11l11lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡔࡕࡥࡉࡅࠩࡡ"), bstack11l11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡕࡖࠧࡢ")],
  bstack11l11lll1_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧࡣ"): bstack11l11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࡤࡊࡅࡃࡗࡊࠫࡤ"),
  bstack11l11lll1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫࡥ"): bstack11l11lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫࡦ")
}
bstack1l11llll1_opy_ = {
  bstack11l11lll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࡧ"): [bstack11l11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸ࡟࡯ࡣࡰࡩࠬࡨ"), bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࡩ")],
  bstack11l11lll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࡪ"): [bstack11l11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡤࡱࡥࡺࠩ࡫"), bstack11l11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ࡬")],
  bstack11l11lll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡭"): bstack11l11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ࡮"),
  bstack11l11lll1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ࡯"): bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨࡰ"),
  bstack11l11lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡱ"): bstack11l11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࡲ"),
  bstack11l11lll1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧࡳ"): [bstack11l11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡲࡳࠫࡴ"), bstack11l11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࡵ")],
  bstack11l11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࡶ"): bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩࡷ"),
  bstack11l11lll1_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡸ"): bstack11l11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩࡹ"),
  bstack11l11lll1_opy_ (u"ࠧࡢࡲࡳࠫࡺ"): bstack11l11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳࠫࡻ"),
  bstack11l11lll1_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡼ"): bstack11l11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫࡽ"),
  bstack11l11lll1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡾ"): bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨࡿ")
}
bstack11ll1ll_opy_ = {
  bstack11l11lll1_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩࢀ"): bstack11l11lll1_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫࢁ"),
  bstack11l11lll1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪࢂ"): [bstack11l11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫࢃ"), bstack11l11lll1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ࢄ")],
  bstack11l11lll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢅ"): bstack11l11lll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪࢆ"),
  bstack11l11lll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪࢇ"): bstack11l11lll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ࢈"),
  bstack11l11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ࢉ"): [bstack11l11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪࢊ"), bstack11l11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩࢋ")],
  bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢌ"): bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧࢍ"),
  bstack11l11lll1_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪࢎ"): bstack11l11lll1_opy_ (u"ࠧࡳࡧࡤࡰࡤࡳ࡯ࡣ࡫࡯ࡩࠬ࢏"),
  bstack11l11lll1_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࢐"): [bstack11l11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ࢑"), bstack11l11lll1_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫ࢒")],
  bstack11l11lll1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪ࢓"): [bstack11l11lll1_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࡸ࠭࢔"), bstack11l11lll1_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹ࡙ࡳ࡭ࡅࡨࡶࡹ࠭࢕")]
}
bstack1111l11l_opy_ = [
  bstack11l11lll1_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭࢖"),
  bstack11l11lll1_opy_ (u"ࠨࡲࡤ࡫ࡪࡒ࡯ࡢࡦࡖࡸࡷࡧࡴࡦࡩࡼࠫࢗ"),
  bstack11l11lll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ࢘"),
  bstack11l11lll1_opy_ (u"ࠪࡷࡪࡺࡗࡪࡰࡧࡳࡼࡘࡥࡤࡶ࢙ࠪ"),
  bstack11l11lll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࢚࠭"),
  bstack11l11lll1_opy_ (u"ࠬࡹࡴࡳ࡫ࡦࡸࡋ࡯࡬ࡦࡋࡱࡸࡪࡸࡡࡤࡶࡤࡦ࡮ࡲࡩࡵࡻ࢛ࠪ"),
  bstack11l11lll1_opy_ (u"࠭ࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࡒࡵࡳࡲࡶࡴࡃࡧ࡫ࡥࡻ࡯࡯ࡳࠩ࢜"),
  bstack11l11lll1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ࢝"),
  bstack11l11lll1_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭࢞"),
  bstack11l11lll1_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ࢟"),
  bstack11l11lll1_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢠ"),
  bstack11l11lll1_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬࢡ"),
]
bstack1lll1l11_opy_ = [
  bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࢢ"),
  bstack11l11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢣ"),
  bstack11l11lll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢤ"),
  bstack11l11lll1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨࢥ"),
  bstack11l11lll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢦ"),
  bstack11l11lll1_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬࢧ"),
  bstack11l11lll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧࢨ"),
  bstack11l11lll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩࢩ"),
  bstack11l11lll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩࢪ"),
  bstack11l11lll1_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬࢫ")
]
bstack1l1ll11l_opy_ = [
  bstack11l11lll1_opy_ (u"ࠨࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭ࢬ"),
  bstack11l11lll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫࢭ"),
  bstack11l11lll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ࢮ"),
  bstack11l11lll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩࢯ"),
  bstack11l11lll1_opy_ (u"ࠬࡺࡥࡴࡶࡓࡶ࡮ࡵࡲࡪࡶࡼࠫࢰ"),
  bstack11l11lll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩࢱ"),
  bstack11l11lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩ࡚ࡡࡨࠩࢲ"),
  bstack11l11lll1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ࢳ"),
  bstack11l11lll1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫࢴ"),
  bstack11l11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࢵ"),
  bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬࢶ"),
  bstack11l11lll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫࢷ"),
  bstack11l11lll1_opy_ (u"࠭࡯ࡴࠩࢸ"),
  bstack11l11lll1_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪࢹ"),
  bstack11l11lll1_opy_ (u"ࠨࡪࡲࡷࡹࡹࠧࢺ"),
  bstack11l11lll1_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷࠫࢻ"),
  bstack11l11lll1_opy_ (u"ࠪࡶࡪ࡭ࡩࡰࡰࠪࢼ"),
  bstack11l11lll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭ࢽ"),
  bstack11l11lll1_opy_ (u"ࠬࡳࡡࡤࡪ࡬ࡲࡪ࠭ࢾ"),
  bstack11l11lll1_opy_ (u"࠭ࡲࡦࡵࡲࡰࡺࡺࡩࡰࡰࠪࢿ"),
  bstack11l11lll1_opy_ (u"ࠧࡪࡦ࡯ࡩ࡙࡯࡭ࡦࡱࡸࡸࠬࣀ"),
  bstack11l11lll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡐࡴ࡬ࡩࡳࡺࡡࡵ࡫ࡲࡲࠬࣁ"),
  bstack11l11lll1_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࠨࣂ"),
  bstack11l11lll1_opy_ (u"ࠪࡲࡴࡖࡡࡨࡧࡏࡳࡦࡪࡔࡪ࡯ࡨࡳࡺࡺࠧࣃ"),
  bstack11l11lll1_opy_ (u"ࠫࡧ࡬ࡣࡢࡥ࡫ࡩࠬࣄ"),
  bstack11l11lll1_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫࣅ"),
  bstack11l11lll1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪࣆ"),
  bstack11l11lll1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡓࡦࡰࡧࡏࡪࡿࡳࠨࣇ"),
  bstack11l11lll1_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬࣈ"),
  bstack11l11lll1_opy_ (u"ࠩࡱࡳࡕ࡯ࡰࡦ࡮࡬ࡲࡪ࠭ࣉ"),
  bstack11l11lll1_opy_ (u"ࠪࡧ࡭࡫ࡣ࡬ࡗࡕࡐࠬ࣊"),
  bstack11l11lll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣋"),
  bstack11l11lll1_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡈࡵ࡯࡬࡫ࡨࡷࠬ࣌"),
  bstack11l11lll1_opy_ (u"࠭ࡣࡢࡲࡷࡹࡷ࡫ࡃࡳࡣࡶ࡬ࠬ࣍"),
  bstack11l11lll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ࣎"),
  bstack11l11lll1_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࣏"),
  bstack11l11lll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࡜ࡥࡳࡵ࡬ࡳࡳ࣐࠭"),
  bstack11l11lll1_opy_ (u"ࠪࡲࡴࡈ࡬ࡢࡰ࡮ࡔࡴࡲ࡬ࡪࡰࡪ࣑ࠫ"),
  bstack11l11lll1_opy_ (u"ࠫࡲࡧࡳ࡬ࡕࡨࡲࡩࡑࡥࡺࡵ࣒ࠪ"),
  bstack11l11lll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡑࡵࡧࡴ࣓ࠩ"),
  bstack11l11lll1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡏࡤࠨࣔ"),
  bstack11l11lll1_opy_ (u"ࠧࡥࡧࡧ࡭ࡨࡧࡴࡦࡦࡇࡩࡻ࡯ࡣࡦࠩࣕ"),
  bstack11l11lll1_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡑࡣࡵࡥࡲࡹࠧࣖ"),
  bstack11l11lll1_opy_ (u"ࠩࡳ࡬ࡴࡴࡥࡏࡷࡰࡦࡪࡸࠧࣗ"),
  bstack11l11lll1_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࠨࣘ"),
  bstack11l11lll1_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡑࡳࡸ࡮ࡵ࡮ࡴࠩࣙ"),
  bstack11l11lll1_opy_ (u"ࠬࡩ࡯࡯ࡵࡲࡰࡪࡒ࡯ࡨࡵࠪࣚ"),
  bstack11l11lll1_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ࣛ"),
  bstack11l11lll1_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫࣜ"),
  bstack11l11lll1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡃ࡫ࡲࡱࡪࡺࡲࡪࡥࠪࣝ"),
  bstack11l11lll1_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࡗ࠴ࠪࣞ"),
  bstack11l11lll1_opy_ (u"ࠪࡱ࡮ࡪࡓࡦࡵࡶ࡭ࡴࡴࡉ࡯ࡵࡷࡥࡱࡲࡁࡱࡲࡶࠫࣟ"),
  bstack11l11lll1_opy_ (u"ࠫࡪࡹࡰࡳࡧࡶࡷࡴ࡙ࡥࡳࡸࡨࡶࠬ࣠"),
  bstack11l11lll1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫ࣡"),
  bstack11l11lll1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡄࡦࡳࠫ࣢"),
  bstack11l11lll1_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࣣࠧ"),
  bstack11l11lll1_opy_ (u"ࠨࡵࡼࡲࡨ࡚ࡩ࡮ࡧ࡚࡭ࡹ࡮ࡎࡕࡒࠪࣤ"),
  bstack11l11lll1_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧࣥ"),
  bstack11l11lll1_opy_ (u"ࠪ࡫ࡵࡹࡌࡰࡥࡤࡸ࡮ࡵ࡮ࠨࣦ"),
  bstack11l11lll1_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡕࡸ࡯ࡧ࡫࡯ࡩࠬࣧ"),
  bstack11l11lll1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡓ࡫ࡴࡸࡱࡵ࡯ࠬࣨ"),
  bstack11l11lll1_opy_ (u"࠭ࡦࡰࡴࡦࡩࡈ࡮ࡡ࡯ࡩࡨࡎࡦࡸࣩࠧ"),
  bstack11l11lll1_opy_ (u"ࠧࡹ࡯ࡶࡎࡦࡸࠧ࣪"),
  bstack11l11lll1_opy_ (u"ࠨࡺࡰࡼࡏࡧࡲࠨ࣫"),
  bstack11l11lll1_opy_ (u"ࠩࡰࡥࡸࡱࡃࡰ࡯ࡰࡥࡳࡪࡳࠨ࣬"),
  bstack11l11lll1_opy_ (u"ࠪࡱࡦࡹ࡫ࡃࡣࡶ࡭ࡨࡇࡵࡵࡪ࣭ࠪ"),
  bstack11l11lll1_opy_ (u"ࠫࡼࡹࡌࡰࡥࡤࡰࡘࡻࡰࡱࡱࡵࡸ࣮ࠬ"),
  bstack11l11lll1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡉ࡯ࡳࡵࡕࡩࡸࡺࡲࡪࡥࡷ࡭ࡴࡴࡳࠨ࣯"),
  bstack11l11lll1_opy_ (u"࠭ࡡࡱࡲ࡙ࡩࡷࡹࡩࡰࡰࣰࠪ"),
  bstack11l11lll1_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸࣱ࠭"),
  bstack11l11lll1_opy_ (u"ࠨࡴࡨࡷ࡮࡭࡮ࡂࡲࡳࣲࠫ"),
  bstack11l11lll1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࡸ࠭ࣳ"),
  bstack11l11lll1_opy_ (u"ࠪࡧࡦࡴࡡࡳࡻࠪࣴ"),
  bstack11l11lll1_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬࣵ"),
  bstack11l11lll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࣶࠬ"),
  bstack11l11lll1_opy_ (u"࠭ࡩࡦࠩࣷ"),
  bstack11l11lll1_opy_ (u"ࠧࡦࡦࡪࡩࠬࣸ"),
  bstack11l11lll1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨࣹ"),
  bstack11l11lll1_opy_ (u"ࠩࡴࡹࡪࡻࡥࠨࣺ"),
  bstack11l11lll1_opy_ (u"ࠪ࡭ࡳࡺࡥࡳࡰࡤࡰࠬࣻ"),
  bstack11l11lll1_opy_ (u"ࠫࡦࡶࡰࡔࡶࡲࡶࡪࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠬࣼ"),
  bstack11l11lll1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡈࡧ࡭ࡦࡴࡤࡍࡲࡧࡧࡦࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫࣽ"),
  bstack11l11lll1_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࡉࡽࡩ࡬ࡶࡦࡨࡌࡴࡹࡴࡴࠩࣾ"),
  bstack11l11lll1_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡎࡴࡣ࡭ࡷࡧࡩࡍࡵࡳࡵࡵࠪࣿ"),
  bstack11l11lll1_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡂࡲࡳࡗࡪࡺࡴࡪࡰࡪࡷࠬऀ"),
  bstack11l11lll1_opy_ (u"ࠩࡵࡩࡸ࡫ࡲࡷࡧࡇࡩࡻ࡯ࡣࡦࠩँ"),
  bstack11l11lll1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪं"),
  bstack11l11lll1_opy_ (u"ࠫࡸ࡫࡮ࡥࡍࡨࡽࡸ࠭ः"),
  bstack11l11lll1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡕࡧࡳࡴࡥࡲࡨࡪ࠭ऄ"),
  bstack11l11lll1_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡏ࡯ࡴࡆࡨࡺ࡮ࡩࡥࡔࡧࡷࡸ࡮ࡴࡧࡴࠩअ"),
  bstack11l11lll1_opy_ (u"ࠧࡦࡰࡤࡦࡱ࡫ࡁࡶࡦ࡬ࡳࡎࡴࡪࡦࡥࡷ࡭ࡴࡴࠧआ"),
  bstack11l11lll1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡂࡲࡳࡰࡪࡖࡡࡺࠩइ"),
  bstack11l11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪई"),
  bstack11l11lll1_opy_ (u"ࠪࡻࡩ࡯࡯ࡔࡧࡵࡺ࡮ࡩࡥࠨउ"),
  bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ऊ"),
  bstack11l11lll1_opy_ (u"ࠬࡶࡲࡦࡸࡨࡲࡹࡉࡲࡰࡵࡶࡗ࡮ࡺࡥࡕࡴࡤࡧࡰ࡯࡮ࡨࠩऋ"),
  bstack11l11lll1_opy_ (u"࠭ࡨࡪࡩ࡫ࡇࡴࡴࡴࡳࡣࡶࡸࠬऌ"),
  bstack11l11lll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡐࡳࡧࡩࡩࡷ࡫࡮ࡤࡧࡶࠫऍ"),
  bstack11l11lll1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡔ࡫ࡰࠫऎ"),
  bstack11l11lll1_opy_ (u"ࠩࡶ࡭ࡲࡕࡰࡵ࡫ࡲࡲࡸ࠭ए"),
  bstack11l11lll1_opy_ (u"ࠪࡶࡪࡳ࡯ࡷࡧࡌࡓࡘࡇࡰࡱࡕࡨࡸࡹ࡯࡮ࡨࡵࡏࡳࡨࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨऐ"),
  bstack11l11lll1_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ऑ"),
  bstack11l11lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऒ"),
  bstack11l11lll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨओ"),
  bstack11l11lll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭औ"),
  bstack11l11lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪक"),
  bstack11l11lll1_opy_ (u"ࠩࡳࡥ࡬࡫ࡌࡰࡣࡧࡗࡹࡸࡡࡵࡧࡪࡽࠬख"),
  bstack11l11lll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩग"),
  bstack11l11lll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡱࡸࡸࡸ࠭घ"),
  bstack11l11lll1_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨङ")
]
bstack1lll11_opy_ = {
  bstack11l11lll1_opy_ (u"࠭ࡶࠨच"): bstack11l11lll1_opy_ (u"ࠧࡷࠩछ"),
  bstack11l11lll1_opy_ (u"ࠨࡨࠪज"): bstack11l11lll1_opy_ (u"ࠩࡩࠫझ"),
  bstack11l11lll1_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩञ"): bstack11l11lll1_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪट"),
  bstack11l11lll1_opy_ (u"ࠬࡵ࡮࡭ࡻࡤࡹࡹࡵ࡭ࡢࡶࡨࠫठ"): bstack11l11lll1_opy_ (u"࠭࡯࡯࡮ࡼࡅࡺࡺ࡯࡮ࡣࡷࡩࠬड"),
  bstack11l11lll1_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫढ"): bstack11l11lll1_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬण"),
  bstack11l11lll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬत"): bstack11l11lll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭थ"),
  bstack11l11lll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧद"): bstack11l11lll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨध"),
  bstack11l11lll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩन"): bstack11l11lll1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऩ"),
  bstack11l11lll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫप"): bstack11l11lll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬफ"),
  bstack11l11lll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫब"): bstack11l11lll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡉࡱࡶࡸࠬभ"),
  bstack11l11lll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭म"): bstack11l11lll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧय"),
  bstack11l11lll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨर"): bstack11l11lll1_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪऱ"),
  bstack11l11lll1_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫल"): bstack11l11lll1_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬळ"),
  bstack11l11lll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬऴ"): bstack11l11lll1_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡥࡸࡹࠧव"),
  bstack11l11lll1_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨश"): bstack11l11lll1_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩष"),
  bstack11l11lll1_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬस"): bstack11l11lll1_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ह"),
  bstack11l11lll1_opy_ (u"ࠪࡴࡦࡩࡦࡪ࡮ࡨࠫऺ"): bstack11l11lll1_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧऻ"),
  bstack11l11lll1_opy_ (u"ࠬࡶࡡࡤ࠯ࡩ࡭ࡱ࡫़ࠧ"): bstack11l11lll1_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩऽ"),
  bstack11l11lll1_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪा"): bstack11l11lll1_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫि"),
  bstack11l11lll1_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪी"): bstack11l11lll1_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫु"),
  bstack11l11lll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ू"): bstack11l11lll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧृ"),
}
bstack1lllll1l1_opy_ = bstack11l11lll1_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡸࡦ࠲࡬ࡺࡨࠧॄ")
bstack1l11l1lll_opy_ = bstack11l11lll1_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠪॅ")
bstack11l1_opy_ = bstack11l11lll1_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡫ࡹࡧ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠬॆ")
bstack11lll11_opy_ = {
  bstack11l11lll1_opy_ (u"ࠩࡦࡶ࡮ࡺࡩࡤࡣ࡯ࠫे"): 50,
  bstack11l11lll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩै"): 40,
  bstack11l11lll1_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬॉ"): 30,
  bstack11l11lll1_opy_ (u"ࠬ࡯࡮ࡧࡱࠪॊ"): 20,
  bstack11l11lll1_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬो"): 10
}
bstack1llll11l1_opy_ = bstack11lll11_opy_[bstack11l11lll1_opy_ (u"ࠧࡪࡰࡩࡳࠬौ")]
bstack111111_opy_ = bstack11l11lll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵्ࠧ")
bstack1ll11lll_opy_ = bstack11l11lll1_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧॎ")
bstack1l11ll1ll_opy_ = bstack11l11lll1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩॏ")
bstack1l1111_opy_ = bstack11l11lll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࠪॐ")
bstack1l1111l1_opy_ = [bstack11l11lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭॑"), bstack11l11lll1_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ॒࠭")]
bstack11l11ll_opy_ = [bstack11l11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॓"), bstack11l11lll1_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪ॔")]
bstack1111l111_opy_ = [
  bstack11l11lll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡔࡡ࡮ࡧࠪॕ"),
  bstack11l11lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬॖ"),
  bstack11l11lll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨॗ"),
  bstack11l11lll1_opy_ (u"ࠬࡴࡥࡸࡅࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࠩक़"),
  bstack11l11lll1_opy_ (u"࠭ࡡࡱࡲࠪख़"),
  bstack11l11lll1_opy_ (u"ࠧࡶࡦ࡬ࡨࠬग़"),
  bstack11l11lll1_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪज़"),
  bstack11l11lll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡦࠩड़"),
  bstack11l11lll1_opy_ (u"ࠪࡳࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨढ़"),
  bstack11l11lll1_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡨࡦࡻ࡯ࡥࡸࠩफ़"),
  bstack11l11lll1_opy_ (u"ࠬࡴ࡯ࡓࡧࡶࡩࡹ࠭य़"), bstack11l11lll1_opy_ (u"࠭ࡦࡶ࡮࡯ࡖࡪࡹࡥࡵࠩॠ"),
  bstack11l11lll1_opy_ (u"ࠧࡤ࡮ࡨࡥࡷ࡙ࡹࡴࡶࡨࡱࡋ࡯࡬ࡦࡵࠪॡ"),
  bstack11l11lll1_opy_ (u"ࠨࡧࡹࡩࡳࡺࡔࡪ࡯࡬ࡲ࡬ࡹࠧॢ"),
  bstack11l11lll1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡨࡶ࡫ࡵࡲ࡮ࡣࡱࡧࡪࡒ࡯ࡨࡩ࡬ࡲ࡬࠭ॣ"),
  bstack11l11lll1_opy_ (u"ࠪࡳࡹ࡮ࡥࡳࡃࡳࡴࡸ࠭।"),
  bstack11l11lll1_opy_ (u"ࠫࡵࡸࡩ࡯ࡶࡓࡥ࡬࡫ࡓࡰࡷࡵࡧࡪࡕ࡮ࡇ࡫ࡱࡨࡋࡧࡩ࡭ࡷࡵࡩࠬ॥"),
  bstack11l11lll1_opy_ (u"ࠬࡧࡰࡱࡃࡦࡸ࡮ࡼࡩࡵࡻࠪ०"), bstack11l11lll1_opy_ (u"࠭ࡡࡱࡲࡓࡥࡨࡱࡡࡨࡧࠪ१"), bstack11l11lll1_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩ२"), bstack11l11lll1_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡒࡤࡧࡰࡧࡧࡦࠩ३"), bstack11l11lll1_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡇࡹࡷࡧࡴࡪࡱࡱࠫ४"),
  bstack11l11lll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨ५"),
  bstack11l11lll1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡩࡸࡺࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠨ६"),
  bstack11l11lll1_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࠧ७"), bstack11l11lll1_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࡆࡰࡧࡍࡳࡺࡥ࡯ࡶࠪ८"),
  bstack11l11lll1_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡒࡦࡣࡧࡽ࡙࡯࡭ࡦࡱࡸࡸࠬ९"),
  bstack11l11lll1_opy_ (u"ࠨࡣࡧࡦࡕࡵࡲࡵࠩ॰"),
  bstack11l11lll1_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡕࡲࡧࡰ࡫ࡴࠨॱ"),
  bstack11l11lll1_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡘ࡮ࡳࡥࡰࡷࡷࠫॲ"),
  bstack11l11lll1_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡴࡩࠩॳ"),
  bstack11l11lll1_opy_ (u"ࠬࡧࡶࡥࠩॴ"), bstack11l11lll1_opy_ (u"࠭ࡡࡷࡦࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩॵ"), bstack11l11lll1_opy_ (u"ࠧࡢࡸࡧࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩॶ"), bstack11l11lll1_opy_ (u"ࠨࡣࡹࡨࡆࡸࡧࡴࠩॷ"),
  bstack11l11lll1_opy_ (u"ࠩࡸࡷࡪࡑࡥࡺࡵࡷࡳࡷ࡫ࠧॸ"), bstack11l11lll1_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡴࡩࠩॹ"), bstack11l11lll1_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡴࡵࡺࡳࡷࡪࠧॺ"),
  bstack11l11lll1_opy_ (u"ࠬࡱࡥࡺࡃ࡯࡭ࡦࡹࠧॻ"), bstack11l11lll1_opy_ (u"࠭࡫ࡦࡻࡓࡥࡸࡹࡷࡰࡴࡧࠫॼ"),
  bstack11l11lll1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩॽ"), bstack11l11lll1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡁࡳࡩࡶࠫॾ"), bstack11l11lll1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࡈ࡮ࡸࠧॿ"), bstack11l11lll1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡅ࡫ࡶࡴࡳࡥࡎࡣࡳࡴ࡮ࡴࡧࡇ࡫࡯ࡩࠬঀ"), bstack11l11lll1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡘࡷࡪ࡙ࡹࡴࡶࡨࡱࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨঁ"),
  bstack11l11lll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࠨং"), bstack11l11lll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࡵࠪঃ"),
  bstack11l11lll1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡊࡩࡴࡣࡥࡰࡪࡈࡵࡪ࡮ࡧࡇ࡭࡫ࡣ࡬ࠩ঄"),
  bstack11l11lll1_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡥࡣࡸ࡬ࡩࡼ࡚ࡩ࡮ࡧࡲࡹࡹ࠭অ"),
  bstack11l11lll1_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡃࡦࡸ࡮ࡵ࡮ࠨআ"), bstack11l11lll1_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡆࡥࡹ࡫ࡧࡰࡴࡼࠫই"), bstack11l11lll1_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡊࡱࡧࡧࡴࠩঈ"), bstack11l11lll1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡦࡲࡉ࡯ࡶࡨࡲࡹࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨউ"),
  bstack11l11lll1_opy_ (u"࠭ࡤࡰࡰࡷࡗࡹࡵࡰࡂࡲࡳࡓࡳࡘࡥࡴࡧࡷࠫঊ"),
  bstack11l11lll1_opy_ (u"ࠧࡶࡰ࡬ࡧࡴࡪࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩঋ"), bstack11l11lll1_opy_ (u"ࠨࡴࡨࡷࡪࡺࡋࡦࡻࡥࡳࡦࡸࡤࠨঌ"),
  bstack11l11lll1_opy_ (u"ࠩࡱࡳࡘ࡯ࡧ࡯ࠩ঍"),
  bstack11l11lll1_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࡘࡲ࡮ࡳࡰࡰࡴࡷࡥࡳࡺࡖࡪࡧࡺࡷࠬ঎"),
  bstack11l11lll1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡴࡤࡳࡱ࡬ࡨ࡜ࡧࡴࡤࡪࡨࡶࡸ࠭এ"),
  bstack11l11lll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬঐ"),
  bstack11l11lll1_opy_ (u"࠭ࡲࡦࡥࡵࡩࡦࡺࡥࡄࡪࡵࡳࡲ࡫ࡄࡳ࡫ࡹࡩࡷ࡙ࡥࡴࡵ࡬ࡳࡳࡹࠧ঑"),
  bstack11l11lll1_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭঒"),
  bstack11l11lll1_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡕࡧࡴࡩࠩও"),
  bstack11l11lll1_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡖࡴࡪ࡫ࡤࠨঔ"),
  bstack11l11lll1_opy_ (u"ࠪ࡫ࡵࡹࡅ࡯ࡣࡥࡰࡪࡪࠧক"),
  bstack11l11lll1_opy_ (u"ࠫ࡮ࡹࡈࡦࡣࡧࡰࡪࡹࡳࠨখ"),
  bstack11l11lll1_opy_ (u"ࠬࡧࡤࡣࡇࡻࡩࡨ࡚ࡩ࡮ࡧࡲࡹࡹ࠭গ"),
  bstack11l11lll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡪ࡙ࡣࡳ࡫ࡳࡸࠬঘ"),
  bstack11l11lll1_opy_ (u"ࠧࡴ࡭࡬ࡴࡉ࡫ࡶࡪࡥࡨࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫঙ"),
  bstack11l11lll1_opy_ (u"ࠨࡣࡸࡸࡴࡍࡲࡢࡰࡷࡔࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠨচ"),
  bstack11l11lll1_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡑࡥࡹࡻࡲࡢ࡮ࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧছ"),
  bstack11l11lll1_opy_ (u"ࠪࡷࡾࡹࡴࡦ࡯ࡓࡳࡷࡺࠧজ"),
  bstack11l11lll1_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡩࡨࡈࡰࡵࡷࠫঝ"),
  bstack11l11lll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡘࡲࡱࡵࡣ࡬ࠩঞ"), bstack11l11lll1_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰ࡚ࡹࡱࡧࠪট"), bstack11l11lll1_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡋࡦࡻࠪঠ"),
  bstack11l11lll1_opy_ (u"ࠨࡣࡸࡸࡴࡒࡡࡶࡰࡦ࡬ࠬড"),
  bstack11l11lll1_opy_ (u"ࠩࡶ࡯࡮ࡶࡌࡰࡩࡦࡥࡹࡉࡡࡱࡶࡸࡶࡪ࠭ঢ"),
  bstack11l11lll1_opy_ (u"ࠪࡹࡳ࡯࡮ࡴࡶࡤࡰࡱࡕࡴࡩࡧࡵࡔࡦࡩ࡫ࡢࡩࡨࡷࠬণ"),
  bstack11l11lll1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩ࡜࡯࡮ࡥࡱࡺࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳ࠭ত"),
  bstack11l11lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡘࡴࡵ࡬ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩথ"),
  bstack11l11lll1_opy_ (u"࠭ࡥ࡯ࡨࡲࡶࡨ࡫ࡁࡱࡲࡌࡲࡸࡺࡡ࡭࡮ࠪদ"),
  bstack11l11lll1_opy_ (u"ࠧࡦࡰࡶࡹࡷ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡳࡉࡣࡹࡩࡕࡧࡧࡦࡵࠪধ"), bstack11l11lll1_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡆࡨࡺࡹࡵ࡯࡭ࡵࡓࡳࡷࡺࠧন"), bstack11l11lll1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡆࡨࡸࡦ࡯࡬ࡴࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠬ঩"),
  bstack11l11lll1_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡴࡵࡹࡃࡢࡥ࡫ࡩࡑ࡯࡭ࡪࡶࠪপ"),
  bstack11l11lll1_opy_ (u"ࠫࡨࡧ࡬ࡦࡰࡧࡥࡷࡌ࡯ࡳ࡯ࡤࡸࠬফ"),
  bstack11l11lll1_opy_ (u"ࠬࡨࡵ࡯ࡦ࡯ࡩࡎࡪࠧব"),
  bstack11l11lll1_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ভ"),
  bstack11l11lll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡈࡲࡦࡨ࡬ࡦࡦࠪম"), bstack11l11lll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡅࡺࡺࡨࡰࡴ࡬ࡾࡪࡪࠧয"),
  bstack11l11lll1_opy_ (u"ࠩࡤࡹࡹࡵࡁࡤࡥࡨࡴࡹࡇ࡬ࡦࡴࡷࡷࠬর"), bstack11l11lll1_opy_ (u"ࠪࡥࡺࡺ࡯ࡅ࡫ࡶࡱ࡮ࡹࡳࡂ࡮ࡨࡶࡹࡹࠧ঱"),
  bstack11l11lll1_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨࡍࡳࡹࡴࡳࡷࡰࡩࡳࡺࡳࡍ࡫ࡥࠫল"),
  bstack11l11lll1_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡕࡣࡳࠫ঳"),
  bstack11l11lll1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏ࡮ࡪࡶ࡬ࡥࡱ࡛ࡲ࡭ࠩ঴"), bstack11l11lll1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡁ࡭࡮ࡲࡻࡕࡵࡰࡶࡲࡶࠫ঵"), bstack11l11lll1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡩࡱࡳࡷ࡫ࡆࡳࡣࡸࡨ࡜ࡧࡲ࡯࡫ࡱ࡫ࠬশ"), bstack11l11lll1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡑࡳࡩࡳࡒࡩ࡯࡭ࡶࡍࡳࡈࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥࠩষ"),
  bstack11l11lll1_opy_ (u"ࠪ࡯ࡪ࡫ࡰࡌࡧࡼࡇ࡭ࡧࡩ࡯ࡵࠪস"),
  bstack11l11lll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡾࡦࡨ࡬ࡦࡕࡷࡶ࡮ࡴࡧࡴࡆ࡬ࡶࠬহ"),
  bstack11l11lll1_opy_ (u"ࠬࡶࡲࡰࡥࡨࡷࡸࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨ঺"),
  bstack11l11lll1_opy_ (u"࠭ࡩ࡯ࡶࡨࡶࡐ࡫ࡹࡅࡧ࡯ࡥࡾ࠭঻"),
  bstack11l11lll1_opy_ (u"ࠧࡴࡪࡲࡻࡎࡕࡓࡍࡱࡪ়ࠫ"),
  bstack11l11lll1_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡕࡷࡶࡦࡺࡥࡨࡻࠪঽ"),
  bstack11l11lll1_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡔࡨࡷࡵࡵ࡮ࡴࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪা"), bstack11l11lll1_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡗࡢ࡫ࡷࡘ࡮ࡳࡥࡰࡷࡷࠫি"),
  bstack11l11lll1_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡈࡪࡨࡵࡨࡒࡵࡳࡽࡿࠧী"),
  bstack11l11lll1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡹࡹ࡯ࡥࡈࡼࡪࡩࡵࡵࡧࡉࡶࡴࡳࡈࡵࡶࡳࡷࠬু"),
  bstack11l11lll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡐࡴ࡭ࡃࡢࡲࡷࡹࡷ࡫ࠧূ"),
  bstack11l11lll1_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡄࡦࡤࡸ࡫ࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧৃ"),
  bstack11l11lll1_opy_ (u"ࠨࡨࡸࡰࡱࡉ࡯࡯ࡶࡨࡼࡹࡒࡩࡴࡶࠪৄ"),
  bstack11l11lll1_opy_ (u"ࠩࡺࡥ࡮ࡺࡆࡰࡴࡄࡴࡵ࡙ࡣࡳ࡫ࡳࡸࠬ৅"),
  bstack11l11lll1_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡇࡴࡴ࡮ࡦࡥࡷࡖࡪࡺࡲࡪࡧࡶࠫ৆"),
  bstack11l11lll1_opy_ (u"ࠫࡦࡶࡰࡏࡣࡰࡩࠬে"),
  bstack11l11lll1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘ࡙ࡌࡄࡧࡵࡸࠬৈ"),
  bstack11l11lll1_opy_ (u"࠭ࡴࡢࡲ࡚࡭ࡹ࡮ࡓࡩࡱࡵࡸࡕࡸࡥࡴࡵࡇࡹࡷࡧࡴࡪࡱࡱࠫ৉"),
  bstack11l11lll1_opy_ (u"ࠧࡴࡥࡤࡰࡪࡌࡡࡤࡶࡲࡶࠬ৊"),
  bstack11l11lll1_opy_ (u"ࠨࡹࡧࡥࡑࡵࡣࡢ࡮ࡓࡳࡷࡺࠧো"),
  bstack11l11lll1_opy_ (u"ࠩࡶ࡬ࡴࡽࡘࡤࡱࡧࡩࡑࡵࡧࠨৌ"),
  bstack11l11lll1_opy_ (u"ࠪ࡭ࡴࡹࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡷࡶࡩ্ࠬ"),
  bstack11l11lll1_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡆࡳࡳ࡬ࡩࡨࡈ࡬ࡰࡪ࠭ৎ"),
  bstack11l11lll1_opy_ (u"ࠬࡱࡥࡺࡥ࡫ࡥ࡮ࡴࡐࡢࡵࡶࡻࡴࡸࡤࠨ৏"),
  bstack11l11lll1_opy_ (u"࠭ࡵࡴࡧࡓࡶࡪࡨࡵࡪ࡮ࡷ࡛ࡉࡇࠧ৐"),
  bstack11l11lll1_opy_ (u"ࠧࡱࡴࡨࡺࡪࡴࡴࡘࡆࡄࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠨ৑"),
  bstack11l11lll1_opy_ (u"ࠨࡹࡨࡦࡉࡸࡩࡷࡧࡵࡅ࡬࡫࡮ࡵࡗࡵࡰࠬ৒"),
  bstack11l11lll1_opy_ (u"ࠩ࡮ࡩࡾࡩࡨࡢ࡫ࡱࡔࡦࡺࡨࠨ৓"),
  bstack11l11lll1_opy_ (u"ࠪࡹࡸ࡫ࡎࡦࡹ࡚ࡈࡆ࠭৔"),
  bstack11l11lll1_opy_ (u"ࠫࡼࡪࡡࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧ৕"), bstack11l11lll1_opy_ (u"ࠬࡽࡤࡢࡅࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲ࡙࡯࡭ࡦࡱࡸࡸࠬ৖"),
  bstack11l11lll1_opy_ (u"࠭ࡸࡤࡱࡧࡩࡔࡸࡧࡊࡦࠪৗ"), bstack11l11lll1_opy_ (u"ࠧࡹࡥࡲࡨࡪ࡙ࡩࡨࡰ࡬ࡲ࡬ࡏࡤࠨ৘"),
  bstack11l11lll1_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡥ࡙ࡇࡅࡇࡻ࡮ࡥ࡮ࡨࡍࡩ࠭৙"),
  bstack11l11lll1_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡐࡰࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡸࡴࡐࡰ࡯ࡽࠬ৚"),
  bstack11l11lll1_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࡷࠬ৛"),
  bstack11l11lll1_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶ࡮࡫ࡳࠨড়"), bstack11l11lll1_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷࡿࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠨঢ়"),
  bstack11l11lll1_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࡈࡢࡴࡧࡻࡦࡸࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩ৞"),
  bstack11l11lll1_opy_ (u"ࠧ࡮ࡣࡻࡘࡾࡶࡩ࡯ࡩࡉࡶࡪࡷࡵࡦࡰࡦࡽࠬয়"),
  bstack11l11lll1_opy_ (u"ࠨࡵ࡬ࡱࡵࡲࡥࡊࡵ࡙࡭ࡸ࡯ࡢ࡭ࡧࡆ࡬ࡪࡩ࡫ࠨৠ"),
  bstack11l11lll1_opy_ (u"ࠩࡸࡷࡪࡉࡡࡳࡶ࡫ࡥ࡬࡫ࡓࡴ࡮ࠪৡ"),
  bstack11l11lll1_opy_ (u"ࠪࡷ࡭ࡵࡵ࡭ࡦࡘࡷࡪ࡙ࡩ࡯ࡩ࡯ࡩࡹࡵ࡮ࡕࡧࡶࡸࡒࡧ࡮ࡢࡩࡨࡶࠬৢ"),
  bstack11l11lll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡌ࡛ࡉࡖࠧৣ"),
  bstack11l11lll1_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡴࡻࡣࡩࡋࡧࡉࡳࡸ࡯࡭࡮ࠪ৤"),
  bstack11l11lll1_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪࡎࡩࡥࡦࡨࡲࡆࡶࡩࡑࡱ࡯࡭ࡨࡿࡅࡳࡴࡲࡶࠬ৥"),
  bstack11l11lll1_opy_ (u"ࠧ࡮ࡱࡦ࡯ࡑࡵࡣࡢࡶ࡬ࡳࡳࡇࡰࡱࠩ০"),
  bstack11l11lll1_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇࡱࡵࡱࡦࡺࠧ১"), bstack11l11lll1_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈ࡬ࡰࡹ࡫ࡲࡔࡲࡨࡧࡸ࠭২"),
  bstack11l11lll1_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡆࡨࡰࡦࡿࡁࡥࡤࠪ৩")
]
bstack1l11l1l11_opy_ = bstack11l11lll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡰࡪ࠯ࡦࡰࡴࡻࡤ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡹࡵࡲ࡯ࡢࡦࠪ৪")
bstack1l1l11l11_opy_ = [bstack11l11lll1_opy_ (u"ࠬ࠴ࡡࡱ࡭ࠪ৫"), bstack11l11lll1_opy_ (u"࠭࠮ࡢࡣࡥࠫ৬"), bstack11l11lll1_opy_ (u"ࠧ࠯࡫ࡳࡥࠬ৭")]
bstack1ll111l11_opy_ = [bstack11l11lll1_opy_ (u"ࠨ࡫ࡧࠫ৮"), bstack11l11lll1_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ৯"), bstack11l11lll1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ৰ"), bstack11l11lll1_opy_ (u"ࠫࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦࠪৱ")]
bstack111ll1ll_opy_ = {
  bstack11l11lll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ৲"): bstack11l11lll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৳"),
  bstack11l11lll1_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ৴"): bstack11l11lll1_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭৵"),
  bstack11l11lll1_opy_ (u"ࠩࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৶"): bstack11l11lll1_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৷"),
  bstack11l11lll1_opy_ (u"ࠫ࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ৸"): bstack11l11lll1_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫ৹"),
  bstack11l11lll1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡕࡰࡵ࡫ࡲࡲࡸ࠭৺"): bstack11l11lll1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨ৻")
}
bstack11lll1ll_opy_ = [
  bstack11l11lll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ৼ"),
  bstack11l11lll1_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ৽"),
  bstack11l11lll1_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫ৾"),
  bstack11l11lll1_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ৿"),
  bstack11l11lll1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭਀"),
]
bstack1l11l1111_opy_ = bstack1lll1l11_opy_ + bstack1l1ll11l_opy_ + bstack1111l111_opy_
bstack1ll11111_opy_ = [
  bstack11l11lll1_opy_ (u"࠭࡞࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶࠧࠫਁ"),
  bstack11l11lll1_opy_ (u"ࠧ࡟ࡤࡶ࠱ࡱࡵࡣࡢ࡮࠱ࡧࡴࡳࠤࠨਂ"),
  bstack11l11lll1_opy_ (u"ࠨࡠ࠴࠶࠼࠴ࠧਃ"),
  bstack11l11lll1_opy_ (u"ࠩࡡ࠵࠵࠴ࠧ਄"),
  bstack11l11lll1_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠳࡞࠺࠲࠿࡝࠯ࠩਅ"),
  bstack11l11lll1_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠵࡟࠵࠳࠹࡞࠰ࠪਆ"),
  bstack11l11lll1_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠷ࡠ࠶࠭࠲࡟࠱ࠫਇ"),
  bstack11l11lll1_opy_ (u"࠭࡞࠲࠻࠵࠲࠶࠼࠸࠯ࠩਈ")
]
bstack1ll11l11l_opy_ = bstack11l11lll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡳ࡭࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀࠫਉ")
bstack1ll1l1ll_opy_ = bstack11l11lll1_opy_ (u"ࠨࡵࡧ࡯࠴ࡼ࠱࠰ࡧࡹࡩࡳࡺࠧਊ")
bstack1l11ll_opy_ = [ bstack11l11lll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ਋") ]
bstack1lll1111l_opy_ = [ bstack11l11lll1_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ਌") ]
bstack1lll1ll1l_opy_ = [ bstack11l11lll1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ਍") ]
bstack1ll11l111_opy_ = bstack11l11lll1_opy_ (u"࡙ࠬࡄࡌࡕࡨࡸࡺࡶࠧ਎")
bstack111l111ll_opy_ = bstack11l11lll1_opy_ (u"࠭ࡓࡅࡍࡗࡩࡸࡺࡁࡵࡶࡨࡱࡵࡺࡥࡥࠩਏ")
bstack1lll111ll_opy_ = bstack11l11lll1_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠫਐ")
bstack1111lll1_opy_ = bstack11l11lll1_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࠧ਑")
bstack11llll111_opy_ = [
  bstack11l11lll1_opy_ (u"ࠩࡈࡖࡗࡥࡆࡂࡋࡏࡉࡉ࠭਒"),
  bstack11l11lll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡋࡐࡉࡉࡥࡏࡖࡖࠪਓ"),
  bstack11l11lll1_opy_ (u"ࠫࡊࡘࡒࡠࡄࡏࡓࡈࡑࡅࡅࡡࡅ࡝ࡤࡉࡌࡊࡇࡑࡘࠬਔ"),
  bstack11l11lll1_opy_ (u"ࠬࡋࡒࡓࡡࡑࡉ࡙࡝ࡏࡓࡍࡢࡇࡍࡇࡎࡈࡇࡇࠫਕ"),
  bstack11l11lll1_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡆࡖࡢࡒࡔ࡚࡟ࡄࡑࡑࡒࡊࡉࡔࡆࡆࠪਖ"),
  bstack11l11lll1_opy_ (u"ࠧࡆࡔࡕࡣࡈࡕࡎࡏࡇࡆࡘࡎࡕࡎࡠࡅࡏࡓࡘࡋࡄࠨਗ"),
  bstack11l11lll1_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡕࡉࡘࡋࡔࠨਘ"),
  bstack11l11lll1_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊࡌࡕࡔࡇࡇࠫਙ"),
  bstack11l11lll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡆࡈࡏࡓࡖࡈࡈࠬਚ"),
  bstack11l11lll1_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਛ"),
  bstack11l11lll1_opy_ (u"ࠬࡋࡒࡓࡡࡑࡅࡒࡋ࡟ࡏࡑࡗࡣࡗࡋࡓࡐࡎ࡙ࡉࡉ࠭ਜ"),
  bstack11l11lll1_opy_ (u"࠭ࡅࡓࡔࡢࡅࡉࡊࡒࡆࡕࡖࡣࡎࡔࡖࡂࡎࡌࡈࠬਝ"),
  bstack11l11lll1_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤ࡛ࡎࡓࡇࡄࡇࡍࡇࡂࡍࡇࠪਞ"),
  bstack11l11lll1_opy_ (u"ࠨࡇࡕࡖࡤ࡚ࡕࡏࡐࡈࡐࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩਟ"),
  bstack11l11lll1_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡘࡎࡓࡅࡅࡡࡒ࡙࡙࠭ਠ"),
  bstack11l11lll1_opy_ (u"ࠪࡉࡗࡘ࡟ࡔࡑࡆࡏࡘࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪਡ"),
  bstack11l11lll1_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡍࡕࡓࡕࡡࡘࡒࡗࡋࡁࡄࡊࡄࡆࡑࡋࠧਢ"),
  bstack11l11lll1_opy_ (u"ࠬࡋࡒࡓࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬਣ"),
  bstack11l11lll1_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧਤ"),
  bstack11l11lll1_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡕࡉࡘࡕࡌࡖࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ਥ"),
  bstack11l11lll1_opy_ (u"ࠨࡇࡕࡖࡤࡓࡁࡏࡆࡄࡘࡔࡘ࡙ࡠࡒࡕࡓ࡝࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧਦ"),
]
bstack1l111111_opy_ = bstack11l11lll1_opy_ (u"ࠩ࠱࠳ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡥࡷࡺࡩࡧࡣࡦࡸࡸ࠵ࠧਧ")
def bstack111l11ll1_opy_():
  global CONFIG
  headers = {
        bstack11l11lll1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩਨ"): bstack11l11lll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ਩"),
      }
  proxies = bstack1l1l1ll1_opy_(CONFIG, bstack11l1_opy_)
  try:
    response = requests.get(bstack11l1_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack11lll1l_opy_ = response.json()[bstack11l11lll1_opy_ (u"ࠬ࡮ࡵࡣࡵࠪਪ")]
      logger.debug(bstack1111111_opy_.format(response.json()))
      return bstack11lll1l_opy_
    else:
      logger.debug(bstack1l1l1l1l_opy_.format(bstack11l11lll1_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧਫ")))
  except Exception as e:
    logger.debug(bstack1l1l1l1l_opy_.format(e))
def bstack11lll1lll_opy_(hub_url):
  global CONFIG
  url = bstack11l11lll1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤਬ")+  hub_url + bstack11l11lll1_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣਭ")
  headers = {
        bstack11l11lll1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨਮ"): bstack11l11lll1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ਯ"),
      }
  proxies = bstack1l1l1ll1_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack11l1l1l_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1lll1ll11_opy_.format(hub_url, e))
def bstack1ll1l1l1l_opy_():
  try:
    global bstack1l1llllll_opy_
    bstack11lll1l_opy_ = bstack111l11ll1_opy_()
    bstack111l1l1_opy_ = []
    results = []
    for bstack11111ll_opy_ in bstack11lll1l_opy_:
      bstack111l1l1_opy_.append(bstack11l11ll1l_opy_(target=bstack11lll1lll_opy_,args=(bstack11111ll_opy_,)))
    for t in bstack111l1l1_opy_:
      t.start()
    for t in bstack111l1l1_opy_:
      results.append(t.join())
    bstack1llll11l_opy_ = {}
    for item in results:
      hub_url = item[bstack11l11lll1_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬਰ")]
      latency = item[bstack11l11lll1_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭਱")]
      bstack1llll11l_opy_[hub_url] = latency
    bstack11l11111_opy_ = min(bstack1llll11l_opy_, key= lambda x: bstack1llll11l_opy_[x])
    bstack1l1llllll_opy_ = bstack11l11111_opy_
    logger.debug(bstack1llll111_opy_.format(bstack11l11111_opy_))
  except Exception as e:
    logger.debug(bstack1lll1l11l_opy_.format(e))
bstack1llll_opy_ = bstack11l11lll1_opy_ (u"࠭ࡓࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡲࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠼ࠣࡿࢂ࠭ਲ")
bstack1l1lll1l_opy_ = bstack11l11lll1_opy_ (u"ࠧࡄࡱࡰࡴࡱ࡫ࡴࡦࡦࠣࡷࡪࡺࡵࡱࠣࠪਲ਼")
bstack11_opy_ = bstack11l11lll1_opy_ (u"ࠨࡒࡤࡶࡸ࡫ࡤࠡࡥࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࡀࠠࡼࡿࠪ਴")
bstack11llllll_opy_ = bstack11l11lll1_opy_ (u"ࠩࡖࡥࡳ࡯ࡴࡪࡼࡨࡨࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠧਵ")
bstack1ll1l1l11_opy_ = bstack11l11lll1_opy_ (u"࡙ࠪࡸ࡯࡮ࡨࠢ࡫ࡹࡧࠦࡵࡳ࡮࠽ࠤࢀࢃࠧਸ਼")
bstack1lll11ll_opy_ = bstack11l11lll1_opy_ (u"ࠫࡘ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡴࡷࡩࡩࠦࡷࡪࡶ࡫ࠤ࡮ࡪ࠺ࠡࡽࢀࠫ਷")
bstack1lll1l1l1_opy_ = bstack11l11lll1_opy_ (u"ࠬࡘࡥࡤࡧ࡬ࡺࡪࡪࠠࡪࡰࡷࡩࡷࡸࡵࡱࡶ࠯ࠤࡪࡾࡩࡵ࡫ࡱ࡫ࠬਸ")
bstack11111l1_opy_ = bstack11l11lll1_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࡣࠫਹ")
bstack111lll_opy_ = bstack11l11lll1_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴࠡࡣࡱࡨࠥࡶࡹࡵࡧࡶࡸ࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡱࡣࡦ࡯ࡦ࡭ࡥࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡶࡩࡱ࡫࡮ࡪࡷࡰࡤࠬ਺")
bstack1l1l1111l_opy_ = bstack11l11lll1_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡄࡴࡵ࡯ࡵ࡮ࡎ࡬ࡦࡷࡧࡲࡺࠢࡳࡥࡨࡱࡡࡨࡧ࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡶࡴࡨ࡯ࡵࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠱ࡦࡶࡰࡪࡷࡰࡰ࡮ࡨࡲࡢࡴࡼࡤࠬ਻")
bstack1lll1l1_opy_ = bstack11l11lll1_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡶࡴࡨ࡯ࡵ࠮ࠣࡴࡦࡨ࡯ࡵࠢࡤࡲࡩࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࡭࡫ࡥࡶࡦࡸࡹࠡࡲࡤࡧࡰࡧࡧࡦࡵࠣࡸࡴࠦࡲࡶࡰࠣࡶࡴࡨ࡯ࡵࠢࡷࡩࡸࡺࡳࠡ࡫ࡱࠤࡵࡧࡲࡢ࡮࡯ࡩࡱ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡲࡰࡤࡲࡸ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡳࡱࡥࡳࡹ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠮ࡲࡤࡦࡴࡺࠠࡳࡱࡥࡳࡹ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠮ࡵࡨࡰࡪࡴࡩࡶ࡯࡯࡭ࡧࡸࡡࡳࡻࡣ਼ࠫ")
bstack1l1lll_opy_ = bstack11l11lll1_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡧ࡫ࡨࡢࡸࡨࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵ࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡦࡪ࡮ࡡࡷࡧࡣࠫ਽")
bstack1ll1l111l_opy_ = bstack11l11lll1_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡧࡰࡱ࡫ࡸࡱ࠲ࡩ࡬ࡪࡧࡱࡸࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶ࠲ࠥࡦࡰࡪࡲࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡆࡶࡰࡪࡷࡰ࠱ࡕࡿࡴࡩࡱࡱ࠱ࡈࡲࡩࡦࡰࡷࡤࠬਾ")
bstack1l11_opy_ = bstack11l11lll1_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡦࠧਿ")
bstack11lllll_opy_ = bstack11l11lll1_opy_ (u"࠭ࡃࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡩ࡭ࡳࡪࠠࡦ࡫ࡷ࡬ࡪࡸࠠࡔࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡲࡶࠥࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳ࠯ࠢࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡹࡧ࡬࡭ࠢࡷ࡬ࡪࠦࡲࡦ࡮ࡨࡺࡦࡴࡴࠡࡲࡤࡧࡰࡧࡧࡦࡵࠣࡹࡸ࡯࡮ࡨࠢࡳ࡭ࡵࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷ࠳࠭ੀ")
bstack11l1l1l1_opy_ = bstack11l11lll1_opy_ (u"ࠧࡉࡣࡱࡨࡱ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡱࡵࡳࡦࠩੁ")
bstack1lll1lll_opy_ = bstack11l11lll1_opy_ (u"ࠨࡃ࡯ࡰࠥࡪ࡯࡯ࡧࠤࠫੂ")
bstack1l11lllll_opy_ = bstack11l11lll1_opy_ (u"ࠩࡆࡳࡳ࡬ࡩࡨࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴࠡࡣࡷࠤࡦࡴࡹࠡࡲࡤࡶࡪࡴࡴࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡴ࡬ࠠࠣࡽࢀࠦ࠳ࠦࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡥ࡯ࡹࡩ࡫ࠠࡢࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰ࠴ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡧ࡭࡭ࠢࡩ࡭ࡱ࡫ࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࡹ࠮ࠨ੃")
bstack1l11llll_opy_ = bstack11l11lll1_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡶࡪࡪࡥ࡯ࡶ࡬ࡥࡱࡹࠠ࡯ࡱࡷࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡢࡦࡧࠤࡹ࡮ࡥ࡮ࠢ࡬ࡲࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠡࡥࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࠦࡡࡴࠢࠥࡹࡸ࡫ࡲࡏࡣࡰࡩࠧࠦࡡ࡯ࡦࠣࠦࡦࡩࡣࡦࡵࡶࡏࡪࡿࠢࠡࡱࡵࠤࡸ࡫ࡴࠡࡶ࡫ࡩࡲࠦࡡࡴࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࡵ࠽ࠤࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊࠨࠠࡢࡰࡧࠤࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆࡉࡃࡆࡕࡖࡣࡐࡋ࡙ࠣࠩ੄")
bstack1l111llll_opy_ = bstack11l11lll1_opy_ (u"ࠫࡒࡧ࡬ࡧࡱࡵࡱࡪࡪࠠࡤࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩ࠿ࠨࡻࡾࠤࠪ੅")
bstack1l1l111ll_opy_ = bstack11l11lll1_opy_ (u"ࠬࡋ࡮ࡤࡱࡸࡲࡹ࡫ࡲࡦࡦࠣࡩࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡸࡴࠥ࠳ࠠࡼࡿࠪ੆")
bstack1l1111lll_opy_ = bstack11l11lll1_opy_ (u"࠭ࡓࡵࡣࡵࡸ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡍࡱࡦࡥࡱ࠭ੇ")
bstack11l111l_opy_ = bstack11l11lll1_opy_ (u"ࠧࡔࡶࡲࡴࡵ࡯࡮ࡨࠢࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡎࡲࡧࡦࡲࠧੈ")
bstack11lll1l11_opy_ = bstack11l11lll1_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡍࡱࡦࡥࡱࠦࡩࡴࠢࡱࡳࡼࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠡࠨ੉")
bstack1ll11l1l1_opy_ = bstack11l11lll1_opy_ (u"ࠩࡆࡳࡺࡲࡤࠡࡰࡲࡸࠥࡹࡴࡢࡴࡷࠤࡇࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡐࡴࡩࡡ࡭࠼ࠣࡿࢂ࠭੊")
bstack1ll111_opy_ = bstack11l11lll1_opy_ (u"ࠪࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡲ࡯ࡤࡣ࡯ࠤࡧ࡯࡮ࡢࡴࡼࠤࡼ࡯ࡴࡩࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࢀࢃࠧੋ")
bstack1llll1l1_opy_ = bstack11l11lll1_opy_ (u"࡚ࠫࡶࡤࡢࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡥࡧࡷࡥ࡮ࡲࡳ࠻ࠢࡾࢁࠬੌ")
bstack11l11l1_opy_ = bstack11l11lll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡷࡳࡨࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳࠡࡽࢀ੍ࠫ")
bstack1111ll11_opy_ = bstack11l11lll1_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡰࡳࡱࡹ࡭ࡩ࡫ࠠࡢࡰࠣࡥࡵࡶࡲࡰࡲࡵ࡭ࡦࡺࡥࠡࡈ࡚ࠤ࠭ࡸ࡯ࡣࡱࡷ࠳ࡵࡧࡢࡰࡶࠬࠤ࡮ࡴࠠࡤࡱࡱࡪ࡮࡭ࠠࡧ࡫࡯ࡩ࠱ࠦࡳ࡬࡫ࡳࠤࡹ࡮ࡥࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡰ࡫ࡹࠡ࡫ࡱࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡮࡬ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡵ࡬ࡱࡵࡲࡥࠡࡲࡼࡸ࡭ࡵ࡮ࠡࡵࡦࡶ࡮ࡶࡴࠡࡹ࡬ࡸ࡭ࡵࡵࡵࠢࡤࡲࡾࠦࡆࡘ࠰ࠪ੎")
bstack11lll1ll1_opy_ = bstack11l11lll1_opy_ (u"ࠧࡔࡧࡷࡸ࡮ࡴࡧࠡࡪࡷࡸࡵࡖࡲࡰࡺࡼ࠳࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠡ࡫ࡶࠤࡳࡵࡴࠡࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤࡴࡴࠠࡤࡷࡵࡶࡪࡴࡴ࡭ࡻࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡰࡨࠣࡷࡪࡲࡥ࡯࡫ࡸࡱࠥ࠮ࡻࡾࠫ࠯ࠤࡵࡲࡥࡢࡵࡨࠤࡺࡶࡧࡳࡣࡧࡩࠥࡺ࡯ࠡࡕࡨࡰࡪࡴࡩࡶ࡯ࡁࡁ࠹࠴࠰࠯࠲ࠣࡳࡷࠦࡲࡦࡨࡨࡶࠥࡺ࡯ࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡺࡻࡼ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡳࡨࡹ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡶࡩࡱ࡫࡮ࡪࡷࡰ࠳ࡷࡻ࡮࠮ࡶࡨࡷࡹࡹ࠭ࡣࡧ࡫࡭ࡳࡪ࠭ࡱࡴࡲࡼࡾࠩࡰࡺࡶ࡫ࡳࡳࠦࡦࡰࡴࠣࡥࠥࡽ࡯ࡳ࡭ࡤࡶࡴࡻ࡮ࡥ࠰ࠪ੏")
bstack1ll11l_opy_ = bstack11l11lll1_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡾࡳ࡬ࠡࡨ࡬ࡰࡪ࠴࠮ࠨ੐")
bstack111ll_opy_ = bstack11l11lll1_opy_ (u"ࠩࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡩࡨࡲࡪࡸࡡࡵࡧࡧࠤࡹ࡮ࡥࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨ࡬ࡰࡪࠧࠧੑ")
bstack1lll1111_opy_ = bstack11l11lll1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡶ࡫ࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫࡯࡬ࡦ࠰ࠣࡿࢂ࠭੒")
bstack1ll1l1ll1_opy_ = bstack11l11lll1_opy_ (u"ࠫࡊࡾࡰࡦࡥࡷࡩࡩࠦࡡࡵࠢ࡯ࡩࡦࡹࡴࠡ࠳ࠣ࡭ࡳࡶࡵࡵ࠮ࠣࡶࡪࡩࡥࡪࡸࡨࡨࠥ࠶ࠧ੓")
bstack11111111_opy_ = bstack11l11lll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡩࡻࡲࡪࡰࡪࠤࡆࡶࡰࠡࡷࡳࡰࡴࡧࡤ࠯ࠢࡾࢁࠬ੔")
bstack11l1l1l11_opy_ = bstack11l11lll1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡸࡴࡱࡵࡡࡥࠢࡄࡴࡵ࠴ࠠࡊࡰࡹࡥࡱ࡯ࡤࠡࡨ࡬ࡰࡪࠦࡰࡢࡶ࡫ࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡩࠦࡻࡾ࠰ࠪ੕")
bstack111l1ll11_opy_ = bstack11l11lll1_opy_ (u"ࠧࡌࡧࡼࡷࠥࡩࡡ࡯ࡰࡲࡸࠥࡩ࡯࠮ࡧࡻ࡭ࡸࡺࠠࡢࡵࠣࡥࡵࡶࠠࡷࡣ࡯ࡹࡪࡹࠬࠡࡷࡶࡩࠥࡧ࡮ࡺࠢࡲࡲࡪࠦࡰࡳࡱࡳࡩࡷࡺࡹࠡࡨࡵࡳࡲࠦࡻࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡶࡡࡵࡪ࠿ࡷࡹࡸࡩ࡯ࡩࡁ࠰ࠥࡩࡵࡴࡶࡲࡱࡤ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡷ࡭ࡧࡲࡦࡣࡥࡰࡪࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀࢀ࠰ࠥࡵ࡮࡭ࡻࠣࠦࡵࡧࡴࡩࠤࠣࡥࡳࡪࠠࠣࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠦࠥࡩࡡ࡯ࠢࡦࡳ࠲࡫ࡸࡪࡵࡷࠤࡹࡵࡧࡦࡶ࡫ࡩࡷ࠴ࠧ੖")
bstack1l1l11l_opy_ = bstack11l11lll1_opy_ (u"ࠨ࡝ࡌࡲࡻࡧ࡬ࡪࡦࠣࡥࡵࡶࠠࡱࡴࡲࡴࡪࡸࡴࡺ࡟ࠣࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠣࡥࡷ࡫ࠠࡼ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡰࡢࡶ࡫ࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡣࡶࡵࡷࡳࡲࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁࢁ࠳ࠦࡆࡰࡴࠣࡱࡴࡸࡥࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡳࡰࡪࡧࡳࡦࠢࡹ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡺࡻࡼ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡳࡨࡹ࠯ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱࡲ࡬ࡹࡲ࠵ࡳࡦࡶ࠰ࡹࡵ࠳ࡴࡦࡵࡷࡷ࠴ࡹࡰࡦࡥ࡬ࡪࡾ࠳ࡡࡱࡲࠪ੗")
bstack1ll1lll_opy_ = bstack11l11lll1_opy_ (u"ࠩ࡞ࡍࡳࡼࡡ࡭࡫ࡧࠤࡦࡶࡰࠡࡲࡵࡳࡵ࡫ࡲࡵࡻࡠࠤࡘࡻࡰࡱࡱࡵࡸࡪࡪࠠࡷࡣ࡯ࡹࡪࡹࠠࡰࡨࠣࡥࡵࡶࠠࡢࡴࡨࠤࡴ࡬ࠠࡼ࡫ࡧࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡰࡢࡶ࡫ࡀࡸࡺࡲࡪࡰࡪࡂ࠱ࠦࡣࡶࡵࡷࡳࡲࡥࡩࡥ࠾ࡶࡸࡷ࡯࡮ࡨࡀ࠯ࠤࡸ࡮ࡡࡳࡧࡤࡦࡱ࡫࡟ࡪࡦ࠿ࡷࡹࡸࡩ࡯ࡩࡁࢁ࠳ࠦࡆࡰࡴࠣࡱࡴࡸࡥࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡳࡰࡪࡧࡳࡦࠢࡹ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡺࡻࡼ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡧࡳࡨࡹ࠯ࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱࡲ࡬ࡹࡲ࠵ࡳࡦࡶ࠰ࡹࡵ࠳ࡴࡦࡵࡷࡷ࠴ࡹࡰࡦࡥ࡬ࡪࡾ࠳ࡡࡱࡲࠪ੘")
bstack11l1l1111_opy_ = bstack11l11lll1_opy_ (u"࡙ࠪࡸ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡦࡶࡰࠡ࡫ࡧࠤࢀࢃࠠࡧࡱࡵࠤ࡭ࡧࡳࡩࠢ࠽ࠤࢀࢃ࠮ࠨਖ਼")
bstack111ll1111_opy_ = bstack11l11lll1_opy_ (u"ࠫࡆࡶࡰࠡࡗࡳࡰࡴࡧࡤࡦࡦࠣࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺ࠰ࠣࡍࡉࠦ࠺ࠡࡽࢀࠫਗ਼")
bstack1l111_opy_ = bstack11l11lll1_opy_ (u"࡛ࠬࡳࡪࡰࡪࠤࡆࡶࡰࠡ࠼ࠣࡿࢂ࠴ࠧਜ਼")
bstack1l11ll111_opy_ = bstack11l11lll1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲࠦࡩࡴࠢࡱࡳࡹࠦࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡩࡳࡷࠦࡶࡢࡰ࡬ࡰࡱࡧࠠࡱࡻࡷ࡬ࡴࡴࠠࡵࡧࡶࡸࡸ࠲ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡹ࡬ࡸ࡭ࠦࡰࡢࡴࡤࡰࡱ࡫࡬ࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠥࡃࠠ࠲ࠩੜ")
bstack1l11l1ll1_opy_ = bstack11l11lll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࡀࠠࡼࡿࠪ੝")
bstack1ll1ll1l_opy_ = bstack11l11lll1_opy_ (u"ࠨࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡨࡲ࡯ࡴࡧࠣࡦࡷࡵࡷࡴࡧࡵ࠾ࠥࢁࡽࠨਫ਼")
bstack1l1l1l11_opy_ = bstack11l11lll1_opy_ (u"ࠩࡆࡳࡺࡲࡤࠡࡰࡲࡸࠥ࡭ࡥࡵࠢࡵࡩࡦࡹ࡯࡯ࠢࡩࡳࡷࠦࡢࡦࡪࡤࡺࡪࠦࡦࡦࡣࡷࡹࡷ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥ࠯ࠢࡾࢁࠬ੟")
bstack1lll111_opy_ = bstack11l11lll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠤ࡫ࡸ࡯࡮ࠢࡤࡴ࡮ࠦࡣࡢ࡮࡯࠲ࠥࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠨ੠")
bstack1l1lll1_opy_ = bstack11l11lll1_opy_ (u"࡚ࠫࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡪࡲࡻࠥࡨࡵࡪ࡮ࡧࠤ࡚ࡘࡌ࠭ࠢࡤࡷࠥࡨࡵࡪ࡮ࡧࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠡ࡫ࡶࠤࡳࡵࡴࠡࡷࡶࡩࡩ࠴ࠧ੡")
bstack11l1l1lll_opy_ = bstack11l11lll1_opy_ (u"࡙ࠬࡥࡳࡸࡨࡶࠥࡹࡩࡥࡧࠣࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠮ࡻࡾࠫࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡷࡦࡳࡥࠡࡣࡶࠤࡨࡲࡩࡦࡰࡷࠤࡸ࡯ࡤࡦࠢࡥࡹ࡮ࡲࡤࡏࡣࡰࡩ࠭ࢁࡽࠪࠩ੢")
bstack1ll1l1l_opy_ = bstack11l11lll1_opy_ (u"࠭ࡖࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡳࡳࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡪࡡࡴࡪࡥࡳࡦࡸࡤ࠻ࠢࡾࢁࠬ੣")
bstack1ll1111ll_opy_ = bstack11l11lll1_opy_ (u"ࠧࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡥࡨࡩࡥࡴࡵࠣࡥࠥࡶࡲࡪࡸࡤࡸࡪࠦࡤࡰ࡯ࡤ࡭ࡳࡀࠠࡼࡿࠣ࠲࡙ࠥࡥࡵࠢࡷ࡬ࡪࠦࡦࡰ࡮࡯ࡳࡼ࡯࡮ࡨࠢࡦࡳࡳ࡬ࡩࡨࠢ࡬ࡲࠥࡿ࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨ࠾ࠥࡢ࡮࠮࠯࠰࠱࠲࠳࠭࠮࠯࠰࠱ࠥࡢ࡮ࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰ࠿ࠦࡴࡳࡷࡨࠤࡡࡴ࠭࠮࠯࠰࠱࠲࠳࠭࠮࠯࠰ࠫ੤")
bstack111lllll1_opy_ = bstack11l11lll1_opy_ (u"ࠨࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣ࡫ࡪࡺ࡟࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࡤ࡫ࡲࡳࡱࡵࠤ࠿ࠦࡻࡾࠩ੥")
bstack11l1l1l1l_opy_ = bstack11l11lll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫࡮ࡥࡡࡤࡱࡵࡲࡩࡵࡷࡧࡩࡤ࡫ࡶࡦࡰࡷࠤ࡫ࡵࡲࠡࡕࡇࡏࡘ࡫ࡴࡶࡲࠣࡿࢂࠨ੦")
bstack1lllll1l_opy_ = bstack11l11lll1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥ࡯ࡦࡢࡥࡲࡶ࡬ࡪࡶࡸࡨࡪࡥࡥࡷࡧࡱࡸࠥ࡬࡯ࡳࠢࡖࡈࡐ࡚ࡥࡴࡶࡄࡸࡹ࡫࡭ࡱࡶࡨࡨࠥࢁࡽࠣ੧")
bstack11lll1111_opy_ = bstack11l11lll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡰࡧࡣࡦࡳࡰ࡭࡫ࡷࡹࡩ࡫࡟ࡦࡸࡨࡲࡹࠦࡦࡰࡴࠣࡗࡉࡑࡔࡦࡵࡷࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠠࡼࡿࠥ੨")
bstack11lll1_opy_ = bstack11l11lll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧ࡫ࡵࡩࡤࡸࡥࡲࡷࡨࡷࡹࠦࡻࡾࠤ੩")
bstack1lllll1ll_opy_ = bstack11l11lll1_opy_ (u"ࠨࡐࡐࡕࡗࠤࡊࡼࡥ࡯ࡶࠣࡿࢂࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡ࠼ࠣࡿࢂࠨ੪")
bstack1l11l1ll_opy_ = bstack11l11lll1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧࡴࡴࡦࡪࡩࡸࡶࡪࠦࡰࡳࡱࡻࡽࠥࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠫ੫")
bstack1111111_opy_ = bstack11l11lll1_opy_ (u"ࠨࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡪࡷࡵ࡭ࠡ࠱ࡱࡩࡽࡺ࡟ࡩࡷࡥࡷࠥࢁࡽࠨ੬")
bstack1l1l1l1l_opy_ = bstack11l11lll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠠࡧࡴࡲࡱࠥ࠵࡮ࡦࡺࡷࡣ࡭ࡻࡢࡴ࠼ࠣࡿࢂ࠭੭")
bstack1llll111_opy_ = bstack11l11lll1_opy_ (u"ࠪࡒࡪࡧࡲࡦࡵࡷࠤ࡭ࡻࡢࠡࡣ࡯ࡰࡴࡩࡡࡵࡧࡧࠤ࡮ࡹ࠺ࠡࡽࢀࠫ੮")
bstack1lll1l11l_opy_ = bstack11l11lll1_opy_ (u"ࠫࡊࡘࡒࡐࡔࠣࡍࡓࠦࡁࡍࡎࡒࡇࡆ࡚ࡅࠡࡊࡘࡆࠥࢁࡽࠨ੯")
bstack11l1l1l_opy_ = bstack11l11lll1_opy_ (u"ࠬࡒࡡࡵࡧࡱࡧࡾࠦ࡯ࡧࠢ࡫ࡹࡧࡀࠠࡼࡿࠣ࡭ࡸࡀࠠࡼࡿࠪੰ")
bstack1lll1ll11_opy_ = bstack11l11lll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡸࡹ࡯࡮ࡨࠢ࡯ࡥࡹ࡫࡮ࡤࡻࠣࡪࡴࡸࠠࡼࡿࠣ࡬ࡺࡨ࠺ࠡࡽࢀࠫੱ")
bstack1ll11ll1_opy_ = bstack11l11lll1_opy_ (u"ࠧࡉࡷࡥࠤࡺࡸ࡬ࠡࡥ࡫ࡥࡳ࡭ࡥࡥࠢࡷࡳࠥࡺࡨࡦࠢࡲࡴࡹ࡯࡭ࡢ࡮ࠣ࡬ࡺࡨ࠺ࠡࡽࢀࠫੲ")
bstack11llllll1_opy_ = bstack11l11lll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡴࡶࡴࡪ࡯ࡤࡰࠥ࡮ࡵࡣࠢࡸࡶࡱࡀࠠࡼࡿࠪੳ")
bstack1llll1l1l_opy_ = bstack11l11lll1_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡰ࡮ࡹࡴࡴ࠼ࠣࡿࢂ࠭ੴ")
bstack1l1ll1l1_opy_ = bstack11l11lll1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡣࡷ࡬ࡰࡩࠦࡡࡳࡶ࡬ࡪࡦࡩࡴࡴ࠼ࠣࡿࢂ࠭ੵ")
bstack11ll1l11l_opy_ = bstack11l11lll1_opy_ (u"࡚ࠫࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡰࡢࡥࠣࡪ࡮ࡲࡥࠡࡽࢀ࠲ࠥࡋࡲࡳࡱࡵࠤ࠲ࠦࡻࡾࠩ੶")
bstack1l111l_opy_ = bstack11l11lll1_opy_ (u"ࠬࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠥࠦࡩࡧࠪࡳࡥ࡬࡫ࠠ࠾࠿ࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠥࢁ࡜࡯ࠢࠣࠤࡹࡸࡹࡼ࡞ࡱࠤࡨࡵ࡮ࡴࡶࠣࡪࡸࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪ࡟ࠫ࡫ࡹ࡜ࠨࠫ࠾ࡠࡳࠦࠠࠡࠢࠣࡪࡸ࠴ࡡࡱࡲࡨࡲࡩࡌࡩ࡭ࡧࡖࡽࡳࡩࠨࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷ࡬࠱ࠦࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡱࡡ࡬ࡲࡩ࡫ࡸࠪࠢ࠮ࠤࠧࡀࠢࠡ࠭ࠣࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࠪࡤࡻࡦ࡯ࡴࠡࡰࡨࡻࡕࡧࡧࡦ࠴࠱ࡩࡻࡧ࡬ࡶࡣࡷࡩ࠭ࠨࠨࠪࠢࡀࡂࠥࢁࡽࠣ࠮ࠣࡠࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠤࢀࡠࠬ࠯ࠩࠪ࡝ࠥ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩࠨ࡝ࠪࠢ࠮ࠤࠧ࠲࡜࡝ࡰࠥ࠭ࡡࡴࠠࠡࠢࠣࢁࡨࡧࡴࡤࡪࠫࡩࡽ࠯ࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࢂࡢ࡮ࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠬ੷")
bstack11l1ll_opy_ = bstack11l11lll1_opy_ (u"࠭࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸ࡣ࡜࡯ࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࡟ࡲࡨࡵ࡮ࡴࡶࠣࡴࡤ࡯࡮ࡥࡧࡻࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠲࡞࡞ࡱࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳ࠪ࡞ࡱࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࡠࡳ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬ࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨ࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࡢ࡮࡭ࡧࡷࠤࡨࡧࡰࡴ࠽࡟ࡲࡹࡸࡹࠡࡽ࡟ࡲࡨࡧࡰࡴࠢࡀࠤࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸ࠯࡜࡯ࠢࠣࢁࠥࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࠡࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻ࡝ࡰࠣࠤࠥࠦࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ࠽ࠤࡥࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠤࡼࡧࡱࡧࡴࡪࡥࡖࡔࡌࡇࡴࡳࡰࡰࡰࡨࡲࡹ࠮ࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡤࡣࡳࡷ࠮࠯ࡽࡡ࠮࡟ࡲࠥࠦࠠࠡ࠰࠱࠲ࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶࡠࡳࠦࠠࡾࠫ࡟ࡲࢂࡢ࡮࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠬ੸")
from ._version import __version__
bstack1ll1111l_opy_ = None
CONFIG = {}
bstack1l11lll1_opy_ = {}
bstack1l11l11l_opy_ = {}
bstack1llllll_opy_ = None
bstack1l11l1l1_opy_ = None
bstack111llll_opy_ = None
bstack111l1ll1l_opy_ = -1
bstack1ll1llll_opy_ = bstack1llll11l1_opy_
bstack11111ll1_opy_ = 1
bstack1lll1l1ll_opy_ = False
bstack1111_opy_ = False
bstack1ll1ll1ll_opy_ = bstack11l11lll1_opy_ (u"ࠧࠨ੹")
bstack1l111ll1l_opy_ = bstack11l11lll1_opy_ (u"ࠨࠩ੺")
bstack1lll11l_opy_ = False
bstack111lll111_opy_ = True
bstack11l11l_opy_ = bstack11l11lll1_opy_ (u"ࠩࠪ੻")
bstack11l111ll1_opy_ = []
bstack1l1llllll_opy_ = bstack11l11lll1_opy_ (u"ࠪࠫ੼")
bstack11l11l1l_opy_ = False
bstack11l11l111_opy_ = None
bstack11ll1l1ll_opy_ = None
bstack1l1l11ll_opy_ = -1
bstack11lll111_opy_ = os.path.join(os.path.expanduser(bstack11l11lll1_opy_ (u"ࠫࢃ࠭੽")), bstack11l11lll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ੾"), bstack11l11lll1_opy_ (u"࠭࠮ࡳࡱࡥࡳࡹ࠳ࡲࡦࡲࡲࡶࡹ࠳ࡨࡦ࡮ࡳࡩࡷ࠴ࡪࡴࡱࡱࠫ੿"))
bstack1l1ll1l_opy_ = []
bstack11111l_opy_ = False
bstack111l1l1l_opy_ = False
bstack1lll1llll_opy_ = None
bstack1l11l11l1_opy_ = None
bstack1l11l11_opy_ = None
bstack1l1l1_opy_ = None
bstack11111l1l_opy_ = None
bstack1llll1ll_opy_ = None
bstack1ll111lll_opy_ = None
bstack11l1l11ll_opy_ = None
bstack111ll1ll1_opy_ = None
bstack111llllll_opy_ = None
bstack11ll1l111_opy_ = None
bstack1ll111ll_opy_ = None
bstack1111l_opy_ = None
bstack111ll1lll_opy_ = None
bstack11l1l11l1_opy_ = None
bstack111l1l_opy_ = None
bstack11llll11l_opy_ = None
bstack1ll11_opy_ = None
bstack1ll1l1_opy_ = bstack11l11lll1_opy_ (u"ࠢࠣ઀")
class bstack11l11ll1l_opy_(threading.Thread):
  def run(self):
    self.exc = None
    try:
      self.ret = self._target(*self._args, **self._kwargs)
    except Exception as e:
      self.exc = e
  def join(self, timeout=None):
    super(bstack11l11ll1l_opy_, self).join(timeout)
    if self.exc:
      raise self.exc
    return self.ret
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1ll1llll_opy_,
                    format=bstack11l11lll1_opy_ (u"ࠨ࡞ࡱࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ઁ"),
                    datefmt=bstack11l11lll1_opy_ (u"ࠩࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫં"))
def bstack11ll1lll1_opy_():
  global CONFIG
  global bstack1ll1llll_opy_
  if bstack11l11lll1_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬઃ") in CONFIG:
    bstack1ll1llll_opy_ = bstack11lll11_opy_[CONFIG[bstack11l11lll1_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭઄")]]
    logging.getLogger().setLevel(bstack1ll1llll_opy_)
def bstack11l1ll1ll_opy_():
  global CONFIG
  global bstack11111l_opy_
  bstackl_opy_ = bstack11ll1l1l1_opy_(CONFIG)
  if(bstack11l11lll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧઅ") in bstackl_opy_ and str(bstackl_opy_[bstack11l11lll1_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨઆ")]).lower() == bstack11l11lll1_opy_ (u"ࠧࡵࡴࡸࡩࠬઇ")):
    bstack11111l_opy_ = True
def bstack1ll11l1ll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l11lll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11lll11l1_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack11l11lll1_opy_ (u"ࠣ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡥࡲࡲ࡫࡯ࡧࡧ࡫࡯ࡩࠧઈ") == args[i].lower() or bstack11l11lll1_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡦࡪࡩࠥઉ") == args[i].lower():
      path = args[i+1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack11l11l_opy_
      bstack11l11l_opy_ += bstack11l11lll1_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠠࠨઊ") + path
      return path
  return None
def bstack11l11l11l_opy_():
  bstack11llll1l1_opy_ = bstack11lll11l1_opy_()
  if bstack11llll1l1_opy_ and os.path.exists(os.path.abspath(bstack11llll1l1_opy_)):
    fileName = bstack11llll1l1_opy_
  if bstack11l11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨઋ") in os.environ and os.path.exists(os.path.abspath(os.environ[bstack11l11lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆࠩઌ")])) and not bstack11l11lll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨઍ") in locals():
    fileName = os.environ[bstack11l11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ઎")]
  if bstack11l11lll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪએ") in locals():
    bstack11111_opy_ = os.path.abspath(fileName)
  else:
    bstack11111_opy_ = bstack11l11lll1_opy_ (u"ࠩࠪઐ")
  bstack1111llll_opy_ = os.getcwd()
  bstack11l11l1l1_opy_ = bstack11l11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ઑ")
  bstack11ll1_opy_ = bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠨ઒")
  while (not os.path.exists(bstack11111_opy_)) and bstack1111llll_opy_ != bstack11l11lll1_opy_ (u"ࠧࠨઓ"):
    bstack11111_opy_ = os.path.join(bstack1111llll_opy_, bstack11l11l1l1_opy_)
    if not os.path.exists(bstack11111_opy_):
      bstack11111_opy_ = os.path.join(bstack1111llll_opy_, bstack11ll1_opy_)
    if bstack1111llll_opy_ != os.path.dirname(bstack1111llll_opy_):
      bstack1111llll_opy_ = os.path.dirname(bstack1111llll_opy_)
    else:
      bstack1111llll_opy_ = bstack11l11lll1_opy_ (u"ࠨࠢઔ")
  if not os.path.exists(bstack11111_opy_):
    bstack111l1l111_opy_(
      bstack1l11lllll_opy_.format(os.getcwd()))
  with open(bstack11111_opy_, bstack11l11lll1_opy_ (u"ࠧࡳࠩક")) as stream:
    try:
      config = yaml.safe_load(stream)
      return config
    except yaml.YAMLError as exc:
      bstack111l1l111_opy_(bstack1l111llll_opy_.format(str(exc)))
def bstack1llll1_opy_(config):
  bstack1ll111l1l_opy_ = bstack1ll1ll11_opy_(config)
  for option in list(bstack1ll111l1l_opy_):
    if option.lower() in bstack1lll11_opy_ and option != bstack1lll11_opy_[option.lower()]:
      bstack1ll111l1l_opy_[bstack1lll11_opy_[option.lower()]] = bstack1ll111l1l_opy_[option]
      del bstack1ll111l1l_opy_[option]
  return config
def bstack1ll1lll11_opy_():
  global bstack1l11l11l_opy_
  for key, bstack1l11ll11_opy_ in bstack11ll1l1_opy_.items():
    if isinstance(bstack1l11ll11_opy_, list):
      for var in bstack1l11ll11_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1l11l11l_opy_[key] = os.environ[var]
          break
    elif bstack1l11ll11_opy_ in os.environ and os.environ[bstack1l11ll11_opy_] and str(os.environ[bstack1l11ll11_opy_]).strip():
      bstack1l11l11l_opy_[key] = os.environ[bstack1l11ll11_opy_]
  if bstack11l11lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪખ") in os.environ:
    bstack1l11l11l_opy_[bstack11l11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ગ")] = {}
    bstack1l11l11l_opy_[bstack11l11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧઘ")][bstack11l11lll1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ઙ")] = os.environ[bstack11l11lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧચ")]
def bstack1l1ll111l_opy_():
  global bstack1l11lll1_opy_
  global bstack11l11l_opy_
  for idx, val in enumerate(sys.argv):
    if idx<len(sys.argv) and bstack11l11lll1_opy_ (u"࠭࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩછ").lower() == val.lower():
      bstack1l11lll1_opy_[bstack11l11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫજ")] = {}
      bstack1l11lll1_opy_[bstack11l11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬઝ")][bstack11l11lll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫઞ")] = sys.argv[idx+1]
      del sys.argv[idx:idx+2]
      break
  for key, bstack111l11ll_opy_ in bstack1l11llll1_opy_.items():
    if isinstance(bstack111l11ll_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack111l11ll_opy_:
          if idx<len(sys.argv) and bstack11l11lll1_opy_ (u"ࠪ࠱࠲࠭ટ") + var.lower() == val.lower() and not key in bstack1l11lll1_opy_:
            bstack1l11lll1_opy_[key] = sys.argv[idx+1]
            bstack11l11l_opy_ += bstack11l11lll1_opy_ (u"ࠫࠥ࠳࠭ࠨઠ") + var + bstack11l11lll1_opy_ (u"ࠬࠦࠧડ") + sys.argv[idx+1]
            del sys.argv[idx:idx+2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx<len(sys.argv) and bstack11l11lll1_opy_ (u"࠭࠭࠮ࠩઢ") + bstack111l11ll_opy_.lower() == val.lower() and not key in bstack1l11lll1_opy_:
          bstack1l11lll1_opy_[key] = sys.argv[idx+1]
          bstack11l11l_opy_ += bstack11l11lll1_opy_ (u"ࠧࠡ࠯࠰ࠫણ") + bstack111l11ll_opy_ + bstack11l11lll1_opy_ (u"ࠨࠢࠪત") + sys.argv[idx+1]
          del sys.argv[idx:idx+2]
def bstack1l11111l1_opy_(config):
  bstack11ll11l_opy_ = config.keys()
  for bstack1111l1l_opy_, bstack1l1l111l_opy_ in bstack1lllllll1_opy_.items():
    if bstack1l1l111l_opy_ in bstack11ll11l_opy_:
      config[bstack1111l1l_opy_] = config[bstack1l1l111l_opy_]
      del config[bstack1l1l111l_opy_]
  for bstack1111l1l_opy_, bstack1l1l111l_opy_ in bstack11ll1ll_opy_.items():
    if isinstance(bstack1l1l111l_opy_, list):
      for bstack1lllll_opy_ in bstack1l1l111l_opy_:
        if bstack1lllll_opy_ in bstack11ll11l_opy_:
          config[bstack1111l1l_opy_] = config[bstack1lllll_opy_]
          del config[bstack1lllll_opy_]
          break
    elif bstack1l1l111l_opy_ in bstack11ll11l_opy_:
        config[bstack1111l1l_opy_] = config[bstack1l1l111l_opy_]
        del config[bstack1l1l111l_opy_]
  for bstack1lllll_opy_ in list(config):
    for bstack111ll1_opy_ in bstack1l11l1111_opy_:
      if bstack1lllll_opy_.lower() == bstack111ll1_opy_.lower() and bstack1lllll_opy_ != bstack111ll1_opy_:
        config[bstack111ll1_opy_] = config[bstack1lllll_opy_]
        del config[bstack1lllll_opy_]
  bstack1l111ll11_opy_ = []
  if bstack11l11lll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬથ") in config:
    bstack1l111ll11_opy_ = config[bstack11l11lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭દ")]
  for platform in bstack1l111ll11_opy_:
    for bstack1lllll_opy_ in list(platform):
      for bstack111ll1_opy_ in bstack1l11l1111_opy_:
        if bstack1lllll_opy_.lower() == bstack111ll1_opy_.lower() and bstack1lllll_opy_ != bstack111ll1_opy_:
          platform[bstack111ll1_opy_] = platform[bstack1lllll_opy_]
          del platform[bstack1lllll_opy_]
  for bstack1111l1l_opy_, bstack1l1l111l_opy_ in bstack11ll1ll_opy_.items():
    for platform in bstack1l111ll11_opy_:
      if isinstance(bstack1l1l111l_opy_, list):
        for bstack1lllll_opy_ in bstack1l1l111l_opy_:
          if bstack1lllll_opy_ in platform:
            platform[bstack1111l1l_opy_] = platform[bstack1lllll_opy_]
            del platform[bstack1lllll_opy_]
            break
      elif bstack1l1l111l_opy_ in platform:
        platform[bstack1111l1l_opy_] = platform[bstack1l1l111l_opy_]
        del platform[bstack1l1l111l_opy_]
  for bstack11111l11_opy_ in bstack111ll1ll_opy_:
    if bstack11111l11_opy_ in config:
      if not bstack111ll1ll_opy_[bstack11111l11_opy_] in config:
        config[bstack111ll1ll_opy_[bstack11111l11_opy_]] = {}
      config[bstack111ll1ll_opy_[bstack11111l11_opy_]].update(config[bstack11111l11_opy_])
      del config[bstack11111l11_opy_]
  for platform in bstack1l111ll11_opy_:
    for bstack11111l11_opy_ in bstack111ll1ll_opy_:
      if bstack11111l11_opy_ in list(platform):
        if not bstack111ll1ll_opy_[bstack11111l11_opy_] in platform:
          platform[bstack111ll1ll_opy_[bstack11111l11_opy_]] = {}
        platform[bstack111ll1ll_opy_[bstack11111l11_opy_]].update(platform[bstack11111l11_opy_])
        del platform[bstack11111l11_opy_]
  config = bstack1llll1_opy_(config)
  return config
def bstack1lll1_opy_(config):
  global bstack1l111ll1l_opy_
  if bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨધ") in config and str(config[bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩન")]).lower() != bstack11l11lll1_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ઩"):
    if not bstack11l11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫપ") in config:
      config[bstack11l11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬફ")] = {}
    if not bstack11l11lll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫબ") in config[bstack11l11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧભ")]:
      bstack1llll1111_opy_ = datetime.datetime.now()
      bstack1l1lll1l1_opy_ = bstack1llll1111_opy_.strftime(bstack11l11lll1_opy_ (u"ࠫࠪࡪ࡟ࠦࡤࡢࠩࡍࠫࡍࠨમ"))
      hostname = socket.gethostname()
      bstack1lllll11_opy_ = bstack11l11lll1_opy_ (u"ࠬ࠭ય").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11l11lll1_opy_ (u"࠭ࡻࡾࡡࡾࢁࡤࢁࡽࠨર").format(bstack1l1lll1l1_opy_, hostname, bstack1lllll11_opy_)
      config[bstack11l11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ઱")][bstack11l11lll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪલ")] = identifier
    bstack1l111ll1l_opy_ = config[bstack11l11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ળ")][bstack11l11lll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ઴")]
  return config
def bstack1ll11l1l_opy_():
  if (
    isinstance(os.getenv(bstack11l11lll1_opy_ (u"ࠫࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠩવ")), str) and len(os.getenv(bstack11l11lll1_opy_ (u"ࠬࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠪશ"))) > 0
  ) or (
    isinstance(os.getenv(bstack11l11lll1_opy_ (u"࠭ࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠬષ")), str) and len(os.getenv(bstack11l11lll1_opy_ (u"ࠧࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊ࠭સ"))) > 0
  ):
    return os.getenv(bstack11l11lll1_opy_ (u"ࠨࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠧહ"), 0)
  if str(os.getenv(bstack11l11lll1_opy_ (u"ࠩࡆࡍࠬ઺"))).lower() == bstack11l11lll1_opy_ (u"ࠪࡸࡷࡻࡥࠨ઻") and str(os.getenv(bstack11l11lll1_opy_ (u"ࠫࡈࡏࡒࡄࡎࡈࡇࡎ઼࠭"))).lower() == bstack11l11lll1_opy_ (u"ࠬࡺࡲࡶࡧࠪઽ"):
    return os.getenv(bstack11l11lll1_opy_ (u"࠭ࡃࡊࡔࡆࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࠩા"), 0)
  if str(os.getenv(bstack11l11lll1_opy_ (u"ࠧࡄࡋࠪિ"))).lower() == bstack11l11lll1_opy_ (u"ࠨࡶࡵࡹࡪ࠭ી") and str(os.getenv(bstack11l11lll1_opy_ (u"ࠩࡗࡖࡆ࡜ࡉࡔࠩુ"))).lower() == bstack11l11lll1_opy_ (u"ࠪࡸࡷࡻࡥࠨૂ"):
    return os.getenv(bstack11l11lll1_opy_ (u"࡙ࠫࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠪૃ"), 0)
  if str(os.getenv(bstack11l11lll1_opy_ (u"ࠬࡉࡉࠨૄ"))).lower() == bstack11l11lll1_opy_ (u"࠭ࡴࡳࡷࡨࠫૅ") and str(os.getenv(bstack11l11lll1_opy_ (u"ࠧࡄࡋࡢࡒࡆࡓࡅࠨ૆"))).lower() == bstack11l11lll1_opy_ (u"ࠨࡥࡲࡨࡪࡹࡨࡪࡲࠪે"):
    return 0 # bstack111l1l1ll_opy_ bstack1lllll1_opy_ not set build number env
  if os.getenv(bstack11l11lll1_opy_ (u"ࠩࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡒࡂࡐࡆࡌࠬૈ")) and os.getenv(bstack11l11lll1_opy_ (u"ࠪࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡃࡐࡏࡐࡍ࡙࠭ૉ")):
    return os.getenv(bstack11l11lll1_opy_ (u"ࠫࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗ࠭૊"), 0)
  if str(os.getenv(bstack11l11lll1_opy_ (u"ࠬࡉࡉࠨો"))).lower() == bstack11l11lll1_opy_ (u"࠭ࡴࡳࡷࡨࠫૌ") and str(os.getenv(bstack11l11lll1_opy_ (u"ࠧࡅࡔࡒࡒࡊ્࠭"))).lower() == bstack11l11lll1_opy_ (u"ࠨࡶࡵࡹࡪ࠭૎"):
    return os.getenv(bstack11l11lll1_opy_ (u"ࠩࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠧ૏"), 0)
  if str(os.getenv(bstack11l11lll1_opy_ (u"ࠪࡇࡎ࠭ૐ"))).lower() == bstack11l11lll1_opy_ (u"ࠫࡹࡸࡵࡦࠩ૑") and str(os.getenv(bstack11l11lll1_opy_ (u"࡙ࠬࡅࡎࡃࡓࡌࡔࡘࡅࠨ૒"))).lower() == bstack11l11lll1_opy_ (u"࠭ࡴࡳࡷࡨࠫ૓"):
    return os.getenv(bstack11l11lll1_opy_ (u"ࠧࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡊࡆࠪ૔"), 0)
  if str(os.getenv(bstack11l11lll1_opy_ (u"ࠨࡅࡌࠫ૕"))).lower() == bstack11l11lll1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ૖") and str(os.getenv(bstack11l11lll1_opy_ (u"ࠪࡋࡎ࡚ࡌࡂࡄࡢࡇࡎ࠭૗"))).lower() == bstack11l11lll1_opy_ (u"ࠫࡹࡸࡵࡦࠩ૘"):
    return os.getenv(bstack11l11lll1_opy_ (u"ࠬࡉࡉࡠࡌࡒࡆࡤࡏࡄࠨ૙"), 0)
  if str(os.getenv(bstack11l11lll1_opy_ (u"࠭ࡃࡊࠩ૚"))).lower() == bstack11l11lll1_opy_ (u"ࠧࡵࡴࡸࡩࠬ૛") and str(os.getenv(bstack11l11lll1_opy_ (u"ࠨࡄࡘࡍࡑࡊࡋࡊࡖࡈࠫ૜"))).lower() == bstack11l11lll1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ૝"):
    return os.getenv(bstack11l11lll1_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠬ૞"), 0)
  if str(os.getenv(bstack11l11lll1_opy_ (u"࡙ࠫࡌ࡟ࡃࡗࡌࡐࡉ࠭૟"))).lower() == bstack11l11lll1_opy_ (u"ࠬࡺࡲࡶࡧࠪૠ"):
    return os.getenv(bstack11l11lll1_opy_ (u"࠭ࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉ࠭ૡ"), 0)
  return -1
def bstack1lll111l1_opy_(bstack1111lll_opy_):
  global CONFIG
  if not bstack11l11lll1_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩૢ") in CONFIG[bstack11l11lll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪૣ")]:
    return
  CONFIG[bstack11l11lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૤")] = CONFIG[bstack11l11lll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૥")].replace(
    bstack11l11lll1_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭૦"),
    str(bstack1111lll_opy_)
  )
def bstack11ll1111l_opy_():
  global CONFIG
  if not bstack11l11lll1_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫ૧") in CONFIG[bstack11l11lll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૨")]:
    return
  bstack1llll1111_opy_ = datetime.datetime.now()
  bstack1l1lll1l1_opy_ = bstack1llll1111_opy_.strftime(bstack11l11lll1_opy_ (u"ࠧࠦࡦ࠰ࠩࡧ࠳ࠥࡉ࠼ࠨࡑࠬ૩"))
  CONFIG[bstack11l11lll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૪")] = CONFIG[bstack11l11lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ૫")].replace(
    bstack11l11lll1_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩ૬"),
    bstack1l1lll1l1_opy_
  )
def bstack11ll11ll_opy_():
  global CONFIG
  if bstack11l11lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૭") in CONFIG and not bool(CONFIG[bstack11l11lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૮")]):
    del CONFIG[bstack11l11lll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૯")]
    return
  if not bstack11l11lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૰") in CONFIG:
    CONFIG[bstack11l11lll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૱")] = bstack11l11lll1_opy_ (u"ࠩࠦࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬ૲")
  if bstack11l11lll1_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩ૳") in CONFIG[bstack11l11lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૴")]:
    bstack11ll1111l_opy_()
    os.environ[bstack11l11lll1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ૵")] = CONFIG[bstack11l11lll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ૶")]
  if not bstack11l11lll1_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩ૷") in CONFIG[bstack11l11lll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ૸")]:
    return
  bstack1111lll_opy_ = bstack11l11lll1_opy_ (u"ࠩࠪૹ")
  bstack1l111l1l_opy_ = bstack1ll11l1l_opy_()
  if bstack1l111l1l_opy_ != -1:
    bstack1111lll_opy_ = bstack11l11lll1_opy_ (u"ࠪࡇࡎࠦࠧૺ") + str(bstack1l111l1l_opy_)
  if bstack1111lll_opy_ == bstack11l11lll1_opy_ (u"ࠫࠬૻ"):
    bstack1l11l_opy_ = bstack11l1l1_opy_(CONFIG[bstack11l11lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨૼ")])
    if bstack1l11l_opy_ != -1:
      bstack1111lll_opy_ = str(bstack1l11l_opy_)
  if bstack1111lll_opy_:
    bstack1lll111l1_opy_(bstack1111lll_opy_)
    os.environ[bstack11l11lll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ૽")] = CONFIG[bstack11l11lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ૾")]
def bstack111l_opy_(bstack11ll_opy_, bstack111l11l11_opy_, path):
  bstack111lll1ll_opy_ = {
    bstack11l11lll1_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ૿"): bstack111l11l11_opy_
  }
  if os.path.exists(path):
    bstack11l1lllll_opy_ = json.load(open(path, bstack11l11lll1_opy_ (u"ࠩࡵࡦࠬ଀")))
  else:
    bstack11l1lllll_opy_ = {}
  bstack11l1lllll_opy_[bstack11ll_opy_] = bstack111lll1ll_opy_
  with open(path, bstack11l11lll1_opy_ (u"ࠥࡻ࠰ࠨଁ")) as outfile:
    json.dump(bstack11l1lllll_opy_, outfile)
def bstack11l1l1_opy_(bstack11ll_opy_):
  bstack11ll_opy_ = str(bstack11ll_opy_)
  bstack11l111l11_opy_ = os.path.join(os.path.expanduser(bstack11l11lll1_opy_ (u"ࠫࢃ࠭ଂ")), bstack11l11lll1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬଃ"))
  try:
    if not os.path.exists(bstack11l111l11_opy_):
      os.makedirs(bstack11l111l11_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11l11lll1_opy_ (u"࠭ࡾࠨ଄")), bstack11l11lll1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧଅ"), bstack11l11lll1_opy_ (u"ࠨ࠰ࡥࡹ࡮ࡲࡤ࠮ࡰࡤࡱࡪ࠳ࡣࡢࡥ࡫ࡩ࠳ࡰࡳࡰࡰࠪଆ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11l11lll1_opy_ (u"ࠩࡺࠫଇ")):
        pass
      with open(file_path, bstack11l11lll1_opy_ (u"ࠥࡻ࠰ࠨଈ")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11l11lll1_opy_ (u"ࠫࡷ࠭ଉ")) as bstack11ll111ll_opy_:
      bstack11llll1ll_opy_ = json.load(bstack11ll111ll_opy_)
    if bstack11ll_opy_ in bstack11llll1ll_opy_:
      bstack1lll111l_opy_ = bstack11llll1ll_opy_[bstack11ll_opy_][bstack11l11lll1_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩଊ")]
      bstack1l1lll11_opy_ = int(bstack1lll111l_opy_) + 1
      bstack111l_opy_(bstack11ll_opy_, bstack1l1lll11_opy_, file_path)
      return bstack1l1lll11_opy_
    else:
      bstack111l_opy_(bstack11ll_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1l11l1ll1_opy_.format(str(e)))
    return -1
def bstack11l111lll_opy_(config):
  if not config[bstack11l11lll1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨଋ")] or not config[bstack11l11lll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪଌ")]:
    return True
  else:
    return False
def bstack1lllll11l_opy_(config):
  if bstack11l11lll1_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧ଍") in config:
    del(config[bstack11l11lll1_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨ଎")])
    return False
  if bstack1l11lll_opy_() < version.parse(bstack11l11lll1_opy_ (u"ࠪ࠷࠳࠺࠮࠱ࠩଏ")):
    return False
  if bstack1l11lll_opy_() >= version.parse(bstack11l11lll1_opy_ (u"ࠫ࠹࠴࠱࠯࠷ࠪଐ")):
    return True
  if bstack11l11lll1_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ଑") in config and config[bstack11l11lll1_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭଒")] == False:
    return False
  else:
    return True
def bstack1l1lll11l_opy_(config, index = 0):
  global bstack1lll11l_opy_
  bstack111l111l1_opy_ = {}
  caps = bstack1lll1l11_opy_ + bstack1111l11l_opy_
  if bstack1lll11l_opy_:
    caps += bstack1111l111_opy_
  for key in config:
    if key in caps + [bstack11l11lll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଓ")]:
      continue
    bstack111l111l1_opy_[key] = config[key]
  if bstack11l11lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫଔ") in config:
    for bstack1ll1llll1_opy_ in config[bstack11l11lll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬକ")][index]:
      if bstack1ll1llll1_opy_ in caps + [bstack11l11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨଖ"), bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬଗ")]:
        continue
      bstack111l111l1_opy_[bstack1ll1llll1_opy_] = config[bstack11l11lll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨଘ")][index][bstack1ll1llll1_opy_]
  bstack111l111l1_opy_[bstack11l11lll1_opy_ (u"࠭ࡨࡰࡵࡷࡒࡦࡳࡥࠨଙ")] = socket.gethostname()
  if bstack11l11lll1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨଚ") in bstack111l111l1_opy_:
    del(bstack111l111l1_opy_[bstack11l11lll1_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩଛ")])
  return bstack111l111l1_opy_
def bstack11l1l1ll_opy_(config):
  global bstack1lll11l_opy_
  bstack111ll11l_opy_ = {}
  caps = bstack1111l11l_opy_
  if bstack1lll11l_opy_:
    caps+= bstack1111l111_opy_
  for key in caps:
    if key in config:
      bstack111ll11l_opy_[key] = config[key]
  return bstack111ll11l_opy_
def bstack111lllll_opy_(bstack111l111l1_opy_, bstack111ll11l_opy_):
  bstack11ll11l11_opy_ = {}
  for key in bstack111l111l1_opy_.keys():
    if key in bstack1lllllll1_opy_:
      bstack11ll11l11_opy_[bstack1lllllll1_opy_[key]] = bstack111l111l1_opy_[key]
    else:
      bstack11ll11l11_opy_[key] = bstack111l111l1_opy_[key]
  for key in bstack111ll11l_opy_:
    if key in bstack1lllllll1_opy_:
      bstack11ll11l11_opy_[bstack1lllllll1_opy_[key]] = bstack111ll11l_opy_[key]
    else:
      bstack11ll11l11_opy_[key] = bstack111ll11l_opy_[key]
  return bstack11ll11l11_opy_
def bstack1l1lll111_opy_(config, index = 0):
  global bstack1lll11l_opy_
  config = copy.deepcopy(config)
  caps = {}
  bstack111ll11l_opy_ = bstack11l1l1ll_opy_(config)
  bstack11ll111l1_opy_ = bstack1111l11l_opy_
  bstack11ll111l1_opy_ += bstack11lll1ll_opy_
  if bstack1lll11l_opy_:
    bstack11ll111l1_opy_ += bstack1111l111_opy_
  if bstack11l11lll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬଜ") in config:
    if bstack11l11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨଝ") in config[bstack11l11lll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଞ")][index]:
      caps[bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪଟ")] = config[bstack11l11lll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଠ")][index][bstack11l11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬଡ")]
    if bstack11l11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩଢ") in config[bstack11l11lll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬଣ")][index]:
      caps[bstack11l11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫତ")] = str(config[bstack11l11lll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଥ")][index][bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ଦ")])
    bstack11l1l1ll1_opy_ = {}
    for bstack11111lll_opy_ in bstack11ll111l1_opy_:
      if bstack11111lll_opy_ in config[bstack11l11lll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଧ")][index]:
        if bstack11111lll_opy_ == bstack11l11lll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩନ"):
          bstack11l1l1ll1_opy_[bstack11111lll_opy_] = str(config[bstack11l11lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ଩")][index][bstack11111lll_opy_] * 1.0)
        else:
          bstack11l1l1ll1_opy_[bstack11111lll_opy_] = config[bstack11l11lll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬପ")][index][bstack11111lll_opy_]
        del(config[bstack11l11lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଫ")][index][bstack11111lll_opy_])
    bstack111ll11l_opy_ = update(bstack111ll11l_opy_, bstack11l1l1ll1_opy_)
  bstack111l111l1_opy_ = bstack1l1lll11l_opy_(config, index)
  for bstack1lllll_opy_ in bstack1111l11l_opy_ + [bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩବ"), bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ଭ")]:
    if bstack1lllll_opy_ in bstack111l111l1_opy_:
      bstack111ll11l_opy_[bstack1lllll_opy_] = bstack111l111l1_opy_[bstack1lllll_opy_]
      del(bstack111l111l1_opy_[bstack1lllll_opy_])
  if bstack1lllll11l_opy_(config):
    bstack111l111l1_opy_[bstack11l11lll1_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ମ")] = True
    caps.update(bstack111ll11l_opy_)
    caps[bstack11l11lll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨଯ")] = bstack111l111l1_opy_
  else:
    bstack111l111l1_opy_[bstack11l11lll1_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨର")] = False
    caps.update(bstack111lllll_opy_(bstack111l111l1_opy_, bstack111ll11l_opy_))
    if bstack11l11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ଱") in caps:
      caps[bstack11l11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫଲ")] = caps[bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩଳ")]
      del(caps[bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ଴")])
    if bstack11l11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧଵ") in caps:
      caps[bstack11l11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩଶ")] = caps[bstack11l11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩଷ")]
      del(caps[bstack11l11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪସ")])
  return caps
def bstack111_opy_():
  global bstack1l1llllll_opy_
  if bstack1l11lll_opy_() <= version.parse(bstack11l11lll1_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪହ")):
    if bstack1l1llllll_opy_ != bstack11l11lll1_opy_ (u"ࠫࠬ଺"):
      return bstack11l11lll1_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ଻") + bstack1l1llllll_opy_ + bstack11l11lll1_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤ଼ࠥ")
    return bstack1l11l1lll_opy_
  if  bstack1l1llllll_opy_ != bstack11l11lll1_opy_ (u"ࠧࠨଽ"):
    return bstack11l11lll1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥା") + bstack1l1llllll_opy_ + bstack11l11lll1_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥି")
  return bstack1lllll1l1_opy_
def bstack1l111l1_opy_(options):
  return hasattr(options, bstack11l11lll1_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫୀ"))
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
def bstack1l1_opy_(options, bstack1l111ll1_opy_):
  for bstack11lll111l_opy_ in bstack1l111ll1_opy_:
    if bstack11lll111l_opy_ in [bstack11l11lll1_opy_ (u"ࠫࡦࡸࡧࡴࠩୁ"), bstack11l11lll1_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩୂ")]:
      next
    if bstack11lll111l_opy_ in options._experimental_options:
      options._experimental_options[bstack11lll111l_opy_]= update(options._experimental_options[bstack11lll111l_opy_], bstack1l111ll1_opy_[bstack11lll111l_opy_])
    else:
      options.add_experimental_option(bstack11lll111l_opy_, bstack1l111ll1_opy_[bstack11lll111l_opy_])
  if bstack11l11lll1_opy_ (u"࠭ࡡࡳࡩࡶࠫୃ") in bstack1l111ll1_opy_:
    for arg in bstack1l111ll1_opy_[bstack11l11lll1_opy_ (u"ࠧࡢࡴࡪࡷࠬୄ")]:
      options.add_argument(arg)
    del(bstack1l111ll1_opy_[bstack11l11lll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭୅")])
  if bstack11l11lll1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭୆") in bstack1l111ll1_opy_:
    for ext in bstack1l111ll1_opy_[bstack11l11lll1_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧେ")]:
      options.add_extension(ext)
    del(bstack1l111ll1_opy_[bstack11l11lll1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨୈ")])
def bstack1l111111l_opy_(options, bstack1l1l1l111_opy_):
  if bstack11l11lll1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ୉") in bstack1l1l1l111_opy_:
    for bstack1l1l1llll_opy_ in bstack1l1l1l111_opy_[bstack11l11lll1_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ୊")]:
      if bstack1l1l1llll_opy_ in options._preferences:
        options._preferences[bstack1l1l1llll_opy_] = update(options._preferences[bstack1l1l1llll_opy_], bstack1l1l1l111_opy_[bstack11l11lll1_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ୋ")][bstack1l1l1llll_opy_])
      else:
        options.set_preference(bstack1l1l1llll_opy_, bstack1l1l1l111_opy_[bstack11l11lll1_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧୌ")][bstack1l1l1llll_opy_])
  if bstack11l11lll1_opy_ (u"ࠩࡤࡶ࡬ࡹ୍ࠧ") in bstack1l1l1l111_opy_:
    for arg in bstack1l1l1l111_opy_[bstack11l11lll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ୎")]:
      options.add_argument(arg)
def bstack111lll11_opy_(options, bstack11ll11l1_opy_):
  if bstack11l11lll1_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬ୏") in bstack11ll11l1_opy_:
    options.use_webview(bool(bstack11ll11l1_opy_[bstack11l11lll1_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭୐")]))
  bstack1l1_opy_(options, bstack11ll11l1_opy_)
def bstack111lll11l_opy_(options, bstack1lll1l111_opy_):
  for bstack1l1111ll1_opy_ in bstack1lll1l111_opy_:
    if bstack1l1111ll1_opy_ in [bstack11l11lll1_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪ୑"), bstack11l11lll1_opy_ (u"ࠧࡢࡴࡪࡷࠬ୒")]:
      next
    options.set_capability(bstack1l1111ll1_opy_, bstack1lll1l111_opy_[bstack1l1111ll1_opy_])
  if bstack11l11lll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭୓") in bstack1lll1l111_opy_:
    for arg in bstack1lll1l111_opy_[bstack11l11lll1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ୔")]:
      options.add_argument(arg)
  if bstack11l11lll1_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧ୕") in bstack1lll1l111_opy_:
    options.use_technology_preview(bool(bstack1lll1l111_opy_[bstack11l11lll1_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨୖ")]))
def bstack1lll11lll_opy_(options, bstack11l1ll1_opy_):
  for bstack111l11l1_opy_ in bstack11l1ll1_opy_:
    if bstack111l11l1_opy_ in [bstack11l11lll1_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩୗ"), bstack11l11lll1_opy_ (u"࠭ࡡࡳࡩࡶࠫ୘")]:
      next
    options._options[bstack111l11l1_opy_] = bstack11l1ll1_opy_[bstack111l11l1_opy_]
  if bstack11l11lll1_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ୙") in bstack11l1ll1_opy_:
    for bstack11l111l1_opy_ in bstack11l1ll1_opy_[bstack11l11lll1_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ୚")]:
      options.bstack111l1llll_opy_(
          bstack11l111l1_opy_, bstack11l1ll1_opy_[bstack11l11lll1_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭୛")][bstack11l111l1_opy_])
  if bstack11l11lll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨଡ଼") in bstack11l1ll1_opy_:
    for arg in bstack11l1ll1_opy_[bstack11l11lll1_opy_ (u"ࠫࡦࡸࡧࡴࠩଢ଼")]:
      options.add_argument(arg)
def bstack1lll_opy_(options, caps):
  if not hasattr(options, bstack11l11lll1_opy_ (u"ࠬࡑࡅ࡚ࠩ୞")):
    return
  if options.KEY == bstack11l11lll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫୟ") and options.KEY in caps:
    bstack1l1_opy_(options, caps[bstack11l11lll1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬୠ")])
  elif options.KEY == bstack11l11lll1_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ୡ") and options.KEY in caps:
    bstack1l111111l_opy_(options, caps[bstack11l11lll1_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧୢ")])
  elif options.KEY == bstack11l11lll1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫୣ") and options.KEY in caps:
    bstack111lll11l_opy_(options, caps[bstack11l11lll1_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬ୤")])
  elif options.KEY == bstack11l11lll1_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭୥") and options.KEY in caps:
    bstack111lll11_opy_(options, caps[bstack11l11lll1_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ୦")])
  elif options.KEY == bstack11l11lll1_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭୧") and options.KEY in caps:
    bstack1lll11lll_opy_(options, caps[bstack11l11lll1_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ୨")])
def bstack11l1ll11l_opy_(caps):
  global bstack1lll11l_opy_
  if bstack1lll11l_opy_:
    if bstack1ll11l1ll_opy_() < version.parse(bstack11l11lll1_opy_ (u"ࠩ࠵࠲࠸࠴࠰ࠨ୩")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11l11lll1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ୪")
    if bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ୫") in caps:
      browser = caps[bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ୬")]
    elif bstack11l11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ୭") in caps:
      browser = caps[bstack11l11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ୮")]
    browser = str(browser).lower()
    if browser == bstack11l11lll1_opy_ (u"ࠨ࡫ࡳ࡬ࡴࡴࡥࠨ୯") or browser == bstack11l11lll1_opy_ (u"ࠩ࡬ࡴࡦࡪࠧ୰"):
      browser = bstack11l11lll1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪୱ")
    if browser == bstack11l11lll1_opy_ (u"ࠫࡸࡧ࡭ࡴࡷࡱ࡫ࠬ୲"):
      browser = bstack11l11lll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ୳")
    if browser not in [bstack11l11lll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭୴"), bstack11l11lll1_opy_ (u"ࠧࡦࡦࡪࡩࠬ୵"), bstack11l11lll1_opy_ (u"ࠨ࡫ࡨࠫ୶"), bstack11l11lll1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩ୷"), bstack11l11lll1_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫ୸")]:
      return None
    try:
      package = bstack11l11lll1_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡾࢁ࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭୹").format(browser)
      name = bstack11l11lll1_opy_ (u"ࠬࡕࡰࡵ࡫ࡲࡲࡸ࠭୺")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l111l1_opy_(options):
        return None
      for bstack1lllll_opy_ in caps.keys():
        options.set_capability(bstack1lllll_opy_, caps[bstack1lllll_opy_])
      bstack1lll_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1lllll111_opy_(options, bstack1lll11l11_opy_):
  if not bstack1l111l1_opy_(options):
    return
  for bstack1lllll_opy_ in bstack1lll11l11_opy_.keys():
    if bstack1lllll_opy_ in bstack11lll1ll_opy_:
      next
    if bstack1lllll_opy_ in options._caps and type(options._caps[bstack1lllll_opy_]) in [dict, list]:
      options._caps[bstack1lllll_opy_] = update(options._caps[bstack1lllll_opy_], bstack1lll11l11_opy_[bstack1lllll_opy_])
    else:
      options.set_capability(bstack1lllll_opy_, bstack1lll11l11_opy_[bstack1lllll_opy_])
  bstack1lll_opy_(options, bstack1lll11l11_opy_)
  if bstack11l11lll1_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬ୻") in options._caps:
    if options._caps[bstack11l11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ୼")] and options._caps[bstack11l11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭୽")].lower() != bstack11l11lll1_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪ୾"):
      del options._caps[bstack11l11lll1_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩ୿")]
def bstack11l111111_opy_(proxy_config):
  if bstack11l11lll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ஀") in proxy_config:
    proxy_config[bstack11l11lll1_opy_ (u"ࠬࡹࡳ࡭ࡒࡵࡳࡽࡿࠧ஁")] = proxy_config[bstack11l11lll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪஂ")]
    del(proxy_config[bstack11l11lll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫஃ")])
  if bstack11l11lll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ஄") in proxy_config and proxy_config[bstack11l11lll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬஅ")].lower() != bstack11l11lll1_opy_ (u"ࠪࡨ࡮ࡸࡥࡤࡶࠪஆ"):
    proxy_config[bstack11l11lll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧஇ")] = bstack11l11lll1_opy_ (u"ࠬࡳࡡ࡯ࡷࡤࡰࠬஈ")
  if bstack11l11lll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡆࡻࡴࡰࡥࡲࡲ࡫࡯ࡧࡖࡴ࡯ࠫஉ") in proxy_config:
    proxy_config[bstack11l11lll1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪஊ")] = bstack11l11lll1_opy_ (u"ࠨࡲࡤࡧࠬ஋")
  return proxy_config
def bstack1l1l1ll1l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11l11lll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ஌") in config:
    return proxy
  config[bstack11l11lll1_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ஍")] = bstack11l111111_opy_(config[bstack11l11lll1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪஎ")])
  if proxy == None:
    proxy = Proxy(config[bstack11l11lll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫஏ")])
  return proxy
def bstack11l1llll_opy_(self):
  global CONFIG
  global bstack11ll1l111_opy_
  try:
    proxy = bstack1ll1lll1l_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11l11lll1_opy_ (u"࠭࠮ࡱࡣࡦࠫஐ")):
        proxies = bstack11l1l111_opy_(proxy, bstack111_opy_())
        if len(proxies) > 0:
          protocol, bstack1llllll1_opy_ = proxies.popitem()
          if bstack11l11lll1_opy_ (u"ࠢ࠻࠱࠲ࠦ஑") in bstack1llllll1_opy_:
            return bstack1llllll1_opy_
          else:
            return bstack11l11lll1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤஒ") + bstack1llllll1_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11l11lll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨஓ").format(str(e)))
  return bstack11ll1l111_opy_(self)
def bstack1l1lllll1_opy_():
  global CONFIG
  return bstack11l11lll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ஔ") in CONFIG or bstack11l11lll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨக") in CONFIG
def bstack1ll1lll1l_opy_(config):
  if not bstack1l1lllll1_opy_():
    return
  if config.get(bstack11l11lll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ஖")):
    return config.get(bstack11l11lll1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ஗"))
  if config.get(bstack11l11lll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ஘")):
    return config.get(bstack11l11lll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬங"))
def bstack1l11lll1l_opy_(url):
  try:
      result = urlparse(url)
      return all([result.scheme, result.netloc])
  except:
      return False
def bstack111l1lll1_opy_(bstack11l1lll1l_opy_, bstack11l1llll1_opy_):
  from pypac import get_pac
  from pypac import PACSession
  from pypac.parser import PACFile
  import socket
  if os.path.isfile(bstack11l1lll1l_opy_):
    with open(bstack11l1lll1l_opy_) as f:
      pac = PACFile(f.read())
  elif bstack1l11lll1l_opy_(bstack11l1lll1l_opy_):
    pac = get_pac(url=bstack11l1lll1l_opy_)
  else:
    raise Exception(bstack11l11lll1_opy_ (u"ࠩࡓࡥࡨࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠩச").format(bstack11l1lll1l_opy_))
  session = PACSession(pac)
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((bstack11l11lll1_opy_ (u"ࠥ࠼࠳࠾࠮࠹࠰࠻ࠦ஛"), 80))
    bstack111ll11_opy_ = s.getsockname()[0]
    s.close()
  except:
    bstack111ll11_opy_ = bstack11l11lll1_opy_ (u"ࠫ࠵࠴࠰࠯࠲࠱࠴ࠬஜ")
  proxy_url = session.get_pac().find_proxy_for_url(bstack11l1llll1_opy_, bstack111ll11_opy_)
  return proxy_url
def bstack11l1l111_opy_(bstack11l1lll1l_opy_, bstack11l1llll1_opy_):
  proxies = {}
  global bstack1l11ll1l_opy_
  if bstack11l11lll1_opy_ (u"ࠬࡖࡁࡄࡡࡓࡖࡔ࡞࡙ࠨ஝") in globals():
    return bstack1l11ll1l_opy_
  try:
    proxy = bstack111l1lll1_opy_(bstack11l1lll1l_opy_,bstack11l1llll1_opy_)
    if bstack11l11lll1_opy_ (u"ࠨࡄࡊࡔࡈࡇ࡙ࠨஞ") in proxy:
      proxies = {}
    elif bstack11l11lll1_opy_ (u"ࠢࡉࡖࡗࡔࠧட") in proxy or bstack11l11lll1_opy_ (u"ࠣࡊࡗࡘࡕ࡙ࠢ஠") in proxy or bstack11l11lll1_opy_ (u"ࠤࡖࡓࡈࡑࡓࠣ஡") in proxy:
      bstack1ll111ll1_opy_ = proxy.split(bstack11l11lll1_opy_ (u"ࠥࠤࠧ஢"))
      if bstack11l11lll1_opy_ (u"ࠦ࠿࠵࠯ࠣண") in bstack11l11lll1_opy_ (u"ࠧࠨத").join(bstack1ll111ll1_opy_[1:]):
        proxies = {
          bstack11l11lll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ஥"): bstack11l11lll1_opy_ (u"ࠢࠣ஦").join(bstack1ll111ll1_opy_[1:])
        }
      else:
        proxies = {
          bstack11l11lll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ஧") : str(bstack1ll111ll1_opy_[0]).lower()+ bstack11l11lll1_opy_ (u"ࠤ࠽࠳࠴ࠨந") + bstack11l11lll1_opy_ (u"ࠥࠦன").join(bstack1ll111ll1_opy_[1:])
        }
    elif bstack11l11lll1_opy_ (u"ࠦࡕࡘࡏ࡙࡛ࠥப") in proxy:
      bstack1ll111ll1_opy_ = proxy.split(bstack11l11lll1_opy_ (u"ࠧࠦࠢ஫"))
      if bstack11l11lll1_opy_ (u"ࠨ࠺࠰࠱ࠥ஬") in bstack11l11lll1_opy_ (u"ࠢࠣ஭").join(bstack1ll111ll1_opy_[1:]):
        proxies = {
          bstack11l11lll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧம"): bstack11l11lll1_opy_ (u"ࠤࠥய").join(bstack1ll111ll1_opy_[1:])
        }
      else:
        proxies = {
          bstack11l11lll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩர"): bstack11l11lll1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧற") + bstack11l11lll1_opy_ (u"ࠧࠨல").join(bstack1ll111ll1_opy_[1:])
        }
    else:
      proxies = {
        bstack11l11lll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬள"): proxy
      }
  except Exception as e:
    logger.error(bstack11ll1l11l_opy_.format(bstack11l1lll1l_opy_, str(e)))
  bstack1l11ll1l_opy_ = proxies
  return proxies
def bstack1l1l1ll1_opy_(config, bstack11l1llll1_opy_):
  proxy = bstack1ll1lll1l_opy_(config)
  proxies = {}
  if config.get(bstack11l11lll1_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪழ")) or config.get(bstack11l11lll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬவ")):
    if proxy.endswith(bstack11l11lll1_opy_ (u"ࠩ࠱ࡴࡦࡩࠧஶ")):
      proxies = bstack11l1l111_opy_(proxy,bstack11l1llll1_opy_)
    else:
      proxies = {
        bstack11l11lll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩஷ"): proxy
      }
  return proxies
def bstack11ll11ll1_opy_():
  return bstack1l1lllll1_opy_() and bstack1l11lll_opy_() >= version.parse(bstack1111lll1_opy_)
def bstack1ll1ll11_opy_(config):
  bstack1ll111l1l_opy_ = {}
  if bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨஸ") in config:
    bstack1ll111l1l_opy_ =  config[bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩஹ")]
  if bstack11l11lll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ஺") in config:
    bstack1ll111l1l_opy_ = config[bstack11l11lll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭஻")]
  proxy = bstack1ll1lll1l_opy_(config)
  if proxy:
    if proxy.endswith(bstack11l11lll1_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭஼")) and os.path.isfile(proxy):
      bstack1ll111l1l_opy_[bstack11l11lll1_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬ஽")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11l11lll1_opy_ (u"ࠪ࠲ࡵࡧࡣࠨா")):
        proxies = bstack1l1l1ll1_opy_(config, bstack111_opy_())
        if len(proxies) > 0:
          protocol, bstack1llllll1_opy_ = proxies.popitem()
          if bstack11l11lll1_opy_ (u"ࠦ࠿࠵࠯ࠣி") in bstack1llllll1_opy_:
            parsed_url = urlparse(bstack1llllll1_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11l11lll1_opy_ (u"ࠧࡀ࠯࠰ࠤீ") + bstack1llllll1_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1ll111l1l_opy_[bstack11l11lll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡍࡵࡳࡵࠩு")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1ll111l1l_opy_[bstack11l11lll1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪூ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1ll111l1l_opy_[bstack11l11lll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫ௃")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1ll111l1l_opy_[bstack11l11lll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬ௄")] = str(parsed_url.password)
  return bstack1ll111l1l_opy_
def bstack11ll1l1l1_opy_(config):
  if bstack11l11lll1_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨ௅") in config:
    return config[bstack11l11lll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩெ")]
  return {}
def bstack1l11l1l1l_opy_(caps):
  global bstack1l111ll1l_opy_
  if bstack11l11lll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ே") in caps:
    caps[bstack11l11lll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧை")][bstack11l11lll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭௉")] = True
    if bstack1l111ll1l_opy_:
      caps[bstack11l11lll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩொ")][bstack11l11lll1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫோ")] = bstack1l111ll1l_opy_
  else:
    caps[bstack11l11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨௌ")] = True
    if bstack1l111ll1l_opy_:
      caps[bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ்ࠬ")] = bstack1l111ll1l_opy_
def bstack111l11l1l_opy_():
  global CONFIG
  if bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ௎") in CONFIG and CONFIG[bstack11l11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ௏")]:
    bstack1ll111l1l_opy_ = bstack1ll1ll11_opy_(CONFIG)
    bstack1ll1lll1_opy_(CONFIG[bstack11l11lll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪௐ")], bstack1ll111l1l_opy_)
def bstack1ll1lll1_opy_(key, bstack1ll111l1l_opy_):
  global bstack1ll1111l_opy_
  logger.info(bstack1l1111lll_opy_)
  try:
    bstack1ll1111l_opy_ = Local()
    bstack1l1111111_opy_ = {bstack11l11lll1_opy_ (u"ࠨ࡭ࡨࡽࠬ௑"): key}
    bstack1l1111111_opy_.update(bstack1ll111l1l_opy_)
    logger.debug(bstack1ll111_opy_.format(str(bstack1l1111111_opy_)))
    bstack1ll1111l_opy_.start(**bstack1l1111111_opy_)
    if bstack1ll1111l_opy_.isRunning():
      logger.info(bstack11lll1l11_opy_)
  except Exception as e:
    bstack111l1l111_opy_(bstack1ll11l1l1_opy_.format(str(e)))
def bstack1ll11111l_opy_():
  global bstack1ll1111l_opy_
  if bstack1ll1111l_opy_.isRunning():
    logger.info(bstack11l111l_opy_)
    bstack1ll1111l_opy_.stop()
  bstack1ll1111l_opy_ = None
def bstack11l1ll1l1_opy_(bstack111llll1_opy_=[]):
  global CONFIG
  bstack1l_opy_ = []
  bstack1l1lll1ll_opy_ = [bstack11l11lll1_opy_ (u"ࠩࡲࡷࠬ௒"), bstack11l11lll1_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭௓"), bstack11l11lll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ௔"), bstack11l11lll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ௕"), bstack11l11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ௖"), bstack11l11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨௗ")]
  try:
    for err in bstack111llll1_opy_:
      bstack1ll1ll1l1_opy_ = {}
      for k in bstack1l1lll1ll_opy_:
        val = CONFIG[bstack11l11lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௘")][int(err[bstack11l11lll1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ௙")])].get(k)
        if val:
          bstack1ll1ll1l1_opy_[k] = val
      bstack1ll1ll1l1_opy_[bstack11l11lll1_opy_ (u"ࠪࡸࡪࡹࡴࡴࠩ௚")] = {
        err[bstack11l11lll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ௛")]: err[bstack11l11lll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ௜")]
      }
      bstack1l_opy_.append(bstack1ll1ll1l1_opy_)
  except Exception as e:
    logger.debug(bstack11l11lll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨࡲࡶࡲࡧࡴࡵ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡀࠠࠨ௝") +str(e))
  finally:
    return bstack1l_opy_
def bstack1l1l11111_opy_():
  global bstack1ll1l1_opy_
  global bstack11l111ll1_opy_
  global bstack1l1ll1l_opy_
  if bstack1ll1l1_opy_:
    logger.warning(bstack1ll1111ll_opy_.format(str(bstack1ll1l1_opy_)))
  logger.info(bstack11l1l1l1_opy_)
  global bstack1ll1111l_opy_
  if bstack1ll1111l_opy_:
    bstack1ll11111l_opy_()
  try:
    for driver in bstack11l111ll1_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1lll1lll_opy_)
  bstack1l11ll1_opy_()
  if len(bstack1l1ll1l_opy_) > 0:
    message = bstack11l1ll1l1_opy_(bstack1l1ll1l_opy_)
    bstack1l11ll1_opy_(message)
  else:
    bstack1l11ll1_opy_()
def bstack1l11ll11l_opy_(self, *args):
  logger.error(bstack1lll1l1l1_opy_)
  bstack1l1l11111_opy_()
  sys.exit(1)
def bstack111l1l111_opy_(err):
  logger.critical(bstack1l1l111ll_opy_.format(str(err)))
  bstack1l11ll1_opy_(bstack1l1l111ll_opy_.format(str(err)))
  atexit.unregister(bstack1l1l11111_opy_)
  sys.exit(1)
def bstack1111l1l1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1l11ll1_opy_(message)
  atexit.unregister(bstack1l1l11111_opy_)
  sys.exit(1)
def bstack111l11l_opy_():
  global CONFIG
  global bstack1l11lll1_opy_
  global bstack1l11l11l_opy_
  global bstack111lll111_opy_
  CONFIG = bstack11l11l11l_opy_()
  bstack1ll1lll11_opy_()
  bstack1l1ll111l_opy_()
  CONFIG = bstack1l11111l1_opy_(CONFIG)
  update(CONFIG, bstack1l11l11l_opy_)
  update(CONFIG, bstack1l11lll1_opy_)
  CONFIG = bstack1lll1_opy_(CONFIG)
  if bstack11l11lll1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ௞") in CONFIG and str(CONFIG[bstack11l11lll1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ௟")]).lower() == bstack11l11lll1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ௠"):
    bstack111lll111_opy_ = False
  if (bstack11l11lll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭௡") in CONFIG and bstack11l11lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ௢") in bstack1l11lll1_opy_) or (bstack11l11lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ௣") in CONFIG and bstack11l11lll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ௤") not in bstack1l11l11l_opy_):
    if os.getenv(bstack11l11lll1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫ௥")):
      CONFIG[bstack11l11lll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ௦")] = os.getenv(bstack11l11lll1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭௧"))
    else:
      bstack11ll11ll_opy_()
  elif (bstack11l11lll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭௨") not in CONFIG and bstack11l11lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭௩") in CONFIG) or (bstack11l11lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ௪") in bstack1l11l11l_opy_ and bstack11l11lll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ௫") not in bstack1l11lll1_opy_):
    del(CONFIG[bstack11l11lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ௬")])
  if bstack11l111lll_opy_(CONFIG):
    bstack111l1l111_opy_(bstack1l11llll_opy_)
  bstack1l1l1lll1_opy_()
  bstack1l1ll_opy_()
  if bstack1lll11l_opy_:
    CONFIG[bstack11l11lll1_opy_ (u"ࠨࡣࡳࡴࠬ௭")] = bstack11ll1llll_opy_(CONFIG)
    logger.info(bstack1l111_opy_.format(CONFIG[bstack11l11lll1_opy_ (u"ࠩࡤࡴࡵ࠭௮")]))
def bstack1l1ll_opy_():
  global CONFIG
  global bstack1lll11l_opy_
  if bstack11l11lll1_opy_ (u"ࠪࡥࡵࡶࠧ௯") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1111l1l1_opy_(e, bstack1ll1l111l_opy_)
    bstack1lll11l_opy_ = True
def bstack11ll1llll_opy_(config):
  bstack1ll1ll1_opy_ = bstack11l11lll1_opy_ (u"ࠫࠬ௰")
  app = config[bstack11l11lll1_opy_ (u"ࠬࡧࡰࡱࠩ௱")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1l1l11l11_opy_:
      if os.path.exists(app):
        bstack1ll1ll1_opy_ = bstack11lll11ll_opy_(config, app)
      elif bstack11ll1l_opy_(app):
        bstack1ll1ll1_opy_ = app
      else:
        bstack111l1l111_opy_(bstack11l1l1l11_opy_.format(app))
    else:
      if bstack11ll1l_opy_(app):
        bstack1ll1ll1_opy_ = app
      elif os.path.exists(app):
        bstack1ll1ll1_opy_ = bstack11lll11ll_opy_(app)
      else:
        bstack111l1l111_opy_(bstack1ll1lll_opy_)
  else:
    if len(app) > 2:
      bstack111l1l111_opy_(bstack111l1ll11_opy_)
    elif len(app) == 2:
      if bstack11l11lll1_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ௲") in app and bstack11l11lll1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪ௳") in app:
        if os.path.exists(app[bstack11l11lll1_opy_ (u"ࠨࡲࡤࡸ࡭࠭௴")]):
          bstack1ll1ll1_opy_ = bstack11lll11ll_opy_(config, app[bstack11l11lll1_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ௵")], app[bstack11l11lll1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭௶")])
        else:
          bstack111l1l111_opy_(bstack11l1l1l11_opy_.format(app))
      else:
        bstack111l1l111_opy_(bstack111l1ll11_opy_)
    else:
      for key in app:
        if key in bstack1ll111l11_opy_:
          if key == bstack11l11lll1_opy_ (u"ࠫࡵࡧࡴࡩࠩ௷"):
            if os.path.exists(app[key]):
              bstack1ll1ll1_opy_ = bstack11lll11ll_opy_(config, app[key])
            else:
              bstack111l1l111_opy_(bstack11l1l1l11_opy_.format(app))
          else:
            bstack1ll1ll1_opy_ = app[key]
        else:
          bstack111l1l111_opy_(bstack1l1l11l_opy_)
  return bstack1ll1ll1_opy_
def bstack11ll1l_opy_(bstack1ll1ll1_opy_):
  import re
  bstack11l1l11_opy_ = re.compile(bstack11l11lll1_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧ௸"))
  bstack1lll1lll1_opy_ = re.compile(bstack11l11lll1_opy_ (u"ࡸࠢ࡟࡝ࡤ࠱ࡿࡇ࡛࠭࠲࠰࠽ࡡࡥ࠮࡝࠯ࡠ࠮࠴ࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥ௹"))
  if bstack11l11lll1_opy_ (u"ࠧࡣࡵ࠽࠳࠴࠭௺") in bstack1ll1ll1_opy_ or re.fullmatch(bstack11l1l11_opy_, bstack1ll1ll1_opy_) or re.fullmatch(bstack1lll1lll1_opy_, bstack1ll1ll1_opy_):
    return True
  else:
    return False
def bstack11lll11ll_opy_(config, path, bstack11ll1ll1_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11l11lll1_opy_ (u"ࠨࡴࡥࠫ௻")).read()).hexdigest()
  bstack11l1111_opy_ = bstack11l11l11_opy_(md5_hash)
  bstack1ll1ll1_opy_ = None
  if bstack11l1111_opy_:
    logger.info(bstack11l1l1111_opy_.format(bstack11l1111_opy_, md5_hash))
    return bstack11l1111_opy_
  bstack1llll1ll1_opy_ = MultipartEncoder(
    fields={
        bstack11l11lll1_opy_ (u"ࠩࡩ࡭ࡱ࡫ࠧ௼"): (os.path.basename(path), open(os.path.abspath(path), bstack11l11lll1_opy_ (u"ࠪࡶࡧ࠭௽")), bstack11l11lll1_opy_ (u"ࠫࡹ࡫ࡸࡵ࠱ࡳࡰࡦ࡯࡮ࠨ௾")),
        bstack11l11lll1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ௿"): bstack11ll1ll1_opy_
    }
  )
  response = requests.post(bstack1l11l1l11_opy_, data=bstack1llll1ll1_opy_,
                         headers={bstack11l11lll1_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬఀ"): bstack1llll1ll1_opy_.content_type}, auth=(config[bstack11l11lll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩఁ")], config[bstack11l11lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫం")]))
  try:
    res = json.loads(response.text)
    bstack1ll1ll1_opy_ = res[bstack11l11lll1_opy_ (u"ࠩࡤࡴࡵࡥࡵࡳ࡮ࠪః")]
    logger.info(bstack111ll1111_opy_.format(bstack1ll1ll1_opy_))
    bstack1ll11llll_opy_(md5_hash, bstack1ll1ll1_opy_)
  except ValueError as err:
    bstack111l1l111_opy_(bstack11111111_opy_.format(str(err)))
  return bstack1ll1ll1_opy_
def bstack1l1l1lll1_opy_():
  global CONFIG
  global bstack11111ll1_opy_
  bstack111l1lll_opy_ = 0
  bstack1l1l1l1l1_opy_ = 1
  if bstack11l11lll1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪఄ") in CONFIG:
    bstack1l1l1l1l1_opy_ = CONFIG[bstack11l11lll1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫఅ")]
  if bstack11l11lll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨఆ") in CONFIG:
    bstack111l1lll_opy_ = len(CONFIG[bstack11l11lll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩఇ")])
  bstack11111ll1_opy_ = int(bstack1l1l1l1l1_opy_) * int(bstack111l1lll_opy_)
def bstack11l11l11_opy_(md5_hash):
  bstack11l1lll1_opy_ = os.path.join(os.path.expanduser(bstack11l11lll1_opy_ (u"ࠧࡿࠩఈ")), bstack11l11lll1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨఉ"), bstack11l11lll1_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪఊ"))
  if os.path.exists(bstack11l1lll1_opy_):
    bstack11l11ll11_opy_ = json.load(open(bstack11l1lll1_opy_,bstack11l11lll1_opy_ (u"ࠪࡶࡧ࠭ఋ")))
    if md5_hash in bstack11l11ll11_opy_:
      bstack11l11ll1_opy_ = bstack11l11ll11_opy_[md5_hash]
      bstack1l1111ll_opy_ = datetime.datetime.now()
      bstack1ll1ll_opy_ = datetime.datetime.strptime(bstack11l11ll1_opy_[bstack11l11lll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧఌ")], bstack11l11lll1_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ఍"))
      if (bstack1l1111ll_opy_ - bstack1ll1ll_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack11l11ll1_opy_[bstack11l11lll1_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫఎ")]):
        return None
      return bstack11l11ll1_opy_[bstack11l11lll1_opy_ (u"ࠧࡪࡦࠪఏ")]
  else:
    return None
def bstack1ll11llll_opy_(md5_hash, bstack1ll1ll1_opy_):
  bstack11l111l11_opy_ = os.path.join(os.path.expanduser(bstack11l11lll1_opy_ (u"ࠨࢀࠪఐ")), bstack11l11lll1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ఑"))
  if not os.path.exists(bstack11l111l11_opy_):
    os.makedirs(bstack11l111l11_opy_)
  bstack11l1lll1_opy_ = os.path.join(os.path.expanduser(bstack11l11lll1_opy_ (u"ࠪࢂࠬఒ")), bstack11l11lll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫఓ"), bstack11l11lll1_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭ఔ"))
  bstack1lll1ll_opy_ = {
    bstack11l11lll1_opy_ (u"࠭ࡩࡥࠩక"): bstack1ll1ll1_opy_,
    bstack11l11lll1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪఖ"): datetime.datetime.strftime(datetime.datetime.now(), bstack11l11lll1_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬగ")),
    bstack11l11lll1_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧఘ"): str(__version__)
  }
  if os.path.exists(bstack11l1lll1_opy_):
    bstack11l11ll11_opy_ = json.load(open(bstack11l1lll1_opy_,bstack11l11lll1_opy_ (u"ࠪࡶࡧ࠭ఙ")))
  else:
    bstack11l11ll11_opy_ = {}
  bstack11l11ll11_opy_[md5_hash] = bstack1lll1ll_opy_
  with open(bstack11l1lll1_opy_, bstack11l11lll1_opy_ (u"ࠦࡼ࠱ࠢచ")) as outfile:
    json.dump(bstack11l11ll11_opy_, outfile)
def bstack11l1111ll_opy_(self):
  return
def bstack1l11lll11_opy_(self):
  return
def bstack1ll11l11_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1l1l11l1_opy_(self):
  global bstack1ll1ll1ll_opy_
  global bstack1llllll_opy_
  global bstack1l11l11l1_opy_
  try:
    if bstack11l11lll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬఛ") in bstack1ll1ll1ll_opy_ and self.session_id != None:
      bstack11ll11lll_opy_ = bstack11l11lll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭జ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11l11lll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧఝ")
      bstack11lll1l1_opy_ = bstack1llllllll_opy_(bstack11l11lll1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫఞ"), bstack11l11lll1_opy_ (u"ࠩࠪట"), bstack11ll11lll_opy_, bstack11l11lll1_opy_ (u"ࠪ࠰ࠥ࠭ఠ").join(threading.current_thread().bstackTestErrorMessages), bstack11l11lll1_opy_ (u"ࠫࠬడ"), bstack11l11lll1_opy_ (u"ࠬ࠭ఢ"))
      if self != None:
        self.execute_script(bstack11lll1l1_opy_)
  except Exception as e:
    logger.info(bstack11l11lll1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࠢణ") + str(e))
  bstack1l11l11l1_opy_(self)
  self.session_id = None
def bstack11l1lll11_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1llllll_opy_
  global bstack111l1ll1l_opy_
  global bstack111llll_opy_
  global bstack1lll1l1ll_opy_
  global bstack1111_opy_
  global bstack1ll1ll1ll_opy_
  global bstack1lll1llll_opy_
  global bstack11l111ll1_opy_
  global bstack1l1l11ll_opy_
  CONFIG[bstack11l11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩత")] = str(bstack1ll1ll1ll_opy_) + str(__version__)
  command_executor = bstack111_opy_()
  logger.debug(bstack1ll1l1l11_opy_.format(command_executor))
  proxy = bstack1l1l1ll1l_opy_(CONFIG, proxy)
  bstack1l111l1ll_opy_ = 0 if bstack111l1ll1l_opy_ < 0 else bstack111l1ll1l_opy_
  try:
    if bstack1lll1l1ll_opy_ is True:
      bstack1l111l1ll_opy_ = int(multiprocessing.current_process().name)
    elif bstack1111_opy_ is True:
      bstack1l111l1ll_opy_ = int(threading.current_thread().name)
  except:
    bstack1l111l1ll_opy_ = 0
  bstack1lll11l11_opy_ = bstack1l1lll111_opy_(CONFIG, bstack1l111l1ll_opy_)
  logger.debug(bstack11_opy_.format(str(bstack1lll11l11_opy_)))
  if bstack11l11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬథ") in CONFIG and CONFIG[bstack11l11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ద")]:
    bstack1l11l1l1l_opy_(bstack1lll11l11_opy_)
  if desired_capabilities:
    bstack11l11l1ll_opy_ = bstack1l11111l1_opy_(desired_capabilities)
    bstack11l11l1ll_opy_[bstack11l11lll1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪధ")] = bstack1lllll11l_opy_(CONFIG)
    bstack11l1ll111_opy_ = bstack1l1lll111_opy_(bstack11l11l1ll_opy_)
    if bstack11l1ll111_opy_:
      bstack1lll11l11_opy_ = update(bstack11l1ll111_opy_, bstack1lll11l11_opy_)
    desired_capabilities = None
  if options:
    bstack1lllll111_opy_(options, bstack1lll11l11_opy_)
  if not options:
    options = bstack11l1ll11l_opy_(bstack1lll11l11_opy_)
  if proxy and bstack1l11lll_opy_() >= version.parse(bstack11l11lll1_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫన")):
    options.proxy(proxy)
  if options and bstack1l11lll_opy_() >= version.parse(bstack11l11lll1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ఩")):
    desired_capabilities = None
  if (
      not options and not desired_capabilities
  ) or (
      bstack1l11lll_opy_() < version.parse(bstack11l11lll1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬప")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1lll11l11_opy_)
  logger.info(bstack1l1lll1l_opy_)
  if bstack1l11lll_opy_() >= version.parse(bstack11l11lll1_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧఫ")):
    bstack1lll1llll_opy_(self, command_executor=command_executor,
          options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l11lll_opy_() >= version.parse(bstack11l11lll1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧబ")):
    bstack1lll1llll_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l11lll_opy_() >= version.parse(bstack11l11lll1_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩభ")):
    bstack1lll1llll_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1lll1llll_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  try:
    bstack111ll1l1l_opy_ = bstack11l11lll1_opy_ (u"ࠪࠫమ")
    if bstack1l11lll_opy_() >= version.parse(bstack11l11lll1_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬయ")):
      bstack111ll1l1l_opy_ = self.caps.get(bstack11l11lll1_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧర"))
    else:
      bstack111ll1l1l_opy_ = self.capabilities.get(bstack11l11lll1_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨఱ"))
    if bstack111ll1l1l_opy_:
      if bstack1l11lll_opy_() <= version.parse(bstack11l11lll1_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧల")):
        self.command_executor._url = bstack11l11lll1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤళ") + bstack1l1llllll_opy_ + bstack11l11lll1_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨఴ")
      else:
        self.command_executor._url = bstack11l11lll1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧవ") + bstack111ll1l1l_opy_ + bstack11l11lll1_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧశ")
      logger.debug(bstack1ll11ll1_opy_.format(bstack111ll1l1l_opy_))
    else:
      logger.debug(bstack11llllll1_opy_.format(bstack11l11lll1_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨష")))
  except Exception as e:
    logger.debug(bstack11llllll1_opy_.format(e))
  if bstack11l11lll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬస") in bstack1ll1ll1ll_opy_:
    bstack1l1llll1l_opy_(bstack111l1ll1l_opy_, bstack1l1l11ll_opy_)
  bstack1llllll_opy_ = self.session_id
  if bstack11l11lll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧహ") in bstack1ll1ll1ll_opy_:
    threading.current_thread().bstack1ll1l11_opy_ = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack11l111ll1_opy_.append(self)
  if bstack11l11lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ఺") in CONFIG and bstack11l11lll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ఻") in CONFIG[bstack11l11lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ఼࠭")][bstack1l111l1ll_opy_]:
    bstack111llll_opy_ = CONFIG[bstack11l11lll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧఽ")][bstack1l111l1ll_opy_][bstack11l11lll1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪా")]
  logger.debug(bstack1lll11ll_opy_.format(bstack1llllll_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack11ll1l11_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack11l11l1l_opy_
      if(bstack11l11lll1_opy_ (u"ࠨࡩ࡯ࡦࡨࡼ࠳ࡰࡳࠣి") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11l11lll1_opy_ (u"ࠧࡿࠩీ")), bstack11l11lll1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨు"), bstack11l11lll1_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫూ")), bstack11l11lll1_opy_ (u"ࠪࡻࠬృ")) as fp:
          fp.write(bstack11l11lll1_opy_ (u"ࠦࠧౄ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11l11lll1_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢ౅")))):
          with open(args[1], bstack11l11lll1_opy_ (u"࠭ࡲࠨె")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11l11lll1_opy_ (u"ࠧࡢࡵࡼࡲࡨࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡡࡱࡩࡼࡖࡡࡨࡧࠫࡧࡴࡴࡴࡦࡺࡷ࠰ࠥࡶࡡࡨࡧࠣࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮࠭ే") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l111l_opy_)
            lines.insert(1, bstack11l1ll_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11l11lll1_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥై")), bstack11l11lll1_opy_ (u"ࠩࡺࠫ౉")) as bstack1l1ll11_opy_:
              bstack1l1ll11_opy_.writelines(lines)
        CONFIG[bstack11l11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬొ")] = str(bstack1ll1ll1ll_opy_) + str(__version__)
        bstack1l111l1ll_opy_ = 0 if bstack111l1ll1l_opy_ < 0 else bstack111l1ll1l_opy_
        if bstack1lll1l1ll_opy_ is True:
          bstack1l111l1ll_opy_ = int(threading.current_thread().getName())
        CONFIG[bstack11l11lll1_opy_ (u"ࠦࡺࡹࡥࡘ࠵ࡆࠦో")] = False
        CONFIG[bstack11l11lll1_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦౌ")] = True
        bstack1lll11l11_opy_ = bstack1l1lll111_opy_(CONFIG, bstack1l111l1ll_opy_)
        logger.debug(bstack11_opy_.format(str(bstack1lll11l11_opy_)))
        if CONFIG[bstack11l11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮్ࠪ")]:
          bstack1l11l1l1l_opy_(bstack1lll11l11_opy_)
        if bstack11l11lll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ౎") in CONFIG and bstack11l11lll1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭౏") in CONFIG[bstack11l11lll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౐")][bstack1l111l1ll_opy_]:
          bstack111llll_opy_ = CONFIG[bstack11l11lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭౑")][bstack1l111l1ll_opy_][bstack11l11lll1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ౒")]
        args.append(os.path.join(os.path.expanduser(bstack11l11lll1_opy_ (u"ࠬࢄࠧ౓")), bstack11l11lll1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭౔"), bstack11l11lll1_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵౕࠩ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1lll11l11_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11l11lll1_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵౖࠥ"))
      bstack11l11l1l_opy_ = True
      return bstack111ll1lll_opy_(self, args, bufsize=bufsize, executable=executable,
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
  def bstack1l1ll1ll1_opy_(self,
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
    global bstack1llllll_opy_
    global bstack111l1ll1l_opy_
    global bstack111llll_opy_
    global bstack1lll1l1ll_opy_
    global bstack1ll1ll1ll_opy_
    global bstack1lll1llll_opy_
    CONFIG[bstack11l11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ౗")] = str(bstack1ll1ll1ll_opy_) + str(__version__)
    bstack1l111l1ll_opy_ = 0 if bstack111l1ll1l_opy_ < 0 else bstack111l1ll1l_opy_
    if bstack1lll1l1ll_opy_ is True:
      bstack1l111l1ll_opy_ = int(threading.current_thread().getName())
    CONFIG[bstack11l11lll1_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤౘ")] = True
    bstack1lll11l11_opy_ = bstack1l1lll111_opy_(CONFIG, bstack1l111l1ll_opy_)
    logger.debug(bstack11_opy_.format(str(bstack1lll11l11_opy_)))
    if CONFIG[bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨౙ")]:
      bstack1l11l1l1l_opy_(bstack1lll11l11_opy_)
    if bstack11l11lll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨౚ") in CONFIG and bstack11l11lll1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ౛") in CONFIG[bstack11l11lll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ౜")][bstack1l111l1ll_opy_]:
      bstack111llll_opy_ = CONFIG[bstack11l11lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫౝ")][bstack1l111l1ll_opy_][bstack11l11lll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ౞")]
    import urllib
    import json
    bstack111llll1l_opy_ = bstack11l11lll1_opy_ (u"ࠪࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠬ౟") + urllib.parse.quote(json.dumps(bstack1lll11l11_opy_))
    browser = self.connect(bstack111llll1l_opy_)
    return browser
except Exception as e:
    pass
def bstack1l11111l_opy_():
    global bstack11l11l1l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1l1ll1ll1_opy_
        bstack11l11l1l_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack11ll1l11_opy_
      bstack11l11l1l_opy_ = True
    except Exception as e:
      pass
def bstack1l1l111l1_opy_(context, bstack111111l_opy_):
  try:
    context.page.evaluate(bstack11l11lll1_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧౠ"), bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠩౡ")+ json.dumps(bstack111111l_opy_) + bstack11l11lll1_opy_ (u"ࠨࡽࡾࠤౢ"))
  except Exception as e:
    logger.debug(bstack11l11lll1_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧౣ"), e)
def bstack1llll1l_opy_(context, message, level):
  try:
    context.page.evaluate(bstack11l11lll1_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ౤"), bstack11l11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ౥") + json.dumps(message) + bstack11l11lll1_opy_ (u"ࠪ࠰ࠧࡲࡥࡷࡧ࡯ࠦ࠿࠭౦") + json.dumps(level) + bstack11l11lll1_opy_ (u"ࠫࢂࢃࠧ౧"))
  except Exception as e:
    logger.debug(bstack11l11lll1_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࢁࡽࠣ౨"), e)
def bstack1ll1l11l_opy_(context, status, message = bstack11l11lll1_opy_ (u"ࠨࠢ౩")):
  try:
    if(status == bstack11l11lll1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ౪")):
      context.page.evaluate(bstack11l11lll1_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ౫"), bstack11l11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡴࡨࡥࡸࡵ࡮ࠣ࠼ࠪ౬") + json.dumps(bstack11l11lll1_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࠧ౭") + str(message)) + bstack11l11lll1_opy_ (u"ࠫ࠱ࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠨ౮") + json.dumps(status) + bstack11l11lll1_opy_ (u"ࠧࢃࡽࠣ౯"))
    else:
      context.page.evaluate(bstack11l11lll1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ౰"), bstack11l11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠨ౱") + json.dumps(status) + bstack11l11lll1_opy_ (u"ࠣࡿࢀࠦ౲"))
  except Exception as e:
    logger.debug(bstack11l11lll1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡿࢂࠨ౳"), e)
def bstack11lllll1l_opy_(self, url):
  global bstack1111l_opy_
  try:
    bstack1ll11ll_opy_(url)
  except Exception as err:
    logger.debug(bstack111lllll1_opy_.format(str(err)))
  try:
    bstack1111l_opy_(self, url)
  except Exception as e:
    try:
      bstack1lll1l_opy_ = str(e)
      if any(err_msg in bstack1lll1l_opy_ for err_msg in bstack11llll111_opy_):
        bstack1ll11ll_opy_(url, True)
    except Exception as err:
      logger.debug(bstack111lllll1_opy_.format(str(err)))
    raise e
def bstack11ll111l_opy_(self):
  global bstack11ll1l1ll_opy_
  bstack11ll1l1ll_opy_ = self
  return
def bstack1ll1l_opy_(self):
  global bstack11l11l111_opy_
  bstack11l11l111_opy_ = self
  return
def bstack1l1l1l1_opy_(self, test):
  global CONFIG
  global bstack11l11l111_opy_
  global bstack11ll1l1ll_opy_
  global bstack1llllll_opy_
  global bstack1l11l1l1_opy_
  global bstack111llll_opy_
  global bstack1l11l11_opy_
  global bstack1l1l1_opy_
  global bstack11111l1l_opy_
  global bstack11l111ll1_opy_
  try:
    if not bstack1llllll_opy_:
      with open(os.path.join(os.path.expanduser(bstack11l11lll1_opy_ (u"ࠪࢂࠬ౴")), bstack11l11lll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ౵"), bstack11l11lll1_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧ౶"))) as f:
        bstack11ll1l1l_opy_ = json.loads(bstack11l11lll1_opy_ (u"ࠨࡻࠣ౷") + f.read().strip() + bstack11l11lll1_opy_ (u"ࠧࠣࡺࠥ࠾ࠥࠨࡹࠣࠩ౸") + bstack11l11lll1_opy_ (u"ࠣࡿࠥ౹"))
        bstack1llllll_opy_ = bstack11ll1l1l_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack11l111ll1_opy_:
    for driver in bstack11l111ll1_opy_:
      if bstack1llllll_opy_ == driver.session_id:
        if test:
          bstack11lll11l_opy_ = str(test.data)
        if not bstack11111l_opy_ and bstack11lll11l_opy_:
          bstack1ll111111_opy_ = {
            bstack11l11lll1_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩ౺"): bstack11l11lll1_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ౻"),
            bstack11l11lll1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ౼"): {
              bstack11l11lll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ౽"): bstack11lll11l_opy_
            }
          }
          bstack11l11_opy_ = bstack11l11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ౾").format(json.dumps(bstack1ll111111_opy_))
          driver.execute_script(bstack11l11_opy_)
        if bstack1l11l1l1_opy_:
          bstack1llllll1l_opy_ = {
            bstack11l11lll1_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧ౿"): bstack11l11lll1_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪಀ"),
            bstack11l11lll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬಁ"): {
              bstack11l11lll1_opy_ (u"ࠪࡨࡦࡺࡡࠨಂ"): bstack11lll11l_opy_ + bstack11l11lll1_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭ಃ"),
              bstack11l11lll1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ಄"): bstack11l11lll1_opy_ (u"࠭ࡩ࡯ࡨࡲࠫಅ")
            }
          }
          bstack1ll111111_opy_ = {
            bstack11l11lll1_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧಆ"): bstack11l11lll1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫಇ"),
            bstack11l11lll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬಈ"): {
              bstack11l11lll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪಉ"): bstack11l11lll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫಊ")
            }
          }
          if bstack1l11l1l1_opy_.status == bstack11l11lll1_opy_ (u"ࠬࡖࡁࡔࡕࠪಋ"):
            bstack11l1111l_opy_ = bstack11l11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫಌ").format(json.dumps(bstack1llllll1l_opy_))
            driver.execute_script(bstack11l1111l_opy_)
            bstack11l11_opy_ = bstack11l11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ಍").format(json.dumps(bstack1ll111111_opy_))
            driver.execute_script(bstack11l11_opy_)
          elif bstack1l11l1l1_opy_.status == bstack11l11lll1_opy_ (u"ࠨࡈࡄࡍࡑ࠭ಎ"):
            reason = bstack11l11lll1_opy_ (u"ࠤࠥಏ")
            bstack111ll1l_opy_ = bstack11lll11l_opy_ + bstack11l11lll1_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠫಐ")
            if bstack1l11l1l1_opy_.message:
              reason = str(bstack1l11l1l1_opy_.message)
              bstack111ll1l_opy_ = bstack111ll1l_opy_ + bstack11l11lll1_opy_ (u"ࠫࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࠫ಑") + reason
            bstack1llllll1l_opy_[bstack11l11lll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨಒ")] = {
              bstack11l11lll1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬಓ"): bstack11l11lll1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ಔ"),
              bstack11l11lll1_opy_ (u"ࠨࡦࡤࡸࡦ࠭ಕ"): bstack111ll1l_opy_
            }
            bstack1ll111111_opy_[bstack11l11lll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬಖ")] = {
              bstack11l11lll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪಗ"): bstack11l11lll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫಘ"),
              bstack11l11lll1_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬಙ"): reason
            }
            bstack11l1111l_opy_ = bstack11l11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫಚ").format(json.dumps(bstack1llllll1l_opy_))
            driver.execute_script(bstack11l1111l_opy_)
            bstack11l11_opy_ = bstack11l11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬಛ").format(json.dumps(bstack1ll111111_opy_))
            driver.execute_script(bstack11l11_opy_)
  elif bstack1llllll_opy_:
    try:
      data = {}
      bstack11lll11l_opy_ = None
      if test:
        bstack11lll11l_opy_ = str(test.data)
      if not bstack11111l_opy_ and bstack11lll11l_opy_:
        data[bstack11l11lll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ಜ")] = bstack11lll11l_opy_
      if bstack1l11l1l1_opy_:
        if bstack1l11l1l1_opy_.status == bstack11l11lll1_opy_ (u"ࠩࡓࡅࡘ࡙ࠧಝ"):
          data[bstack11l11lll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪಞ")] = bstack11l11lll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫಟ")
        elif bstack1l11l1l1_opy_.status == bstack11l11lll1_opy_ (u"ࠬࡌࡁࡊࡎࠪಠ"):
          data[bstack11l11lll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ಡ")] = bstack11l11lll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧಢ")
          if bstack1l11l1l1_opy_.message:
            data[bstack11l11lll1_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨಣ")] = str(bstack1l11l1l1_opy_.message)
      user = CONFIG[bstack11l11lll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫತ")]
      key = CONFIG[bstack11l11lll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ಥ")]
      url = bstack11l11lll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࡦࡶࡩ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦࡵࡶ࡭ࡴࡴࡳ࠰ࡽࢀ࠲࡯ࡹ࡯࡯ࠩದ").format(user, key, bstack1llllll_opy_)
      headers = {
        bstack11l11lll1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫಧ"): bstack11l11lll1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩನ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack11l11l1_opy_.format(str(e)))
  if bstack11l11l111_opy_:
    bstack1l1l1_opy_(bstack11l11l111_opy_)
  if bstack11ll1l1ll_opy_:
    bstack11111l1l_opy_(bstack11ll1l1ll_opy_)
  bstack1l11l11_opy_(self, test)
def bstack1l1ll111_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1llll1ll_opy_
  bstack1llll1ll_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l11l1l1_opy_
  bstack1l11l1l1_opy_ = self._test
def bstack11lll_opy_():
  global bstack11lll111_opy_
  try:
    if os.path.exists(bstack11lll111_opy_):
      os.remove(bstack11lll111_opy_)
  except Exception as e:
    logger.debug(bstack11l11lll1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪ಩") + str(e))
def bstack111ll11ll_opy_():
  global bstack11lll111_opy_
  bstack11l1lllll_opy_ = {}
  try:
    if not os.path.isfile(bstack11lll111_opy_):
      with open(bstack11lll111_opy_, bstack11l11lll1_opy_ (u"ࠨࡹࠪಪ")):
        pass
      with open(bstack11lll111_opy_, bstack11l11lll1_opy_ (u"ࠤࡺ࠯ࠧಫ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack11lll111_opy_):
      bstack11l1lllll_opy_ = json.load(open(bstack11lll111_opy_, bstack11l11lll1_opy_ (u"ࠪࡶࡧ࠭ಬ")))
  except Exception as e:
    logger.debug(bstack11l11lll1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ಭ") + str(e))
  finally:
    return bstack11l1lllll_opy_
def bstack1l1llll1l_opy_(platform_index, item_index):
  global bstack11lll111_opy_
  try:
    bstack11l1lllll_opy_ = bstack111ll11ll_opy_()
    bstack11l1lllll_opy_[item_index] = platform_index
    with open(bstack11lll111_opy_, bstack11l11lll1_opy_ (u"ࠧࡽࠫࠣಮ")) as outfile:
      json.dump(bstack11l1lllll_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11l11lll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡹࡵ࡭ࡹ࡯࡮ࡨࠢࡷࡳࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫಯ") + str(e))
def bstack1lllllll_opy_(bstack1ll11ll11_opy_):
  global CONFIG
  bstack1l111ll_opy_ = bstack11l11lll1_opy_ (u"ࠧࠨರ")
  if not bstack11l11lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫಱ") in CONFIG:
    logger.info(bstack11l11lll1_opy_ (u"ࠩࡑࡳࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠡࡲࡤࡷࡸ࡫ࡤࠡࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡲࡦࡲࡲࡶࡹࠦࡦࡰࡴࠣࡖࡴࡨ࡯ࡵࠢࡵࡹࡳ࠭ಲ"))
  try:
    platform = CONFIG[bstack11l11lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ಳ")][bstack1ll11ll11_opy_]
    if bstack11l11lll1_opy_ (u"ࠫࡴࡹࠧ಴") in platform:
      bstack1l111ll_opy_ += str(platform[bstack11l11lll1_opy_ (u"ࠬࡵࡳࠨವ")]) + bstack11l11lll1_opy_ (u"࠭ࠬࠡࠩಶ")
    if bstack11l11lll1_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪಷ") in platform:
      bstack1l111ll_opy_ += str(platform[bstack11l11lll1_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫಸ")]) + bstack11l11lll1_opy_ (u"ࠩ࠯ࠤࠬಹ")
    if bstack11l11lll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ಺") in platform:
      bstack1l111ll_opy_ += str(platform[bstack11l11lll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ಻")]) + bstack11l11lll1_opy_ (u"ࠬ࠲ࠠࠨ಼")
    if bstack11l11lll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨಽ") in platform:
      bstack1l111ll_opy_ += str(platform[bstack11l11lll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩಾ")]) + bstack11l11lll1_opy_ (u"ࠨ࠮ࠣࠫಿ")
    if bstack11l11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧೀ") in platform:
      bstack1l111ll_opy_ += str(platform[bstack11l11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨು")]) + bstack11l11lll1_opy_ (u"ࠫ࠱ࠦࠧೂ")
    if bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ೃ") in platform:
      bstack1l111ll_opy_ += str(platform[bstack11l11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧೄ")]) + bstack11l11lll1_opy_ (u"ࠧ࠭ࠢࠪ೅")
  except Exception as e:
    logger.debug(bstack11l11lll1_opy_ (u"ࠨࡕࡲࡱࡪࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡷ࡫ࡰࡰࡴࡷࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡵ࡮ࠨೆ") + str(e))
  finally:
    if bstack1l111ll_opy_[len(bstack1l111ll_opy_) - 2:] == bstack11l11lll1_opy_ (u"ࠩ࠯ࠤࠬೇ"):
      bstack1l111ll_opy_ = bstack1l111ll_opy_[:-2]
    return bstack1l111ll_opy_
def bstack1l1ll1ll_opy_(path, bstack1l111ll_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack11llll11_opy_ = ET.parse(path)
    bstack1111ll1l_opy_ = bstack11llll11_opy_.getroot()
    bstack11l1l11l_opy_ = None
    for suite in bstack1111ll1l_opy_.iter(bstack11l11lll1_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩೈ")):
      if bstack11l11lll1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ೉") in suite.attrib:
        suite.attrib[bstack11l11lll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪೊ")] += bstack11l11lll1_opy_ (u"࠭ࠠࠨೋ") + bstack1l111ll_opy_
        bstack11l1l11l_opy_ = suite
    bstack1111ll1_opy_ = None
    for robot in bstack1111ll1l_opy_.iter(bstack11l11lll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ೌ")):
      bstack1111ll1_opy_ = robot
    bstack111ll111_opy_ = len(bstack1111ll1_opy_.findall(bstack11l11lll1_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫್ࠧ")))
    if bstack111ll111_opy_ == 1:
      bstack1111ll1_opy_.remove(bstack1111ll1_opy_.findall(bstack11l11lll1_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ೎"))[0])
      bstack1l11l11ll_opy_ = ET.Element(bstack11l11lll1_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩ೏"), attrib={bstack11l11lll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ೐"):bstack11l11lll1_opy_ (u"࡙ࠬࡵࡪࡶࡨࡷࠬ೑"), bstack11l11lll1_opy_ (u"࠭ࡩࡥࠩ೒"):bstack11l11lll1_opy_ (u"ࠧࡴ࠲ࠪ೓")})
      bstack1111ll1_opy_.insert(1, bstack1l11l11ll_opy_)
      bstack111l1111_opy_ = None
      for suite in bstack1111ll1_opy_.iter(bstack11l11lll1_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ೔")):
        bstack111l1111_opy_ = suite
      bstack111l1111_opy_.append(bstack11l1l11l_opy_)
      bstack111111ll_opy_ = None
      for status in bstack11l1l11l_opy_.iter(bstack11l11lll1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩೕ")):
        bstack111111ll_opy_ = status
      bstack111l1111_opy_.append(bstack111111ll_opy_)
    bstack11llll11_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11l11lll1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡳࡵ࡬ࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠨೖ") + str(e))
def bstack1ll1l1l1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack11llll11l_opy_
  global CONFIG
  if bstack11l11lll1_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨࠣ೗") in options:
    del options[bstack11l11lll1_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤ೘")]
  bstack111lll1ll_opy_ = bstack111ll11ll_opy_()
  for bstack11l11111l_opy_ in bstack111lll1ll_opy_.keys():
    path = os.path.join(os.getcwd(), bstack11l11lll1_opy_ (u"࠭ࡰࡢࡤࡲࡸࡤࡸࡥࡴࡷ࡯ࡸࡸ࠭೙"), str(bstack11l11111l_opy_), bstack11l11lll1_opy_ (u"ࠧࡰࡷࡷࡴࡺࡺ࠮ࡹ࡯࡯ࠫ೚"))
    bstack1l1ll1ll_opy_(path, bstack1lllllll_opy_(bstack111lll1ll_opy_[bstack11l11111l_opy_]))
  bstack11lll_opy_()
  return bstack11llll11l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack111l1_opy_(self, ff_profile_dir):
  global bstack1ll111lll_opy_
  if not ff_profile_dir:
    return None
  return bstack1ll111lll_opy_(self, ff_profile_dir)
def bstack11l1l_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l111ll1l_opy_
  bstack1l1ll11l1_opy_ = []
  if bstack11l11lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ೛") in CONFIG:
    bstack1l1ll11l1_opy_ = CONFIG[bstack11l11lll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ೜")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11l11lll1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦೝ")],
      pabot_args[bstack11l11lll1_opy_ (u"ࠦࡻ࡫ࡲࡣࡱࡶࡩࠧೞ")],
      argfile,
      pabot_args.get(bstack11l11lll1_opy_ (u"ࠧ࡮ࡩࡷࡧࠥ೟")),
      pabot_args[bstack11l11lll1_opy_ (u"ࠨࡰࡳࡱࡦࡩࡸࡹࡥࡴࠤೠ")],
      platform[0],
      bstack1l111ll1l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11l11lll1_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡨ࡬ࡰࡪࡹࠢೡ")] or [(bstack11l11lll1_opy_ (u"ࠣࠤೢ"), None)]
    for platform in enumerate(bstack1l1ll11l1_opy_)
  ]
def bstack1l1l1111_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack111ll111l_opy_=bstack11l11lll1_opy_ (u"ࠩࠪೣ")):
  global bstack111ll1ll1_opy_
  self.platform_index = platform_index
  self.bstack1l1l1lll_opy_ = bstack111ll111l_opy_
  bstack111ll1ll1_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack1ll11l1_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack111llllll_opy_
  global bstack11l11l_opy_
  if not bstack11l11lll1_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ೤") in item.options:
    item.options[bstack11l11lll1_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭೥")] = []
  for v in item.options[bstack11l11lll1_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ೦")]:
    if bstack11l11lll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜ࠬ೧") in v:
      item.options[bstack11l11lll1_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ೨")].remove(v)
    if bstack11l11lll1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨ೩") in v:
      item.options[bstack11l11lll1_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ೪")].remove(v)
  item.options[bstack11l11lll1_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ೫")].insert(0, bstack11l11lll1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚࠽ࡿࢂ࠭೬").format(item.platform_index))
  item.options[bstack11l11lll1_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ೭")].insert(0, bstack11l11lll1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔ࠽ࡿࢂ࠭೮").format(item.bstack1l1l1lll_opy_))
  if bstack11l11l_opy_:
    item.options[bstack11l11lll1_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ೯")].insert(0, bstack11l11lll1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓ࠻ࡽࢀࠫ೰").format(bstack11l11l_opy_))
  return bstack111llllll_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1l1111l1l_opy_(command, item_index):
  global bstack11l11l_opy_
  if bstack11l11l_opy_:
    command[0] = command[0].replace(bstack11l11lll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨೱ"), bstack11l11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽࠦࠧೲ") + str(item_index) + bstack11l11l_opy_, 1)
  else:
    command[0] = command[0].replace(bstack11l11lll1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪೳ"), bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩ೴") + str(item_index), 1)
def bstack1l1ll1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11l1l11ll_opy_
  bstack1l1111l1l_opy_(command, item_index)
  return bstack11l1l11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack111l1l11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11l1l11ll_opy_
  bstack1l1111l1l_opy_(command, item_index)
  return bstack11l1l11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1l1ll1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11l1l11ll_opy_
  bstack1l1111l1l_opy_(command, item_index)
  return bstack11l1l11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1ll11ll1l_opy_(self, runner, quiet=False, capture=True):
  global bstack1l11l111l_opy_
  bstack1l111l1l1_opy_ = bstack1l11l111l_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack11l11lll1_opy_ (u"࠭ࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࡡࡤࡶࡷ࠭೵")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11l11lll1_opy_ (u"ࠧࡦࡺࡦࡣࡹࡸࡡࡤࡧࡥࡥࡨࡱ࡟ࡢࡴࡵࠫ೶")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1l111l1l1_opy_
def bstack111l111_opy_(self, name, context, *args):
  global bstack111llll11_opy_
  if name in [bstack11l11lll1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩ೷"), bstack11l11lll1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ೸")]:
    bstack111llll11_opy_(self, name, context, *args)
  if name == bstack11l11lll1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠫ೹"):
    try:
      if(not bstack11111l_opy_):
        bstack111111l_opy_ = str(self.feature.name)
        bstack1l1l111l1_opy_(context, bstack111111l_opy_)
        context.browser.execute_script(bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩ೺") + json.dumps(bstack111111l_opy_) + bstack11l11lll1_opy_ (u"ࠬࢃࡽࠨ೻"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack11l11lll1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥ࡯࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭೼").format(str(e)))
  if name == bstack11l11lll1_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩ೽"):
    try:
      if not hasattr(self, bstack11l11lll1_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ೾")):
        self.driver_before_scenario = True
      if(not bstack11111l_opy_):
        scenario_name = args[0].name
        feature_name = bstack111111l_opy_ = str(self.feature.name)
        bstack111111l_opy_ = feature_name + bstack11l11lll1_opy_ (u"ࠩࠣ࠱ࠥ࠭೿") + scenario_name
        if self.driver_before_scenario:
          bstack1l1l111l1_opy_(context, bstack111111l_opy_)
          context.browser.execute_script(bstack11l11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨഀ") + json.dumps(bstack111111l_opy_) + bstack11l11lll1_opy_ (u"ࠫࢂࢃࠧഁ"))
    except Exception as e:
      logger.debug(bstack11l11lll1_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤ࡮ࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭ം").format(str(e)))
  if name == bstack11l11lll1_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧഃ"):
    try:
      bstack1ll1l11ll_opy_ = args[0].status.name
      if str(bstack1ll1l11ll_opy_).lower() == bstack11l11lll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧഄ"):
        bstack1l1l111_opy_ = bstack11l11lll1_opy_ (u"ࠨࠩഅ")
        bstack1ll_opy_ = bstack11l11lll1_opy_ (u"ࠩࠪആ")
        bstack1l111l111_opy_ = bstack11l11lll1_opy_ (u"ࠪࠫഇ")
        try:
          import traceback
          bstack1l1l111_opy_ = self.exception.__class__.__name__
          bstack1l1l11ll1_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1ll_opy_ = bstack11l11lll1_opy_ (u"ࠫࠥ࠭ഈ").join(bstack1l1l11ll1_opy_)
          bstack1l111l111_opy_ = bstack1l1l11ll1_opy_[-1]
        except Exception as e:
          logger.debug(bstack1l1l1l11_opy_.format(str(e)))
        bstack1l1l111_opy_ += bstack1l111l111_opy_
        bstack1llll1l_opy_(context, json.dumps(str(args[0].name) + bstack11l11lll1_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦഉ") + str(bstack1ll_opy_)), bstack11l11lll1_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧഊ"))
        if self.driver_before_scenario:
          bstack1ll1l11l_opy_(context, bstack11l11lll1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢഋ"), bstack1l1l111_opy_)
        context.browser.execute_script(bstack11l11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ഌ") + json.dumps(str(args[0].name) + bstack11l11lll1_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ഍") + str(bstack1ll_opy_)) + bstack11l11lll1_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪഎ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ࠲ࠠࠣࡴࡨࡥࡸࡵ࡮ࠣ࠼ࠣࠫഏ") + json.dumps(bstack11l11lll1_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤഐ") + str(bstack1l1l111_opy_)) + bstack11l11lll1_opy_ (u"࠭ࡽࡾࠩ഑"))
      else:
        bstack1llll1l_opy_(context, bstack11l11lll1_opy_ (u"ࠢࡑࡣࡶࡷࡪࡪࠡࠣഒ"), bstack11l11lll1_opy_ (u"ࠣ࡫ࡱࡪࡴࠨഓ"))
        if self.driver_before_scenario:
          bstack1ll1l11l_opy_(context, bstack11l11lll1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤഔ"))
        context.browser.execute_script(bstack11l11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨക") + json.dumps(str(args[0].name) + bstack11l11lll1_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣഖ")) + bstack11l11lll1_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫഗ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack11l11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡱࡣࡶࡷࡪࡪࠢࡾࡿࠪഘ"))
    except Exception as e:
      logger.debug(bstack11l11lll1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩങ").format(str(e)))
  if name == bstack11l11lll1_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨച"):
    try:
      if context.failed is True:
        bstack1ll1l1lll_opy_ = []
        bstack1l1llll_opy_ = []
        bstack1l111lll_opy_ = []
        bstack1l1l1l11l_opy_ = bstack11l11lll1_opy_ (u"ࠩࠪഛ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1ll1l1lll_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1l1l11ll1_opy_ = traceback.format_tb(exc_tb)
            bstack1l1l11_opy_ = bstack11l11lll1_opy_ (u"ࠪࠤࠬജ").join(bstack1l1l11ll1_opy_)
            bstack1l1llll_opy_.append(bstack1l1l11_opy_)
            bstack1l111lll_opy_.append(bstack1l1l11ll1_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l1l1l11_opy_.format(str(e)))
        bstack1l1l111_opy_ = bstack11l11lll1_opy_ (u"ࠫࠬഝ")
        for i in range(len(bstack1ll1l1lll_opy_)):
          bstack1l1l111_opy_ += bstack1ll1l1lll_opy_[i] + bstack1l111lll_opy_[i] + bstack11l11lll1_opy_ (u"ࠬࡢ࡮ࠨഞ")
        bstack1l1l1l11l_opy_ = bstack11l11lll1_opy_ (u"࠭ࠠࠨട").join(bstack1l1llll_opy_)
        if not self.driver_before_scenario:
          bstack1llll1l_opy_(context, bstack1l1l1l11l_opy_, bstack11l11lll1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨഠ"))
          bstack1ll1l11l_opy_(context, bstack11l11lll1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣഡ"), bstack1l1l111_opy_)
          context.browser.execute_script(bstack11l11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧഢ") + json.dumps(bstack1l1l1l11l_opy_) + bstack11l11lll1_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪണ"))
          context.browser.execute_script(bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡷࡹࡧࡴࡶࡵࠥ࠾ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ࠲ࠠࠣࡴࡨࡥࡸࡵ࡮ࠣ࠼ࠣࠫത") + json.dumps(bstack11l11lll1_opy_ (u"࡙ࠧ࡯࡮ࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳࡸࠦࡦࡢ࡫࡯ࡩࡩࡀࠠ࡝ࡰࠥഥ") + str(bstack1l1l111_opy_)) + bstack11l11lll1_opy_ (u"࠭ࡽࡾࠩദ"))
      else:
        if not self.driver_before_scenario:
          bstack1llll1l_opy_(context, bstack11l11lll1_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥധ") + str(self.feature.name) + bstack11l11lll1_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥന"), bstack11l11lll1_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢഩ"))
          bstack1ll1l11l_opy_(context, bstack11l11lll1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥപ"))
          context.browser.execute_script(bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩഫ") + json.dumps(bstack11l11lll1_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣബ") + str(self.feature.name) + bstack11l11lll1_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣഭ")) + bstack11l11lll1_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭മ"))
          context.browser.execute_script(bstack11l11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠤࡳࡥࡸࡹࡥࡥࠤࢀࢁࠬയ"))
    except Exception as e:
      logger.debug(bstack11l11lll1_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫര").format(str(e)))
  if name in [bstack11l11lll1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪറ"), bstack11l11lll1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬല")]:
    bstack111llll11_opy_(self, name, context, *args)
    if (name == bstack11l11lll1_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ള") and self.driver_before_scenario) or (name == bstack11l11lll1_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ഴ") and not self.driver_before_scenario):
      try:
        context.browser.quit()
      except Exception:
        pass
def bstack11lllllll_opy_(config, startdir):
  return bstack11l11lll1_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࠳ࢁࠧവ").format(bstack11l11lll1_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢശ"))
class Notset:
  def __repr__(self):
    return bstack11l11lll1_opy_ (u"ࠤ࠿ࡒࡔ࡚ࡓࡆࡖࡁࠦഷ")
notset = Notset()
def bstack1l1llll1_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack11l1l11l1_opy_
  if str(name).lower() == bstack11l11lll1_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪസ"):
    return bstack11l11lll1_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥഹ")
  else:
    return bstack11l1l11l1_opy_(self, name, default, skip)
def bstack1ll1l111_opy_(item, when):
  global bstack111l1l_opy_
  try:
    bstack111l1l_opy_(item, when)
  except Exception as e:
    pass
def bstack1l1ll1l1l_opy_():
  return
def bstack1llllllll_opy_(type, name, status, reason, bstack1_opy_, bstack1111l1ll_opy_):
  bstack1ll111111_opy_ = {
    bstack11l11lll1_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬഺ"): type,
    bstack11l11lll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴ഻ࠩ"): {}
  }
  if type == bstack11l11lll1_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦ഼ࠩ"):
    bstack1ll111111_opy_[bstack11l11lll1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫഽ")][bstack11l11lll1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨാ")] = bstack1_opy_
    bstack1ll111111_opy_[bstack11l11lll1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ി")][bstack11l11lll1_opy_ (u"ࠫࡩࡧࡴࡢࠩീ")] = json.dumps(str(bstack1111l1ll_opy_))
  if type == bstack11l11lll1_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ു"):
    bstack1ll111111_opy_[bstack11l11lll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩൂ")][bstack11l11lll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬൃ")] = name
  if type == bstack11l11lll1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫൄ"):
    bstack1ll111111_opy_[bstack11l11lll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ൅")][bstack11l11lll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪെ")] = status
    if status == bstack11l11lll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫേ"):
      bstack1ll111111_opy_[bstack11l11lll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨൈ")][bstack11l11lll1_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭൉")] = json.dumps(str(reason))
  bstack11l11_opy_ = bstack11l11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬൊ").format(json.dumps(bstack1ll111111_opy_))
  return bstack11l11_opy_
def bstack11lllll1_opy_(item, call, rep):
  global bstack1ll11_opy_
  global bstack11l111ll1_opy_
  name = bstack11l11lll1_opy_ (u"ࠨࠩോ")
  try:
    if rep.when == bstack11l11lll1_opy_ (u"ࠩࡦࡥࡱࡲࠧൌ"):
      bstack1llllll_opy_ = threading.current_thread().bstack1ll1l11_opy_
      try:
        name = str(rep.nodeid)
        bstack11lll1l1_opy_ = bstack1llllllll_opy_(bstack11l11lll1_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨ്ࠫ"), name, bstack11l11lll1_opy_ (u"ࠫࠬൎ"), bstack11l11lll1_opy_ (u"ࠬ࠭൏"), bstack11l11lll1_opy_ (u"࠭ࠧ൐"), bstack11l11lll1_opy_ (u"ࠧࠨ൑"))
        for driver in bstack11l111ll1_opy_:
          if bstack1llllll_opy_ == driver.session_id:
            driver.execute_script(bstack11lll1l1_opy_)
      except Exception as e:
        logger.debug(bstack11l11lll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨ൒").format(str(e)))
      try:
        status = bstack11l11lll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ൓") if rep.outcome.lower() == bstack11l11lll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪൔ") else bstack11l11lll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫൕ")
        reason = bstack11l11lll1_opy_ (u"ࠬ࠭ൖ")
        if (reason != bstack11l11lll1_opy_ (u"ࠨࠢൗ")):
          try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
          except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
          threading.current_thread().bstackTestErrorMessages.append(str(reason))
        if status == bstack11l11lll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ൘"):
          reason = rep.longrepr.reprcrash.message
          if (not threading.current_thread().bstackTestErrorMessages):
            threading.current_thread().bstackTestErrorMessages = []
          threading.current_thread().bstackTestErrorMessages.append(reason)
        level = bstack11l11lll1_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭൙") if status == bstack11l11lll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ൚") else bstack11l11lll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ൛")
        data = name + bstack11l11lll1_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭൜") if status == bstack11l11lll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ൝") else name + bstack11l11lll1_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩ൞") + reason
        bstack11ll1ll1l_opy_ = bstack1llllllll_opy_(bstack11l11lll1_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩൟ"), bstack11l11lll1_opy_ (u"ࠨࠩൠ"), bstack11l11lll1_opy_ (u"ࠩࠪൡ"), bstack11l11lll1_opy_ (u"ࠪࠫൢ"), level, data)
        for driver in bstack11l111ll1_opy_:
          if bstack1llllll_opy_ == driver.session_id:
            driver.execute_script(bstack11ll1ll1l_opy_)
      except Exception as e:
        logger.debug(bstack11l11lll1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨൣ").format(str(e)))
  except Exception as e:
    logger.debug(bstack11l11lll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩ൤").format(str(e)))
  bstack1ll11_opy_(item, call, rep)
def bstack11ll11l1l_opy_(framework_name):
  global bstack1ll1ll1ll_opy_
  global bstack11l11l1l_opy_
  global bstack111l1l1l_opy_
  bstack1ll1ll1ll_opy_ = framework_name
  logger.info(bstack1llll_opy_.format(bstack1ll1ll1ll_opy_.split(bstack11l11lll1_opy_ (u"࠭࠭ࠨ൥"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    Service.start = bstack11l1111ll_opy_
    Service.stop = bstack1l11lll11_opy_
    webdriver.Remote.__init__ = bstack11l1lll11_opy_
    webdriver.Remote.get = bstack11lllll1l_opy_
    WebDriver.close = bstack1ll11l11_opy_
    WebDriver.quit = bstack1l1l11l1_opy_
    bstack11l11l1l_opy_ = True
  except Exception as e:
    pass
  bstack1l11111l_opy_()
  if not bstack11l11l1l_opy_:
    bstack1111l1l1_opy_(bstack11l11lll1_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤ൦"), bstack11lllll_opy_)
  if bstack11ll11ll1_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack11l1llll_opy_
    except Exception as e:
      logger.error(bstack1l11l1ll_opy_.format(str(e)))
  if (bstack11l11lll1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ൧") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack111l1_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1ll1l_opy_
      except Exception as e:
        logger.warn(bstack1lll1l1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack11ll111l_opy_
      except Exception as e:
        logger.debug(bstack1l1l1111l_opy_ + str(e))
    except Exception as e:
      bstack1111l1l1_opy_(e, bstack1lll1l1_opy_)
    Output.end_test = bstack1l1l1l1_opy_
    TestStatus.__init__ = bstack1l1ll111_opy_
    QueueItem.__init__ = bstack1l1l1111_opy_
    pabot._create_items = bstack11l1l_opy_
    try:
      from pabot import __version__ as bstack111l111l_opy_
      if version.parse(bstack111l111l_opy_) >= version.parse(bstack11l11lll1_opy_ (u"ࠩ࠵࠲࠶࠻࠮࠱ࠩ൨")):
        pabot._run = bstack1l1ll1lll_opy_
      elif version.parse(bstack111l111l_opy_) >= version.parse(bstack11l11lll1_opy_ (u"ࠪ࠶࠳࠷࠳࠯࠲ࠪ൩")):
        pabot._run = bstack111l1l11l_opy_
      else:
        pabot._run = bstack1l1ll1l11_opy_
    except Exception as e:
      pabot._run = bstack1l1ll1l11_opy_
    pabot._create_command_for_execution = bstack1ll11l1_opy_
    pabot._report_results = bstack1ll1l1l1_opy_
  if bstack11l11lll1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ൪") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1111l1l1_opy_(e, bstack1l1lll_opy_)
    Runner.run_hook = bstack111l111_opy_
    Step.run = bstack1ll11ll1l_opy_
  if bstack11l11lll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ൫") in str(framework_name).lower():
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      from _pytest import runner
      pytest_selenium.pytest_report_header = bstack11lllllll_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1l1ll1l1l_opy_
      Config.getoption = bstack1l1llll1_opy_
      runner._update_current_test_var = bstack1ll1l111_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack11lllll1_opy_
    except Exception as e:
      pass
def bstack111l1ll_opy_():
  global CONFIG
  if bstack11l11lll1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭൬") in CONFIG and int(CONFIG[bstack11l11lll1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ൭")]) > 1:
    logger.warn(bstack1l11ll111_opy_)
def bstack11l1111l1_opy_(arg):
  arg.append(bstack11l11lll1_opy_ (u"ࠣ࠯࠰ࡧࡦࡶࡴࡶࡴࡨࡁࡸࡿࡳࠣ൮"))
  arg.append(bstack11l11lll1_opy_ (u"ࠤ࠰࡛ࠧ൯"))
  arg.append(bstack11l11lll1_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧ࠽ࡑࡴࡪࡵ࡭ࡧࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡮ࡳࡰࡰࡴࡷࡩࡩࡀࡰࡺࡶࡨࡷࡹ࠴ࡐࡺࡶࡨࡷࡹ࡝ࡡࡳࡰ࡬ࡲ࡬ࠨ൰"))
  global CONFIG
  bstack11ll11l1l_opy_(bstack1l1111_opy_)
  os.environ[bstack11l11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬ൱")] = CONFIG[bstack11l11lll1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ൲")]
  os.environ[bstack11l11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩ൳")] = CONFIG[bstack11l11lll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ൴")]
  from _pytest.config import main as bstack1ll1lllll_opy_
  bstack1ll1lllll_opy_(arg)
def bstack111111l1_opy_(arg):
  bstack11ll11l1l_opy_(bstack1l11ll1ll_opy_)
  from behave.__main__ import main as bstack11lllll11_opy_
  bstack11lllll11_opy_(arg)
def bstack11l1l111l_opy_():
  logger.info(bstack1ll11l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11l11lll1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ൵"), help=bstack11l11lll1_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡧࡴࡴࡦࡪࡩࠪ൶"))
  parser.add_argument(bstack11l11lll1_opy_ (u"ࠪ࠱ࡺ࠭൷"), bstack11l11lll1_opy_ (u"ࠫ࠲࠳ࡵࡴࡧࡵࡲࡦࡳࡥࠨ൸"), help=bstack11l11lll1_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫ൹"))
  parser.add_argument(bstack11l11lll1_opy_ (u"࠭࠭࡬ࠩൺ"), bstack11l11lll1_opy_ (u"ࠧ࠮࠯࡮ࡩࡾ࠭ൻ"), help=bstack11l11lll1_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡧࡣࡤࡧࡶࡷࠥࡱࡥࡺࠩർ"))
  parser.add_argument(bstack11l11lll1_opy_ (u"ࠩ࠰ࡪࠬൽ"), bstack11l11lll1_opy_ (u"ࠪ࠱࠲࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨൾ"), help=bstack11l11lll1_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪൿ"))
  bstack11ll1ll11_opy_ = parser.parse_args()
  try:
    bstack1l1ll11ll_opy_ = bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡬࡫࡮ࡦࡴ࡬ࡧ࠳ࡿ࡭࡭࠰ࡶࡥࡲࡶ࡬ࡦࠩ඀")
    if bstack11ll1ll11_opy_.framework and bstack11ll1ll11_opy_.framework not in (bstack11l11lll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ඁ"), bstack11l11lll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨං")):
      bstack1l1ll11ll_opy_ = bstack11l11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࡽࡲࡲ࠮ࡴࡣࡰࡴࡱ࡫ࠧඃ")
    bstack1lll11l1l_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l1ll11ll_opy_)
    bstack1llll11ll_opy_ = open(bstack1lll11l1l_opy_, bstack11l11lll1_opy_ (u"ࠩࡵࠫ඄"))
    bstack11l1lll_opy_ = bstack1llll11ll_opy_.read()
    bstack1llll11ll_opy_.close()
    if bstack11ll1ll11_opy_.username:
      bstack11l1lll_opy_ = bstack11l1lll_opy_.replace(bstack11l11lll1_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡗࡖࡉࡗࡔࡁࡎࡇࠪඅ"), bstack11ll1ll11_opy_.username)
    if bstack11ll1ll11_opy_.key:
      bstack11l1lll_opy_ = bstack11l1lll_opy_.replace(bstack11l11lll1_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ආ"), bstack11ll1ll11_opy_.key)
    if bstack11ll1ll11_opy_.framework:
      bstack11l1lll_opy_ = bstack11l1lll_opy_.replace(bstack11l11lll1_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ඇ"), bstack11ll1ll11_opy_.framework)
    file_name = bstack11l11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩඈ")
    file_path = os.path.abspath(file_name)
    bstack11l_opy_ = open(file_path, bstack11l11lll1_opy_ (u"ࠧࡸࠩඉ"))
    bstack11l_opy_.write(bstack11l1lll_opy_)
    bstack11l_opy_.close()
    logger.info(bstack111ll_opy_)
    try:
      os.environ[bstack11l11lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪඊ")] = bstack11ll1ll11_opy_.framework if bstack11ll1ll11_opy_.framework != None else bstack11l11lll1_opy_ (u"ࠤࠥඋ")
      config = yaml.safe_load(bstack11l1lll_opy_)
      config[bstack11l11lll1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪඌ")] = bstack11l11lll1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱ࡸ࡫ࡴࡶࡲࠪඍ")
      bstack1111ll_opy_(bstack1ll11l111_opy_, config)
    except Exception as e:
      logger.debug(bstack11l1l1l1l_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1lll1111_opy_.format(str(e)))
def bstack1111ll_opy_(bstack1lll1ll1_opy_, config, bstack1l1l1ll_opy_ = {}):
  global bstack111lll111_opy_
  if not config:
    return
  bstack111l11lll_opy_ = bstack1lll1ll1l_opy_ if not bstack111lll111_opy_ else ( bstack1lll1111l_opy_ if bstack11l11lll1_opy_ (u"ࠬࡧࡰࡱࠩඎ") in config else bstack1l11ll_opy_ )
  data = {
    bstack11l11lll1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨඏ"): config[bstack11l11lll1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩඐ")],
    bstack11l11lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫඑ"): config[bstack11l11lll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬඒ")],
    bstack11l11lll1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧඓ"): bstack1lll1ll1_opy_,
    bstack11l11lll1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧඔ"): {
      bstack11l11lll1_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪඕ"): str(config[bstack11l11lll1_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ඖ")]) if bstack11l11lll1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ඗") in config else bstack11l11lll1_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ඘"),
      bstack11l11lll1_opy_ (u"ࠩࡵࡩ࡫࡫ࡲࡳࡧࡵࠫ඙"): bstack1lll11111_opy_(os.getenv(bstack11l11lll1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠧක"), bstack11l11lll1_opy_ (u"ࠦࠧඛ"))),
      bstack11l11lll1_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧග"): bstack11l11lll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ඝ"),
      bstack11l11lll1_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨඞ"): bstack111l11lll_opy_,
      bstack11l11lll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫඟ"): config[bstack11l11lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬච")]if config[bstack11l11lll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ඡ")] else bstack11l11lll1_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧජ"),
      bstack11l11lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧඣ"): str(config[bstack11l11lll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨඤ")]) if bstack11l11lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩඥ") in config else bstack11l11lll1_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤඦ"),
      bstack11l11lll1_opy_ (u"ࠩࡲࡷࠬට"): sys.platform,
      bstack11l11lll1_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬඨ"): socket.gethostname()
    }
  }
  update(data[bstack11l11lll1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧඩ")], bstack1l1l1ll_opy_)
  try:
    response = bstack11l111_opy_(bstack11l11lll1_opy_ (u"ࠬࡖࡏࡔࡖࠪඪ"), bstack1ll1l1ll_opy_, data, config)
    if response:
      logger.debug(bstack1lllll1ll_opy_.format(bstack1lll1ll1_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack11lll1_opy_.format(str(e)))
def bstack11l111_opy_(type, url, data, config):
  bstack1ll111l1_opy_ = bstack1ll11l11l_opy_.format(url)
  proxies = bstack1l1l1ll1_opy_(config, bstack1ll111l1_opy_)
  if type == bstack11l11lll1_opy_ (u"࠭ࡐࡐࡕࡗࠫණ"):
    response = requests.post(bstack1ll111l1_opy_, json=data,
                    headers={bstack11l11lll1_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ඬ"): bstack11l11lll1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫත")}, auth=(config[bstack11l11lll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫථ")], config[bstack11l11lll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ද")]), proxies=proxies)
  return response
def bstack1lll11111_opy_(framework):
  return bstack11l11lll1_opy_ (u"ࠦࢀࢃ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣධ").format(str(framework), __version__) if framework else bstack11l11lll1_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡦ࡭ࡥ࡯ࡶ࠲ࡿࢂࠨන").format(__version__)
def bstack1ll11lll1_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack111l11l_opy_()
    logger.debug(bstack11llllll_opy_.format(str(CONFIG)))
    bstack11ll1lll1_opy_()
    bstack11l1ll1ll_opy_()
  except Exception as e:
    logger.error(bstack11l11lll1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࡻࡰ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࠥ඲") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1l1l_opy_
  atexit.register(bstack1l1l11111_opy_)
  signal.signal(signal.SIGINT, bstack1l11ll11l_opy_)
  signal.signal(signal.SIGTERM, bstack1l11ll11l_opy_)
def bstack1l1l_opy_(exctype, value, traceback):
  global bstack11l111ll1_opy_
  try:
    for driver in bstack11l111ll1_opy_:
      driver.execute_script(
        bstack11l11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ࠮ࠣࠦࡷ࡫ࡡࡴࡱࡱࠦ࠿ࠦࠧඳ") + json.dumps(bstack11l11lll1_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦප") + str(value)) + bstack11l11lll1_opy_ (u"ࠩࢀࢁࠬඵ"))
  except Exception:
    pass
  bstack1l11ll1_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1l11ll1_opy_(message = bstack11l11lll1_opy_ (u"ࠪࠫබ")):
  global CONFIG
  try:
    if message:
      bstack1l1l1ll_opy_ = {
        bstack11l11lll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪභ"): str(message)
      }
      bstack1111ll_opy_(bstack1lll111ll_opy_, CONFIG, bstack1l1l1ll_opy_)
    else:
      bstack1111ll_opy_(bstack1lll111ll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11lll1111_opy_.format(str(e)))
def bstack11l111ll_opy_(bstack1l1llll11_opy_, size):
  bstack11l1ll11_opy_ = []
  while len(bstack1l1llll11_opy_) > size:
    bstack1llllll11_opy_ = bstack1l1llll11_opy_[:size]
    bstack11l1ll11_opy_.append(bstack1llllll11_opy_)
    bstack1l1llll11_opy_   = bstack1l1llll11_opy_[size:]
  bstack11l1ll11_opy_.append(bstack1l1llll11_opy_)
  return bstack11l1ll11_opy_
def bstack11ll111_opy_(args):
  if bstack11l11lll1_opy_ (u"ࠬ࠳࡭ࠨම") in args and bstack11l11lll1_opy_ (u"࠭ࡰࡥࡤࠪඹ") in args:
    return True
  return False
def run_on_browserstack(bstack1lll11l1_opy_=None, bstack1llll1l11_opy_=None, bstack1ll1l1111_opy_=False):
  global CONFIG
  global bstack1l1llllll_opy_
  global bstack1lll11l_opy_
  bstack1l1l1l1ll_opy_ = bstack11l11lll1_opy_ (u"ࠧࠨය")
  if bstack1lll11l1_opy_ and isinstance(bstack1lll11l1_opy_, str):
    bstack1lll11l1_opy_ = eval(bstack1lll11l1_opy_)
  if bstack1lll11l1_opy_:
    CONFIG = bstack1lll11l1_opy_[bstack11l11lll1_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨර")]
    bstack1l1llllll_opy_ = bstack1lll11l1_opy_[bstack11l11lll1_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪ඼")]
    bstack1lll11l_opy_ = bstack1lll11l1_opy_[bstack11l11lll1_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬල")]
    bstack1l1l1l1ll_opy_ = bstack11l11lll1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ඾")
  if not bstack1ll1l1111_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1ll1l1ll1_opy_)
      return
    if sys.argv[1] == bstack11l11lll1_opy_ (u"ࠬ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ඿")  or sys.argv[1] == bstack11l11lll1_opy_ (u"࠭࠭ࡷࠩව"):
      logger.info(bstack11l11lll1_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡐࡺࡶ࡫ࡳࡳࠦࡓࡅࡍࠣࡺࢀࢃࠧශ").format(__version__))
      return
    if sys.argv[1] == bstack11l11lll1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧෂ"):
      bstack11l1l111l_opy_()
      return
  args = sys.argv
  bstack1ll11lll1_opy_()
  global bstack11111ll1_opy_
  global bstack1lll1l1ll_opy_
  global bstack1111_opy_
  global bstack111l1ll1l_opy_
  global bstack1l111ll1l_opy_
  global bstack11l11l_opy_
  global bstack1l1ll1l_opy_
  global bstack111l1l1l_opy_
  if not bstack1l1l1l1ll_opy_:
    if args[1] == bstack11l11lll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩස") or args[1] == bstack11l11lll1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫහ"):
      bstack1l1l1l1ll_opy_ = bstack11l11lll1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫළ")
      args = args[2:]
    elif args[1] == bstack11l11lll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫෆ"):
      bstack1l1l1l1ll_opy_ = bstack11l11lll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ෇")
      args = args[2:]
    elif args[1] == bstack11l11lll1_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭෈"):
      bstack1l1l1l1ll_opy_ = bstack11l11lll1_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ෉")
      args = args[2:]
    elif args[1] == bstack11l11lll1_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮්ࠪ"):
      bstack1l1l1l1ll_opy_ = bstack11l11lll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ෋")
      args = args[2:]
    elif args[1] == bstack11l11lll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ෌"):
      bstack1l1l1l1ll_opy_ = bstack11l11lll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ෍")
      args = args[2:]
    elif args[1] == bstack11l11lll1_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭෎"):
      bstack1l1l1l1ll_opy_ = bstack11l11lll1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧා")
      args = args[2:]
    else:
      if not bstack11l11lll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫැ") in CONFIG or str(CONFIG[bstack11l11lll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬෑ")]).lower() in [bstack11l11lll1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪි"), bstack11l11lll1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬී")]:
        bstack1l1l1l1ll_opy_ = bstack11l11lll1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬු")
        args = args[1:]
      elif str(CONFIG[bstack11l11lll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ෕")]).lower() == bstack11l11lll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ූ"):
        bstack1l1l1l1ll_opy_ = bstack11l11lll1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ෗")
        args = args[1:]
      elif str(CONFIG[bstack11l11lll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬෘ")]).lower() == bstack11l11lll1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩෙ"):
        bstack1l1l1l1ll_opy_ = bstack11l11lll1_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪේ")
        args = args[1:]
      elif str(CONFIG[bstack11l11lll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨෛ")]).lower() == bstack11l11lll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ො"):
        bstack1l1l1l1ll_opy_ = bstack11l11lll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧෝ")
        args = args[1:]
      elif str(CONFIG[bstack11l11lll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫෞ")]).lower() == bstack11l11lll1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩෟ"):
        bstack1l1l1l1ll_opy_ = bstack11l11lll1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ෠")
        args = args[1:]
      else:
        os.environ[bstack11l11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭෡")] = bstack1l1l1l1ll_opy_
        bstack111l1l111_opy_(bstack1111ll11_opy_)
  global bstack111ll1lll_opy_
  if bstack1lll11l1_opy_:
    try:
      os.environ[bstack11l11lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ෢")] = bstack1l1l1l1ll_opy_
      bstack1111ll_opy_(bstack111l111ll_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack11lll1111_opy_.format(str(e)))
  global bstack1lll1llll_opy_
  global bstack1l11l11l1_opy_
  global bstack1l11l11_opy_
  global bstack11111l1l_opy_
  global bstack1l1l1_opy_
  global bstack1llll1ll_opy_
  global bstack1ll111lll_opy_
  global bstack11l1l11ll_opy_
  global bstack111ll1ll1_opy_
  global bstack111llllll_opy_
  global bstack1ll111ll_opy_
  global bstack111llll11_opy_
  global bstack1l11l111l_opy_
  global bstack1111l_opy_
  global bstack11ll1l111_opy_
  global bstack11l1l11l1_opy_
  global bstack111l1l_opy_
  global bstack11llll11l_opy_
  global bstack1ll11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1lll1llll_opy_ = webdriver.Remote.__init__
    bstack1l11l11l1_opy_ = WebDriver.quit
    bstack1ll111ll_opy_ = WebDriver.close
    bstack1111l_opy_ = WebDriver.get
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack111ll1lll_opy_ = Popen.__init__
  except Exception as e:
    pass
  if bstack1l1lllll1_opy_():
    if bstack1l11lll_opy_() < version.parse(bstack1111lll1_opy_):
      logger.error(bstack11lll1ll1_opy_.format(bstack1l11lll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack11ll1l111_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1l11l1ll_opy_.format(str(e)))
  if bstack1l1l1l1ll_opy_ != bstack11l11lll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭෣") or (bstack1l1l1l1ll_opy_ == bstack11l11lll1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ෤") and not bstack1lll11l1_opy_):
    bstack1ll1l1l1l_opy_()
  if (bstack1l1l1l1ll_opy_ in [bstack11l11lll1_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ෥"), bstack11l11lll1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ෦"), bstack11l11lll1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ෧")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack111l1_opy_
        bstack1l1l1_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1lll1l1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack11111l1l_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1l1l1111l_opy_ + str(e))
    except Exception as e:
      bstack1111l1l1_opy_(e, bstack1lll1l1_opy_)
    if bstack1l1l1l1ll_opy_ != bstack11l11lll1_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ෨"):
      bstack11lll_opy_()
    bstack1l11l11_opy_ = Output.end_test
    bstack1llll1ll_opy_ = TestStatus.__init__
    bstack11l1l11ll_opy_ = pabot._run
    bstack111ll1ll1_opy_ = QueueItem.__init__
    bstack111llllll_opy_ = pabot._create_command_for_execution
    bstack11llll11l_opy_ = pabot._report_results
  if bstack1l1l1l1ll_opy_ == bstack11l11lll1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ෩"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1111l1l1_opy_(e, bstack1l1lll_opy_)
    bstack111llll11_opy_ = Runner.run_hook
    bstack1l11l111l_opy_ = Step.run
  if bstack1l1l1l1ll_opy_ == bstack11l11lll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭෪"):
    try:
      from _pytest.config import Config
      bstack11l1l11l1_opy_ = Config.getoption
      from _pytest import runner
      bstack111l1l_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack111lll_opy_)
    try:
      from pytest_bdd import reporting
      bstack1ll11_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack11l11lll1_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨ෫"))
  if bstack1l1l1l1ll_opy_ == bstack11l11lll1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ෬"):
    bstack1lll1l1ll_opy_ = True
    if bstack1lll11l1_opy_ and bstack1ll1l1111_opy_:
      bstack1l111ll1l_opy_ = CONFIG.get(bstack11l11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭෭"), {}).get(bstack11l11lll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ෮"))
      bstack11ll11l1l_opy_(bstack111111_opy_)
    elif bstack1lll11l1_opy_:
      bstack1l111ll1l_opy_ = CONFIG.get(bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ෯"), {}).get(bstack11l11lll1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ෰"))
      global bstack11l111ll1_opy_
      try:
        if bstack11ll111_opy_(bstack1lll11l1_opy_[bstack11l11lll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ෱")]) and multiprocessing.current_process().name == bstack11l11lll1_opy_ (u"ࠧ࠱ࠩෲ"):
          bstack1lll11l1_opy_[bstack11l11lll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫෳ")].remove(bstack11l11lll1_opy_ (u"ࠩ࠰ࡱࠬ෴"))
          bstack1lll11l1_opy_[bstack11l11lll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭෵")].remove(bstack11l11lll1_opy_ (u"ࠫࡵࡪࡢࠨ෶"))
          bstack1lll11l1_opy_[bstack11l11lll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ෷")] = bstack1lll11l1_opy_[bstack11l11lll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ෸")][0]
          with open(bstack1lll11l1_opy_[bstack11l11lll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ෹")], bstack11l11lll1_opy_ (u"ࠨࡴࠪ෺")) as f:
            bstack111ll1l11_opy_ = f.read()
          bstack1ll1111_opy_ = bstack11l11lll1_opy_ (u"ࠤࠥࠦ࡫ࡸ࡯࡮ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡧ࡯ࠥ࡯࡭ࡱࡱࡵࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥ࠼ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩ࠭ࢁࡽࠪ࠽ࠣࡪࡷࡵ࡭ࠡࡲࡧࡦࠥ࡯࡭ࡱࡱࡵࡸࠥࡖࡤࡣ࠽ࠣࡳ࡬ࡥࡤࡣࠢࡀࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࡸࡥࡢ࡭࠾ࠎࡩ࡫ࡦࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠬࡸ࡫࡬ࡧ࠮ࠣࡥࡷ࡭ࠬࠡࡶࡨࡱࡵࡵࡲࡢࡴࡼࠤࡂࠦ࠰ࠪ࠼ࠍࠤࠥࡺࡲࡺ࠼ࠍࠤࠥࠦࠠࡢࡴࡪࠤࡂࠦࡳࡵࡴࠫ࡭ࡳࡺࠨࡢࡴࡪ࠭࠰࠷࠰ࠪࠌࠣࠤࡪࡾࡣࡦࡲࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡢࡵࠣࡩ࠿ࠐࠠࠡࠢࠣࡴࡦࡹࡳࠋࠢࠣࡳ࡬ࡥࡤࡣࠪࡶࡩࡱ࡬ࠬࡢࡴࡪ࠰ࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠩࠋࡒࡧࡦ࠳ࡪ࡯ࡠࡤࠣࡁࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠋࡒࡧࡦ࠳ࡪ࡯ࡠࡤࡵࡩࡦࡱࠠ࠾ࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯ࠏࡖࡤࡣࠪࠬ࠲ࡸ࡫ࡴࡠࡶࡵࡥࡨ࡫ࠨࠪ࡞ࡱࠦࠧࠨ෻").format(str(bstack1lll11l1_opy_))
          bstack1l1l1l_opy_ = bstack1ll1111_opy_ + bstack111ll1l11_opy_
          bstack1l111l11_opy_ = bstack1lll11l1_opy_[bstack11l11lll1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭෼")] + bstack11l11lll1_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡺࡥ࡮ࡲ࠱ࡴࡾ࠭෽")
          with open(bstack1l111l11_opy_, bstack11l11lll1_opy_ (u"ࠬࡽࠧ෾")):
            pass
          with open(bstack1l111l11_opy_, bstack11l11lll1_opy_ (u"ࠨࡷࠬࠤ෿")) as f:
            f.write(bstack1l1l1l_opy_)
          import subprocess
          bstack1l111l11l_opy_ = subprocess.run([bstack11l11lll1_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢ฀"), bstack1l111l11_opy_])
          if os.path.exists(bstack1l111l11_opy_):
            os.unlink(bstack1l111l11_opy_)
          os._exit(bstack1l111l11l_opy_.returncode)
        else:
          if bstack11ll111_opy_(bstack1lll11l1_opy_[bstack11l11lll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫก")]):
            bstack1lll11l1_opy_[bstack11l11lll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬข")].remove(bstack11l11lll1_opy_ (u"ࠪ࠱ࡲ࠭ฃ"))
            bstack1lll11l1_opy_[bstack11l11lll1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧค")].remove(bstack11l11lll1_opy_ (u"ࠬࡶࡤࡣࠩฅ"))
            bstack1lll11l1_opy_[bstack11l11lll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩฆ")] = bstack1lll11l1_opy_[bstack11l11lll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪง")][0]
          bstack11ll11l1l_opy_(bstack111111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1lll11l1_opy_[bstack11l11lll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫจ")])))
          mod_globals = globals()
          mod_globals[bstack11l11lll1_opy_ (u"ࠩࡢࡣࡳࡧ࡭ࡦࡡࡢࠫฉ")] = bstack11l11lll1_opy_ (u"ࠪࡣࡤࡳࡡࡪࡰࡢࡣࠬช")
          mod_globals[bstack11l11lll1_opy_ (u"ࠫࡤࡥࡦࡪ࡮ࡨࡣࡤ࠭ซ")] = os.path.abspath(bstack1lll11l1_opy_[bstack11l11lll1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨฌ")])
          exec(open(bstack1lll11l1_opy_[bstack11l11lll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩญ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11l11lll1_opy_ (u"ࠧࡄࡣࡸ࡫࡭ࡺࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠧฎ").format(str(e)))
          for driver in bstack11l111ll1_opy_:
            bstack1llll1l11_opy_.append({
              bstack11l11lll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ฏ"): bstack1lll11l1_opy_[bstack11l11lll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬฐ")],
              bstack11l11lll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩฑ"): str(e),
              bstack11l11lll1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪฒ"): multiprocessing.current_process().name
            })
            driver.execute_script(
              bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡸࡺࡡࡵࡷࡶࠦ࠿ࠨࡦࡢ࡫࡯ࡩࡩࠨࠬࠡࠤࡵࡩࡦࡹ࡯࡯ࠤ࠽ࠤࠬณ") + json.dumps(bstack11l11lll1_opy_ (u"ࠨࡓࡦࡵࡶ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤด") + str(e)) + bstack11l11lll1_opy_ (u"ࠧࡾࡿࠪต"))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack11l111ll1_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      bstack111l11l1l_opy_()
      bstack111l1ll_opy_()
      bstack11llll1l_opy_ = {
        bstack11l11lll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫถ"): args[0],
        bstack11l11lll1_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩท"): CONFIG,
        bstack11l11lll1_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫธ"): bstack1l1llllll_opy_,
        bstack11l11lll1_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭น"): bstack1lll11l_opy_
      }
      if bstack11l11lll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨบ") in CONFIG:
        bstack11ll11111_opy_ = []
        manager = multiprocessing.Manager()
        bstack1111l11_opy_ = manager.list()
        if bstack11ll111_opy_(args):
          for index, platform in enumerate(CONFIG[bstack11l11lll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩป")]):
            if index == 0:
              bstack11llll1l_opy_[bstack11l11lll1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪผ")] = args
            bstack11ll11111_opy_.append(multiprocessing.Process(name=str(index),
                                          target=run_on_browserstack, args=(bstack11llll1l_opy_, bstack1111l11_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack11l11lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫฝ")]):
            bstack11ll11111_opy_.append(multiprocessing.Process(name=str(index),
                                          target=run_on_browserstack, args=(bstack11llll1l_opy_, bstack1111l11_opy_)))
        for t in bstack11ll11111_opy_:
          t.start()
        for t in bstack11ll11111_opy_:
          t.join()
        bstack1l1ll1l_opy_ = list(bstack1111l11_opy_)
      else:
        if bstack11ll111_opy_(args):
          bstack11llll1l_opy_[bstack11l11lll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬพ")] = args
          test = multiprocessing.Process(name=str(0),
                                        target=run_on_browserstack, args=(bstack11llll1l_opy_,))
          test.start()
          test.join()
        else:
          bstack11ll11l1l_opy_(bstack111111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11l11lll1_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬฟ")] = bstack11l11lll1_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭ภ")
          mod_globals[bstack11l11lll1_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧม")] = os.path.abspath(args[0])
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l1l1l1ll_opy_ == bstack11l11lll1_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬย") or bstack1l1l1l1ll_opy_ == bstack11l11lll1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ร"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack1111l1l1_opy_(e, bstack1lll1l1_opy_)
    bstack111l11l1l_opy_()
    bstack11ll11l1l_opy_(bstack1ll11lll_opy_)
    if bstack11l11lll1_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ฤ") in args:
      i = args.index(bstack11l11lll1_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧล"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack11111ll1_opy_))
    args.insert(0, str(bstack11l11lll1_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨฦ")))
    pabot.main(args)
  elif bstack1l1l1l1ll_opy_ == bstack11l11lll1_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬว"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1111l1l1_opy_(e, bstack1lll1l1_opy_)
    for a in args:
      if bstack11l11lll1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛ࠫศ") in a:
        bstack111l1ll1l_opy_ = int(a.split(bstack11l11lll1_opy_ (u"࠭࠺ࠨษ"))[1])
      if bstack11l11lll1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫส") in a:
        bstack1l111ll1l_opy_ = str(a.split(bstack11l11lll1_opy_ (u"ࠨ࠼ࠪห"))[1])
      if bstack11l11lll1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔࠩฬ") in a:
        bstack11l11l_opy_ = str(a.split(bstack11l11lll1_opy_ (u"ࠪ࠾ࠬอ"))[1])
    bstack1ll1111l1_opy_ = None
    if bstack11l11lll1_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠪฮ") in args:
      i = args.index(bstack11l11lll1_opy_ (u"ࠬ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠫฯ"))
      args.pop(i)
      bstack1ll1111l1_opy_ = args.pop(i)
    if bstack1ll1111l1_opy_ is not None:
      global bstack1l1l11ll_opy_
      bstack1l1l11ll_opy_ = bstack1ll1111l1_opy_
    bstack11ll11l1l_opy_(bstack1ll11lll_opy_)
    run_cli(args)
  elif bstack1l1l1l1ll_opy_ == bstack11l11lll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ะ"):
    try:
      from _pytest.config import _prepareconfig
      from _pytest.config import Config
      from _pytest import runner
      import importlib
      bstack1ll1_opy_ = importlib.find_loader(bstack11l11lll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩั"))
    except Exception as e:
      logger.warn(e, bstack111lll_opy_)
    bstack111l11l1l_opy_()
    try:
      if bstack11l11lll1_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪา") in args:
        i = args.index(bstack11l11lll1_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫำ"))
        args.pop(i+1)
        args.pop(i)
      if bstack11l11lll1_opy_ (u"ࠪ࠱࠲ࡶ࡬ࡶࡩ࡬ࡲࡸ࠭ิ") in args:
        i = args.index(bstack11l11lll1_opy_ (u"ࠫ࠲࠳ࡰ࡭ࡷࡪ࡭ࡳࡹࠧี"))
        args.pop(i+1)
        args.pop(i)
      if bstack11l11lll1_opy_ (u"ࠬ࠳ࡰࠨึ") in args:
        i = args.index(bstack11l11lll1_opy_ (u"࠭࠭ࡱࠩื"))
        args.pop(i+1)
        args.pop(i)
      if bstack11l11lll1_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨุ") in args:
        i = args.index(bstack11l11lll1_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴูࠩ"))
        args.pop(i+1)
        args.pop(i)
      if bstack11l11lll1_opy_ (u"ࠩ࠰ࡲฺࠬ") in args:
        i = args.index(bstack11l11lll1_opy_ (u"ࠪ࠱ࡳ࠭฻"))
        args.pop(i+1)
        args.pop(i)
    except Exception as exc:
      logger.error(str(exc))
    config = _prepareconfig(args)
    bstack1l11111_opy_ = config.args
    bstack11l11lll_opy_ = config.invocation_params.args
    bstack11l11lll_opy_ = list(bstack11l11lll_opy_)
    bstack11l1ll1l_opy_ = [os.path.normpath(item) for item in bstack1l11111_opy_]
    bstack1ll1l11l1_opy_ = [os.path.normpath(item) for item in bstack11l11lll_opy_]
    bstack1ll1ll11l_opy_ = [item for item in bstack1ll1l11l1_opy_ if item not in bstack11l1ll1l_opy_]
    if bstack11l11lll1_opy_ (u"ࠫ࠲࠳ࡣࡢࡥ࡫ࡩ࠲ࡩ࡬ࡦࡣࡵࠫ฼") not in bstack1ll1ll11l_opy_:
      bstack1ll1ll11l_opy_.append(bstack11l11lll1_opy_ (u"ࠬ࠳࠭ࡤࡣࡦ࡬ࡪ࠳ࡣ࡭ࡧࡤࡶࠬ฽"))
    import platform as pf
    if pf.system().lower() == bstack11l11lll1_opy_ (u"࠭ࡷࡪࡰࡧࡳࡼࡹࠧ฾"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l11111_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1llll11_opy_)))
                    for bstack1llll11_opy_ in bstack1l11111_opy_]
    if (bstack11111l_opy_):
      bstack1ll1ll11l_opy_.append(bstack11l11lll1_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ฿"))
      bstack1ll1ll11l_opy_.append(bstack11l11lll1_opy_ (u"ࠨࡖࡵࡹࡪ࠭เ"))
    try:
      from pytest_bdd import reporting
      bstack111l1l1l_opy_ = True
    except Exception as e:
      pass
    if (not bstack111l1l1l_opy_):
      bstack1ll1ll11l_opy_.append(bstack11l11lll1_opy_ (u"ࠩ࠰ࡴࠬแ"))
      bstack1ll1ll11l_opy_.append(bstack11l11lll1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠨโ"))
    bstack1ll1ll11l_opy_.append(bstack11l11lll1_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭ใ"))
    bstack1ll1ll11l_opy_.append(bstack11l11lll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬไ"))
    bstack111l11_opy_ = []
    for spec in bstack1l11111_opy_:
      bstack1l11l1_opy_ = []
      bstack1l11l1_opy_.append(spec)
      bstack1l11l1_opy_ += bstack1ll1ll11l_opy_
      bstack111l11_opy_.append(bstack1l11l1_opy_)
    bstack1111_opy_ = True
    bstack11llll_opy_ = 1
    if bstack11l11lll1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ๅ") in CONFIG:
      bstack11llll_opy_ = CONFIG[bstack11l11lll1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧๆ")]
    bstack11ll1lll_opy_ = int(bstack11llll_opy_)*int(len(CONFIG[bstack11l11lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ็")]))
    execution_items = []
    for bstack1l11l1_opy_ in bstack111l11_opy_:
      for index, _ in enumerate(CONFIG[bstack11l11lll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷ่ࠬ")]):
        item = {}
        item[bstack11l11lll1_opy_ (u"ࠪࡥࡷ࡭้ࠧ")] = bstack1l11l1_opy_
        item[bstack11l11lll1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺ๊ࠪ")] = index
        execution_items.append(item)
    bstack11lll1l1l_opy_ = bstack11l111ll_opy_(execution_items, bstack11ll1lll_opy_)
    for execution_item in bstack11lll1l1l_opy_:
      bstack11ll11111_opy_ = []
      for item in execution_item:
        bstack11ll11111_opy_.append(bstack11l11ll1l_opy_(name=str(item[bstack11l11lll1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻ๋ࠫ")]),
                                            target=bstack11l1111l1_opy_,
                                            args=(item[bstack11l11lll1_opy_ (u"࠭ࡡࡳࡩࠪ์")],)))
      for t in bstack11ll11111_opy_:
        t.start()
      for t in bstack11ll11111_opy_:
        t.join()
  elif bstack1l1l1l1ll_opy_ == bstack11l11lll1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧํ"):
    try:
      from behave.__main__ import main as bstack11lllll11_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1111l1l1_opy_(e, bstack1l1lll_opy_)
    bstack111l11l1l_opy_()
    bstack1111_opy_ = True
    bstack11llll_opy_ = 1
    if bstack11l11lll1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ๎") in CONFIG:
      bstack11llll_opy_ = CONFIG[bstack11l11lll1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ๏")]
    bstack11ll1lll_opy_ = int(bstack11llll_opy_)*int(len(CONFIG[bstack11l11lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭๐")]))
    config = Configuration(args)
    bstack1l11111_opy_ = config.paths
    bstack1l1ll1111_opy_ = []
    for arg in args:
      if os.path.normpath(arg) not in bstack1l11111_opy_:
        bstack1l1ll1111_opy_.append(arg)
    import platform as pf
    if pf.system().lower() == bstack11l11lll1_opy_ (u"ࠫࡼ࡯࡮ࡥࡱࡺࡷࠬ๑"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l11111_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1llll11_opy_)))
                    for bstack1llll11_opy_ in bstack1l11111_opy_]
    bstack111l11_opy_ = []
    for spec in bstack1l11111_opy_:
      bstack1l11l1_opy_ = []
      bstack1l11l1_opy_ += bstack1l1ll1111_opy_
      bstack1l11l1_opy_.append(spec)
      bstack111l11_opy_.append(bstack1l11l1_opy_)
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack11l11lll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ๒")]):
      for bstack1l11l1_opy_ in bstack111l11_opy_:
        item = {}
        item[bstack11l11lll1_opy_ (u"࠭ࡡࡳࡩࠪ๓")] = bstack11l11lll1_opy_ (u"ࠧࠡࠩ๔").join(bstack1l11l1_opy_)
        item[bstack11l11lll1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ๕")] = index
        execution_items.append(item)
    bstack11lll1l1l_opy_ = bstack11l111ll_opy_(execution_items, bstack11ll1lll_opy_)
    for execution_item in bstack11lll1l1l_opy_:
      bstack11ll11111_opy_ = []
      for item in execution_item:
        bstack11ll11111_opy_.append(bstack11l11ll1l_opy_(name=str(item[bstack11l11lll1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ๖")]),
                                            target=bstack111111l1_opy_,
                                            args=(item[bstack11l11lll1_opy_ (u"ࠪࡥࡷ࡭ࠧ๗")],)))
      for t in bstack11ll11111_opy_:
        t.start()
      for t in bstack11ll11111_opy_:
        t.join()
  else:
    bstack111l1l111_opy_(bstack1111ll11_opy_)
  if not bstack1lll11l1_opy_:
    bstack1l1l11l1l_opy_()
def browserstack_initialize(bstack111ll1l1_opy_=None):
  run_on_browserstack(bstack111ll1l1_opy_, None, True)
def bstack1l1l11l1l_opy_():
  [bstack1ll111l_opy_, bstack11llll1_opy_] = bstack1l1111l_opy_()
  if bstack1ll111l_opy_ is not None and bstack1ll11l1l_opy_() != -1:
    sessions = bstack1l11l111_opy_(bstack1ll111l_opy_)
    bstack111l1l1l1_opy_(sessions, bstack11llll1_opy_)
def bstack111l1l11_opy_(bstack11ll11_opy_):
    if bstack11ll11_opy_:
        return bstack11ll11_opy_.capitalize()
    else:
        return bstack11ll11_opy_
def bstack111lll1l_opy_(bstack111lll1l1_opy_):
    if bstack11l11lll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ๘") in bstack111lll1l1_opy_ and bstack111lll1l1_opy_[bstack11l11lll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ๙")] != bstack11l11lll1_opy_ (u"࠭ࠧ๚"):
        return bstack111lll1l1_opy_[bstack11l11lll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ๛")]
    else:
        bstack11lll11l_opy_ = bstack11l11lll1_opy_ (u"ࠣࠤ๜")
        if bstack11l11lll1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ๝") in bstack111lll1l1_opy_ and bstack111lll1l1_opy_[bstack11l11lll1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ๞")] != None:
            bstack11lll11l_opy_ += bstack111lll1l1_opy_[bstack11l11lll1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ๟")] + bstack11l11lll1_opy_ (u"ࠧ࠲ࠠࠣ๠")
            if bstack111lll1l1_opy_[bstack11l11lll1_opy_ (u"࠭࡯ࡴࠩ๡")] == bstack11l11lll1_opy_ (u"ࠢࡪࡱࡶࠦ๢"):
                bstack11lll11l_opy_ += bstack11l11lll1_opy_ (u"ࠣ࡫ࡒࡗࠥࠨ๣")
            bstack11lll11l_opy_ += (bstack111lll1l1_opy_[bstack11l11lll1_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭๤")] or bstack11l11lll1_opy_ (u"ࠪࠫ๥"))
            return bstack11lll11l_opy_
        else:
            bstack11lll11l_opy_ += bstack111l1l11_opy_(bstack111lll1l1_opy_[bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ๦")]) + bstack11l11lll1_opy_ (u"ࠧࠦࠢ๧") + (bstack111lll1l1_opy_[bstack11l11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ๨")] or bstack11l11lll1_opy_ (u"ࠧࠨ๩")) + bstack11l11lll1_opy_ (u"ࠣ࠮ࠣࠦ๪")
            if bstack111lll1l1_opy_[bstack11l11lll1_opy_ (u"ࠩࡲࡷࠬ๫")] == bstack11l11lll1_opy_ (u"࡛ࠥ࡮ࡴࡤࡰࡹࡶࠦ๬"):
                bstack11lll11l_opy_ += bstack11l11lll1_opy_ (u"ࠦ࡜࡯࡮ࠡࠤ๭")
            bstack11lll11l_opy_ += bstack111lll1l1_opy_[bstack11l11lll1_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ๮")] or bstack11l11lll1_opy_ (u"࠭ࠧ๯")
            return bstack11lll11l_opy_
def bstack111l1ll1_opy_(bstack11ll1111_opy_):
    if bstack11ll1111_opy_ == bstack11l11lll1_opy_ (u"ࠢࡥࡱࡱࡩࠧ๰"):
        return bstack11l11lll1_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡇࡴࡳࡰ࡭ࡧࡷࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ๱")
    elif bstack11ll1111_opy_ == bstack11l11lll1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ๲"):
        return bstack11l11lll1_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡈࡤ࡭ࡱ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭๳")
    elif bstack11ll1111_opy_ == bstack11l11lll1_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ๴"):
        return bstack11l11lll1_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡨࡴࡨࡩࡳࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡨࡴࡨࡩࡳࠨ࠾ࡑࡣࡶࡷࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ๵")
    elif bstack11ll1111_opy_ == bstack11l11lll1_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ๶"):
        return bstack11l11lll1_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡵࡩࡩࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡳࡧࡧࠦࡃࡋࡲࡳࡱࡵࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ๷")
    elif bstack11ll1111_opy_ == bstack11l11lll1_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤ๸"):
        return bstack11l11lll1_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࠨ࡫ࡥࡢ࠵࠵࠺ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࠣࡦࡧࡤ࠷࠷࠼ࠢ࠿ࡖ࡬ࡱࡪࡵࡵࡵ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ๹")
    elif bstack11ll1111_opy_ == bstack11l11lll1_opy_ (u"ࠥࡶࡺࡴ࡮ࡪࡰࡪࠦ๺"):
        return bstack11l11lll1_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡢ࡭ࡣࡦ࡯ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡢ࡭ࡣࡦ࡯ࠧࡄࡒࡶࡰࡱ࡭ࡳ࡭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ๻")
    else:
        return bstack11l11lll1_opy_ (u"ࠬࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡤ࡯ࡥࡨࡱ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡤ࡯ࡥࡨࡱࠢ࠿ࠩ๼")+bstack111l1l11_opy_(bstack11ll1111_opy_)+bstack11l11lll1_opy_ (u"࠭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ๽")
def bstack1111l1_opy_(session):
    return bstack11l11lll1_opy_ (u"ࠧ࠽ࡶࡵࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡷࡵࡷࠣࡀ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡴࡡ࡮ࡧࠥࡂࡁࡧࠠࡩࡴࡨࡪࡂࠨࡻࡾࠤࠣࡸࡦࡸࡧࡦࡶࡀࠦࡤࡨ࡬ࡢࡰ࡮ࠦࡃࢁࡽ࠽࠱ࡤࡂࡁ࠵ࡴࡥࡀࡾࢁࢀࢃ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾࠲ࡸࡷࡄࠧ๾").format(session[bstack11l11lll1_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬ๿")],bstack111lll1l_opy_(session), bstack111l1ll1_opy_(session[bstack11l11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡷࡥࡹࡻࡳࠨ຀")]), bstack111l1ll1_opy_(session[bstack11l11lll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪກ")]), bstack111l1l11_opy_(session[bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬຂ")] or session[bstack11l11lll1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ຃")] or bstack11l11lll1_opy_ (u"࠭ࠧຄ")) + bstack11l11lll1_opy_ (u"ࠢࠡࠤ຅") + (session[bstack11l11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪຆ")] or bstack11l11lll1_opy_ (u"ࠩࠪງ")), session[bstack11l11lll1_opy_ (u"ࠪࡳࡸ࠭ຈ")] + bstack11l11lll1_opy_ (u"ࠦࠥࠨຉ") + session[bstack11l11lll1_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩຊ")], session[bstack11l11lll1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ຋")] or bstack11l11lll1_opy_ (u"ࠧࠨຌ"), session[bstack11l11lll1_opy_ (u"ࠨࡥࡵࡩࡦࡺࡥࡥࡡࡤࡸࠬຍ")] if session[bstack11l11lll1_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭ຎ")] else bstack11l11lll1_opy_ (u"ࠪࠫຏ"))
def bstack111l1l1l1_opy_(sessions, bstack11llll1_opy_):
  try:
    bstack1l1111l11_opy_ = bstack11l11lll1_opy_ (u"ࠦࠧຐ")
    if not os.path.exists(bstack1l111111_opy_):
      os.mkdir(bstack1l111111_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l11lll1_opy_ (u"ࠬࡧࡳࡴࡧࡷࡷ࠴ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪຑ")), bstack11l11lll1_opy_ (u"࠭ࡲࠨຒ")) as f:
      bstack1l1111l11_opy_ = f.read()
    bstack1l1111l11_opy_ = bstack1l1111l11_opy_.replace(bstack11l11lll1_opy_ (u"ࠧࡼࠧࡕࡉࡘ࡛ࡌࡕࡕࡢࡇࡔ࡛ࡎࡕࠧࢀࠫຓ"), str(len(sessions)))
    bstack1l1111l11_opy_ = bstack1l1111l11_opy_.replace(bstack11l11lll1_opy_ (u"ࠨࡽࠨࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠫࡽࠨດ"), bstack11llll1_opy_)
    bstack1l1111l11_opy_ = bstack1l1111l11_opy_.replace(bstack11l11lll1_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠦࡿࠪຕ"), sessions[0].get(bstack11l11lll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡥࡲ࡫ࠧຖ")) if sessions[0] else bstack11l11lll1_opy_ (u"ࠫࠬທ"))
    with open(os.path.join(bstack1l111111_opy_, bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡷ࡫ࡰࡰࡴࡷ࠲࡭ࡺ࡭࡭ࠩຘ")), bstack11l11lll1_opy_ (u"࠭ࡷࠨນ")) as stream:
      stream.write(bstack1l1111l11_opy_.split(bstack11l11lll1_opy_ (u"ࠧࡼࠧࡖࡉࡘ࡙ࡉࡐࡐࡖࡣࡉࡇࡔࡂࠧࢀࠫບ"))[0])
      for session in sessions:
        stream.write(bstack1111l1_opy_(session))
      stream.write(bstack1l1111l11_opy_.split(bstack11l11lll1_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬປ"))[1])
    logger.info(bstack11l11lll1_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࡨࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡧࡻࡩ࡭ࡦࠣࡥࡷࡺࡩࡧࡣࡦࡸࡸࠦࡡࡵࠢࡾࢁࠬຜ").format(bstack1l111111_opy_));
  except Exception as e:
    logger.debug(bstack1l1ll1l1_opy_.format(str(e)))
def bstack1l11l111_opy_(bstack1ll111l_opy_):
  global CONFIG
  try:
    host = bstack11l11lll1_opy_ (u"ࠪࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠭ຝ") if bstack11l11lll1_opy_ (u"ࠫࡦࡶࡰࠨພ") in CONFIG else bstack11l11lll1_opy_ (u"ࠬࡧࡰࡪࠩຟ")
    user = CONFIG[bstack11l11lll1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨຠ")]
    key = CONFIG[bstack11l11lll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪມ")]
    bstack1111111l_opy_ = bstack11l11lll1_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧຢ") if bstack11l11lll1_opy_ (u"ࠩࡤࡴࡵ࠭ຣ") in CONFIG else bstack11l11lll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ຤")
    url = bstack11l11lll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࢀࢃ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡶࡩࡸࡹࡩࡰࡰࡶ࠲࡯ࡹ࡯࡯ࠩລ").format(user, key, host, bstack1111111l_opy_, bstack1ll111l_opy_)
    headers = {
      bstack11l11lll1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ຦"): bstack11l11lll1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩວ"),
    }
    proxies = bstack1l1l1ll1_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack11l11lll1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬຨ")], response.json()))
  except Exception as e:
    logger.debug(bstack1llll1l1l_opy_.format(str(e)))
def bstack1l1111l_opy_():
  global CONFIG
  try:
    if bstack11l11lll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫຩ") in CONFIG:
      host = bstack11l11lll1_opy_ (u"ࠩࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨࠬສ") if bstack11l11lll1_opy_ (u"ࠪࡥࡵࡶࠧຫ") in CONFIG else bstack11l11lll1_opy_ (u"ࠫࡦࡶࡩࠨຬ")
      user = CONFIG[bstack11l11lll1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧອ")]
      key = CONFIG[bstack11l11lll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩຮ")]
      bstack1111111l_opy_ = bstack11l11lll1_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ຯ") if bstack11l11lll1_opy_ (u"ࠨࡣࡳࡴࠬະ") in CONFIG else bstack11l11lll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫັ")
      url = bstack11l11lll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡿࢂ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠳ࡰࡳࡰࡰࠪາ").format(user, key, host, bstack1111111l_opy_)
      headers = {
        bstack11l11lll1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪຳ"): bstack11l11lll1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨິ"),
      }
      if bstack11l11lll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨີ") in CONFIG:
        params = {bstack11l11lll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬຶ"):CONFIG[bstack11l11lll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫື")], bstack11l11lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶຸࠬ"):CONFIG[bstack11l11lll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶູࠬ")]}
      else:
        params = {bstack11l11lll1_opy_ (u"ࠫࡳࡧ࡭ࡦ຺ࠩ"):CONFIG[bstack11l11lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨົ")]}
      proxies = bstack1l1l1ll1_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1l11ll1l1_opy_ = response.json()[0][bstack11l11lll1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡦࡺ࡯࡬ࡥࠩຼ")]
        if bstack1l11ll1l1_opy_:
          bstack11llll1_opy_ = bstack1l11ll1l1_opy_[bstack11l11lll1_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࡟ࡶࡴ࡯ࠫຽ")].split(bstack11l11lll1_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣ࠮ࡤࡸ࡭ࡱࡪࠧ຾"))[0] + bstack11l11lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴ࠱ࠪ຿") + bstack1l11ll1l1_opy_[bstack11l11lll1_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ເ")]
          logger.info(bstack1ll1l1l_opy_.format(bstack11llll1_opy_))
          bstack1l1l11lll_opy_ = CONFIG[bstack11l11lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧແ")]
          if bstack11l11lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧໂ") in CONFIG:
            bstack1l1l11lll_opy_ += bstack11l11lll1_opy_ (u"࠭ࠠࠨໃ") + CONFIG[bstack11l11lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩໄ")]
          if bstack1l1l11lll_opy_!= bstack1l11ll1l1_opy_[bstack11l11lll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭໅")]:
            logger.debug(bstack11l1l1lll_opy_.format(bstack1l11ll1l1_opy_[bstack11l11lll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧໆ")], bstack1l1l11lll_opy_))
          return [bstack1l11ll1l1_opy_[bstack11l11lll1_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭໇")], bstack11llll1_opy_]
    else:
      logger.warn(bstack1l1lll1_opy_)
  except Exception as e:
    logger.debug(bstack1lll111_opy_.format(str(e)))
  return [None, None]
def bstack1ll11ll_opy_(url, bstack111lll1_opy_=False):
  global CONFIG
  global bstack1ll1l1_opy_
  if not bstack1ll1l1_opy_:
    hostname = bstack1l1lllll_opy_(url)
    is_private = bstack11l111l1l_opy_(hostname)
    if (bstack11l11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ່") in CONFIG and not CONFIG[bstack11l11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭້ࠩ")]) and (is_private or bstack111lll1_opy_):
      bstack1ll1l1_opy_ = hostname
def bstack1l1lllll_opy_(url):
  return urlparse(url).hostname
def bstack11l111l1l_opy_(hostname):
  for bstack1l11111ll_opy_ in bstack1ll11111_opy_:
    regex = re.compile(bstack1l11111ll_opy_)
    if regex.match(hostname):
      return True
  return False