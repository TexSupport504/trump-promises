# Figma Integration for Trump Promises Tracker

This project uses Figma for design system management and maintains a seamless designer-to-developer workflow.

## 🎨 Design System Overview

Our design system is built on a **pure black and white aesthetic** with sophisticated grayscale gradients, creating a timeless and professional appearance.

### Core Principles
- **Monochromatic Palette**: Only black, white, and grayscale colors
- **Consistent Spacing**: 8px grid system
- **Typography Hierarchy**: Roboto font family with clear weight distinctions
- **Component-Based**: Reusable, modular design components

## 📁 File Structure

```
├── docs/figma/                 # Figma documentation
│   └── component-mapping.md    # Component-to-code mapping
├── static/css/
│   ├── figma-tokens.css        # Design tokens (manual)
│   └── figma-tokens-sync.css   # Auto-synced tokens
├── scripts/
│   ├── figma_integration.py    # API integration script
│   ├── setup-figma.sh         # Setup script
│   └── figma/
│       └── sync-workflow.sh    # Sync workflow helper
├── figma-config.json          # Figma API configuration
└── package.json               # NPM dependencies for Figma tools
```

## 🚀 Quick Start

### 1. Setup Figma Integration

```bash
# Run the setup script
chmod +x scripts/setup-figma.sh
./scripts/setup-figma.sh
```

### 2. Configure Figma Access

1. **Get Figma Personal Access Token**:
   - Go to [Figma Account Settings](https://www.figma.com/settings)
   - Generate a new Personal Access Token
   - Copy the token

2. **Create Figma Design File**:
   - Create a new file: "Trump Promises Design System"
   - Copy the file key from the URL (after `/file/`)

3. **Configure Integration**:
   ```bash
   python scripts/figma_integration.py
   # Choose option 1 to create config
   # Edit figma-config.json with your credentials
   ```

### 3. Sync Design Tokens

```bash
# Sync design tokens from Figma
python scripts/figma_integration.py
# Choose option 2
```

## 🎯 Design Workflow

### For Designers

1. **Design in Figma**:
   - Use the established design tokens
   - Create components with proper naming
   - Follow the component library structure

2. **Handoff to Developers**:
   - Use Figma Dev Mode for specifications
   - Export assets in required formats
   - Document any special interactions

### For Developers

1. **Sync Design Changes**:
   ```bash
   ./scripts/figma/sync-workflow.sh
   ```

2. **Implement Components**:
   - Use Figma design tokens (`--figma-*` variables)
   - Follow the component mapping guide
   - Maintain responsive behavior

3. **Update Styles**:
   - Import synced tokens: `@import 'figma-tokens-sync.css'`
   - Use Figma utility classes when available

## 🎨 Design Token Usage

### CSS Variables

```css
/* Use Figma design tokens in your CSS */
.custom-component {
  background: var(--figma-white);
  color: var(--figma-black);
  padding: var(--figma-space-4);
  border-radius: var(--figma-radius-md);
  font-size: var(--figma-font-size-base);
  box-shadow: var(--figma-shadow-md);
}
```

### Utility Classes

```html
<!-- Use Figma utility classes -->
<div class="figma-auto-layout figma-auto-layout--vertical">
  <h1 class="figma-text--heading-1">Title</h1>
  <p class="figma-text--body">Description</p>
</div>
```

## 🧩 Component Library

### Available Components

- **Navigation**: Header, menu, theme toggle
- **Stats Cards**: 4 variants with different styling
- **Forms**: Inputs, buttons, toggles
- **Data Display**: Progress bars, badges, tables
- **Layout**: Cards, modals, grids

### Component Naming Convention

- **Figma**: `category/component-variant`
- **CSS**: `.figma-category__component--variant`
- **Example**: `button/primary` → `.figma-button__primary`

## 🔄 Sync Workflows

### Manual Sync

1. **Design Tokens**:
   ```bash
   python scripts/figma_integration.py
   ```

2. **Components**:
   - Open Figma Dev Mode
   - Copy CSS specifications
   - Update component styles

3. **Assets**:
   - Export from Figma
   - Place in appropriate directories
   - Update references

### Automated Sync (Future)

- Set up webhooks for automatic updates
- GitHub Actions for design token sync
- Continuous integration with design changes

## 📋 Best Practices

### Design Consistency

- **Always use design tokens** instead of hard-coded values
- **Follow the 8px grid** for spacing and sizing
- **Maintain the monochromatic palette** (black, white, gray only)
- **Use consistent typography** hierarchy

### Code Quality

- **Import Figma tokens** before other styles
- **Use semantic naming** for components
- **Test responsive behavior** across devices
- **Document custom implementations**

### Collaboration

- **Communicate design changes** through proper channels
- **Version control** both design and code changes
- **Review handoffs** before implementation
- **Test implementations** against designs

## 🛠 Tools & Resources

### Figma Plugins

- **Design Tokens**: Manage and export tokens
- **Auto Layout**: Create responsive components
- **Dev Mode**: Generate CSS specifications
- **Component Inspector**: Detailed component specs

### Development Tools

- **CSS Custom Properties**: For design token usage
- **PostCSS**: For advanced CSS processing
- **Storybook**: Component documentation (future)
- **Visual Regression Testing**: Design consistency (future)

## 🔧 Troubleshooting

### Common Issues

1. **Token Sync Fails**:
   - Check Figma API token validity
   - Verify file key is correct
   - Ensure proper permissions

2. **Styles Not Updating**:
   - Clear browser cache
   - Check CSS import order
   - Verify token file path

3. **Component Misalignment**:
   - Review Figma specifications
   - Check responsive behavior
   - Validate grid usage

### Support

- **Documentation**: Check `/docs/figma/` directory
- **Issues**: Create GitHub issues for bugs
- **Design Questions**: Contact design team lead

## 📈 Roadmap

### Phase 1 (Current)
- ✅ Basic design token sync
- ✅ Component mapping documentation
- ✅ Manual sync workflows

### Phase 2 (Next)
- 🔄 Automated design token sync
- 🔄 Component code generation
- 🔄 Visual regression testing

### Phase 3 (Future)
- 📋 Storybook integration
- 📋 Design system documentation site
- 📋 Advanced automation workflows

---

*This integration ensures our design system remains consistent, scalable, and maintainable while fostering excellent designer-developer collaboration.*
