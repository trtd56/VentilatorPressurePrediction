# 実験管理

推論MSD

|code|OOF|LB|memo|
|--|--|--|--|
|exp045_now_best||0.195|post processing & median|
|exp047_time_back|0.1752|0.193|fold-0のみ, 150 epoch|
|exp064_out_back|0.1873|0.212|fold-0のみ|
|[exp068_categorical]|0.1745|0.166|mean|
|[exp068_categorical]|0.1745|0.165|mean_pp|
|[exp068_categorical]|0.1745|0.168|median|
|[exp068_categorical]|0.1745|0.168|median_pp|
|exp069_no_back|0.1813|0.203|fold-0のみ|
|exp070_no_skip|0.1767|0.198|fold-0のみ|
|exp071_no_dropout|0.170|0.154|mean_pp|
|exp071_no_dropout|0.170|0.153|median_pp|
|[exp072_rolling]|0.1729|0.187|fold-0のみ, 特徴量は別で計算したほうが良さそう|
|[exp073_bce_smooth]||fold-0のみ,　あまり良くない|
|exp074_layer5|0.1704|0.157||
|[exp075_dropout0]||||
|[exp076_transformer]||||


## ToDo
- 特徴量増やしていく
  - 平均との差など(u_outに依存する部分があるので効かなそう)
- u_outを0/1に(0/1を入れ替えたほうがいいかも)
- RとCごとにLSTM
- backも使える？
- norm消す（回帰？）
## Share
- LIMEで特徴量: https://www.kaggle.com/takamichitoda/ventilator-lime/edit



[exp068_categorical]:https://www.kaggle.com/takamichitoda/ventilator-train-classification/notebook?scriptVersionId=76446772
[exp072_rolling]:https://github.com/trtd56/VentilatorPressurePrediction/blob/03a0f142a306d867fc6cb730c2804ba642e22806/src/ventilatorlstm.py
[exp073_bce_smooth]:https://github.com/trtd56/VentilatorPressurePrediction/blob/e0e9e2deed91d82bfe3c482209024de209487515/src/ventilatorlstm.py
[exp075_dropout0]:https://www.kaggle.com/takamichitoda/ventilator-train-classification?scriptVersionId=76597714
[exp076_transformer]:https://github.com/trtd56/VentilatorPressurePrediction/blob/4fb4c6e244c749bbe5ee35da2bb6a01fef5b5815/src/ventilatorlstm.py
