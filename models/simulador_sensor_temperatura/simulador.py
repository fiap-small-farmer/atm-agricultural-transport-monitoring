import random

def sensor_temperatura(temp_min: float, temp_max: float, tolerancia: float) -> float:
    # Calcula a faixa de tolerância
    faixa = temp_max - temp_min
    margem = faixa * (tolerancia / 100)
    
    # Define o novo intervalo com a margem de tolerância
    novo_min = temp_min - margem
    novo_max = temp_max + margem
    
    # Gera um valor aleatório dentro da nova faixa de tolerância
    temperatura = random.uniform(novo_min, novo_max)
    
    return temperatura