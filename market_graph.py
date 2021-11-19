# %%

import graph_tool.all as gt
import numpy as np
import urllib.request
import os
import csg as csg
from pycoingecko import CoinGeckoAPI
from sklearn import preprocessing

# %%

cg = CoinGeckoAPI()

if not os.path.exists("symbols_imgs"):
    os.mkdir("symbols_imgs")

img_path = os.path.join(os.getcwd(), "symbols_imgs")
markets = cg.get_coins_markets(
    "usd", per_page=40, page=1, sparkline=True, price_change_percent="1h,24h,7d"
)

# %%
markets

# %%
def process_market_data(data):
    sd = {}
    derived_sd = {}
    for symbol in data:
        s = symbol["symbol"]
        img = symbol["image"]
        mcap = symbol["market_cap"]
        vol = symbol["total_volume"]
        price = symbol["current_price"]
        price_change = symbol["price_change_percentage_24h"]
        mcap_change = symbol["market_cap_change_percentage_24h"]
        sd[s] = [mcap, vol, price_change, mcap_change]
        derived_sd[s] = [100 * vol / mcap, price_change, mcap_change]
    return sd, derived_sd


# %%
sd, derived_sd = process_market_data(markets)


# %%
sd

# %%
derived_sd

# %%
names = np.array(list(sd.keys()))
sdarray = np.array(list(sd.values()))
dsd = np.array(list(derived_sd.values()))


# %%
tdsd = preprocessing.minmax_scale(dsd)
# %%
volmcap = dsd[:, 0]
price_change = dsd[:, 1]
mcap_change = dsd[:, 2]
mcap = sdarray[:, 0]
# %%

names
volmcap
# %%

g = gt.Graph(directed=False)

# %%
g.vp.name = g.new_vp("string")
g.vp.color = g.new_vp("string")
g.vp.volmcap = g.new_vp("float")
g.vp.pricec = g.new_vp("float")
g.vp.mcapc = g.new_vp("float")
g.vp.mcap = g.new_vp("float")
# %%
M = np.column_stack((mcap, price_change))
# %%


cs = csg.ConnectedSparseGraph(M, g=g)

# %%
cs.build()

# %%
for v in cs.get_vertices():

    cs.vp.name[v] = names[v]
    cs.vp.color[v] = "green" if price_change[v] >= 0 else "red"
    cs.vp.volmcap[v] = volmcap[v]
    cs.vp.pricec[v] = price_change[v]
    cs.vp.mcapc[v] = mcap_change[v]
    cs.vp.mcap[v] = mcap[v]

    print(names[v], volmcap[v], price_change[v])


# %%

cs.vp.name[1]
cs.vp.color[1]
cs.vp.volmcap[1]

# %%
gt.graph_draw(
    cs,
    vertex_text=cs.vp.name,
    vertex_text_position="centered",
    vertex_font_size=8,
    vertex_fill_color=cs.vp.color,
    vertex_size=gt.prop_to_size(cs.vp.mcap, mi=5, ma=15, power=1, log=True),
    output = "market_graph.png",
)

# %%
