# mdnet
`mdnet` is a simple static site generator that converts Markdown files into HTML using specified templates. It's designed to be lightweight and easy to use.

## Installation
You can install `mdnet` via pip:
```
pip install mdnet
```

## Usage
### Basic Command
To generate a static site using the default configurations specified in `config.yaml`:

```
mdnet
```


### Command-Line Arguments
You can override the default configurations using command-line arguments:
- **input_dir**: Directory containing the Markdown source files.
- **output_dir**: Destination directory for the generated HTML files.
- **post_template_path**: Path to the HTML template for individual posts.
- **index_template_path**: Path to the HTML template for the main index page.

For example:
```
mdnet custom_input custom_output custom_post_template.html custom_index_template.html
```


### Optional Arguments
- **-t, --tag_template_path**: Path to the HTML template for individual tag pages. If provided, tag pages will be generated.
- **-a, --all_tags_template_path**: Path to the HTML template for the page listing all tags.
- **-n, --num_posts**: Number of latest posts to display on the main index page. Defaults to 8.
- **-p, --all_posts_template_path**: Path to the HTML template for the page listing all posts.

### Interactive Mode
Run the generator in interactive mode, prompting for each required input:
```
mdnet -i
```

## Configuration
You can specify default configurations in a `config.yaml` file. This allows you to run `mdnet` without having to provide command-line arguments every time.

Example `config.yaml`:
```
input_dir: default_input
output_dir: default_output
post_template_path: default_post_template.html
index_template_path: default_index_template.html
```

## Frontmatter YAML Parameters
When writing your Markdown files, you can optionally include a frontmatter section at the beginning of each file. This section is written in YAML and allows you to specify metadata for each post. Here are the supported parameters:
- **title**: The title of the post. If not provided, the filename (without extension) will be used.
  - Format: String
- **date**: The publication date of the post. If not provided, posts without dates will be considered older.
  - Format: `YYYY-MM-DD`
- **tldr**: A short summary or "too long; didn't read" for the post.
  - Format: String
- **tags**: A list of tags associated with the post.
  - Format: List of strings

### Example Frontmatter
```
---
title: "My First Post"
date: 2023-07-27
tldr: "A brief summary of the post's content."
tags:
  - tutorial
  - markdown
---
```

## Example Project Structure
my_project/
│
├── posts/
│   ├── post1.md
│   ├── post2.md
│   └── ...
│
├── public/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   ├── posts/
│   │   ├── post1.html
│   │   ├── post2.html
│   │   └── ...
│   └── tags/
│       ├── tutorial.html
│       ├── markdown.html
│       └── ...
│
├── templates/
│   ├── post_template.html
│   ├── index_template.html
│   ├── tag_template.html
│   ├── all_tags_template.html
│   └── all_posts_template.html
│
└── config.yaml
