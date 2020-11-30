import numpy as np
import usingwave

def str_azi(num):
    """
    stringで3桁の数字をreturn
    :param num: 角度
    :return: 3桁の数字(string)
    """




def readhrtf():
    """
    HRTFの読み込み
    先に読み込んでおき，畳み込みで選択するようにする
    （今回は0度の水平方向のみで，5度間隔）
    :return:
    """


def convolve(data, hrtf, N, L):
    """
    畳み込み
    
    :param data: 音源データ
    :param hrtf: 畳み込むhrtf
    :param N: fftブロック長
    :param L: 切り出し区間
    :return: 畳み込み結果 1,前半部分　2,足し合わせる部分
    """
    spectrum = np.fft.fft(data, n=N)  # 第二引数：Nの長さに0詰めされる
    hrtf_fft = np.fft.fft(hrtf, n=N)
    add = spectrum * hrtf_fft
    result_data = np.real(np.fft.ifft(add, n=N))
    return result_data[:L], result_data[L:]


def generate(sound_data, N, L, hrtf_L, hrtf_R, azi):
    index = 0
    overlap = L - N - 2
    overlap_L = np.zeros(overlap)
    overlap_R = np.zeros(overlap)


    while(sound_data[index:].size > L):
        result_data = np.empty((0, 2), dtype=np.int16)  # 足し合わせに必要？？
        conv_L, add_L = convolve(sound_data[index:index + L], hrtf_L[azi], N, L)
        conv_R, add_R = convolve(sound_data[index:index + L], hrtf_R[azi], N, L)

        conv_L[:overlap] += overlap_L  # １つ前のoverlapを足し合わせ
        conv_R[:overlap] += overlap_R

        overlap_L = add_L  # overlap分を保存して次に回す
        overlap_R = add_R

        result_data = np.append(result_data, np.array([[conv_L, conv_R]], dtype=np.int16))

        index += L

    return result_data


def main():
    soundfilepath = "/Users/shugoto/3時のおやつ_short.wav"
    data_fs, data = usingwave.readwav(soundfilepath)






if __name__ == "__main__":
    main()