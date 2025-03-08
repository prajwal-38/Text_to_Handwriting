
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
        template = self.paper_formatter.load_template()

        line_positions = self.paper_formatter.get_line_positions()
        result = template.copy()
        margin_left = self.config['paper']['margin_left']

        for i, line in enumerate(lines):
            if i >= len(line_positions):
                break
                
            y_pos = line_positions[i]
            if not line.strip():
                continue

            text_img = self.handwriting.render_text(line, font_style)
            text_height = text_img.height
            paste_y = y_pos - text_height // 3
            result.paste(text_img, (margin_left, paste_y), text_img)

        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        result.save(output_path, format=self.config['output']['format'].upper(), 
                   dpi=(self.config['output']['dpi'], self.config['output']['dpi']),
                   quality=self.config['output']['quality'])
        
        return output_path