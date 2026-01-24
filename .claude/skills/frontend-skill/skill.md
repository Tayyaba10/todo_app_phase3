---
name: frontend-skill
description: Build frontend interfaces including pages, reusable components, layouts, and styling.
---

# Frontend Skill

## Instructions

1. **Page Structure**
   - Define page-level layouts
   - Organize routes and views
   - Separate public and protected pages
   - Ensure consistent navigation

2. **Component Design**
   - Build reusable UI components
   - Follow component-based architecture
   - Manage props and state
   - Keep components small and focused

3. **Layout System**
   - Use grid or flexbox for layout
   - Create responsive designs
   - Maintain spacing and alignment
   - Support mobile, tablet, and desktop views

4. **Styling**
   - Apply consistent color schemes
   - Use typography hierarchy
   - Style components with CSS / Tailwind / styled-components
   - Handle dark and light themes

## Best Practices
- Reuse components instead of duplicating UI
- Keep styles consistent across pages
- Design mobile-first
- Avoid inline styling for large components
- Follow accessibility (a11y) standards
- Optimize UI for performance

## Example Structure

### Page Layout
```html
<main class="layout">
  <Navbar />
  <section class="content">
    <h1>Dashboard</h1>
  </section>
</main>
