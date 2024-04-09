import json

def calcular_estadisticas(ventas):
    total_ventas = len(ventas)
    total_valor_ventas = 0
    for sale in ventas:
        total_valor_ventas = total_valor_ventas + sale['value']
    promedio_ventas = total_valor_ventas / total_ventas
    return {
        "total_ventas": total_ventas,
        "promedio_ventas": promedio_ventas,
        "total_valor_ventas": total_valor_ventas
    }

estadisticas = calcular_estadisticas(json.load(open('ventas.json')))
with open('estadisticas_ventas.txt', 'w') as file:
    file.write("Total de ventas: {}\n".format(estadisticas["total_ventas"]))
    file.write("Promedio de ventas: {:.2f}\n".format(estadisticas["promedio_ventas"]))
    file.write("Total de valor de ventas: {:.2f}\n".format(estadisticas["total_valor_ventas"]))
print("Estadísticas guardadas en el archivo estadisticas_ventas.txt")
