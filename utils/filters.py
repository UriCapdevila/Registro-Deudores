from datetime import datetime

def formatear_fecha(fecha):
    return fecha.strftime('%d/%m/%Y') if fecha else 'Sin fecha'

def calcular_total_pagos(pagos):
    return sum(p.monto for p in pagos)

def estado_pago(pago):
    if pago.estado == 'completo':
        return '✅ Pago completo'
    elif pago.estado == 'parcial':
        return '🟡 Pago parcial'
    else:
        return '🔴 Pendiente'