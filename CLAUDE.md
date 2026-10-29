# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static HTML personal portfolio and blog for Ephraiem Sarabamoun, hosted on GitHub Pages at **www.scipolitic.com**. No build system, no static site generator, no JavaScript — just hand-coded HTML and CSS served directly by GitHub Pages.

## Deployment

Push to `main` branch deploys automatically via GitHub Pages. No build step, CI/CD, or processing pipeline. The CNAME file maps to www.scipolitic.com.

## Architecture

- **`index.html`** is the homepage with the profile, the bio, profile links and navigation to Writings, Papers and Projects.
- **`writings.html`** is the blog listing page, a table layout where highlighted rows use `bgcolor="#ffffd0"`.
- **`papers.html`** lists his papers, newest first, one table row per paper (title link, authors, venue and year, short summary).
- **`projects.html`** lists his projects, newest first, one table row per project (title link, date, short description, then a row of GitHub, demo or dataset links).
- **`posts/blog[N].html`** holds the blog posts, blog1 to blog21. There is no blog13, because it was renamed to blog14 to bust a cache.
- **`styles.css`** is the single stylesheet for the entire site (Lato font via Google Fonts).
- **`images/`** holds all image assets, named `blog[N]img[M].[ext]` plus `profilepic.jpg`.
- **`Human.md`** explains the site in plain words for people reading the repo.

## Content Rules

Site copy is public. Use only facts Ephraiem has made public. Never add private details such as application outcomes, a pending employer, health, money, home address, phone, birth date, family, or the names of private repos. Link only public URLs, and check that each GitHub repo you link is public.

## Adding a New Blog Post

1. Create `posts/blog[N+1].html` following the existing post template structure:
   - `div.blog-container` wrapper
   - Back link to `../writings.html`
   - `h1.blog-title`, `p.blog-meta` (date + author), optional `img.blog-image`, `div.blog-content`
   - Closing back link
2. Add a corresponding entry row in `writings.html` (newest posts go at the top of the table)
3. Place any images in `images/` using the `blog[N]img[M].[ext]` naming convention

## Styling Conventions

- Links: `#1772d0` (blue), hover: `#f09228` (orange)
- Highlighted/featured rows in writings.html: `bgcolor="#ffffd0"`
- Layout uses nested HTML tables (not CSS grid/flexbox) — maintain this pattern for consistency
- Blog posts use CSS classes from `styles.css`; main pages use mostly inline styles

## Design Attribution

Design inspired by [Samuel Schmidgall's repo](https://github.com/SamuelSchmidgall/SamuelSchmidgall.github.io), itself based on [jonbarron.info](https://jonbarron.info/).
