# Visual Design Standards - Hamro Agro Farm

## Button Hover States Quick Reference

### Primary CTA Buttons (.btn-add-to-cart)
```
Default:     gradient(#0db04b → #0a9a3f), shadow: 0 4px 15px rgba(13,176,75,0.3)
Hover:       same gradient, translateY(-3px), shadow: 0 8px 24px rgba(13,176,75,0.4)
Active:      same gradient, translateY(-1px), shadow: 0 4px 12px rgba(13,176,75,0.3)
Disabled:    opacity: 0.6, shadow: 0 2px 8px rgba(0,0,0,0.08)
```

### Secondary Buttons (.btn-outline-dark)
```
Default:     white bg, dark border, shadow: 0 2px 8px rgba(0,0,0,0.08)
Hover:       green bg, green border, white text, translateY(-2px), enhanced shadow
Active:      translateY(0), reduced shadow
Disabled:    opacity: 0.6, no shadow
```

### Quantity Control Buttons (.qty-btn, .btn-qty)
```
Default:     gradient background, shadow: 0 2px 8px rgba(13,176,75,0.15)
Hover:       scale(1.08), shadow: 0 4px 12px rgba(13,176,75,0.25)
Active:      scale(1.02), shadow: 0 2px 8px rgba(13,176,75,0.15)
```

### Update/Remove Actions
```
.btn-update:
  Gradient: #0db04b → #0a9a3f
  Hover: translateY(-2px), enhanced shadow
  
.btn-remove:
  Gradient: #dc3545 → #c82333
  Hover: translateY(-2px), enhanced shadow
```

---

## Card Hover Effects

### Product Cards
```
Default:     white bg, border: 1px transparent, shadow: 0 2px 12px rgba(0,0,0,0.08)
Hover:       border: 2px #0db04b, shadow: 0 8px 24px rgba(0,0,0,0.12)
             translateY(-8px), image scale(1.08)
             product name color → #0db04b
```

### Cart Items
```
Default:     white bg, border: 2px transparent, shadow: 0 2px 12px rgba(0,0,0,0.08)
Hover:       border: 2px #0db04b, shadow: 0 8px 24px rgba(0,0,0,0.12)
             translateY(-3px), image scale(1.05)
```

### Related Product Cards
```
Default:     white bg, border: 2px #f0f0f0, shadow: 0 2px 8px rgba(0,0,0,0.05)
Hover:       border: 2px #0db04b, shadow: 0 8px 24px rgba(13,176,75,0.15)
             translateY(-6px), image scale(1.08)
```

---

## Color-Coded Status Badges

### Stock Status
```
In Stock:     gradient(rgba(13,176,75,0.15) → rgba(13,176,75,0.08))
              color: #0db04b
              border: 1px rgba(13,176,75,0.2)
              
Low Stock:    gradient(rgba(255,193,7,0.2) → rgba(255,193,7,0.1))
              color: #856404
              border: 1px rgba(255,193,7,0.3)
              
Out of Stock: gradient(rgba(220,53,69,0.15) → rgba(220,53,69,0.08))
              color: #c82333
              border: 1px rgba(220,53,69,0.2)
```

---

## Form Controls Consistency

### Input Focus States
```
Default:     border: 2px #e0e0e0, shadow: none
Focus:       border: 2px #0db04b, shadow: 0 0 0 3px rgba(13,176,75,0.15)
```

### Dropdown Hover
```
Default:     background transparent
Hover:       background: rgba(255,255,255,0.1)
             border-left: 3px white
             padding-left increased by 5px
```

---

## Animation Timing

All transitions use: `cubic-bezier(0.4, 0, 0.2, 1)` (Material Design standard)

```
Fast:        0.2s - Small buttons, icons, minor changes
Normal:      0.3s - Cards, text changes, moderate elements
Slow:        0.4s - Large sections, major layout changes
```

### Keyframe Animations
- **badge-appear**: Scale from 0.8 → 1, opacity 0 → 1 (0.4s)
- **dropdown-appear**: Slide -10px → 0, opacity 0 → 1 (0.2s)
- **float**: Continuous vertical movement (3s infinite)
- **stock-pulse**: Opacity pulse for stock indicators (2s infinite)

---

## Shadow System

```
--shadow-sm:  0 2px 8px rgba(0, 0, 0, 0.08)     [Default cards]
--shadow-md:  0 4px 15px rgba(0, 0, 0, 0.12)    [Hover state]
--shadow-lg:  0 8px 24px rgba(0, 0, 0, 0.15)    [Elevated cards]
--shadow-xl:  0 12px 32px rgba(0, 0, 0, 0.18)   [Max elevation]
```

---

## Spacing System (4px base)

```
--space-xs:   4px    [Micro spacing]
--space-sm:   8px    [Small gaps]
--space-md:   12px   [Button padding]
--space-lg:   16px   [Card gaps]
--space-xl:   20px   [Card padding]
--space-2xl:  24px   [Section spacing]
--space-3xl:  30px   [Large gaps]
```

---

## Border Radius Standards

```
--radius-sm:   6px    [Small buttons, inputs]
--radius-md:   8px    [Medium elements]
--radius-lg:   12px   [Cards, large buttons]
--radius-xl:   15px   [Main cards]
```

---

## Typography Hierarchy

```
H1:  48px (desktop), 32px (mobile) | weight: 800 | spacing: -1px
H2:  32px | weight: 800 | spacing: -0.5px
H3:  24px | weight: 700 | spacing: -0.5px
H4:  20px | weight: 700
H5:  18px | weight: 700
H6:  16px | weight: 700

Body:        16px | weight: 400 | line-height: 1.6
Small:       14px | weight: 500
Extra Small: 12px | weight: 600
```

---

## Navigation Patterns

### Navbar Links
- White text with white underline animation on hover
- Underline slides from left with 0.3s timing
- Scale effect on hover (translateY -2px)

### Dropdown Items
- White text on gradient background
- Slide animation on dropdown appear
- Left border accent on hover
- Padding increases on hover (padding-left adjustment)

---

## Interactive Element Feedback

All interactive elements provide multi-sensory feedback:

1. **Visual**: Color change, shadow enhancement, or scale
2. **Movement**: Translate or scale transform
3. **Timing**: Smooth 0.2-0.3s cubic-bezier animation
4. **Feedback**: Clear indication of clickability

### Transform Hierarchy
```
Large elements:  translateY(-3px)    [strong feedback]
Medium elements: translateY(-2px)    [standard feedback]
Small elements:  scale(1.05-1.08)    [subtle feedback]
Minimal elements: scale(1.02)        [very subtle]
```

---

## Responsive Adjustments

### Desktop (991px+)
- Full navbar gradient
- Backdrop blur effects
- Enhanced shadows
- Smooth animations

### Tablet (768px - 991px)
- Adjusted font sizes
- Reduced spacing
- Same hover patterns
- Touch-friendly buttons

### Mobile (< 768px)
- Simplified animations (reduced motion)
- Larger touch targets (36px minimum)
- Reduced shadows for performance
- Adjusted spacing for compact layout

---

## Performance Notes

✅ GPU-accelerated transforms (translate, scale)
✅ Shadow transitions only on hover
✅ Efficient cubic-bezier curves
✅ Minimal layout shift
✅ No continuous animations during idle
✅ Optimized for 60fps rendering

---

## Accessibility Considerations

- Clear focus states with visible shadow/border
- Sufficient color contrast (WCAG AA compliant)
- Touch targets minimum 36px
- Keyboard navigation support
- Smooth animations (respects prefers-reduced-motion)

---

This design system ensures:
- **Consistency**: Every element follows the same patterns
- **Predictability**: Users know how elements will respond
- **Modernity**: Gradients, shadows, and smooth animations
- **Professionalism**: Cohesive and polished appearance
- **Usability**: Clear feedback on all interactions
