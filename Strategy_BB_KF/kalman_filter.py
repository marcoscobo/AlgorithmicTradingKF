from numpy import dot, eye, zeros, arange, array, outer
from scipy.linalg import inv
from math import factorial


class KalmanFilter():

	def predict(self):
		self.x = dot(self.F, self.x)
		self.P = dot(self.F,self.P).dot(self.F.T) + self.Q

	def update(self, Z, n):
		y = Z - dot(self.H, self.x)
		S = dot(self.H, self.P).dot(self.H.T) + self.R
		K = dot(self.P, self.H.T).dot(inv(S))
		self.x = self.x + dot(K, y)
		I_KH = eye(n) - dot (K, self.H)
		self.P = dot(I_KH,self.P)


def KF(zs, sigma_meas, sigma_model, dt=0.1, n=2, Id=False):

	F = eye(n)
	for i in range(1,n):
		r = arange(n-i)
		F[r, r+i] = dt ** i / factorial(i)

	H = zeros((1,n)) ; H[0,0] = 1

	if Id:
		Q = eye(n) * sigma_model ** 2
	else:
		w_k = []
		for n_i in range(n):
			w_k.append(dt ** (n - n_i) / factorial(n - n_i))
		Q = outer(array(w_k), array(w_k).T) * sigma_model ** 2

	R = sigma_meas ** 2

	x_ini = zeros((n, 1)) ; x_ini[0, 0] = zs[0]

	P = eye(n) * 0.001

	Kalman_filter = KalmanFilter()
	Kalman_filter.x = x_ini
	Kalman_filter.P = P
	Kalman_filter.Q = Q
	Kalman_filter.R = R
	Kalman_filter.F = F
	Kalman_filter.H = H

	us = []
	for t in range(len(zs)):
		Kalman_filter.predict()
		Kalman_filter.update(zs[t],n)
		us.append(Kalman_filter.x[0,0])
		
	return us