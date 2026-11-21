"""Genera la gráfica SVG con Python estándar, sin PIL ni otras dependencias."""
from pathlib import Path
import math

angles = [2 * math.pi * i / 200 for i in range(201)]
radii = [100 * (math.cos(2*t) * math.sin(5*t) + 1.5) for t in angles]
# Intercambio respecto al script del robot para mostrar la figura de frente.
# Horizontal: Y del marco; vertical: X del marco (incluido su offset de 300 mm).
points = [(r*math.cos(t), r*math.sin(t)+300) for r,t in zip(radii, angles)]

def pixel(horizontal, vertical):
    return 110 + (horizontal+250)*1.36, 790-(vertical-50)*1.36

parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="900" viewBox="0 0 900 900">',
         '<rect width="900" height="900" fill="white"/>',
         '<g font-family="Arial, sans-serif" fill="#444" font-size="22">',
         '<text x="450" y="65" text-anchor="middle" font-size="28">Figura polar seleccionada</text>']
for v in range(100, 551, 100):
    y = pixel(0,v)[1]
    parts.append(f'<path d="M110 {y}H790" stroke="#e6e9ec"/>')
    parts.append(f'<text x="95" y="{y+7}" text-anchor="end">{v}</text>')
for v in range(-200, 251, 100):
    x = pixel(v,300)[0]
    parts.append(f'<path d="M{x} 110V790" stroke="#e6e9ec"/>')
    parts.append(f'<text x="{x}" y="830" text-anchor="middle">{v}</text>')
parts.append('<path d="M110 110V790H790" stroke="#777" fill="none" stroke-width="2"/>')
coords = ' '.join(f'{x:.2f},{y:.2f}' for x,y in (pixel(h,v) for h,v in points))
parts.append(f'<polyline points="{coords}" stroke="#245c80" fill="none" stroke-width="4" stroke-linejoin="round"/>')
parts.extend(['<text x="450" y="875" text-anchor="middle">Y del marco de trabajo (mm)</text>',
              '<text x="110" y="95">X (mm)</text>', '</g></svg>'])
output = Path(__file__).parent / 'imagenes' / 'figura_polar.svg'
output.write_text('\n'.join(parts), encoding='utf-8')
print(output)