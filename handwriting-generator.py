# File structure:
# handwriting_generator/
# ├── assets/
# │   ├── fonts/             # Handwriting fonts
# │   ├── templates/         # A4 lined paper templates
# ├── src/
# │   ├── __init__.py
# │   ├── text_processor.py  # Text processing utilities
# │   ├── paper_formatter.py # Handles page formatting/layout
# │   ├── handwriting.py     # Creates handwriting effect
# │   ├── renderer.py        # Final rendering and output
# ├── main.py                # Main application entry point
# ├── requirements.txt       # Dependencies
# └── config.yaml            # Configuration settings

# First, let's define the requirements.txt file:
"""
# requirements.txt
Pillow==10.1.0
PyYAML==6.0.1
numpy==1.25.2
fonttools==4.43.1
click==8.1.7
"""

# Now, let's create the configuration file:
"""
# config.yaml
paper:
  template: "a4_lined.png"
  width: 2480  # A4 at 300 DPI
  height: 3508
  margin_top: 200
  margin_bottom: 200
  margin_left: 200
  margin_right: 200
  line_height: 100  # Distance between lines

handwriting:
  default_font: "handwriting_regular.ttf"
  fonts:
    - name: "regular"
      file: "handwriting_regular.ttf"
    - name: "neat"
      file: "handwriting_neat.ttf"
    - name: "messy"
      file: "handwriting_messy.ttf"
  
  # Handwriting style parameters
  size: 60  # Font size
  color: [0, 0, 0]  # RGB color (black)
  variation:
    size: 0.1  # Size variation (10%)
    angle: 2.0  # Rotation angle variation in degrees
    spacing: 0.2  # Character spacing variation
    baseline: 3  # Baseline shift variation in pixels

output:
  format: "png"
  dpi: 300
  quality: 95  # For JPEG
"""

# Now let's implement the core modules
# First, text_processor.py
"""
# src/text_processor.py
import re

class TextProcessor:
    def __init__(self, config):
        self.config = config
        
    def process_text(self, text):
        """Process text into lines that fit within page constraints"""
        # Split text into paragraphs
        paragraphs = text.split('\n')
        
        # Calculate max characters per line based on config
        font_size = self.config['handwriting']['size']
        avg_char_width = font_size * 0.6  # Approximation
        
        page_width = self.config['paper']['width']
        margin_left = self.config['paper']['margin_left']
        margin_right = self.config['paper']['margin_right']
        
        usable_width = page_width - margin_left - margin_right
        max_chars_per_line = int(usable_width / avg_char_width)
        
        # Break text into lines
        lines = []
        for paragraph in paragraphs:
            if not paragraph.strip():
                lines.append("")  # Keep empty paragraphs as empty lines
                continue
                
            words = paragraph.split()
            current_line = []
            current_length = 0
            
            for word in words:
                word_length = len(word)
                if current_length + word_length + len(current_line) <= max_chars_per_line:
                    current_line.append(word)
                    current_length += word_length
                else:
                    lines.append(" ".join(current_line))
                    current_line = [word]
                    current_length = word_length
            
            if current_line:
                lines.append(" ".join(current_line))
        
        return lines
    
    def format_for_handwriting(self, lines):
        """Apply additional formatting suitable for handwriting simulation"""
        formatted_lines = []
        
        for line in lines:
            # Remove extra spaces
            line = re.sub(r'\s+', ' ', line).strip()
            formatted_lines.append(line)
            
        return formatted_lines
"""

# Now, paper_formatter.py
"""
# src/paper_formatter.py
from PIL import Image
import os

class PaperFormatter:
    def __init__(self, config):
        self.config = config
        self.template_path = os.path.join("assets", "templates", self.config['paper']['template'])
        
    def load_template(self):
        """Load the template image"""
        try:
            template = Image.open(self.template_path)
            return template
        except FileNotFoundError:
            # If template doesn't exist, create a blank page with lines
            return self.create_blank_template()
            
    def create_blank_template(self):
        """Create a blank A4 lined template"""
        width = self.config['paper']['width']
        height = self.config['paper']['height']
        
        # Create a white background
        template = Image.new('RGB', (width, height), (255, 255, 255))
        
        # Draw horizontal lines
        from PIL import ImageDraw
        draw = ImageDraw.Draw(template)
        
        line_height = self.config['paper']['line_height']
        margin_top = self.config['paper']['margin_top']
        margin_bottom = self.config['paper']['margin_bottom']
        
        line_color = (200, 200, 220)  # Light blue-gray
        
        y = margin_top
        while y < height - margin_bottom:
            draw.line([(0, y), (width, y)], fill=line_color, width=2)
            y += line_height
            
        return template
        
    def get_line_positions(self):
        """Get Y-coordinates for text lines"""
        height = self.config['paper']['height']
        margin_top = self.config['paper']['margin_top']
        margin_bottom = self.config['paper']['margin_bottom']
        line_height = self.config['paper']['line_height']
        
        positions = []
        y = margin_top
        while y < height - margin_bottom:
            positions.append(y)
            y += line_height
            
        return positions
"""

# Now, handwriting.py
"""
# src/handwriting.py
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
                # Load font at base size
                size = self.config['handwriting']['size']
                font = ImageFont.truetype(font_path, size)
                fonts[name] = font
            except FileNotFoundError:
                print(f"Warning: Font file {file} not found")
                
        # Default to a built-in font if no fonts were loaded
        if not fonts:
            default_size = self.config['handwriting']['size']
            fonts['default'] = ImageFont.load_default().font_variant(size=default_size)
            
        return fonts
        
    def render_text(self, text, font_name='regular'):
        """Render a single line of text with handwriting effect"""
        if font_name not in self.fonts:
            font_name = list(self.fonts.keys())[0]  # Use first available font
            
        font = self.fonts[font_name]
        base_size = self.config['handwriting']['size']
        
        # Get variation parameters
        size_var = self.config['handwriting']['variation']['size']
        angle_var = self.config['handwriting']['variation']['angle']
        spacing_var = self.config['handwriting']['variation']['spacing']
        baseline_var = self.config['handwriting']['variation']['baseline']
        
        # Calculate text size to create an appropriately sized image
        sample_size = font.getbbox(text)
        width = int(sample_size[2] * (1 + spacing_var * 2))  # Add extra for variations
        height = int(sample_size[3] * 2)  # Double height for rotations
        
        # Create a transparent image for the text
        text_img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(text_img)
        
        # Get RGB color for text
        color = tuple(self.config['handwriting']['color'])
        
        # Process each character individually for natural variation
        x_offset = 0
        
        for char in text:
            # Skip spaces but add spacing
            if char == ' ':
                space_width = font.getbbox(' ')[2]
                x_offset += space_width
                # Add random variation to space width
                x_offset += random.uniform(-spacing_var, spacing_var) * space_width
                continue
                
            # Vary the font size slightly for each character
            size_factor = 1.0 + random.uniform(-size_var, size_var)
            char_size = int(base_size * size_factor)
            
            # Get a font of the right size for this character
            if size_factor != 1.0:
                char_font = ImageFont.truetype(font.path, char_size)
            else:
                char_font = font
                
            # Vary the baseline position
            y_offset = height // 2
            y_offset += random.uniform(-baseline_var, baseline_var)
            
            # Vary the rotation angle
            angle = random.uniform(-angle_var, angle_var)
            
            # Draw the character
            char_bbox = char_font.getbbox(char)
            char_width = char_bbox[2]
            char_height = char_bbox[3]
            
            # Create a separate image for this character so we can rotate it
            char_img = Image.new('RGBA', (char_width * 2, char_height * 2), (255, 255, 255, 0))
            char_draw = ImageDraw.Draw(char_img)
            
            # Draw in the center of the new image
            char_draw.text(
                (char_width // 2, char_height // 2), 
                char, 
                font=char_font, 
                fill=color
            )
            
            # Rotate the character
            if angle != 0:
                char_img = char_img.rotate(angle, resample=Image.BICUBIC, expand=False)
                
            # Paste onto the main text image
            text_img.paste(char_img, (int(x_offset), int(y_offset - char_height // 2)), char_img)
            
            # Update x_offset for next character with slight variation in spacing
            x_offset += char_width
            x_offset += random.uniform(-spacing_var, spacing_var) * char_width
            
        return text_img
"""

# Finally, renderer.py
"""
# src/renderer.py
from PIL import Image, ImageDraw
import os
from .paper_formatter import PaperFormatter
from .handwriting import HandwritingRenderer

class DocumentRenderer:
    def __init__(self, config):
        self.config = config
        self.paper_formatter = PaperFormatter(config)
        self.handwriting = HandwritingRenderer(config)
        
    def render_document(self, lines, font_style='regular', output_path='output.png'):
        """Render the complete document with all lines of text"""
        # Load or create the template
        template = self.paper_formatter.load_template()
        
        # Get positions for each line
        line_positions = self.paper_formatter.get_line_positions()
        
        # Make a copy of the template to draw on
        result = template.copy()
        
        # Get margins
        margin_left = self.config['paper']['margin_left']
        
        # Draw each line of text
        for i, line in enumerate(lines):
            if i >= len(line_positions):
                # We've run out of space on this page
                # In a more advanced version, this would create a new page
                break
                
            y_pos = line_positions[i]
            
            # Skip empty lines
            if not line.strip():
                continue
                
            # Render the line as handwriting
            text_img = self.handwriting.render_text(line, font_style)
            
            # Calculate position to paste text
            # The y_position is the baseline, so we need to adjust
            text_height = text_img.height
            paste_y = y_pos - text_height // 2
            
            # Paste the text onto the result image
            result.paste(text_img, (margin_left, paste_y), text_img)
            
        # Save the result
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        result.save(output_path, format=self.config['output']['format'].upper(), 
                   dpi=(self.config['output']['dpi'], self.config['output']['dpi']),
                   quality=self.config['output']['quality'])
        
        return output_path
"""

# Lastly, let's create the main application file
"""
# main.py
import os
import yaml
import click
from src.text_processor import TextProcessor
from src.renderer import DocumentRenderer

@click.command()
@click.option('--input', '-i', help='Input text file path', required=True)
@click.option('--output', '-o', help='Output image file path', default='output.png')
@click.option('--style', '-s', help='Handwriting style (regular, neat, messy)', default='regular')
@click.option('--config', '-c', help='Config file path', default='config.yaml')
def main(input, output, style, config):
    """Convert text to handwritten document on lined paper"""
    # Load configuration
    with open(config, 'r') as f:
        config_data = yaml.safe_load(f)
    
    # Read input text
    with open(input, 'r') as f:
        text = f.read()
    
    # Process text
    processor = TextProcessor(config_data)
    lines = processor.process_text(text)
    formatted_lines = processor.format_for_handwriting(lines)
    
    # Render document
    renderer = DocumentRenderer(config_data)
    output_path = renderer.render_document(formatted_lines, font_style=style, output_path=output)
    
    print(f"Document created: {output_path}")

if __name__ == "__main__":
    # Create necessary directories if they don't exist
    os.makedirs("assets/fonts", exist_ok=True)
    os.makedirs("assets/templates", exist_ok=True)
    
    # Run the application
    main()
"""
