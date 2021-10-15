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
|exp125_dec_epoch|0.1669|||
|exp126_pseudo|0.1598|||
|exp127_inc_epoch|0.1566|0.149||
|[exp128_u_out_0]|||あまり改善せず|
|[exp129_fintune_reg]|0.1765|0.165||
|exp130_target_norm||||
|[exp131_tanh]||||
|[exp132_diff]|0.1619|||
|||||
|[exp133_all_features]|0.1691|||
|exp134_drop_rolling|0.1679|||
|exp135_drop_emw||||
|||||
|stacking_01|0.1556|0.146|['exp086_mask', 'exp087_smooth_lag4', 'exp098_transformer', 'exp116_cnn']|
|stacking_01|0.1556|0.148|mean_pp|
|stacking_02|0.1561|0.147|no mask|
|stacking_03|0.1560|0.147|RC分ける|
|stacking_04|0.1555|0.146|["exp086_mask", "exp098_transformer", "exp116_cnn"]|
|[stacking_05]|0.1562||["exp086_mask", "exp098_transformer", "exp116_cnn", "exp126_pseudo"]|
|stacking_06|0.1482|0.144|ここまで全部|
|[stacking_07]|0.1478|0.145|pseudoもいれちゃう|
|stacking_08|0.1478|0.144||
|stacking_09|0.1475|||

## ToDo
- LIME
- target encoding

[exp117_cnn_2]:https://github.com/trtd56/VentilatorPressurePrediction/blob/a3453b6ab14528efa19cf7e7e77558348333a384/src/ventilatorlstm_2nd.py
[exp120_mcnn]:https://github.com/trtd56/VentilatorPressurePrediction/blob/e21fcc9d85eb3c07e84b14cfa1a15d8c14792176/src/ventilatorlstm_2nd.py
[exp122_skip]:https://github.com/trtd56/VentilatorPressurePrediction/blob/85af1fdcdd7ffa7ec91f1abad88dbe7c582220c5/src/ventilatorlstm_2nd.py
[exp129_fintune_reg]:https://www.kaggle.com/takamichitoda/ventilator-fine-tune-regression?scriptVersionId=77059448
[exp128_u_out_0]:https://github.com/trtd56/VentilatorPressurePrediction/blob/0ee49c9b6bfad980427280d620456ca29a22199d/src/ventilatorlstm_2nd.py
[exp131_tanh]:https://github.com/trtd56/VentilatorPressurePrediction/blob/5f42a550ccca23f274e8c4754d49a55a07a3247d/src/ventilatorlstm_2nd.py
[exp132_diff]:https://github.com/trtd56/VentilatorPressurePrediction/blob/211c29bbefcf6f68b0b54c4b0d7b26b52e103341/src/ventilatorlstm_2nd.py

[exp133_all_features]:https://github.com/trtd56/VentilatorPressurePrediction/blob/1243ebe0eaf94bc5b6d7df5673befbbd520aa2a6/src/ventilatorlstm_1st.py

[stacking_05]:https://github.com/trtd56/VentilatorPressurePrediction/blob/0b819b0968eaa91dace97a1b95407f99e3159e15/src/ventilatorlstm_stacking.py
[stacking_07]:https://github.com/trtd56/VentilatorPressurePrediction/blob/5c8f2317926928c3c21971ef02b97e0f27d31358/src/ventilatorlstm_stacking.py
