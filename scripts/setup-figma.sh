#!/bin/bash

# Figma Integration Setup Script for Trump Promises Tracker
# Run this script to set up the Figma design workflow

echo "🎨 Setting up Figma integration for Trump Promises Tracker"
echo "================================================="

# Create directories
echo "📁 Creating directory structure..."
mkdir -p docs/figma
mkdir -p static/css/figma
mkdir -p static/images/figma-assets
mkdir -p scripts/figma

# Create Figma file templates
echo "📄 Creating Figma file templates..."

# Component mapping file
cat > docs/figma/component-mapping.md << 'EOF'
# Figma Component Mapping

## Design System Structure

### Pages in Figma File
1. **🎨 Design Tokens** - Colors, typography, spacing
2. **🧩 Components** - Reusable UI components  
3. **📱 Templates** - Page layouts and compositions
4. **🌓 Themes** - Light and dark mode variants

### Component Library

#### Navigation Components
- `nav/header` → `.navbar` class
- `nav/theme-toggle` → `.theme-toggle` class  
- `nav/menu-item` → `.nav-link` class

#### Data Display
- `stats/card-primary` → `.stats-card-1` class
- `stats/card-secondary` → `.stats-card-2` class
- `stats/card-tertiary` → `.stats-card-3` class
- `stats/card-quaternary` → `.stats-card-4` class

#### Interactive Elements
- `button/primary` → `.btn-primary` class
- `button/secondary` → `.btn-secondary` class
- `badge/category` → `.badge` class
- `badge/tag` → `.tag-badge` class

#### Form Elements
- `input/text` → `.form-control` class
- `input/search` → `.search-input` class
- `toggle/theme` → `.theme-toggle` class

#### Layout Components
- `card/promise` → `.card` class
- `progress/bar` → `.progress` class
- `modal/dialog` → `.modal` class

### Design Token Mapping

#### Colors
- `color/black` → `--figma-black`
- `color/white` → `--figma-white`
- `color/gray/50-950` → `--figma-gray-*`

#### Typography
- `text/heading-1` → `.figma-text--heading-1`
- `text/heading-2` → `.figma-text--heading-2`
- `text/body` → `.figma-text--body`
- `text/caption` → `.figma-text--caption`

#### Spacing
- `space/1-16` → `--figma-space-*`

### Export Guidelines

#### Icons
- Export as SVG
- Naming: `icon-[name].svg`
- Size: 24x24px default

#### Assets
- Export at 1x, 2x, 3x for responsive
- Use PNG for complex graphics
- Use SVG for simple graphics/icons

#### Components
- Use Figma Dev Mode for CSS specs
- Export component variants separately
- Include interaction states (hover, active, disabled)
EOF

# Create sync workflow
cat > scripts/figma/sync-workflow.sh << 'EOF'
#!/bin/bash

# Figma Sync Workflow
# This script helps sync design changes from Figma to code

echo "🔄 Figma Design System Sync"
echo "=========================="

# Check if config exists
if [ ! -f "figma-config.json" ]; then
    echo "❌ figma-config.json not found"
    echo "📝 Run: python scripts/figma_integration.py and choose option 1"
    exit 1
fi

echo "1. 🎨 Sync design tokens"
echo "2. 📦 Export components" 
echo "3. 🖼️  Export assets"
echo "4. 🔄 Full sync"

read -p "Choose option (1-4): " choice

case $choice in
    1)
        echo "🎨 Syncing design tokens..."
        python scripts/figma_integration.py
        ;;
    2)
        echo "📦 Exporting components..."
        echo "Open Figma Dev Mode and copy CSS specs manually"
        ;;
    3)
        echo "🖼️ Exporting assets..."
        echo "Export icons and images from Figma manually"
        ;;
    4)
        echo "🔄 Full sync..."
        python scripts/figma_integration.py
        echo "✅ Full sync complete"
        ;;
    *)
        echo "❌ Invalid option"
        ;;
esac
EOF

chmod +x scripts/figma/sync-workflow.sh

# Create package.json for Figma plugins (if needed)
cat > package.json << 'EOF'
{
  "name": "trump-promises-figma-integration",
  "version": "1.0.0",
  "description": "Figma integration tools for Trump Promises Tracker",
  "scripts": {
    "figma:sync": "python scripts/figma_integration.py",
    "figma:setup": "./scripts/figma/sync-workflow.sh",
    "figma:tokens": "python scripts/figma_integration.py --tokens-only"
  },
  "devDependencies": {
    "@figma/plugin-typings": "^1.75.0"
  },
  "keywords": ["figma", "design-system", "design-tokens"],
  "author": "Trump Promises Team",
  "license": "MIT"
}
EOF

echo "✅ Figma integration setup complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Create a Figma account at https://figma.com"
echo "2. Create a new design file: 'Trump Promises Design System'"
echo "3. Get your Figma Personal Access Token from Account Settings"
echo "4. Run: python scripts/figma_integration.py (choose option 1)"
echo "5. Add your Figma token and file key to figma-config.json"
echo "6. Start designing your components in Figma!"
echo ""
echo "📚 Useful Resources:"
echo "- Figma Design Tokens: https://www.figma.com/community/plugin/888356646278934516"
echo "- Figma Dev Mode: https://www.figma.com/dev-mode/"
echo "- Design System Guide: ./docs/figma-integration.md"
