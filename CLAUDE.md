# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Personal academic website for Dhananjay (PhD scholar, fluorescent materials, Central University of Kerala), served by GitHub Pages at dh4n4njay.github.io. Pushing to `main` deploys it.

## Structure

Two files: `index.html` (markup plus inline JS in a `<script>` block) and `style.css`. There is no build step, no dependencies, no tests. Preview by opening `index.html` in a browser (or `python3 -m http.server`).

Conventions:
- Design system: "fluorescence lab" theme — tokens on `:root` in `style.css` (dark, the default; `--emission` green is the accent, `--excitation` violet only for signature graphics) with a `[data-theme="light"]` override block. Any new color must be defined in both blocks. The navbar toggle persists to `localStorage`; the hero canvas reads its colors from the active theme. Fonts: Spectral (display), IBM Plex Sans (body), IBM Plex Mono (labels/dates/meta).
- The site is a full-viewport hero plus page-switching sections: no hash → hero only; `#id` → that `<main> > section` shown below the hero and scrolled to (hash router in the inline `<script>`). Adding a section means adding a matching `.nav-links` anchor.
- Signature graphics: the hero has a canvas molecular network (`#mol-canvas`, honors `prefers-reduced-motion`) and an absorption/emission spectra SVG (`.spectra`); the Blog section has three animated Jablonski diagram videos (`assets/media/{fluorescence,phosphorescence,tadf}.mp4`), rendered with Manim from the three scenes in `assets/media/jablonski.py` (`manim -qm --fps 30 jablonski.py <SceneName>`).
- Entry patterns to copy when adding content: education uses `.timeline` items; publications `.pub-item`; conferences `.conf-card` grouped under `.group-heading` sub-sections (Talks / Posters / Participation; add `contributed` class to the type pill for posters/talks; certificate PDFs live in `assets/certificates/` linked with `.pub-link`); research/skills use `.card` (research cards hold a `<details>` "Read more"); blog uses `.blog-card`.
- Placeholder content the owner still needs to fill in is marked with `<!-- TODO: ... -->` comments (degree details, research writeups).
