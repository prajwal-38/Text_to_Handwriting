# Handwritten Text Generator

A Python application that converts digital text into realistic handwritten documents on lined paper.

## Overview

This tool transforms plain text into handwritten-style documents that look like they were written with a blue ballpoint pen on lined paper. Perfect for creating personalized notes, letters, or study materials with an authentic handwritten appearance.

## Features

- Convert any text file to handwritten document
- Multiple handwriting styles (regular, neat, messy)
- Blue ballpoint pen effect with realistic ink variations
- Customizable paper templates
- Natural character spacing and text flow

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/handwritten-text-generator.git
cd handwritten-text-generator

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py --input your_text.txt --output handwritten.png --style regular
```

### Options

- `--input, -i`: Input text file path (required)
- `--output, -o`: Output image file path (default: output.png)
- `--style, -s`: Handwriting style (regular, neat, messy) (default: regular)
- `--config, -c`: Config file path (default: config.yaml)

## Examples

### Input Text
```
Dear Friend,

This is a sample text that will be converted to handwriting.
Isn't technology amazing?

Best regards,
Your Name
```

### Output Image
![Sample Output](output.png)

## Customization

You can customize the appearance by modifying the `config.yaml` file:
- Change paper template
- Adjust margins and line spacing
- Modify handwriting size and variation

## Adding Custom Paper Templates

1. Scan your paper at 300 DPI
2. Save it as PNG in the `assets/templates` folder
3. Update the template name in `config.yaml`


## Acknowledgements

- Font creators for the handwriting fonts
- PIL/Pillow library for image processing
