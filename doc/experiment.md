# 実験管理

|code|OOF|LB|memo|
|--|--|--|--|
|[exp000_starter]|5.422|9.538||
|[exp001_u_in_time]|5.605|9.533||
|[exp002_l1_loss]|5.136|10.924||
|[exp003_emb_layer]|5.004|10.677||
|[exp004_lr]|0.616|0.992||
|[exp005_cos]|0.623|1.040||
|[exp006_bilstm]|0.568|0.884||
|[exp007_init]|0.623|0.723||
|[exp008_head]|0.425|0.626||
|[exp009_mask]|||wandb削除しちゃってエラー|
|[exp010_transformer]|||微妙なのでf0で止めた|
|||||
|[exp011_def]|||ここからcolab|
|exp011_lstm2|0.353|0.484||
|exp011_lstm3|0.355|0.464||
|exp012_lstm3_fix|||fold-0 LB: 0.532→0.537|
|[exp013_1dcnn_lstm]|||fold-0のLB=0.740|
|[exp013_cnn_head]||0.681||
|[exp014_transformer_head]|||fold-0 LB: 0.537|
|exp015_skip_conn|0.364|0.493||
|exp016_lstm4|0.334|0.435||
|exp017_h256|0.273|0.323||
|exp018_h512|||fold-0で微妙|
|exp019_transformer_lstm|||やっぱ良くない|
|exp020_liner_sche_f0|0.218|0.247||
|exp020_add_feat|||normすれば良さそう|
|[exp022_cos]|0.212|0.244||
|[exp023_1dcnn]|0.387|0.559||
|exp024_mask2|||以下参照|
|exp025_con_out||||
|exp026_con_emb||||
|exp027_dilation|||メモリオーバー|
|exp028_1dcnn|||あんまり変わらない|
|[exp029_area_fix]||||
|exp030_transformer|||train lossが暴発する|
|exp031_no_dropout|||fold-0=0.232|
|exp032_lag4|||fold-0=0.224|
|exp033_back|||fold-0=0.218|
|exp034_loss_w|||fold-0=0.260, mask lossは良かったが・・・|
|exp035_loss_w_inv|||良くないので途中で打ち切り|
|exp036_norm|||良くないので途中で打ち切り|
|[exp037_skip_conn]|||fold-0=0.216|
|exp038_lstm6|||良くないので途中で打ち切り|
|exp039_lstm6_222|||良くないので途中で打ち切り|
|[exp040_lag6]|||良くないので途中で打ち切り|
|exp041_log_w|||良くないので途中で打ち切り|
|exp045_now_best||0.197||
|exp045_now_best||0.196|ensemble median|
|exp045_now_best||0.195|[post processing](https://www.kaggle.com/snnclsr/a-dummy-approach-to-improve-your-score-postprocess)|
|exp045_mcnn|||良くないので途中で打ち切り|
|[exp046_inc_epoch]||||
|exp047_time_back|||fold-0=0.193|

[exp000_starter]:https://www.kaggle.com/takamichitoda/ventilator-lstm-starter?scriptVersionId=75438952
[exp001_u_in_time]:https://www.kaggle.com/takamichitoda/ventilator-lstm-starter?scriptVersionId=75511345
[exp002_l1_loss]:https://www.kaggle.com/takamichitoda/ventilator-lstm-starter?scriptVersionId=75523088
[exp003_emb_layer]:https://www.kaggle.com/takamichitoda/ventilator-lstm-starter?scriptVersionId=75531233
[exp004_lr]:https://www.kaggle.com/takamichitoda/ventilator-lstm-starter?scriptVersionId=75576040
[exp005_cos]:https://www.kaggle.com/takamichitoda/ventilator-lstm-starter?scriptVersionId=75581766
[exp006_bilstm]:https://www.kaggle.com/takamichitoda/ventilator-lstm-starter?scriptVersionId=75668583
[exp007_init]:https://www.kaggle.com/takamichitoda/ventilator-lstm-starter?scriptVersionId=75668583
[exp008_head]:https://www.kaggle.com/takamichitoda/ventilator-lstm-starter/script?scriptVersionId=75744079
[exp009_mask]:https://www.kaggle.com/takamichitoda/ventilator-lstm-starter?scriptVersionId=75759098
[exp010_transformer]:https://www.kaggle.com/takamichitoda/ventilator-transformer-starter?scriptVersionId=75829880
[exp011_def]:https://github.com/trtd56/VentilatorPressurePrediction/blob/016f42ac7a5890f18407d6a42a04cd66b8555e49/src/ventilatorlstm.py
[exp013_1dcnn_lstm]:https://www.kaggle.com/takamichitoda/ventilator-1dcnn-lstm?scriptVersionId=75942298
[exp013_cnn_head]:https://www.kaggle.com/takamichitoda/ventilator-1dcnn-lstm?scriptVersionId=75945718
[exp014_transformer_head]:https://github.com/trtd56/VentilatorPressurePrediction/blob/b91c64ededd01c53453c5fa1b32321019f624496/src/ventilatorlstm.py
[exp022_cos]:https://github.com/trtd56/VentilatorPressurePrediction/blob/565e0de4231d86b7af88a349e3ec03c1abc379c4/src/ventilatorlstm.py
[exp023_1dcnn]:https://www.kaggle.com/takamichitoda/ventilator-1dcnn-lstm?scriptVersionId=76092602
[exp029_area_fix]:https://github.com/trtd56/VentilatorPressurePrediction/blob/0ad30e01f53bf0953537bded82ce2c47737efded/src/ventilatorlstm.py
[exp037_skip_conn]:https://github.com/trtd56/VentilatorPressurePrediction/blob/5c73c924d776b79e6be5c5af574adf9ea4919ea4/src/ventilatorlstm.py
[exp040_lag6]:https://github.com/trtd56/VentilatorPressurePrediction/blob/b3093318367dbc89484cdf157484b2b5876ab87c/src/ventilatorlstm.py
[exp046_inc_epoch]:https://github.com/trtd56/VentilatorPressurePrediction/tree/30d3d15444573bc502a4bc1790fe26a31754a751

## n_out
fold-0
|method|OOF|OOF mask|LB|
|--|--|--|--|
|maskなし|0.204|0.253|0.253|
|maskあり|0.215|0.255|0.257|
|concat|0.211|0.267|0.269|

## ToDo
- 平均との差など
- u_intime_back
- u_in_cumsum window
