from numpy import where
import matplotlib.pyplot as plt
from Strategy_BB_KF.optimization import optimize
from Strategy_BB_KF.kalman_filter import KF

def bollinger_kf(df, column='close', sigma_meas=1e-3, window_std=21, factor=2, contradir=True, plot=False, signal=False):

    sigma_model = optimize(df_train=df, window_cma=window_std, sigma_meas=sigma_meas, delta=15, order=2)

    df['KF'] = KF(zs=df[column], sigma_meas=sigma_meas, sigma_model=sigma_model)
    df['STD'] = df[column].rolling(window=window_std).std()
    df['BOLLINGER_UP'] = df['KF'] + factor * df['STD']
    df['BOLLINGER_DOWN'] = df['KF'] - factor * df['STD']

    df['action'] = where(df[column] > df['BOLLINGER_UP'], -1, 0)
    df['action'] = where(df[column] < df['BOLLINGER_DOWN'], 1, df['action'])

    if not contradir:
        df['action'] = -1 * df['action']

    if plot:
        plt.plot(df[column], c='grey', label='Market')
        plt.plot(df['KF'], c='blue', label='Kalman filter')
        plt.plot(df['BOLLINGER_UP'], c='red', label='Bollinger up')
        plt.plot(df['BOLLINGER_DOWN'], c='red', label='Bollinger down')
        if signal:
            plt.plot(df.loc[df['action'] == 1, 'close'], '^g')
            plt.plot(df.loc[df['action'] == -1, 'close'], 'vr')
        plt.title('Bollinger Bands') ; plt.show()

    return df['action'][len(df) - 1]