from PIL import Image, ImageFont, ImageDraw
import os
import random
import math
import numpy as np

class HandwritingRenderer:
    def __init__(self, config):
        self.config = config
        self.fonts = self._load_fonts()
        
    def _load_fonts(self):
        """Load the handwriting fonts"""
        fonts = {}
        font_dir = os.path.join("assets", "fonts")
        
        for font_info in self.config['handwriting']['fonts']:
            name = font_info['name']
            file = font_info['file']
            font_path = os.path.join(font_dir, file)
            
            try:
                
                size = self.config['handwriting']['size']
                font = ImageFont.truetype(font_path, size)
                fonts[name] = font
            except FileNotFoundError:
                print(f"Warning: Font file {file} not found")
                
        if not fonts:
            default_size = self.config['handwriting']['size']
            fonts['default'] = ImageFont.load_default().font_variant(size=default_size)
            
        return fonts
        
    def render_text(self, text, style='regular'):
        """Render text in handwriting style with realistic blue ballpoint pen effects"""
        #Get font for the selected style
        font = self.fonts.get(style, self.fonts['regular'])
        width = len(text) * font.size // 2 + 100
        height = font.size * 3
        text_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_img)
        base_blue = (0, 51, 153)
        
        #Draw the text with pressure and ink flow simulation
        self._draw_realistic_text(draw, text, font, base_blue, width, height)
        if self.config['handwriting'].get('variations', True):
            text_img = self._apply_variations(text_img)
        
        #Apply scan-like effects
        text_img = self._apply_scan_effects(text_img)
        
        return text_img

    def _draw_realistic_text(self, draw, text, font, base_color, width, height):
        """Draw text with realistic pen pressure and ink flow variations"""
        import random
        from PIL import ImageDraw, ImageFilter
        
        x_pos = 10
        y_pos = height // 2

        for char in text:
            if char == ' ':
                try:
                    space_width = font.getlength(' ')
                except AttributeError:
                    try:
                        bbox = font.getbbox(' ')
                        space_width = bbox[2] - bbox[0]
                    except AttributeError:
                        space_width = font.getsize(' ')[0]
                
                x_pos += space_width + random.randint(-1, 2)
                continue
            
            #Simulate pen pressure
            pressure = random.uniform(0.85, 1.0)
            r = min(255, int(base_color[0] * pressure))
            g = min(255, int(base_color[1] * pressure))
            b = min(255, int(base_color[2] * pressure))
            
            r = max(0, min(255, r + random.randint(-5, 5)))
            g = max(0, min(255, g + random.randint(-5, 5)))
            b = max(0, min(255, b + random.randint(-10, 10)))
            
            char_color = (r, g, b, 255)
            
            if random.random() < 0.2:
                char_color = (r, g, b, random.randint(180, 240))

            draw.text((x_pos, y_pos), char, font=font, fill=char_color)
            try:
                char_width = font.getlength(char)
            except AttributeError:
                try:
                    bbox = font.getbbox(char)
                    char_width = bbox[2] - bbox[0]
                except AttributeError:
                    char_width = font.getsize(char)[0]
            
            x_pos += char_width + random.randint(-1, 2)

    def _apply_scan_effects(self, img):
        """Apply effects to simulate a scanned document"""
        import random
        import numpy as np
        from PIL import ImageFilter, ImageEnhance
        img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
        img_array = np.array(img)

        for y in range(img_array.shape[0]):
            for x in range(img_array.shape[1]):
                if img_array[y, x, 3] > 0:
                    for c in range(3):
                        noise = random.randint(-3, 3)
                        img_array[y, x, c] = max(0, min(255, img_array[y, x, c] + noise))

        result = Image.fromarray(img_array)
        
        enhancer = ImageEnhance.Contrast(result)
        result = enhancer.enhance(1.05)
        
        return result
    
    def _apply_variations(self, text_img):
        """Apply variations to make handwriting look more natural"""
        variation_config = self.config['handwriting'].get('variation_params', {})
        rotation_range = variation_config.get('rotation', 1.5)
        jitter_range = variation_config.get('jitter', 2)

        img_array = np.array(text_img)
        angle = random.uniform(-rotation_range, rotation_range)
        rotated = Image.fromarray(img_array).rotate(angle, resample=Image.BICUBIC, expand=False, fillcolor=(0, 0, 0, 0))
        width, height = rotated.size
        stretch_factor = random.uniform(0.98, 1.02)
        new_width = int(width * stretch_factor)
        stretched = rotated.resize((new_width, height), Image.LANCZOS)
        result = stretched.copy()
        pixels = result.load()

        for y in range(height):
            for x in range(new_width):
                if 0 <= x < new_width and 0 <= y < height:
                    offset_y = int(math.sin(x/30) * jitter_range)
                    src_y = min(max(0, y + offset_y), height-1)

                    if stretched.getpixel((x, y))[3] > 0:
                        result.putpixel((x, y), stretched.getpixel((x, src_y)))
    
        return result