# Project Overview

This is a blog built with Next.js, a popular React framework for building server-rendered and statically generated web applications. The blog uses Markdown (specifically MDX) for writing posts, which allows for embedding JSX components within the content. Styling is done with Tailwind CSS, a utility-first CSS framework.

## Building and Running

To work with this project, you'll need to have Node.js and either `npm` or `yarn` installed.

1.  **Install dependencies:**
    ```bash
    npm install
    # or
    yarn install
    ```

2.  **Run the development server:**
    ```bash
    npm run dev
    # or
    yarn dev
    ```
    This will start the development server on `http://localhost:3000`.

3.  **Build for production:**
    ```bash
    npm run build
    # or
    yarn build
    ```
    This will create an optimized production build of the application in the `.next` directory.

4.  **Start the production server:**
    ```bash
    npm run start
    # or
    yarn start
    ```
    This will start the production server.

5.  **Lint the code:**
    ```bash
    npm run lint
    # or
    yarn lint
    ```
    This will run ESLint to check for any code quality issues.

## Development Conventions

*   **Content:** Blog posts are written in Markdown (`.md` or `.mdx`) and stored in the `posts` directory.
*   **Frontmatter:** Each post can have a frontmatter section at the top of the file to define metadata like `title`, `date`, and `description`.
*   **Static Generation:** The blog posts are statically generated at build time using Next.js's `getStaticProps` and `getStaticPaths` functions.
*   **Styling:** Styling is done using Tailwind CSS. The configuration is in `tailwind.config.js`.
*   **Components:** Reusable React components are located in the `components` directory.
*   **Custom MDX Components:** You can customize the rendering of Markdown elements by editing the `components/MDXComponents.js` file.

---

## Agent Changelog

### 2025-12-06 - Modern Theme Update with Navigation Tabs (Claude Code)

**Changes Made:**
1. **Tailwind Configuration (`tailwind.config.js`)**
   - Updated color palette with modern primary, secondary, and accent colors (blue, slate, and amber)
   - Added custom animations: fadeInUp, fadeIn, slideIn
   - Added custom shadows: soft shadow and glow effect
   - Configured Inter font family with system fallbacks

2. **Layout Component (`components/Layout.js`)**
   - Added sticky header with glassmorphism effect (backdrop blur)
   - Implemented navigation tabs: Home, Blog, About, Contact
   - Added active state highlighting for current page
   - Modernized footer with 3-column grid layout
   - Integrated Google Fonts (Inter) for better typography
   - Added gradient text logo with hover effects

3. **Global Styles (`styles/globals.css`)**
   - Organized styles using Tailwind's @layer directives
   - Added smooth scroll behavior
   - Enhanced scrollbar styling with modern colors
   - Created reusable component classes: btn-primary, btn-secondary, card, glass
   - Added text gradient utility classes

4. **New Pages Created:**
   - **About Page (`pages/about.js`)** - Company vision, values, and what we do
   - **Contact Page (`pages/contact.js`)** - Contact form with business information
   - **Blog Listing Page (`pages/blog.js`)** - Dedicated page showing all blog posts

5. **Homepage (`pages/index.js`)**
   - Redesigned hero section with gradient text and modern badge
   - Added 3-column feature section highlighting Innovation, Sustainability, and Community
   - Limited to showing 6 latest posts with "View All Posts" link
   - Improved call-to-action buttons with modern styling

6. **PostCard Component (`components/PostCard.js`)**
   - Wrapped entire card in Link for better UX
   - Added colored top border with gradient
   - Implemented hover effects: lift animation, border color change, gap increase
   - Added author badge and improved date formatting
   - Enhanced typography and spacing

**Design System:**
- Primary Color: Sky blue (#0ea5e9 and variants)
- Secondary Color: Slate gray (#64748b and variants)
- Accent Color: Amber/gold (#d97706 and variants)
- Typography: Inter font family
- Border Radius: Mostly 2xl (1rem) for modern, rounded look
- Shadows: Soft, subtle shadows that lift on hover
- Animations: Smooth fade-in and slide effects

**Navigation Structure:**
- Home (/) - Landing page with featured posts
- Blog (/blog) - All blog posts
- About (/about) - Company information
- Contact (/contact) - Contact form and details

**Development Server:**
- Successfully tested on http://localhost:3001 (port 3000 was in use)
