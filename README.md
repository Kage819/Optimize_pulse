# ロバストな平均ハミルトニアンの最適化
数値最適化により、任意の平均ハミルトニアンを生成することが可能。
ここでは、修論の内容のコードを記載しており、操作エラーを抑圧しながら望む平均ハミルトニアンを得るような数値最適化を示している。
コードは全てPython3を使用して書いた。

## ファイルについて
コードを実行する際に, 以下の外部ライブラリが必要である。
- numpy
- matplotlib
- copy
- scipy
- pylab
- scipy
- sympy


data.py, Hamiltonian.py はコードの基本情報について書かれている。
シミューションの際に、スピン数を変更したいときや、パルス照射時間を変更したいときは、data.pyのnとT1を書き換える。



## 数値最適化について
```
python optimization.py
```
optimization.py は最適化を実行し、制御ハミルトニアンのフーリエ次数を得るコードである(修論参照)。
最適化が終わると下図のような結果が得られる。
(x: array([]))は2nの要素を持っているが, 最初からn番目がI成分のフーリエ次数で、n番目から最後までがQ成分のフーリエ次数である。

![スクリーンショット 2021-01-19 17 32 31](https://user-images.githubusercontent.com/63832046/105008417-8e9c8900-5a7c-11eb-9bba-c05d16e140f8.png)

収束しない場合は、反復数が足りていないことが考えられるため、初期値をランダム生成から生成したフーリエ次数に変更して再度最適化を行うことを推奨する。
つまり、
```
initial_v = np.concatenate((vxopt, vyopt))
```
を
```
initial_v = np.array([...])
```
に変更する。
十分な反復回数でも収束しない場合はコスト関数に問題があると考えられる。



## 最適化パルスについて
```
python OptPulse.py
```
optimization.py　で生成されたフーリエ次数をndarray形式に変更し、OptPulse.pyに直書きする。
つまり、生成した2n要素を持つフーリエ次数リストを[...]で表すと、
```
pulse1 = np.array([...])
```
と書く。
OptPulse.py を実行すると、最適化パルスのI, Q波形がFvxmy, Fvymy　という名前で出力される。
```
plt.plot(tlist,Fvxmy)
plt.plot(tlist,Fvymy)
plt.swow()
```
を付け加えることで、下図のような滑らかな波形が生成されていることが確認できる。


![opt_pulse](https://user-images.githubusercontent.com/63832046/105141420-7724d500-5b3c-11eb-93b6-5f243446e3bf.png)



## 性能評価
Fidelityによる性能評価を行うために、Ideal.pyとFidelity.pyを作成した。
Ideal.pyは理想ハミルトニアンの時間発展を計算する関数を記載した。
```
def Uideal(Hamil,T):
    rList = []
    tlist2 = np.linspace(0,T,M) 
    for i in range(M):
        kata = -1j * Hamil * tlist2[i]
        rList.append(expm(kata))
    return rList
```
Hamilに理想ハミルトニアン、Tに発展時間を渡すと、T/M刻みでTまでのユニタリ行列を計算しリストとして返す。


Fidelity.pyにはFidelityを計算する関数を記載した。
```
def Fidelity_for_error(Uopt,Utarget):
    """
    Uopt^\dagger(T) と Uideal(t)の内積でFidelityを計算。ダガーは別のメソッドで計算
    Uopt : n*n　配列のダガー。最適化パルスに関する行列
    Utarget :M個の n*n 配列。理想ハミルトニアンに関する行列
    """
    aa = np.dot(dagger(Uopt),Utarget[len(tlist)-1])
    aa = np.abs(np.trace(aa)) / len(Uopt)
    return aa
```
スピン数をn、計算格子数をMとしたとき、Uoptには(n×n)のリスト、Utargetには(n×n×M)リストの理想ハミルトニアンにユニタリ行列リストを渡すとFideiltyを計算する。
Fidelityの計算は修論を参照。


### 結合定数依存性
main_for_d-Fidelity.pyはFidelityの結合定数依存性をシミュレーションするものである。
外部ライブラリは図の描画と結果の保存を行いたいため、matplotlib, numpyをインポートしている。
必要な自作モジュールは、data, Hamiltonian, OptPulse(pulse8), Ideal, Fidelityである。
main_for_d-Fidelityを実行すると、同ディレクトリ上に.npy形式で各結合定数のFidelityが保存される
(ex : d-fidelity_60us_opt_pulse_1211.npy)。
シミュレーションに使用した結合定数と保存した結果をそれぞれ横軸、縦軸としてプロットすると下図が得られる。

[d-Fidelity_30us_2repeat_0107.pdf](https://github.com/Kage819/Optimize_pulse/files/5839816/d-Fidelity_30us_2repeat_0107.pdf)


全体を関数にした方がよさげなやつ（引数：I,Q,sf,d_list,T,save_name）

### エラー依存性
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


## パルスの比較対象
```
pulse8.py
```
修論では、従来から存在する8パルスと生成した数値最適化パルスの性能を比較している。 
pulse8.py により、最適化パルス同様、I,Qパルスをfvx8, fvy8という名前で生成した。
各種パラメーターは論文を参照。

８ぱるすの図。変数がどの部分にあたるかをkeynoteを使って説明
