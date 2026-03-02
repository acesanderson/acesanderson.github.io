# GitHub Pages Documentation

Source: https://docs.github.com/en/pages
Fetched: 2026-03-02

---

## Table of Contents

1. [What is GitHub Pages](#what-is-github-pages)
2. [Quickstart](#quickstart)
3. [Creating a Site](#creating-a-site)
4. [Jekyll Setup](#jekyll-setup)
5. [Testing Locally](#testing-locally)
6. [Adding Content](#adding-content)
7. [Custom Domains](#custom-domains)
8. [Verifying Your Domain](#verifying-your-domain)
9. [HTTPS](#https)

---

## What is GitHub Pages

GitHub Pages is a static site hosting service that takes HTML, CSS, and JavaScript files straight from a repository on GitHub, optionally runs the files through a build process, and publishes a website.

### Site Types

| Type | Repo Name | URL |
|------|-----------|-----|
| User/Organization | `<owner>.github.io` | `https://<owner>.github.io` |
| Project | any name | `https://<owner>.github.io/<repo>` |

Each account gets one user/organization site. Each repository can have one project site.

### Availability

- Free plan: public repositories only
- Pro, Team, Enterprise Cloud/Server: public and private repositories

### Limitations

- Does not support server-side languages (PHP, Ruby, Python, etc.)
- Sites are publicly accessible regardless of repository privacy
- Visitor IP addresses are logged for security purposes

---

## Quickstart

1. Create a repository named `<username>.github.io` (must be lowercase)
2. Enable "Add README" and create the repository
3. Go to Settings > Pages
4. Under "Build and deployment", select "Deploy from a branch"
5. Choose your publishing source branch
6. Visit `https://<username>.github.io` (may take up to 10 minutes)

### Minimal `_config.yml`

```yaml
theme: jekyll-theme-minimal
title: Your Site Title
description: Your site description
```

---

## Creating a Site

### Repository naming

- User/org site: must be `<user>.github.io` or `<organization>.github.io`
- Uppercase letters in username must be lowercased

### Entry file resolution order

1. `index.html`
2. `index.md`
3. `README.md`

The entry file must be at the top level of your publishing source.

### Publishing

GitHub Actions workflows handle deployment automatically once a publishing source is configured. Changes take up to 10 minutes to appear after pushing.

### Using non-Jekyll generators

Create a `.nojekyll` file in your repo root to bypass Jekyll processing. For other static site generators, use a custom GitHub Actions workflow.

---

## Jekyll Setup

Jekyll is a static site generator with built-in support for GitHub Pages. It converts Markdown and HTML files into complete sites using layouts.

### Features

- Markdown and Liquid templating support
- Built-in syntax highlighting via Rouge (Pygments-compatible)
- Themes and plugins via `_config.yml`

### GitHub Pages constraints on Jekyll

- Rouge is enforced for syntax highlighting (cannot be changed)
- Safe mode is set to `true`
- Jekyll skips files in `/node_modules`, `/vendor`, and files starting with `_`, `.`, or `#`

### Default plugins

GitHub Pages enables these by default: jekyll-coffeescript, jekyll-gist, jekyll-paginate, and six others.

### Creating a Jekyll site

Prerequisites: Ruby, Bundler, Jekyll, Git

```bash
# In your repo directory
jekyll new --skip-bundle .

# Edit Gemfile: replace the jekyll gem line with:
# gem "github-pages", group: :jekyll_plugins

bundle install
```

Then edit `_config.yml`:

```yaml
# For user site
url: "https://<username>.github.io"
baseurl: ""

# For project site
url: "https://<username>.github.io"
baseurl: "/<repo-name>"
```

Push to GitHub and configure the publishing source under Settings > Pages.

---

## Testing Locally

Prerequisites: Ruby, Bundler, Jekyll installed from jekyllrb.com

```bash
cd <your-site-directory>

# Ruby 3.0+ may need this first:
bundle add webrick

bundle install
bundle exec jekyll serve
```

Site runs at `http://127.0.0.1:4000/`

### Ignore baseurl when testing locally

```bash
bundle exec jekyll serve --baseurl=""
```

### Keep dependencies current

```bash
bundle update github-pages
```

This prevents discrepancies between local and published versions.

---

## Adding Content

### Pages (static content)

Create `PAGE-NAME.md` in the root of your publishing source:

```markdown
---
layout: page
title: "About"
permalink: /about
---

Content goes here.
```

### Posts (blog entries)

Create files in `_posts/` following the naming convention `YYYY-MM-DD-name-of-post.md`:

```markdown
---
layout: post
title: "My First Post"
date: 2026-03-02 12:00:00 -0500
categories: blog
---

Post content goes here.
```

Posts auto-generate URLs: `<site-url>/YYYY/MM/DD/title.html`

---

## Custom Domains

Source: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site

### Supported domain types

- Apex domain: `example.com`
- www subdomain: `www.example.com`
- Custom subdomain: `blog.example.com`

GitHub recommends always using a `www` subdomain even if you also use an apex domain.

### DNS Configuration

**Apex domain** — add `A` records pointing to GitHub's IPs:

```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

Or use `ALIAS`/`ANAME` records pointing to `<username>.github.io`.

Optional IPv6 support via `AAAA` records.

**Subdomain** — add a `CNAME` record:

```
www  CNAME  <username>.github.io
```

### Adding the domain in GitHub

1. Go to repository Settings > Pages
2. Enter your custom domain and save
3. A `CNAME` file is automatically committed to your repo

### DNS propagation

Changes can take up to 24 hours. Verify with:

```bash
# For apex domain
dig example.com +noall +answer

# For www subdomain
dig www.example.com +noall +answer
```

### Cross-repository domain behavior

When a custom domain is set on a user/org site, all project sites under that account inherit it by default. Example: if user site uses `www.example.com`, the `my-project` repo is accessible at `www.example.com/my-project`.

### Security warning

If your GitHub Pages site is disabled but has a custom domain set, it is at risk of domain takeover. Verify your domain (see below) and remove DNS records promptly if you disable the site. Avoid wildcard DNS records (`*.example.com`).

---

## Verifying Your Domain

Source: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages

Verifying prevents other GitHub users from using your domain even if your repo is deleted or your plan changes.

### Steps (user site)

1. Go to GitHub profile Settings > Pages (not repo settings)
2. Click "Add a domain"
3. Enter your domain and click "Add domain"
4. Create a DNS TXT record with the values provided by GitHub
5. Wait up to 24 hours for DNS propagation
6. Verify with dig:

```bash
dig _github-pages-challenge-USERNAME.example.com +nostats +nocomments +nocmd TXT
```

7. Click "Verify" in GitHub settings

Keep the TXT record in your DNS permanently to maintain verification.

---

## HTTPS

Source: https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https

### Enforcing HTTPS

1. Go to repository Settings > Pages
2. Check "Enforce HTTPS"

Requires admin permissions. Domain name must be under 64 characters.

### Certificate provisioning

GitHub automatically requests a TLS certificate from Let's Encrypt when you set or change a custom domain. If it doesn't complete within a few minutes, remove and re-add the domain to restart provisioning.

**Note:** Additional A, AAAA, ALIAS, or ANAME records with `@` host can block certificate generation for apex domains.

### Mixed content

If HTTPS is enforced but assets still load over HTTP, update all asset references from `http://` to `https://` — particularly in `<head>` for CSS/JS and `<body>` for images.

---

## Notes

- GitHub Pages is not suitable for sensitive transactions (passwords, payment info)
- Recommended deployment: GitHub Actions (replaces the older `github-pages` gem approach)
- Unsupported plugins require generating the site locally and pushing the built output
