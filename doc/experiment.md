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
|[exp075_dropout0]|0.1708|0.155|median_pp|
|[exp075_dropout0]|0.1708||mean_pp|
|[exp076_transformer]||||
|[exp077_divide_rc]|0.2724||fold-0のみ, 良くない|
|[exp077_divide_r]|0.2034||fold-0のみ, 良くない|
|exp078_transformer|||良くない|
|exp079_smooth|0.1694|||
|[exp080_conti_rc]|0.1714|||
|exp081_smooth02|0.1676|0.153|median_pp|
|exp081_smooth02|0.1676|0.154|mean_pp|
|exp082_smooth04|0.1674|0.154||
|[exp083_smooth2_4]|0.1653|0.153|mean_pp|
|[exp083_smooth2_4]|0.1653|0.152|median_pp|
|[exp084_mcnn]||||
|exp085_smooth1_2_4|0.1647|0.152|mean_pp|
|exp085_smooth1_2_4|0.1647|0.151|median_pp|
|exp085_smooth1_2_4|0.1647|0.151|median_pp|
|[exp086_reg_diff]|0.1986|0.241|diffなしfold-0|
|[exp086_reg_diff]|0.188|0.223|diffありfold-0|
|[exp086_reg_diff]|0.1838||diff2fold-0|
|[exp086_reg_diff]|0.1808|0.188|diff3|
|exp086_mask|0.1653|0.150||
|exp087_smooth_lag4|0.1648|0.150||
|exp088_h1024|0.1647|0.175|fold-0のみ, fold-1は悪かった＆時間かかりすぎ|
|exp089_dropout_train|0.1693|0.182|fold-0のみ|
|exp090_skgfold|0.1683|0.181|fold-0のみ|
|exp091_lstm_head|||全然だめ|
|exp091_mask01|||悪くないけど劇的改善ではなかった|
|exp092_roll_re|||良くないので打ち切り|
|[exp093_add_back]|0.1677||fold-0のみ|
|exp094_cont_v2|0.1694||fold-0のみ|
|exp095_ewm|0.1669||fold-0のみ|
|exp096_reload_reg|||fold-0のみ|
|exp097_unfreeze10||||
|exp098_transformer|0.1627|0.151|mean_pp|
|exp098_transformer|0.1627|0.150|median_pp|
|exp099_head2|||暴発|
|exp100_layer2|||暴発|
|exp101_diff|||良さげ|
|exp102_mask|||diff onlyの方が良さそう|
|exp103_skip|||diff onlyの方が良さそう|
|exp104_use_cls|||暴発|
|exp105_diff8|||ちょい微妙？|
|exp106_diff4||||
|exp107_train_dropout||||
|exp108_bs1024||||
|exp109_unit1024||||
|exp110_mlp2||||
|exp111_diff3|||dropout onにしちゃってた|

## ToDo
- CNN
- pseudo labeling

[exp068_categorical]:https://www.kaggle.com/takamichitoda/ventilator-train-classification/notebook?scriptVersionId=76446772
[exp072_rolling]:https://github.com/trtd56/VentilatorPressurePrediction/blob/03a0f142a306d867fc6cb730c2804ba642e22806/src/ventilatorlstm.py
[exp073_bce_smooth]:https://github.com/trtd56/VentilatorPressurePrediction/blob/e0e9e2deed91d82bfe3c482209024de209487515/src/ventilatorlstm.py
[exp075_dropout0]:https://www.kaggle.com/takamichitoda/ventilator-train-classification?scriptVersionId=76597714
[exp076_transformer]:https://github.com/trtd56/VentilatorPressurePrediction/blob/4fb4c6e244c749bbe5ee35da2bb6a01fef5b5815/src/ventilatorlstm.py
[exp077_divide_rc]:https://www.kaggle.com/takamichitoda/ventilator-train-divide-r-c/notebook?scriptVersionId=76613957
[exp077_divide_r]:https://www.kaggle.com/takamichitoda/ventilator-train-divide-r-c?scriptVersionId=76621692
[exp080_conti_rc]:https://www.kaggle.com/takamichitoda/ventilator-train-classification?scriptVersionId=76624771
[exp083_smooth2_4]:https://github.com/trtd56/VentilatorPressurePrediction/blob/2e34d395975d6ad4ef91b77f4d443fd5f12e691a/src/ventilatorlstm.py
[exp084_mcnn]:https://www.kaggle.com/takamichitoda/ventilator-train-mcnn/edit
[exp086_reg_diff]:https://www.kaggle.com/takamichitoda/ventilator-train-classification-regdiff
[exp093_add_back]:https://github.com/trtd56/VentilatorPressurePrediction/blob/be743745127b72164607b091994d922cf405859a/src/ventilatorlstm.py
