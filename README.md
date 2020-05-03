# 地域リーグデータの機械学習CA解析

選手の2019年の出場数とゴール数により、Sklearnを使い分析すること。calc_ca.pyを実行してください。

入力データでは「クラブ勝点,試合数,リーグ知名度,試合出場数,得点」というベクターで、出力データはCA。回帰学習です。

パイプラインを使ったが、使ったモデルはMLP回帰のみなのであまり意味がありません。ただし、GridSearchCVを使い、パラメータのチューニングをやりました。

いまのデータによると以下のパラメータが一番だそうです：
```
Best parameters: {'mlpregressor__activation': 'tanh', 'mlpregressor__alpha': 1, 'mlpregressor__hidden_layer_sizes': (250, 100), 'mlpregressor__max_iter': 10000, 'mlpregressor__solver': 'adam'}     
Best cross-validation score: 0.932
Test set score: 0.91
```

goalnote_readerはGoalnoteフォーマットの地域リーグレポートを読み込み、選手の試合出場数と得点をまとめることです。
kyushuu_readerでは九州・東北リーグフォーマットの地域リーグレポート、ただしこちらはローカルファイルのみ可。