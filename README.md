# Optimize_pulse
Main.py, main_for_d-Fidelity.py, error_fidelity.pyはシミュレーションを行い、その結果を.npyに保存している。
plot1127.pyでnpyファイルを読み込み画像化している。

main_for_d-Fidelity.pyを実行することによりd-Fidelity_60us_1201.pngのような結果を得ることができる。
また、error_fidelity.pyを実行することによりcompare_error2D_heatmap_60us_1211.pngのような結果を得ることができる。


data.py, Hamiltonian.pyはシミュレーション・最適化に必要なファイルである。
data.pyにはnumpyが必要である。
Hamiltonian.pyはnumpy, sympyが必要で, data.pyも要する。


optimization.py は最適化を実行し、制御ハミルトニアンのフーリエ次数を得るコードである。
必要な外部ライブラリは、numpy, scipy, copyで、必要な自作モジュールはdataのみである。
最適化が終わると下図のような結果が得られる。
(x: array([]))は2nの要素を持っているが, 最初からn番目がI成分のフーリエ次数で、n番目から最後までがQ成分のフーリエ次数である。
![スクリーンショット 2021-01-19 17 32 31](https://user-images.githubusercontent.com/63832046/105008417-8e9c8900-5a7c-11eb-9bba-c05d16e140f8.png)


optimization.py　で生成されたフーリエ次数をndarray形式に変更し、OptPulse.pyに直書きする。
フーリエ次数が書かれた状態で OptPulse.py を実行すると、最適化パルスのI, Q波形がFvxmy, Fvymy　という名前で出力される。
必要な外部ライブラリは、numpy, copy, scipyで、必要な自作モジュールはdata, Hamiltonianである。

pulse8.py では最適化パルスの性能比較として8パルスの生成を行っている。
