# Agent Work Log
- 2025-12-05 21:19:37 EST — aligned imports to `lib/post`, documented contributors in `AGENTS.md`, and added this log entry.
- 2025-12-05 21:22:26 EST — renamed `components/PostCard.js`, cleaned `pages/_document.js`, and attempted `npm run build` (blocked by sandbox port listen EPERM).
- 2025-12-05 21:24:00 EST — expanded `lib/post.js` to support `.md` and `.mdx` slugs so prerendering finds all posts.
- 2025-12-05 21:26:04 EST — rewrote `posts/envisioining-artemis-citys-future.mdx` with valid MDX and interactive vote component to resolve prerender compile error.
- 2025-12-05 21:28:37 EST — adjusted MDX component definition to use `export function` syntax to satisfy mdx-remote parsing.
- 2025-12-05 21:43:31 EST — fully reformatted `posts/envisioining-artemis-citys-future.mdx` to clean JSX/MDX; build now compiles before sandbox port listen EPERM.
