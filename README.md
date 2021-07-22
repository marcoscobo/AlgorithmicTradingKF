# Algorithmic Trading Bot based on Kalman Filter
Algorithmic trading bot based on the Kalman filter, which studies market conditions, trends and indicators to make pre-programmed decisions, to trade mainly in the FOREX market. The algorithmic trading bot obtains the optimal parameters for the Kalman filter by solving an optimization problem, comparing it to a centred moving average, and then returns a market signal based on the Bollinger Bands technical indicator.

## Libraries used:

In this bot we will use Python (version 3.9) and different libraries, among which we can highlight:

- NumPy
- Pandas
- SciPy
- Datetime
- Schedule
- Matplotlib
- MetaTrader5

We recommend not to use a Python version higher than 3.9, as it has not been tested in this project. For the installation of all the libraries used, we recommend installing the requirements.txt file by typing the following command into the shell:

```
pip install -r requirements.txt
```
