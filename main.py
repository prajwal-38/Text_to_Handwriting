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
    with open(config, 'r') as f:
        config_data = yaml.safe_load(f)

    with open(input, 'r') as f:
        text = f.read()

    processor = TextProcessor(config_data)
    lines = processor.process_text(text)
    formatted_lines = processor.format_for_handwriting(lines)

    renderer = DocumentRenderer(config_data)
    output_path = renderer.render_document(formatted_lines, font_style=style, output_path=output)
    
    print(f"Document created: {output_path}")

if __name__ == "__main__":
    os.makedirs("assets/fonts", exist_ok=True)
    os.makedirs("assets/templates", exist_ok=True)
    
    #run the application
    main()