# LivePPT Starter Template (Distinct Style)

This starter is designed to be **premium but clearly different** from creator-origin styles.

## Style Direction

- Visual language: structured command-board + restrained gradient lighting.
- Information rhythm: left narrative rail + center hero scene + right proof metrics.
- Motion pattern: short slide/fade transitions, no heavy blur stacking.

## Why It Is Intentionally Different

- Avoids glass-first composition as the dominant motif.
- Uses panel geometry and tokenized spacing instead of floating card clusters.
- Emphasizes enterprise decision readability over decorative effects.

## Included Files

- `App.tsx`: click-through scene system with keyboard navigation.
- `styles.css`: theme tokens + layout + transitions.
- `DIFFERENTIATION.md`: explicit anti-clone style guardrails.

## Quick Use (Vite React)

```bash
npm create vite@latest liveppt-demo -- --template react-ts
cd liveppt-demo

# replace src/App.tsx and src/index.css
cp <this-template>/App.tsx src/App.tsx
cp <this-template>/styles.css src/index.css

npm install
npm run dev
```

## Interaction Rules

- `←` / `→`: previous/next scene.
- Scene rail click: direct jump.
- Theme switch: runtime style swap without content change.
