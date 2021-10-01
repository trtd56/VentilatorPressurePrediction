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
|[exp022_cos]||||
|[exp023_1dcnn]||||
|exp024_mask2||||


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


## n_out
fold-0
|method|OOF|OOF mask|LB|
|--|--|--|--|
|maskなし|0.204||0.253|

## ToDo
- outを別特徴として連結
- out==1は使われてないっぽい？
- 1dcnn, dilation, https://arxiv.org/pdf/1803.01271.pdf
  - https://qiita.com/top4hac/items/2a044b41c69f3c8802ef
