from scipy.optimize import minimize_scalar
from scipy.linalg import norm
from Strategy_BB_KF.kalman_filter import KF
from numpy import diff


def obj_fun(sigma_model, sigma_meas, window_cma, df_train, delta, order):

    cma = df_train['close'].rolling(window=window_cma, center=True).mean()
    kf = KF(zs=df_train['close'], sigma_meas=sigma_meas, sigma_model=sigma_model)
    diff1 = (cma - kf).fillna(0)
    diff2 = diff(kf)

    return norm(diff1, ord=order) + delta * norm(diff2, ord=order)


def optimize(df_train, window_cma, sigma_meas, delta=0, order=2):

    sigma_model = minimize_scalar(obj_fun, args=(sigma_meas, window_cma, df_train, delta, order), bounds=(1e-5, sigma_meas), method='bounded').x

    return sigma_model