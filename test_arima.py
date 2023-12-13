import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Création d'une série chronologique fictive
np.random.seed(0)
time_series = pd.Series(np.random.randn(1000), index=pd.date_range('2023-01-01', periods=1000))
print(time_series)

# Entraînement du modèle ARIMA
model = ARIMA(time_series, order=(5,1,0))  # Ordre AR(p), Différenciation d, MA(q)
arima_result = model.fit()

# Prédiction sur les prochaines valeurs
forecast = arima_result.forecast(steps=50)  # Prédire les 50 prochaines valeurs

# Affichage des résultats
plt.figure(figsize=(12, 6))
plt.plot(time_series, label='Série Chronologique')
plt.plot(forecast, label='Prédiction')
plt.legend()
plt.show()
