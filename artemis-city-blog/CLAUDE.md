# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Next.js 13 blog application for Artemis City, built with MDX for content authoring, Tailwind CSS for styling, and next-mdx-remote for server-side MDX rendering. The blog uses static site generation (SSG) for optimal performance.

## Development Commands

``` bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run ESLint
npm run lint
```

## Architecture

### Content Management

The project has **two content directories** with different configurations:

-   **`posts/`** - The active content directory used by `lib/post.js`
    -   Supports both `.md` and `.mdx` files
    -   Currently contains marketing and blog content for Artemis City
-   **`content/`** - Legacy directory referenced by `lib/mdx.js` (currently unused)
    -   Was originally configured for `.mdx` files only

**Important**: Blog posts are read from `posts/` directory. The `content/` directory exists but is not currently used in the application.

### Post File Structure

All posts must have frontmatter with these fields:

``` yaml
---
title: "Post Title"
date: "YYYY-MM-DD"
description: "Post description"
author: "Author Name"
---
```

### Data Flow

1.  **Homepage (`pages/index.js`)**:
    -   Calls `getSortedPostsData()` from `lib/post.js` at build time
    -   Renders list using `PostCard` component
    -   Posts are sorted by date (newest first)
2.  **Individual Post Pages (`pages/blog/[slug].js`)**:
    -   Uses dynamic routes with `getStaticPaths()` to generate pages for all posts
    -   Calls `getPostData()` to fetch post content and frontmatter
    -   Serializes MDX content using `next-mdx-remote/serialize`
    -   Renders with `MDXRemote` component using custom `MDXComponents`
3.  **Post Utilities (`lib/post.js`)**:
    -   `getSortedPostsData()` - Returns all posts sorted by date
    -   `getAllPostSlugs()` - Returns slugs for static path generation
    -   `getPostData(slug)` - Returns specific post data with frontmatter and content

### Component Architecture

-   **`Layout.js`** - Main layout wrapper with header/footer (wraps all pages via `_app.js`)
-   **`MDXComponents.js`** - Custom MDX component mapping for styled rendering:
    -   Customized headings (h1, h2) with Tailwind classes
    -   Custom link component that handles internal vs external links
    -   Styled paragraphs, lists, etc.
-   **`PostCard.js`** - Displays post preview cards on homepage

### Styling System

-   Uses Tailwind CSS 3 with `@tailwindcss/typography` plugin
-   Custom color palette defined in `tailwind.config.js`:
    -   primary: `#1A202C`
    -   secondary: `#4A5568`
    -   accent: `#F6AD55`
-   Global styles in `styles/globals.css`

## Working with Posts

### Adding a New Post

1.  Create a new `.md` or `.mdx` file in `posts/` directory
2.  Include proper frontmatter (title, date, description, author)
3.  Write content using Markdown or MDX syntax
4.  The file will automatically be picked up by the build process

### Date Handling Note

There is a known issue where dates may be off by one day between terminal input and display. This is tracked but not yet resolved.

## Configuration Files

-   **`next.config.js`** - Minimal Next.js config with React strict mode enabled
-   **`tailwind.config.js`** - Tailwind configuration with custom theme and typography plugin
-   **`postcss.config.js`** - PostCSS setup for Tailwind

## Important Notes

-   The application uses Next.js 13 with Pages Router (not App Router)
-   All posts use static generation - no ISR or dynamic rendering
-   MDX components can be extended in `components/MDXComponents.js`
-   The build process generates static HTML for all blog posts at build time
