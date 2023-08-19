#!/usr/bin/env python
from abipy import abilab

abifile = abilab.abiopen("diamond_444q_full_SIGEPH.nc")

abifile.plot_qpsolution_skb(0,  0 , 5, solve=True)
