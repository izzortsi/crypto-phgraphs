# crypto-phgraphs
Persistent homology graphs for cryptocurrency datasets with Binance's API
___

A set of (time-contiguous) candles is taken. Some features are calculated, chosen and normalized. Geometric graphs are built upon them and, varying the spatial resolution, this sequence of graphs is constructed. The vertices colors stand for the close price of the corresponding candles, while the vertices sizes are proportional to their volumes. The data is from BTCUSDT symbol, from 10-Aug-2019 to 28-Dez-2019, with candle intervals of 8 hours. 

![btc-usdt-8h](https://github.com/izzorts/crypto-phgraphs/blob/master/output.gif)
