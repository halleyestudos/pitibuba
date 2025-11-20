from PIL import Image
from collections import Counter
import os

img_path = os.path.join('imgs', 'logomarca_oficial.png')

if not os.path.exists(img_path):
    print('ERROR: file not found:', img_path)
    exit(2)

img = Image.open(img_path).convert('RGBA')
# resize to speed up
img = img.resize((120, 120))

pixels = list(img.getdata())
# filter out transparent and near-white pixels
filtered = []
for r,g,b,a in pixels:
    if a < 40:
        continue
    # ignore very white backgrounds
    if r > 240 and g > 240 and b > 240:
        continue
    filtered.append((r,g,b))

if not filtered:
    # fallback to average color including whites
    pixels_rgb = [(r,g,b) for (r,g,b,a) in pixels if a >= 40]
    if not pixels_rgb:
        print('ERROR: no opaque pixels found')
        exit(3)
    r = sum(p[0] for p in pixels_rgb)//len(pixels_rgb)
    g = sum(p[1] for p in pixels_rgb)//len(pixels_rgb)
    b = sum(p[2] for p in pixels_rgb)//len(pixels_rgb)
    hexcol = '#{0:02X}{1:02X}{2:02X}'.format(r,g,b)
    print(hexcol)
    exit(0)

# use most common color
most_common = Counter(filtered).most_common(1)[0][0]
r,g,b = most_common
hexcol = '#{0:02X}{1:02X}{2:02X}'.format(r,g,b)
print(hexcol)
