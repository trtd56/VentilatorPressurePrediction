# 実験管理

|code|OOF|LB|memo|
|--|--|--|--|
|exp098_transformer|0.1627|0.150|median_pp|
|exp116_cnn|0.1622|0.150||
|[exp117_cnn_2]||||
|exp118_lstm|||あんまよくない|
|exp119_layer_lr_diff|||暴発|
|[exp120_mcnn]|0.1627||fold-0のみ|
|exp121_cnn135||||
|[exp122_skip]||||
|exp123_3rd||||
|exp124_inc_epoch||||
|exp125_dec_epoch||||
|||||
|stacking_01|0.1556|0.146|['exp086_mask', 'exp087_smooth_lag4', 'exp098_transformer', 'exp116_cnn']|
|stacking_01|0.1556|0.148|mean_pp|
|stacking_02|0.1561|0.147|no mask|

## ToDo
- pseudo labeling
- RとCを分ける
- ordinal regressionやらcustom lossのShare
- LIME

[exp117_cnn_2]:https://github.com/trtd56/VentilatorPressurePrediction/blob/a3453b6ab14528efa19cf7e7e77558348333a384/src/ventilatorlstm_2nd.py
[exp120_mcnn]:https://github.com/trtd56/VentilatorPressurePrediction/blob/e21fcc9d85eb3c07e84b14cfa1a15d8c14792176/src/ventilatorlstm_2nd.py
[exp122_skip]:https://github.com/trtd56/VentilatorPressurePrediction/blob/85af1fdcdd7ffa7ec91f1abad88dbe7c582220c5/src/ventilatorlstm_2nd.py

