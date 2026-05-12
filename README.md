# Automação de Biodigestor Anaeróbio com Inteligência Artificial

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![C++](https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white)
![IoT](https://img.shields.io/badge/IoT-FF6F00?style=for-the-badge&logo=internet-of-things&logoColor=white)
![Artificial Intelligence](https://img.shields.io/badge/IA-FF00FF?style=for-the-badge&logo=brain&logoColor=white)
![Dissertação](https://img.shields.io/badge/Dissertação-Mestrado-blue?style=for-the-badge)

**Lucas R. Martins**  
Esse repositorio contém código produzido durante a escrita da minha dissertação de mestrado em andamento.

### Sobre o Projeto

Este repositório centraliza todo o desenvolvimento da minha dissertação de mestrado, que tem como objetivo principal a **automatização de um biodigestor anaeróbio de laboratório** utilizando sensores em tempo real e técnicas de Inteligência Artificial.

O sistema é capaz de monitorar continuamente diversas variáveis críticas do processo de biodigestão, tais como temperatura, pH, pressão, nível, umidade e composição gasosa. Através de modelos de IA (redes neurais, LSTM, etc.), o biodigestor realiza ajustes automáticos nos atuadores (aquecimento, agitação, válvulas, etc.) com o objetivo de maximizar a produção de biogás e a qualidade do biofertilizante gerado.

O projeto une hardware IoT, firmware embarcado em C++ e uma camada robusta de software em Python, representando uma solução tecnológica aplicada ao agronegócio e à geração de energia renovável.

### Objetivos Principais

- Automatizar o controle total do biodigestor de laboratório da universiade
- Desenvolver e treinar modelos de Inteligência Artificial para controle preditivo e otimização em tempo real
- Integrar sensores e atuadores de forma confiável
- Aumentar a eficiência, estabilidade e produtividade do processo de biodigestão anaeróbia
- Gerar dados para análise científica e possível publicação

### Tecnologias Utilizadas

- **Python** — Scripts de aquisição de dados, interface, modelos de IA e dashboard
- **C++** — Firmware para microcontroladores (ESP32, Arduino, etc.)
- Sensores IoT (DS18B20, pH, pressão, ultrassônico, MQ-series, etc.)
- Plataformas de Machine Learning (TensorFlow, Keras, scikit-learn)
- Comunicação serial / MQTT

### Estrutura do Repositório

- `/embarcado` → Código C++ para o microcontrolador
- `/leitura` → Scripts Python de aquisição e monitoramento em tempo real
- `/ia` → Notebooks e scripts de treinamento dos modelos de Inteligência Artificial
- `/dashboard` → Interface para visualização dos dados (opcional)

### Como Executar

1. Clone o repositório:

```bash
git clone https://github.com/lucasr300/biodigestor.git
cd biodigestor
```

2. Instale as dependências Python:

```bash
pip install -r requirements.txt
```

3. Para rodar a aquisição de dados:

```bash
cd leitura
python main.py
```

4. Para o código embarcado, abra a pasta `/embarcado`, compile e faça upload para o microcontrolador.

### Como Testar

1. Conecte os sensores ao microcontrolador
2. Execute o script principal de leitura
3. Verifique o log de dados e o envio para a IA
4. Monitore os valores em tempo real e os ajustes automáticos

<img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
````
