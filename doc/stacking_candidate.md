
|code|OOF|LB|memo|now use|
|--|--|--|--|--|
|[exp023_1dcnn]|0.387|0.559|||
|exp045_now_best|0.1885|0.195|post processing & median|N|
|[exp068_categorical]|0.1745|0.165|mean_pp||
|exp071_no_dropout|0.170|0.153|median_pp|Y|
|exp074_layer5|0.1704|0.157||Y|
|[exp075_dropout0]|0.1708|0.155|median_pp|(Y)|
|exp079_smooth|0.1694|||Y|
|[exp080_conti_rc]|0.1714|||(Y)|
|exp081_smooth02|0.1676|0.153|median_pp|Y|
|exp082_smooth04|0.1674|0.154||Y|
|[exp083_smooth2_4]|0.1653|0.152|median_pp|Y|
|exp085_smooth1_2_4|0.1647|0.151|median_pp|Y|
|[exp086_reg_diff]|0.1808|0.188|diff3|N|
|exp086_mask|0.1653|0.150||Y|
|exp087_smooth_lag4|0.1648|0.150||Y|
|exp098_transformer|0.1627|0.150|median_pp|Y|
|exp110_mlp2|0.1673|||(Y)|
|exp116_cnn|0.1622|0.150||Y|
|exp125_dec_epoch|0.1669|||N|
|exp126_pseudo|0.1598|||N|
|exp127_inc_epoch|0.1566|0.149||N|
|[exp129_fintune_reg]|0.1765|0.165||(Y)|
|[exp133_all_features]|0.1691|||(Y)|

[exp023_1dcnn]:https://www.kaggle.com/takamichitoda/ventilator-1dcnn-lstm?scriptVersionId=76092602
[exp068_categorical]:https://www.kaggle.com/takamichitoda/ventilator-train-classification/notebook?scriptVersionId=76446772
[exp075_dropout0]:https://www.kaggle.com/takamichitoda/ventilator-train-classification?scriptVersionId=76597714
[exp080_conti_rc]:https://www.kaggle.com/takamichitoda/ventilator-train-classification?scriptVersionId=76624771
[exp083_smooth2_4]:https://github.com/trtd56/VentilatorPressurePrediction/blob/2e34d395975d6ad4ef91b77f4d443fd5f12e691a/src/ventilatorlstm.py
[exp086_reg_diff]:https://www.kaggle.com/takamichitoda/ventilator-train-classification-regdiff
[exp129_fintune_reg]:https://www.kaggle.com/takamichitoda/ventilator-fine-tune-regression?scriptVersionId=77059448
[exp133_all_features]:https://github.com/trtd56/VentilatorPressurePrediction/blob/1243ebe0eaf94bc5b6d7df5673befbbd520aa2a6/src/ventilatorlstm_1st.py
