# Optimize_pulse
Main.py, main_for_d-Fidelity.py, error_fidelity.pyはシミュレーションを行い、その結果を.npyに保存している。
plot1127.pyでnpyファイルを読み込み画像化している。

main_for_d-Fidelity.pyを実行することによりd-Fidelity_60us_1201.pngのような結果を得ることができる。
また、error_fidelity.pyを実行することによりcompare_error2D_heatmap_60us_1211.pngのような結果を得ることができる。



#シミュレーションの基本情報を入れるファイル
data.py
#理想ハミルトニアンや初期ハミルトニアンを計算するための基本的なハミルトニアンが格納
Hamiltonian.py
#生成したパルスに各エラーを付与するためのメソッドがあるファイル
error.py
#Fidelityを計算するメソッドが書かれているファイル
Fidelity.py
#理想ハミルトニアンのユニタリ発展を計算するためのファイル
Ideal.py

#最適化パルスを生成するコード.最適化はまた別のコード
OptPulse.py
#8パルスを生成するコード
pulse8.py
