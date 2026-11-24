# 📈 Quant Finance: PETR4 Return Regression & Backtest

> **Projeto 1 — Trilha de Pesquisa Quantitativa (Quant Research & Algorithmic Trading)**

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E?logo=scikit-learn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Interactive%20App-FF4B4B?logo=streamlit&logoColor=white)

## 🎯 Objetivo do Projeto

Este repositório marca o primeiro estudo prático da minha trilha de transição para **Finanças Quantitativas**. O objetivo é construir um pipeline ponta a ponta em Python para investigar o comportamento dos retornos diários das ações da Petrobras (`PETR4.SA`) utilizando **Regressão Linear** e **Backtesting**.

Mais do que buscar acurácia estatística pura em séries financeiras ruidosas, o foco deste estudo é aplicar rigor metodológico: evitar vazamento de dados futuros (*look-ahead bias*), estruturar pipelines limpos de engenharia de dados e avaliar se um sinal preditivo sobrevive aos custos operacionais reais no mercado.

---

## 🏗️ Arquitetura do Projeto

O código foi estruturado seguindo a **Arquitetura Medalhão (Bronze, Silver e Gold)** para separar responsabilidades e facilitar a reprodutibilidade:

```text
quant-finance-petr4-regression/
├── app/
│   └── streamlit_app.py          # Interface web interativa para simulação e análise
├── data/
│   ├── 01_bronze/                # Dados históricos brutos extraídos via yfinance
│   ├── 02_silver/                # Dados tratados, retornos diários e features (lags)
│   └── 03_gold/                  # Previsões out-of-sample e resultados do backtest
├── notebooks/
│   └── 01_exploracao_petr4.ipynb # Análise exploratória e testes de autocorrelação
├── src/
│   ├── ingestion.py              # Coleta automatizada de cotações (PETR4.SA)
│   ├── features.py               # Engenharia de atributos temporais sem data leakage
│   ├── model.py                  # Treinamento da Regressão Linear com corte cronológico
│   └── backtest.py               # Motor de simulação financeira vs. Buy & Hold
├── main.py                       # Orquestrador do pipeline completo
├── requirements.txt              # Dependências do projeto
└── README.md
