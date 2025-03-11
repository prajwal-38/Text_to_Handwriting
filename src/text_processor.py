import re
import random

class TextProcessor:
    def __init__(self, config):
        self.config = config
        
    def process_text(self, text):
        """Process the input text into lines that fit on the page"""

        max_chars = self.config['paper'].get('max_chars_per_line', 80)
        raw_lines = text.splitlines()
        
        if len(raw_lines) == 0:
            raw_lines = [text]
        
        processed_lines = []
        
        for line in raw_lines:
            if not line.strip():
                processed_lines.append('')
                continue

            if len(line) <= max_chars:
                processed_lines.append(line)
            else:
                words = line.split()
                current_line = ""
                
                for word in words:
                    if len(current_line) + len(word) + 1 <= max_chars:
                        if current_line:
                            current_line += " " + word
                        else:
                            current_line = word
                    else:
                        processed_lines.append(current_line)
                        current_line = word
                
                if current_line:
                    processed_lines.append(current_line)
        
        return processed_lines
    
    def format_for_handwriting(self, lines):
        """Format text for handwriting rendering with improved spacing"""
        formatted_lines = []
        
        for line in lines:
            words = line.split()
            formatted_line = ""

            for word_idx, word in enumerate(words):
                chars = list(word)
                formatted_word = ""
                for i, char in enumerate(chars):
                    formatted_word += char
                    if i < len(chars) - 1 and chars[i+1] not in ".,;:!?)'\"":
                        next_char = chars[i+1]
                        
                        tight_pairs = ['th', 'he', 'in', 'er', 'an', 're', 'on', 'at', 'en', 'nd', 'ti', 'es', 'or']
                        wide_pairs = ['ow', 'av', 'wa', 'we', 'wo', 'yo', 'yo']
                        
                        pair = char + next_char
                        if pair.lower() in tight_pairs:
                            pass
                        elif pair.lower() in wide_pairs:
                            formatted_word += " " * random.randint(0, 1)
                        else:
                            if random.random() < 0.2:
                                formatted_word += " " * random.randint(0, 1)
                    
                formatted_line += formatted_word
                if word_idx < len(words) - 1:
                    formatted_line += " " * random.randint(3, 5)
            
            formatted_lines.append(formatted_line)
        
        return formatted_lines