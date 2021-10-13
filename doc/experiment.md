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

## ToDo
- pseudo labeling
- Stacking
- RとCを分ける
- mcnn_skip
- 3rd stage
- ordinal regressionやらcustom lossのShare
- LIME

[exp117_cnn_2]:https://github.com/trtd56/VentilatorPressurePrediction/blob/a3453b6ab14528efa19cf7e7e77558348333a384/src/ventilatorlstm_2nd.py
[exp120_mcnn]:https://github.com/trtd56/VentilatorPressurePrediction/blob/e21fcc9d85eb3c07e84b14cfa1a15d8c14792176/src/ventilatorlstm_2nd.py
