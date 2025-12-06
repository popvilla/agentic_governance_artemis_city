# Repository Guidelines

## Project Structure & Module Organization
- `pages/` holds Next.js routes (`pages/index.js` for the feed, `pages/blog/[slug].js` for post detail rendering).
- `components/` contains shared UI (e.g., `Layout`, `MDXComponents`, `PostCard`) built with Tailwind utility classes.
- `lib/` provides data helpers: `post.js` reads `/posts` MDX/MD content; `mdx.js` targets `/content` for alternate MDX sources.
- `posts/` is the primary home for published articles; `content/` can house drafts or experiments; `public/` stores static assets referenced by posts.
- Global styles live in `styles/globals.css`; Tailwind/PostCSS configuration sits in `tailwind.config.js` and `postcss.config.js`.

## Build, Test, and Development Commands
- `npm install` syncs dependencies (`package-lock.json` is present; prefer npm).
- `npm run dev` starts the local server at http://localhost:3000 with hot reload.
- `npm run build` creates the production bundle and surfaces MDX/build-time errors.
- `npm start` serves the built app locally.
- `npm run lint` runs Next/ESLint checks for JS/React/Tailwind usage.

## Coding Style & Naming Conventions
- JavaScript + React function components, 2-space indentation, and semicolons; keep hooks at the top of components.
- Components use PascalCase names; helper exports from `lib/` use camelCase; prefer co-locating UI logic in `components/`.
- MDX files in `posts/` use kebab-case filenames for stable slugs and include front matter: `title`, ISO `date`, `description`, optional `author`.
- Use `next/link` for internal navigation; route rich content through `components/MDXComponents` instead of ad-hoc HTML when possible.

## Testing Guidelines
- No automated test suite yet; always run `npm run lint` before pushing.
- Manually verify key flows: home feed renders cards, blog detail pages render MDX content, and dates format correctly.
- When adding data helpers or complex UI, consider adding lightweight Jest/Testing Library coverage or document manual checks in the PR.

## Commit & Pull Request Guidelines
- Keep commits concise and imperative (e.g., `Add MDX card animation`, `Fix post slug parsing`); wrap body lines near 72 chars when used.
- PRs should summarize intent, list commands/tests run (`npm run lint`, `npm run build`), and attach screenshots for UI changes.
- Link related issues/tickets and note content moves (new files in `posts/` or assets in `public/`) to aid reviewers.
- Preserve slug stability when renaming or relocating posts to avoid broken links.
