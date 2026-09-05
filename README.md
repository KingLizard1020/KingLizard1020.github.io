# kailashnelson.github.io

Personal site for [Kailash Nelson](https://kailashnelson.com), hosted on GitHub Pages.

The GitHub account is `KingLizard1020`, so the user-site repo is `KingLizard1020.github.io`. The custom domain is `kailashnelson.com`.

- Home is a web version of the resume (`/` — not `index.html`)
- Projects and About are short extra pages
- Writing is a Jekyll blog at `/blog/`
- [Kailash_Nelson_Resume.pdf](Kailash_Nelson_Resume.pdf) is the downloadable resume
- Footer “Last updated” is filled from the latest commit on this repo via the GitHub API

## Writing

GitHub Pages already runs Jekyll, so posting is a Markdown file rather than a custom generator.

1. Create `_posts/YYYY-MM-DD-slug.md`
2. Add front matter:

   ```yaml
   ---
   layout: post
   title: The title
   date: YYYY-MM-DD
   ---
   ```

3. Write Markdown under that, then push to `main`. The post is at `/blog/YYYY/MM/DD/slug/`.

Do not add front matter to `index.html`, `projects.html`, `about.html`, or `404.html`. Jekyll copies those through as static files.

`_layouts/`, `_posts/`, and `blog/index.html` are Liquid templates. CI `html-validate` and `scripts/check-site.py` only check the static HTML pages.

Copyright (c) 2026 Kailash Nelson. All rights reserved. See [LICENSE](LICENSE).
