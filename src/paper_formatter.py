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
            return self.create_blank_template()
            
    def create_blank_template(self):
        """Create a blank A4 lined template"""
        width = self.config['paper']['width']
        height = self.config['paper']['height']
        
        #Create a white background
        template = Image.new('RGB', (width, height), (255, 255, 255))
        
        #Draw horizontal lines
        from PIL import ImageDraw
        draw = ImageDraw.Draw(template)
        
        line_height = self.config['paper']['line_height']
        margin_top = self.config['paper']['margin_top']
        margin_bottom = self.config['paper']['margin_bottom']
        
        line_color = (200, 200, 220)
        
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