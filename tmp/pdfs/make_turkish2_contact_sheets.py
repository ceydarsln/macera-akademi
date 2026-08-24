from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

root = Path("/Users/ceyda/Documents/New project/tmp/pdfs/turkish2_qa")
files = sorted(root.glob("page-*.png"))
font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
thumb_w, thumb_h = 230, 325
label_h, gap = 28, 10
cols, rows = 3, 4

for sheet_no, start in enumerate(range(0, len(files), cols * rows), start=1):
    chunk = files[start:start + cols * rows]
    sheet = Image.new("RGB", (cols * thumb_w + (cols + 1) * gap,
                              rows * (thumb_h + label_h) + (rows + 1) * gap), "#d8d6df")
    draw = ImageDraw.Draw(sheet)
    for index, path in enumerate(chunk):
        image = Image.open(path).convert("RGB")
        image.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        col, row = index % cols, index // cols
        x = gap + col * thumb_w + (col + 1) * gap
        y = gap + row * (thumb_h + label_h) + row * gap
        sheet.paste(image, (x + (thumb_w - image.width) // 2, y))
        label = f"Sayfa {start + index + 1}"
        bbox = draw.textbbox((0, 0), label, font=font)
        draw.text((x + (thumb_w - (bbox[2] - bbox[0])) / 2, y + thumb_h + 3), label, fill="#272038", font=font)
    sheet.save(root / f"contact-{sheet_no:02d}.png", quality=92)

print({"pages": len(files), "sheets": sheet_no})
