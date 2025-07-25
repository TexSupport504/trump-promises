"""
Figma API Integration for Trump Promises Tracker
This module handles fetching design tokens and assets from Figma
"""

import requests
import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class FigmaToken:
    """Represents a design token from Figma"""
    name: str
    value: str
    type: str
    description: Optional[str] = None

class FigmaDesignSystem:
    """
    Manages design system synchronization with Figma
    """
    
    def __init__(self, figma_token: str, file_key: str):
        self.figma_token = figma_token
        self.file_key = file_key
        self.base_url = "https://api.figma.com/v1"
        self.headers = {
            "X-Figma-Token": figma_token,
            "Content-Type": "application/json"
        }
    
    def get_file_info(self) -> Dict:
        """Fetch basic file information from Figma"""
        url = f"{self.base_url}/files/{self.file_key}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_design_tokens(self) -> List[FigmaToken]:
        """Extract design tokens from Figma styles"""
        url = f"{self.base_url}/files/{self.file_key}/styles"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        styles_data = response.json()
        tokens = []
        
        for style_id, style in styles_data.get('meta', {}).get('styles', {}).items():
            # Extract color tokens
            if style.get('styleType') == 'FILL':
                token = FigmaToken(
                    name=self._normalize_token_name(style.get('name', '')),
                    value=self._extract_color_value(style),
                    type='color',
                    description=style.get('description')
                )
                tokens.append(token)
            
            # Extract text tokens
            elif style.get('styleType') == 'TEXT':
                token = FigmaToken(
                    name=self._normalize_token_name(style.get('name', '')),
                    value=self._extract_text_value(style),
                    type='typography',
                    description=style.get('description')
                )
                tokens.append(token)
        
        return tokens
    
    def get_components(self) -> Dict:
        """Fetch component definitions from Figma"""
        url = f"{self.base_url}/files/{self.file_key}/components"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def export_images(self, node_ids: List[str], format: str = "svg") -> Dict:
        """Export images/icons from Figma"""
        url = f"{self.base_url}/images/{self.file_key}"
        params = {
            "ids": ",".join(node_ids),
            "format": format,
            "scale": 1
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def generate_css_variables(self, tokens: List[FigmaToken]) -> str:
        """Generate CSS custom properties from design tokens"""
        css_lines = [
            "/* Auto-generated design tokens from Figma */",
            "/* Do not edit manually - use sync script instead */",
            "",
            ":root {"
        ]
        
        # Group tokens by type
        color_tokens = [t for t in tokens if t.type == 'color']
        typography_tokens = [t for t in tokens if t.type == 'typography']
        
        if color_tokens:
            css_lines.append("  /* Colors */")
            for token in color_tokens:
                css_lines.append(f"  --figma-{token.name}: {token.value};")
            css_lines.append("")
        
        if typography_tokens:
            css_lines.append("  /* Typography */")
            for token in typography_tokens:
                css_lines.append(f"  --figma-{token.name}: {token.value};")
        
        css_lines.append("}")
        return "\n".join(css_lines)
    
    def sync_design_tokens(self, output_file: str = "static/css/figma-tokens-sync.css"):
        """Sync design tokens from Figma to CSS file"""
        try:
            tokens = self.get_design_tokens()
            css_content = self.generate_css_variables(tokens)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            with open(output_file, 'w') as f:
                f.write(css_content)
            
            print(f"✅ Successfully synced {len(tokens)} design tokens to {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error syncing design tokens: {e}")
            return False
    
    def _normalize_token_name(self, name: str) -> str:
        """Convert Figma style names to CSS variable names"""
        return name.lower().replace(' ', '-').replace('/', '-')
    
    def _extract_color_value(self, style: Dict) -> str:
        """Extract color value from Figma style"""
        # This would need to be implemented based on Figma's style format
        # For now, return a placeholder
        return "#000000"
    
    def _extract_text_value(self, style: Dict) -> str:
        """Extract typography value from Figma style"""
        # This would need to be implemented based on Figma's style format
        # For now, return a placeholder
        return "16px"

def create_figma_config():
    """Create configuration file for Figma integration"""
    config = {
        "figma": {
            "personal_access_token": "YOUR_FIGMA_TOKEN_HERE",
            "file_key": "YOUR_FIGMA_FILE_KEY_HERE",
            "sync_interval": 3600,  # 1 hour in seconds
            "output_paths": {
                "tokens": "static/css/figma-tokens-sync.css",
                "icons": "static/images/figma-icons/",
                "assets": "static/images/figma-assets/"
            }
        }
    }
    
    with open('figma-config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("📝 Created figma-config.json - Please add your Figma credentials")

if __name__ == "__main__":
    # Example usage
    print("🎨 Figma Design System Integration")
    print("1. Create config file")
    print("2. Sync design tokens")
    print("3. Export components")
    
    choice = input("Enter choice (1-3): ")
    
    if choice == "1":
        create_figma_config()
    elif choice == "2":
        # Load config
        try:
            with open('figma-config.json', 'r') as f:
                config = json.load(f)
            
            figma_token = config['figma']['personal_access_token']
            file_key = config['figma']['file_key']
            
            if figma_token == "YOUR_FIGMA_TOKEN_HERE":
                print("❌ Please set your Figma token in figma-config.json")
            else:
                design_system = FigmaDesignSystem(figma_token, file_key)
                design_system.sync_design_tokens()
        except FileNotFoundError:
            print("❌ Config file not found. Run option 1 first.")
    else:
        print("Invalid choice")
