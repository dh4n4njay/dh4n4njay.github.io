# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Personal academic website for Dhananjay (PhD scholar, fluorescent materials, Central University of Kerala), served by GitHub Pages at dh4n4njay.github.io. Pushing to `main` deploys it.

## Structure

Two files: `index.html` (markup plus inline JS in a `<script>` block) and `style.css`. There is no build step, no dependencies, no tests. Preview by opening `index.html` in a browser (or `python3 -m http.server`).

Conventions:
- Theming uses CSS custom properties on `:root` (dark, the default) with a `[data-theme="light"]` override block. Any new color must be defined in both. The theme toggle persists to `localStorage`.
- Content lives in `<section>` elements (`#about`, `#research`, `#conferences`, `#publications`, `#blog`, `#contact`); nav links, scroll-spy, and reveal-on-scroll animations key off section `id`s, so adding a section means adding a matching nav `<li>`.
- Conference/publication entries follow the `.item` pattern (numbered `.item-num`, `.meta` line); research/blog entries use `.card`. Copy an existing sibling when adding one.
