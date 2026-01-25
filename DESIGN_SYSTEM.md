# Hamro Agro Farm - Design System Reference

## Color Palette

### Primary Colors
- **Primary Green**: `#0db04b` - Main brand color, CTAs, primary actions
- **Secondary Green**: `#0a9a3f` - Darker green for hover states, gradients
- **Accent Green**: `#85d764` - Light green for secondary elements

### Secondary Colors
- **Dark Background**: `#0f1419` - Text, headings
- **Light Background**: `#f8f9fa` - Page background
- **Danger/Alert**: `#dc3545` - Sales, alerts, warnings
- **Muted Gray**: `#666` - Secondary text
- **Light Gray**: `#ddd` - Borders, dividers

### Gradients
```css
/* Main gradient (navbar, buttons) */
linear-gradient(135deg, #0db04b 0%, #0a9a3f 100%)

/* Sale gradient */
linear-gradient(135deg, #dc3545 0%, #c82333 100%)

/* Footer gradient */
linear-gradient(135deg, #0f1419 0%, #1a1f26 100%)
```

---

## Typography

### Font Family
```css
font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
```

### Font Sizes
- **Hero Title**: 48px (desktop), 36px (mobile)
- **Page Title**: 32px
- **Section Title**: 24px
- **Card Title**: 18px
- **Body Text**: 16px
- **Small Text**: 14px
- **Tiny Text**: 12px

### Font Weights
- **Light**: 300 (subtitles)
- **Regular**: 400 (body)
- **Medium**: 500 (navigation)
- **Semi-bold**: 600 (buttons, labels)
- **Bold**: 700 (card titles)
- **Extra-bold**: 800 (page titles)

### Line Heights
- **Headings**: 1.3
- **Body**: 1.6
- **Tight**: 1.4

---

## Spacing System

### Base Unit: 4px

### Common Spacing Values
- **4px** - Micro spacing
- **8px** - Small spacing
- **12px** - Small-medium
- **15px** - Button padding
- **20px** - Card padding
- **25px** - Section padding
- **30px** - Large spacing
- **40px** - Section margin
- **60px** - Large section padding

### Padding
- **Cards**: 20px padding
- **Buttons**: 10px 24px (vertical horizontal)
- **Input**: 10px 15px
- **Sections**: 40-60px vertical, 20px horizontal

### Margins
- **Page sections**: 20-40px bottom
- **Card items**: 20px bottom
- **Text elements**: 10-15px bottom

---

## Shadows

### Shadow Levels
```css
/* Subtle shadow */
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

/* Medium shadow */
box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);

/* Strong shadow */
box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);

/* Hover shadow */
box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
```

### Green-tinted Shadows
```css
/* For green elements on hover */
box-shadow: 0 4px 12px rgba(13, 176, 75, 0.3);

/* Stronger hover effect */
box-shadow: 0 6px 16px rgba(13, 176, 75, 0.4);
```

---

## Animations

### Timing
- **Quick**: 0.2s - Micro interactions (buttons)
- **Standard**: 0.3s - Normal transitions
- **Slow**: 0.5s - Hero elements, badges

### Easing Functions
```css
/* Standard easing */
cubic-bezier(0.4, 0, 0.2, 1)

/* Ease-out (default Bootstrap) */
ease-out

/* Ease-in-out */
cubic-bezier(0.25, 0.46, 0.45, 0.94)
```

### Common Animations

#### Hover Scale
```css
transition: transform 0.3s ease;
&:hover { transform: scale(1.05); }
```

#### Translate
```css
transition: transform 0.3s ease;
&:hover { transform: translateY(-2px); }
```

#### Fade
```css
transition: opacity 0.3s ease;
&:hover { opacity: 0.8; }
```

#### Pulse
```css
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}
animation: pulse 2s ease-in-out infinite;
```

---

## Border Radius

### Standard Values
- **Small buttons**: 6-8px
- **Cards**: 12-15px
- **Large buttons**: 25px (pill-shaped)
- **Input fields**: 8px

---

## Buttons

### Button States
```css
/* Default */
background: #0db04b;
color: white;

/* Hover */
background: #0a9a3f;
transform: translateY(-2px);
box-shadow: 0 4px 12px rgba(13, 176, 75, 0.3);

/* Active */
transform: translateY(0);

/* Disabled */
opacity: 0.6;
cursor: not-allowed;
```

### Button Variants

#### Primary Button
```css
.btn-primary {
  background: linear-gradient(135deg, #0db04b 0%, #0a9a3f 100%);
  color: white;
  padding: 15px 40px;
  border-radius: 10px;
  font-weight: 600;
}
```

#### Outline Button
```css
.btn-outline-dark {
  background: white;
  color: #0f1419;
  border: 2px solid #0f1419;
  padding: 8px 16px;
  border-radius: 8px;
}
```

#### Ghost Button
```css
.btn-ghost {
  background: transparent;
  color: #0db04b;
  border: 2px solid #0db04b;
}
```

---

## Forms

### Input Fields
```css
.form-control {
  border-radius: 8px;
  border: 2px solid #ddd;
  padding: 10px 15px;
  font-size: 14px;
  
  &:focus {
    border-color: #0db04b;
    box-shadow: 0 0 0 3px rgba(13, 176, 75, 0.15);
  }
}
```

### Labels
```css
.form-label {
  color: #0f1419;
  font-weight: 600;
  font-size: 14px;
  margin-bottom: 8px;
}
```

---

## Cards

### Card Structure
```css
.card {
  border: none;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
  }
}
```

### Card Sections
- **Header**: Optional, for images
- **Body**: Main content (20px padding)
- **Footer**: Actions (20px padding)

---

## Badges

### Badge Styling
```css
.badge {
  padding: 8px 16px;
  border-radius: 25px;
  font-weight: 600;
  font-size: 13px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.sale-badge {
  background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
  color: white;
}
```

---

## Responsive Breakpoints

### Bootstrap Breakpoints (Used)
- **xs**: < 576px (Mobile)
- **sm**: 576px - 768px (Tablet)
- **md**: 768px - 992px (Small desktop)
- **lg**: 992px - 1200px (Desktop)
- **xl**: > 1200px (Large desktop)

### Custom Media Queries
```css
/* Mobile */
@media (max-width: 576px) { }

/* Tablet */
@media (max-width: 768px) { }

/* Desktop adjustments */
@media (min-width: 768px) { }
```

---

## Grid System

### Product Grid
- **Mobile**: 2 columns
- **Tablet**: 3 columns
- **Desktop**: 4 columns

```css
row-cols-2 row-cols-md-3 row-cols-xl-4
```

### Gutter
- **Default**: 16px (gx-4)
- **Large**: 32px (gx-5)

---

## Images

### Image Container
```css
.image-container {
  position: relative;
  width: 100%;
  padding-top: 100%; /* 1:1 aspect ratio */
  overflow: hidden;
  border-radius: 12px;
  background: #f5f5f5;
}

.image-container img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

&:hover img {
  transform: scale(1.08);
}
```

---

## Navbar

### Navbar Height
- **Default**: 60-70px

### Logo Size
- **Desktop**: 60px height
- **Mobile**: 50px height

### Spacing
- **Horizontal padding**: 20px
- **Vertical padding**: 10px

---

## Footer

### Footer Structure
- **Background**: Dark gradient
- **Text color**: White with opacity
- **Padding**: 30px vertical
- **Border top**: 3px solid #0db04b

---

## Accessibility Guidelines

### Color Contrast
- Minimum ratio: 4.5:1 for text
- Text on images: Use text-shadow or background overlay

### Font Sizes
- Minimum: 14px body text
- Minimum: 12px small text
- Maximum: 48px titles

### Touch Targets
- Minimum 44x44px for buttons
- Minimum 8px spacing between targets

### ARIA Labels
- All icon buttons need labels
- Form inputs need labels
- Dynamic content needs descriptions

---

## Component Examples

### Hero Section
```html
<section class="hero-section">
  <div class="hero-content">
    <h1 class="hero-title">Title</h1>
    <p class="hero-subtitle">Subtitle</p>
  </div>
</section>
```

### Product Card
```html
<div class="product-card">
  <div class="product-image-wrapper">
    <div class="image-container">
      <img src="..." alt="...">
    </div>
    <div class="product-badge">Badge</div>
  </div>
  <div class="card-body">
    <h5>Product Name</h5>
    <div class="product-price">Price</div>
  </div>
</div>
```

### Button Group
```html
<div class="quantity-control">
  <button class="btn-qty">−</button>
  <input class="qty-input" type="text" value="1">
  <button class="btn-qty">+</button>
</div>
```

---

## CSS Variables Usage

```css
/* Use throughout for consistency */
color: var(--primary-green);
background: var(--light-bg);
box-shadow: var(--card-shadow);
transition: var(--transition);
```

---

## Implementation Tips

1. **Always use CSS variables** for colors and transitions
2. **Test on mobile first** - design is mobile-responsive
3. **Use semantic HTML** - structure matters
4. **Avoid inline styles** - use CSS classes
5. **Test animations** - ensure smooth 60fps
6. **Check accessibility** - WCAG AA minimum
7. **Optimize images** - use modern formats
8. **Monitor performance** - keep bundle small

---

**Design System v1.0**
Hamro Agro Farm - January 25, 2026
