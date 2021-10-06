# 実験管理

推論MSD

|code|OOF|LB|memo|
|--|--|--|--|
|exp045_now_best||0.195|post processing & median|
|exp047_time_back|0.1752|0.193|fold-0のみ, 150 epoch|
|exp064_out_back|0.1873|0.212|fold-0のみ|
|exp069_no_back|0.1813|0.203|fold-0のみ|
|exp070_no_skip|0.1767|0.198|fold-0のみ|
|exp071_no_dropout|||fold-0のみ|
|[exp072_rolling]||||
|[exp073_bce_smooth]|||


## ToDo
- 特徴量増やしていく
  - 平均との差など(u_outに依存する部分があるので効かなそう)


## Share
- LIMEで特徴量: https://www.kaggle.com/takamichitoda/ventilator-lime/edit

[exp072_rolling]:https://github.com/trtd56/VentilatorPressurePrediction/blob/03a0f142a306d867fc6cb730c2804ba642e22806/src/ventilatorlstm.py
[exp073_bce_smooth]:xxx

