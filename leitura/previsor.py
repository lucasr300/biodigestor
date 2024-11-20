import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout


class PrevisorTemperatura:
    def __init__(self, temperaturas, tamanho_janela=30):
        self.temperaturas = temperaturas
        self.tamanho_janela = tamanho_janela
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.modelo = self.construir_modelo()

    def preparar_dados(self):
        dados = pd.DataFrame(self.temperaturas, columns=['TemperaturaAtual'])
        dados_normalizados = self.scaler.fit_transform(dados)
        X, y = self.criar_conjunto_dados(dados_normalizados)
        X = X.reshape(X.shape[0], X.shape[1], 1)
        tamanho_treino = int(len(X) * 0.8)
        return X[:tamanho_treino], X[tamanho_treino:], y[:tamanho_treino], y[tamanho_treino:]

    def criar_conjunto_dados(self, dados):
        X, Y = [], []
        for i in range(len(dados) - self.tamanho_janela - 1):
            a = dados[i:(i + self.tamanho_janela), 0]
            X.append(a)
            Y.append(dados[i + self.tamanho_janela, 0])
        return np.array(X), np.array(Y)

    def construir_modelo(self):
        modelo = Sequential()
        modelo.add(LSTM(25, return_sequences=True, input_shape=(self.tamanho_janela, 1)))
        modelo.add(Dropout(0.2))
        modelo.add(LSTM(25, return_sequences=False))
        modelo.add(Dropout(0.2))
        modelo.add(Dense(1))
        modelo.compile(optimizer='adam', loss='mean_squared_error')
        return modelo

    def treinar(self, epocas=10, tamanho_batch=1):
        X_treino, X_teste, y_treino, y_teste = self.preparar_dados()
        self.modelo.fit(X_treino, y_treino, epochs=epocas, batch_size=tamanho_batch, verbose=2)
        return X_teste, y_teste

    def prever(self, dados_ultimo):
        dados_ultimo = dados_ultimo.reshape(1, self.tamanho_janela, 1)
        proxima_temp_normalizada = self.modelo.predict(dados_ultimo)
        return self.scaler.inverse_transform(proxima_temp_normalizada)[0][0]

def prever_proxima_temperatura():
    def carregar_dados_csv(caminho_arquivo):
        df = pd.read_csv(caminho_arquivo)
        return df['TemperaturaAtual'].values

    try:
        caminho_arquivo = 'leituras.csv'
        temperaturas = carregar_dados_csv(caminho_arquivo)
        previsor = PrevisorTemperatura(temperaturas)
        X_teste, y_teste = previsor.treinar()

        dados_ultimo = np.array(temperaturas[-30:]).reshape(-1, 1)
        proxima_temperatura = previsor.prever(dados_ultimo)
        print("Temperatura prevista", proxima_temperatura)
        return float(proxima_temperatura)
    except:
        print("Erro ao fazer previsao")
        return None
