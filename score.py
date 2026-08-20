def calcular_score(precio, m50, m200, rsi, macd):

    score = 0
    motivos = []

    # Precio sobre Media 50
    if precio > m50:
        score += 20
        motivos.append("✅ +20 Precio sobre Media 50")
    else:
        motivos.append("❌ Precio por debajo de la Media 50")

    # Tendencia principal
    if m50 > m200:
        score += 30
        motivos.append("✅ +30 Media 50 sobre Media 200")
    else:
        motivos.append("❌ Media 50 por debajo de la Media 200")

    # RSI
    if 45 <= rsi <= 60:
        score += 20
        motivos.append("✅ +20 RSI en zona ideal")
    else:
        motivos.append(f"❌ RSI fuera de rango ({rsi:.1f})")

    # MACD
    if macd:
        score += 15
        motivos.append("✅ +15 MACD alcista")
    else:
        motivos.append("❌ MACD bajista")

    return score, motivos