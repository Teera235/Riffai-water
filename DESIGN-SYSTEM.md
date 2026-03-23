# RIFFAI Design System

## Overview
Professional black and white monochrome design system for the RIFFAI water management platform.

## Color Palette

### Primary (Grayscale)
```
primary-50:  #f8f9fa  (Lightest backgrounds)
primary-100: #f1f3f5  (Light backgrounds)
primary-200: #e9ecef  (Borders, dividers)
primary-300: #dee2e6  (Disabled states)
primary-400: #ced4da  (Placeholders)
primary-500: #adb5bd  (Secondary text)
primary-600: #868e96  (Body text)
primary-700: #495057  (Headings)
primary-800: #343a40  (Dark text)
primary-900: #212529  (Primary text, buttons)
primary-950: #0d0f12  (Darkest)
```

### Accent
```
accent-light: #ffffff (White)
accent:       #000000 (Black)
accent-dark:  #0a0a0a (Near black)
```

## Typography

### Fonts
- **Sans-serif**: Inter (300, 400, 500, 600, 700, 800)
- **Monospace**: JetBrains Mono (400, 500, 600)

### Usage
- Headings: `font-sans font-semibold tracking-tight`
- Body: `font-sans`
- Data/Metrics: `font-mono`
- Labels: `font-sans font-semibold uppercase tracking-wider`

## Components

### Buttons

#### Primary Button (btn-mono)
```tsx
<button className="btn-mono">
  <Icon className="w-4 h-4" />
  Button Text
</button>
```
- Background: `bg-primary-900`
- Text: `text-white`
- Border: `border-primary-900`
- Hover: `hover:bg-primary-800`

#### Outline Button (btn-mono-outline)
```tsx
<button className="btn-mono-outline">
  Button Text
</button>
```
- Background: `bg-transparent`
- Text: `text-primary-900`
- Border: `border-primary-900`
- Hover: `hover:bg-primary-900 hover:text-white`

#### Ghost Button (btn-mono-ghost)
```tsx
<button className="btn-mono-ghost">
  Button Text
</button>
```
- Background: `bg-transparent`
- Text: `text-primary-700`
- Hover: `hover:bg-primary-100`

### Cards

#### Standard Card (card-mono)
```tsx
<div className="card-mono p-6">
  Content
</div>
```
- Background: `bg-white`
- Border: `border border-primary-200`
- Border radius: `rounded-mono` (2px)
- Shadow: `shadow-mono`

#### Hover Card (card-mono-hover)
```tsx
<div className="card-mono-hover p-6">
  Content
</div>
```
- Adds hover effects: `hover:shadow-mono-lg hover:border-primary-300`

### Inputs

#### Text Input (input-mono)
```tsx
<input type="text" className="input-mono" />
```
- Background: `bg-white`
- Border: `border-primary-300`
- Focus: `focus:ring-2 focus:ring-primary-900`

### Badges

#### Status Badges
```tsx
<span className="badge-critical">CRITICAL</span>
<span className="badge-warning">WARNING</span>
<span className="badge-normal">NORMAL</span>
<span className="badge-safe">SAFE</span>
```

### Tables

#### Professional Table (table-mono)
```tsx
<table className="table-mono">
  <thead>
    <tr>
      <th>Header</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Data</td>
    </tr>
  </tbody>
</table>
```

## Icons

### Library
Lucide React - Professional, consistent SVG icons

### Common Icons
- **Navigation**: `LayoutDashboard`, `Map`, `TrendingUp`, `AlertTriangle`, `FileText`
- **Data**: `Droplets`, `CloudRain`, `Layers`, `Database`
- **Actions**: `RefreshCw`, `Download`, `Search`, `Settings`
- **Status**: `CheckCircle`, `Eye`, `AlertTriangle`, `AlertOctagon`
- **UI**: `Calendar`, `Clock`, `MapPin`, `Maximize2`, `Target`, `Cpu`

### Icon Sizing
- **Large (Headers)**: `w-9 h-9` with `strokeWidth={2.5}`
- **Medium (Inline)**: `w-5 h-5` or `w-6 h-6` with `strokeWidth={2}`
- **Small (Icons)**: `w-4 h-4` or `w-3.5 h-3.5` with `strokeWidth={2}`

### Usage Example
```tsx
import { Brain, Settings } from "lucide-react";

<Brain className="w-6 h-6 text-primary-900" strokeWidth={2.5} />
```

## Shadows

```css
shadow-mono:    0 2px 8px rgba(0, 0, 0, 0.08)
shadow-mono-lg: 0 4px 16px rgba(0, 0, 0, 0.12)
shadow-mono-xl: 0 8px 32px rgba(0, 0, 0, 0.16)
```

## Border Radius

```css
rounded-mono: 2px (Sharp, professional corners)
```

## Animations

### Slide Up
```tsx
<div className="animate-slide-up">
  Content
</div>
```

### Pulse Mono
```tsx
<div className="animate-pulse-mono">
  Content
</div>
```

### Spin (Loading)
```tsx
<Loader2 className="w-6 h-6 animate-spin" />
```

## Layout Patterns

### Page Header
```tsx
<div className="mb-8 pb-6 border-b-2 border-primary-900">
  <h1 className="text-4xl font-bold text-primary-900 tracking-tight flex items-center gap-3">
    <Icon className="w-9 h-9" strokeWidth={2.5} />
    Page Title
  </h1>
  <p className="text-sm text-primary-600 mt-2 font-mono">
    Subtitle or description
  </p>
</div>
```

### Section Header
```tsx
<h2 className="text-2xl font-bold mb-6 text-primary-900 tracking-tight flex items-center gap-2">
  <Icon className="w-6 h-6" />
  Section Title
</h2>
```

### Stat Card
```tsx
<div className="card-mono p-5">
  <div className="w-10 h-10 bg-primary-900 flex items-center justify-center mb-3">
    <Icon className="w-5 h-5 text-white" strokeWidth={2.5} />
  </div>
  <div className="text-xs font-semibold text-primary-600 uppercase tracking-wider mb-2">
    Label
  </div>
  <div className="text-3xl font-bold text-primary-900 tracking-tight">
    Value
  </div>
</div>
```

## Data Visualization

### Flood Depth Legend
```tsx
import FloodDepthLegend from "@/components/prediction/FloodDepthLegend";

<FloodDepthLegend />
```

Shows:
- Area (m²)
- Volume (m³)
- Depth (m) with color scale

### Color Scale
- **High (2.5m)**: `bg-primary-900` (Black)
- **Medium (1.5m)**: `bg-primary-600` (Dark gray)
- **Low (0.5m)**: `bg-primary-300` (Light gray)
- **None (0m)**: `bg-primary-100` (Very light gray)

## Best Practices

### Do's
✅ Use monospace fonts for data, metrics, and technical information
✅ Use consistent icon sizing and stroke width
✅ Maintain 2px border radius for all elements
✅ Use uppercase labels with tracking-wider for section headers
✅ Keep animations subtle and purposeful
✅ Use semantic HTML elements
✅ Ensure proper contrast ratios (WCAG AA minimum)

### Don'ts
❌ Don't use emojis (use Lucide icons instead)
❌ Don't use colors other than grayscale
❌ Don't use rounded corners (use sharp 2px)
❌ Don't mix font families within components
❌ Don't use gradients or shadows excessively
❌ Don't use animations for decorative purposes

## Accessibility

- All interactive elements have focus states
- Color contrast meets WCAG AA standards
- Icons have appropriate aria-labels when needed
- Form inputs have associated labels
- Tables have proper semantic structure

## Responsive Design

- Mobile-first approach
- Breakpoints: `sm:`, `md:`, `lg:`, `xl:`
- Grid layouts adapt to screen size
- Touch-friendly tap targets (min 44x44px)

## File Structure

```
src/
├── app/
│   ├── globals.css          # Global styles & utilities
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Dashboard
│   ├── map/page.tsx         # Map view
│   ├── predict/page.tsx     # AI Prediction
│   ├── alerts/page.tsx      # Alerts
│   └── reports/page.tsx     # Reports
├── components/
│   ├── common/
│   │   ├── Navbar.tsx
│   │   ├── StatCard.tsx
│   │   └── RiskBadge.tsx
│   ├── dashboard/
│   │   └── BasinCard.tsx
│   ├── charts/
│   │   ├── WaterLevelChart.tsx
│   │   └── RainfallChart.tsx
│   └── prediction/
│       └── FloodDepthLegend.tsx
└── tailwind.config.ts       # Tailwind configuration
```

## Version
Design System v1.0 - March 2026
