# PRD-03: Design System Specifications

## Design Philosophy

The GAS website should look like it was designed by:
- A government contractor
- In the early 2040s
- With accessibility as a primary requirement
- With zero budget for "creativity"
- By people who have never heard of "delight"

The result: **Functional. Accessible. Forgettable. Trustworthy.**

---

## Color Palette

### Primary Colors

| Name | Hex | Usage |
|------|-----|-------|
| GAS Blue | `#1a4480` | Primary brand color, headers, links |
| GAS Blue Dark | `#0c2d5b` | Header backgrounds, footer |
| GAS Blue Light | `#4a77b4` | Hover states, secondary elements |

### Neutral Colors

| Name | Hex | Usage |
|------|-----|-------|
| White | `#ffffff` | Page backgrounds |
| Gray 5 | `#f0f0f0` | Alternate row backgrounds, cards |
| Gray 10 | `#e6e6e6` | Borders, dividers |
| Gray 30 | `#adadad` | Disabled states, metadata |
| Gray 50 | `#757575` | Secondary text |
| Gray 90 | `#1b1b1b` | Primary text |
| Black | `#000000` | Headings (sparingly) |

### Accent Colors

| Name | Hex | Usage |
|------|-----|-------|
| Success Green | `#00a91c` | Success states, active status |
| Warning Yellow | `#ffbe2e` | Warnings, pending status |
| Error Red | `#d54309` | Errors, deprecated status |
| Info Blue | `#00bde3` | Information callouts |

### Usage Rules

1. **80% of the page should be white/gray**
2. **Blue used only for interactive elements and headers**
3. **Accent colors used sparingly for status indicators**
4. **Never use gradients**
5. **Never use shadows (except subtle card shadows if necessary)**

---

## Typography

### Font Stack

```css
font-family: 'Source Sans Pro', 'Helvetica Neue', Helvetica, Arial, sans-serif;
```

**Rationale**: Source Sans Pro is the US Web Design System font. It reads as "government" immediately.

**Fallback**: If not using Source Sans Pro, use system fonts:
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
```

### Type Scale

| Element | Size | Weight | Line Height | Letter Spacing |
|---------|------|--------|-------------|----------------|
| H1 | 40px / 2.5rem | 700 | 1.2 | -0.015em |
| H2 | 32px / 2rem | 700 | 1.25 | -0.01em |
| H3 | 24px / 1.5rem | 700 | 1.3 | 0 |
| H4 | 20px / 1.25rem | 700 | 1.4 | 0 |
| H5 | 18px / 1.125rem | 700 | 1.4 | 0 |
| H6 | 16px / 1rem | 700 | 1.5 | 0 |
| Body | 16px / 1rem | 400 | 1.625 | 0 |
| Body Small | 14px / 0.875rem | 400 | 1.5 | 0 |
| Caption | 12px / 0.75rem | 400 | 1.4 | 0.02em |

### Typography Rules

1. **Maximum line length: 75 characters** (for readability)
2. **Paragraph spacing: 1.5em**
3. **No justified text** (causes accessibility issues)
4. **Left-aligned text only** (except centered hero text)
5. **No italics for emphasis** (use bold sparingly)

---

## Layout Grid

### Container Widths

| Breakpoint | Container Max Width | Side Padding |
|------------|---------------------|--------------|
| Mobile (<640px) | 100% | 16px |
| Tablet (640-1024px) | 100% | 24px |
| Desktop (1024-1400px) | 1200px | 32px |
| Wide (>1400px) | 1400px | 32px |

### Grid System

- 12-column grid
- Gutter width: 24px
- Column ratio: flexible

### Content Width Zones

| Zone | Width | Usage |
|------|-------|-------|
| Narrow | 680px max | Long-form text content |
| Medium | 880px max | Mixed content |
| Wide | 1200px max | Tables, multi-column layouts |
| Full | 100% | Header, footer, hero sections |

---

## Components

### Header

```
┌─────────────────────────────────────────────────────────────┐
│ [GAS LOGO]  Global Agents System                    [Search]│
├─────────────────────────────────────────────────────────────┤
│ Home | About ▼ | Protocols ▼ | Research ▼ | Docs ▼ | Contact│
└─────────────────────────────────────────────────────────────┘
```

- Height: 120px total (logo bar + nav bar)
- Background: White (logo bar), GAS Blue Dark (nav bar)
- Logo: Left-aligned
- Search: Right-aligned (optional)
- Navigation: Full-width bar below logo

### Footer

```
┌─────────────────────────────────────────────────────────────┐
│ About | Protocols | Research | Documentation | News         │
├─────────────────────────────────────────────────────────────┤
│ Privacy Policy | Terms of Use | Accessibility Statement     │
├─────────────────────────────────────────────────────────────┤
│ © 2039-2047 Global Agents System Consortium. All rights    │
│ reserved. THR Global Agents System is an international      │
│ consortium dedicated to agent alignment standards.          │
└─────────────────────────────────────────────────────────────┘
```

- Background: Gray 5
- Text: Gray 50
- Three rows: Nav links, Legal links, Copyright
- Padding: 48px top/bottom

### Breadcrumbs

```
Home > About > History
```

- Separator: `>`
- Current page: Not linked, bold
- Position: Below header, above page title

### Buttons

| Type | Background | Text | Border |
|------|------------|------|--------|
| Primary | GAS Blue | White | None |
| Secondary | White | GAS Blue | GAS Blue 2px |
| Tertiary | Transparent | GAS Blue | None |

- Border radius: 4px
- Padding: 12px 24px
- Font weight: 600
- No shadows
- No gradients

### Cards

- Background: White
- Border: 1px solid Gray 10
- Border radius: 4px
- Padding: 24px
- Shadow: None (or very subtle: `0 1px 2px rgba(0,0,0,0.05)`)

### Tables

- Header background: Gray 5
- Header text: Bold, Gray 90
- Row borders: 1px solid Gray 10
- Alternate row background: Gray 5 (optional)
- Cell padding: 12px 16px

### Forms

- Input height: 44px (accessibility minimum)
- Border: 1px solid Gray 30
- Border radius: 4px
- Focus: 2px solid GAS Blue outline
- Label position: Above input
- Required indicator: Red asterisk

### Alerts/Callouts

| Type | Left Border | Background | Icon |
|------|-------------|------------|------|
| Info | Info Blue | Light blue tint | ℹ |
| Success | Success Green | Light green tint | ✓ |
| Warning | Warning Yellow | Light yellow tint | ⚠ |
| Error | Error Red | Light red tint | ✕ |

- Left border width: 4px
- Padding: 16px 20px
- Border radius: 4px (right side only)

---

## Iconography

### Icon Style
- Line icons only (no filled icons)
- Stroke width: 1.5px
- Size: 24px default, 20px small, 32px large
- Color: Inherits text color

### Required Icons
- Search (magnifying glass)
- Menu (hamburger)
- Close (X)
- Chevron (navigation dropdowns)
- External link (arrow pointing out)
- Download (arrow pointing down)
- Document (page icon)
- PDF (document with "PDF" label)
- Info (circled i)
- Warning (triangle with !)
- Success (checkmark)
- Error (X in circle)

### Icon Source
Recommend: Heroicons (MIT license) or Feather Icons (MIT license)

---

## Responsive Behavior

### Breakpoints

| Name | Width | Behavior |
|------|-------|----------|
| Mobile | <640px | Single column, hamburger menu |
| Tablet | 640-1024px | 2 columns, may use hamburger |
| Desktop | 1024-1400px | Full layout, horizontal nav |
| Wide | >1400px | Full layout, centered container |

### Mobile Adaptations

1. **Navigation**: Collapses to hamburger menu
2. **Tables**: Horizontal scroll or card layout
3. **Multi-column**: Stacks to single column
4. **Images**: Scale to 100% width
5. **Footer**: Stacks vertically

---

## Accessibility Requirements

### WCAG 2.1 AA Compliance

1. **Color contrast**: 4.5:1 minimum for normal text, 3:1 for large text
2. **Focus indicators**: Visible 2px outline on all interactive elements
3. **Touch targets**: Minimum 44x44px
4. **Skip links**: "Skip to main content" link at top
5. **Heading hierarchy**: Proper H1-H6 nesting, no skipped levels
6. **Alt text**: Descriptive alt text for all images
7. **ARIA labels**: For icons and non-text interactive elements
8. **Keyboard navigation**: Full site navigable by keyboard
9. **Screen reader**: All content accessible via screen reader
10. **Motion**: Respect `prefers-reduced-motion`

### Testing Requirements

- Automated: axe, WAVE, Lighthouse
- Manual: Keyboard-only navigation test
- Screen reader: VoiceOver (Mac) or NVDA (Windows) testing

---

## Logo Specifications

### GAS Logo Concept

The logo should be:
- Abstract geometric mark (circle, hexagon, or similar)
- Suggests "interconnection" or "framework"
- Works at small sizes (favicon)
- Works in single color
- Looks like it could be a UN agency logo

### Logo Variants

1. **Full logo**: Mark + "Global Agents System" wordmark
2. **Compact logo**: Mark + "GAS" acronym
3. **Mark only**: For favicon, small spaces
4. **Monochrome**: For documents, one-color printing

### Logo Clear Space

Minimum clear space around logo: Height of the mark on all sides

### Logo Minimum Sizes

- Full logo: 200px wide minimum
- Compact logo: 100px wide minimum
- Mark only: 32px minimum

---

## Animation Guidelines

### General Rule
**Minimal to no animation.** Government sites don't animate.

### Acceptable Animation
1. **Hover states**: Color change, underline (instant or <100ms)
2. **Focus states**: Outline appearance (instant)
3. **Dropdown menus**: Opacity fade (150ms max)
4. **Page transitions**: None

### Forbidden Animation
- Parallax scrolling
- Loading spinners that are decorative
- Bouncing elements
- Sliding panels
- Any animation >300ms
- Any animation that conveys no information
