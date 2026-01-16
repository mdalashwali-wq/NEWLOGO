
import os
import base64
from PIL import Image
import numpy as np

# مسارات الملفات
base_dir = r"c:/Users/ًWinDows/Desktop/DD/datavalue_theme-main/datavalue_theme_15/public/images"
original_png = os.path.join(base_dir, "datavalue-new-logo.png")
light_png = os.path.join(base_dir, "datavalue-new-logo-light.png")
svg_normal = os.path.join(base_dir, "datavalue-new-logo.svg")
svg_light = os.path.join(base_dir, "datavalue-new-logo-light.svg")

def create_light_version(input_path, output_path):
    print(f"Processing {input_path} to create light version...")
    img = Image.open(input_path).convert("RGBA")
    data = np.array(img)
    
    # تحديد اللون الكحلي تقريباً (R, G, B)
    # الشعارات عادة ما تكون بها تدرجات، لذا سنبحث عن البكسلات الداكنة (غير الذهبية)
    # اللون الذهبي المذكور تقريباً: B8860B (184, 134, 11)
    # اللون الكحلي المذكور: 2C3E50 (44, 62, 80)
    
    red, green, blue, alpha = data.T
    
    # تحديد المناطق الداكنة (الكحلي) وتغييرها للأبيض
    # الشرك: أن لا تكون شفافة، وأن لا تكون ذهبية
    # سنفترض أن أي شيء ليس شفافاً وليس ذهبياً بشكل واضح هو كحلي ويجب تبييضه
    
    # تعريف قناع للبكسلات غير الشفافة
    not_transparent = (alpha > 0)
    
    # تعريف قناع للون الذهبي (تقريبي) - لن نلمسه
    # الذهبي يتميز بأن الأحمر والأخضر أعلى بكثير من الأزرق
    is_gold = (red > blue + 50) & (green > blue) & not_transparent
    
    # المناطق التي نريد تغييرها للأبيض: غير شفافة وليست ذهبية
    to_white = not_transparent & (~is_gold)
    
    # تطبيق اللون الأبيض (255, 255, 255)
    data[..., 0][to_white.T] = 255
    data[..., 1][to_white.T] = 255
    data[..., 2][to_white.T] = 255
    
    # حفظ الصورة الجديدة
    new_img = Image.fromarray(data)
    new_img.save(output_path)
    print(f"Saved light version to {output_path}")

def create_svg_embedding(png_path, svg_path):
    print(f"Embedding {png_path} into {svg_path}...")
    with open(png_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    img = Image.open(png_path)
    width, height = img.size
    
    svg_content = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <image width="{width}" height="{height}" xlink:href="data:image/png;base64,{encoded_string}"/>
</svg>'''
    
    with open(svg_path, "w", encoding='utf-8') as f:
        f.write(svg_content)
    print(f"Created SVG: {svg_path}")

try:
    # 1. إنشاء النسخة الفاتحة (Light PNG) من الأصلية
    create_light_version(original_png, light_png)
    
    # 2. إنشاء ملف SVG للنسخة العادية
    create_svg_embedding(original_png, svg_normal)
    
    # 3. إنشاء ملف SVG للنسخة الفاتحة
    create_svg_embedding(light_png, svg_light)

    print("SUCCESS: All files created successfully.")
except Exception as e:
    print(f"ERROR: {str(e)}")
