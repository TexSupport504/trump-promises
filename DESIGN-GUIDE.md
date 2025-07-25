# Trump Promises Tracker - Black & White Dark Mode Design Guide

## Overview
This guide outlines the black and white dark mode theme for the Trump Promises Tracker application and how to integrate it with Figma's free text-to-code AI tool for creating visuals and components.

## Color Palette

### Primary Colors
- **Background Primary**: `#000000` (Pure Black)
- **Background Secondary**: `#1a1a1a` (Dark Gray)
- **Background Tertiary**: `#2d2d2d` (Medium Gray)
- **Text Primary**: `#ffffff` (Pure White)
- **Text Secondary**: `#e0e0e0` (Light Gray)
- **Text Muted**: `#b0b0b0` (Medium Light Gray)

### Accent Colors
- **Accent Primary**: `#ffffff` (White Accent)
- **Accent Secondary**: `#808080` (Gray Accent)
- **Border Color**: `#404040` (Dark Border)

### Shadows & Effects
- **Light Shadow**: `rgba(255, 255, 255, 0.1)`
- **Dark Shadow**: `rgba(0, 0, 0, 0.5)`

## Typography
- **Primary Font**: Inter (Google Fonts)
- **Fallback**: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif
- **Font Weights**: 300, 400, 500, 600, 700

## Design Principles

### 1. High Contrast
- Maximum contrast between text and background for accessibility
- Pure black and white with strategic gray tones
- Ensure WCAG AA compliance for readability

### 2. Minimalism
- Clean, uncluttered interface
- Focus on content over decoration
- Strategic use of whitespace (or "blackspace")

### 3. Subtle Interactions
- Gentle hover effects with `translateY(-2px)`
- Smooth transitions using `transition: all 0.3s ease`
- Box shadows for depth without color

## Component Guidelines

### Navigation
```css
.navbar {
  background-color: #1a1a1a;
  border-bottom: 1px solid #404040;
  backdrop-filter: blur(10px);
}
```

### Cards
```css
.card {
  background-color: #1a1a1a;
  border: 1px solid #404040;
  border-radius: 0.75rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
}
```

### Buttons
```css
.btn-primary {
  background-color: #ffffff;
  border-color: #ffffff;
  color: #000000;
}
```

## Using Figma's Text-to-Code AI Tool

### 1. Design Prompts for Components

#### Navigation Bar
```
Create a dark navigation bar with black background (#1a1a1a), white text, and minimal design. Include logo on left, navigation items in center, and search bar on right. Add subtle border at bottom.
```

#### Promise Card
```
Design a dark card component with black background (#1a1a1a), white text, rounded corners, and subtle shadow. Include header section with category icon, main content area with title and description, and footer with status badge and date.
```

#### Dashboard Cards
```
Create a set of dashboard stat cards with black backgrounds, white text, large numbers, and icons. Include hover effects and minimal shadows. Cards should show metrics like "Total Promises", "Fulfillment Rate", etc.
```

#### Status Badges
```
Design status badges in monochrome style - white background for positive states, gray for neutral, and outlined for negative. Keep them minimal and readable.
```

### 2. Component Specifications for Figma

#### Card Component
- **Width**: 100% (responsive)
- **Padding**: 24px
- **Border Radius**: 12px
- **Background**: #1a1a1a
- **Border**: 1px solid #404040
- **Shadow**: 0 4px 6px rgba(0, 0, 0, 0.5)

#### Button Component
- **Height**: 40px
- **Padding**: 8px 24px
- **Border Radius**: 8px
- **Font Weight**: 500
- **Text Transform**: Uppercase
- **Letter Spacing**: 0.5px

#### Typography Scale
- **H1**: 2.5rem, Weight 700
- **H2**: 2rem, Weight 600
- **H3**: 1.75rem, Weight 600
- **H4**: 1.5rem, Weight 600
- **H5**: 1.25rem, Weight 600
- **Body**: 1rem, Weight 400
- **Small**: 0.875rem, Weight 400

### 3. Figma Design System Setup

#### Create Styles
1. **Color Styles**:
   - Primary Black: #000000
   - Secondary Black: #1a1a1a
   - Tertiary Gray: #2d2d2d
   - Primary White: #ffffff
   - Secondary White: #e0e0e0
   - Border Gray: #404040

2. **Text Styles**:
   - Heading 1: Inter, 40px, Bold
   - Heading 2: Inter, 32px, Semibold
   - Heading 3: Inter, 28px, Semibold
   - Body: Inter, 16px, Regular
   - Caption: Inter, 14px, Regular

3. **Effect Styles**:
   - Card Shadow: Drop Shadow, 0 4px 6px rgba(0,0,0,0.5)
   - Hover Shadow: Drop Shadow, 0 8px 25px rgba(0,0,0,0.5)

#### Component Library
Create reusable components for:
- Navigation Bar
- Promise Card
- Dashboard Card
- Button Variants
- Form Elements
- Status Badges
- Footer

### 4. AI Prompt Best Practices

#### Be Specific About Colors
```
Use exact hex codes: background #1a1a1a, text #ffffff, borders #404040
```

#### Define Spacing
```
Use 24px padding, 12px border radius, 16px between elements
```

#### Specify Interactions
```
Add hover state with 2px upward movement and enhanced shadow
```

#### Include Accessibility
```
Ensure high contrast ratios and readable text sizes for accessibility compliance
```

### 5. Code Export Guidelines

When exporting from Figma to code:

1. **CSS Variables**: Convert Figma tokens to CSS custom properties
2. **Responsive Units**: Use rem/em instead of fixed pixels
3. **Flexbox/Grid**: Ensure layouts are flexible
4. **Hover States**: Include interactive states in export
5. **Dark Mode**: Ensure all components work in dark theme

### 6. Integration with Flask Templates

To integrate Figma-generated components:

1. Export CSS from Figma
2. Convert to our CSS variable system
3. Apply to existing Flask templates
4. Test responsiveness and accessibility
5. Optimize for performance

## File Structure
```
app/web/static/
├── css/
│   ├── dark-theme.css          # Main dark theme styles
│   ├── components.css          # Component-specific styles
│   └── figma-components.css    # Figma-generated components
├── js/
│   └── theme.js               # Theme switching logic
└── images/
    └── icons/                 # Custom icons and graphics
```

## Testing Checklist

### Accessibility
- [ ] High contrast ratio (4.5:1 minimum)
- [ ] Keyboard navigation
- [ ] Screen reader compatibility
- [ ] Focus indicators

### Responsiveness
- [ ] Mobile devices (320px+)
- [ ] Tablets (768px+)
- [ ] Desktop (1024px+)
- [ ] Large screens (1440px+)

### Browser Compatibility
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge

### Performance
- [ ] CSS minification
- [ ] Font loading optimization
- [ ] Image optimization
- [ ] Render performance

## Resources

### Figma Templates
- Component library file: `trump-promises-dark-components.fig`
- Design system file: `trump-promises-design-system.fig`

### External Tools
- [Figma](https://figma.com) - Design and prototyping
- [Figma to Code](https://figma.com/community/plugins/figma-to-code) - Code generation plugin
- [Inter Font](https://fonts.google.com/specimen/Inter) - Typography
- [Font Awesome](https://fontawesome.com) - Icons

### Validation Tools
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [WAVE Web Accessibility Evaluator](https://wave.webaim.org/)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse/) - Performance and accessibility

## Next Steps

1. Create Figma design file with complete component library
2. Generate additional components using Figma's AI tools
3. Export and integrate with Flask application
4. Test across different devices and browsers
5. Gather user feedback and iterate

---

*This design system prioritizes accessibility, performance, and maintainability while delivering a striking black and white aesthetic that emphasizes content clarity and user experience.*
