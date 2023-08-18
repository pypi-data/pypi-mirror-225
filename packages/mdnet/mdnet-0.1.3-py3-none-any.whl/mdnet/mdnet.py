import argparse
import frontmatter
import markdown
import yaml
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from datetime import date

def convert_md_to_html(md):
    return markdown.markdown(md)

def get_template(template_path):
    template_dir = template_path.parent
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    return env.get_template(template_path.name)

def render_template(template_path, **kwargs):
    template = get_template(template_path)
    return template.render(**kwargs)

def generate_site(input_dir, output_dir, post_template_path, index_template_path, tag_template_path=None, all_tags_template_path=None, all_posts_template_path=None, num_posts=8):
    posts_dir = output_dir / 'posts'
    posts_dir.mkdir(parents=True, exist_ok=True)

    posts = []
    tags_dict = {}  # Renamed from tags to tags_dict
    for md_file in Path(input_dir).iterdir():
        if md_file.suffix == ".md":
            post = frontmatter.load(md_file)
            
            # Default values for missing metadata
            title = post.metadata.get('title', md_file.stem)
            date_str_or_obj = post.metadata.get('date', None)
            
            if isinstance(date_str_or_obj, str):
                date_obj = date.fromisoformat(date_str_or_obj)  # Convert string to date object
            elif isinstance(date_str_or_obj, date):
                date_obj = date_str_or_obj
            else:
                date_obj = date(1900, 1, 1)  # Default to a very old date

            tldr = post.metadata.get('tldr', "")
            post_tags = post.metadata.get('tags', [])

            html_file = posts_dir / (title + ".html")
            html_content = render_template(post_template_path, title=title, date=date, content=convert_md_to_html(post.content))
            html_file.write_text(html_content)
            
            post_data = {
                'title': title,
                'date': date_obj,
                'tldr': tldr,
                'file': 'posts/' + html_file.name,
                'tag_file': '../posts/' + html_file.name
            }

            posts.append(post_data)
            for tag in post_tags:  # Using post_tags here
                if tag not in tags_dict:
                    tags_dict[tag] = []
                tags_dict[tag].append(post_data)

    # Sort posts by date in descending order
    posts.sort(key=lambda post: post['date'], reverse=True)

    if tag_template_path:
        tags_dir = output_dir / 'tags'
        tags_dir.mkdir(parents=True, exist_ok=True)
        for tag, tag_posts in tags_dict.items():
            tag_content = render_template(tag_template_path, posts=tag_posts, tag=tag)
            (tags_dir / f'{tag}.html').write_text(tag_content)

        all_tags_content = render_template(all_tags_template_path, tags_dict=tags_dict)
        (output_dir / 'all_tags.html').write_text(all_tags_content)

    index_content = render_template(index_template_path, posts=posts[:num_posts], tags_dict=tags_dict)
    (output_dir / 'index.html').write_text(index_content)

    all_posts_content = render_template(all_posts_template_path, posts=posts)
    (output_dir / 'all_posts.html').write_text(all_posts_content)

def load_config():
    with open("config.yaml", 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(f"Error reading config.yaml: {exc}")
            exit(1)

def main():
    config = load_config()

    parser = argparse.ArgumentParser(description="Generate a static website from Markdown files using specified templates.")
    
    parser.add_argument("-i", "--interactive", action="store_true", help="Run the generator in interactive mode, prompting for each required input.")
    parser.add_argument("input_dir", nargs='?', default=config.get('input_dir'), help="Directory containing the Markdown source files.")
    parser.add_argument("output_dir", nargs='?', default=config.get('output_dir'), help="Destination directory for the generated HTML files.")
    parser.add_argument("post_template_path", nargs='?', default=config.get('post_template_path'), help="Path to the HTML template for individual posts.")
    parser.add_argument("index_template_path", nargs='?', default=config.get('index_template_path'), help="Path to the HTML template for the main index page.")
    parser.add_argument("-t", "--tag_template_path", nargs='?', default=config.get('tag_template_path'), help="Optional: Path to the HTML template for individual tag pages. If provided, tag pages will be generated.")
    parser.add_argument("-a", "--all_tags_template_path", nargs='?', default=config.get('all_tags_template_path'), help="Optional: Path to the HTML template for the page listing all tags.")
    parser.add_argument("-n", "--num_posts", type=int, default=config.get('num_posts', 8), help="Number of latest posts to display on the main index page. Defaults to 8.")
    parser.add_argument("-p", "--all_posts_template_path", nargs='?', default=config.get('all_posts_template_path'), help="Optional: Path to the HTML template for the page listing all posts.")
    
    args = parser.parse_args()

    # Override config values with command-line arguments if provided
    for arg in ['input_dir', 'output_dir', 'post_template_path', 'index_template_path', 'tag_template_path', 'all_tags_template_path', 'all_posts_template_path', 'num_posts']:
        if getattr(args, arg) is not None:
            config[arg] = getattr(args, arg)

    if args.interactive:
        prompts = {
            'input_dir': "Provide the directory containing your Markdown files: ",
            'output_dir': "Specify the directory where the generated HTML files should be saved: ",
            'post_template_path': "Provide the path to your post HTML template: ",
            'index_template_path': "Provide the path to your main index HTML template: "
        }
        
        for arg, prompt in prompts.items():
            setattr(args, arg, input(prompt))

        if input("Would you like to generate a page listing all tags? (y/n) ").lower() == 'y':
            args.all_tags_template_path = input("Provide the path to your all-tags HTML template: ")
        
        if input("Would you like to generate individual pages for each tag? (y/n) ").lower() == 'y':
            args.tag_template_path = input("Provide the path to your individual tag page HTML template: ")

        if input("Would you like to generate a page listing all posts? (y/n) ").lower() == 'y':
            args.all_posts_template_path = input("Provide the path to your all-posts HTML template: ")
        
        num_posts = input("How many of the latest posts would you like to display on the main index page? (default is 8): ")
        args.num_posts = int(num_posts) if num_posts else 8
    else:
        missing_args = [arg for arg in ['input_dir', 'output_dir', 'post_template_path', 'index_template_path'] if getattr(args, arg) is None]
        if missing_args:
            print(f"Error: Missing required argument(s): {', '.join(missing_args)}")
            return

    generate_site(Path(args.input_dir), 
                  Path(args.output_dir), 
                  Path(args.post_template_path), 
                  Path(args.index_template_path), 
                  Path(args.tag_template_path) if args.tag_template_path else None,
                  Path(args.all_tags_template_path) if args.all_tags_template_path else None,
                  Path(args.all_posts_template_path) if args.all_posts_template_path else None,
                  args.num_posts)

if __name__ == "__main__":
    main()

