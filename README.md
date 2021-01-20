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

最適化パルスの概形図？

pulse8.py では最適化パルスの性能比較として8パルスの生成を行っている。
最適化パルス同様、I,Qパルスをfvx8, fvy8という名前で生成した。
各種パラメーターは論文を参照。
必要なライブラリは、numpy,copyで、必要な自作モジュールはdataである.

８ぱるすの図。変数がどの部分にあたるかをkeynoteを使って説明


Fidelityによる性能評価を行うために、Ideal.pyとFidelity.pyを作成した。
Ideal.pyは理想ハミルトニアンの時間発展を計算する関数を記載した。
Uideal関数の引数に理想ハミルトニアンと発展時間を渡すと, 入力した発展時間までのユニタリ発展行列を計算しリストとして返す。

Fidelity.pyにはFidelityを計算する関数を記載した。
スピン数n, 計算格子数Mとしたとき、(n*n)リストの最適化パルスによるユニタリ行列リストと(n*n*M)リストの理想ハミルトニアンのユニタリ行列リストを引数として渡すとFidelityを計算する。
どのような計算かは修論を参照。


性能評価としてmain_for_d-Fidelity.pyとerror_fidelity.pyを作成した。

main_for_d-Fidelity.pyはFidelityの結合定数依存性をシミュレーションするものである。
外部ライブラリは図の描画と結果の保存を行いたいため、matplotlib, numpyをインポートしている。
必要な自作モジュールは、data, Hamiltonian, OptPulse(pulse8), Ideal, Fidelityである。
main_for_d-Fidelityを実行すると、同ディレクトリ上に.npy形式で各結合定数のFidelityが保存される
(ex : d-fidelity_60us_opt_pulse_1211.npy)。
シミュレーションに使用した結合定数と保存した結果をそれぞれ横軸、縦軸としてプロットすると下図が得られる。

[d-Fidelity_30us_2repeat_0107.pdf](https://github.com/Kage819/Optimize_pulse/files/5839816/d-Fidelity_30us_2repeat_0107.pdf)


全体を関数にした方がよさげなやつ（引数：I,Q,sf,d_list,T,save_name）


error_fidelity.pyはFidelityのエラー依存性をシミュレーションするものである。
必須ライブラリはnumpyである。
自作モジュールは、data, Hamiltonian, OptPulse(pulse8), Ideal, Fidelity, errorが必要である。
error_fidelity.pyを実行すると、同ディレクトリ上に.npy形式で(len(e1),len(theta))のシミュレーション結果が複数保存される。
保存される数は、dlistの大きさと同じである。




性能評価で保存した.npy形式のシミュレーション結果はplot1127.pyでプロットした。
必須外部ライブラリはnumpy,matplotlib で、画像の保存のためにpylabをインポートした。
自作モジュールは, numpy, dataが必要である。
9行目から17行目はコメントアウトしているが、保存した.npy形式の結合定数依存性結果をnp.loadで読みだしており、それをプロットしている。
20行目からエラー依存性のプロットを行っている。
21, 29行目ではusing npyファイルから.npy形式のシミュレーション結果を読み込んでいる。
シミュレーション結果を手動でusing npyファイルに移動しているので、深い意味はない。
imshowでプロットすると下図のようなカラーマップが得られる。
[compare_error2D_heatmap_d25k_30us_2repeat_0108.pdf](https://github.com/Kage819/Optimize_pulse/files/5839811/compare_error2D_heatmap_d25k_30us_2repeat_0108.pdf)




