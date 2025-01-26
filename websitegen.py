from flask import Flask, render_template, send_from_directory, abort
from livereload import Server
from pathlib import Path
from typing import Tuple, Optional, List, Dict
from mistune import HTMLRenderer
import jinja2, mistune
import os, argparse, time
import sh


MUSEFILE_NAME = "default"
TEMPLATE_DIR = f"partials"
ASSETS_DIR = f"build/{MUSEFILE_NAME}/files"

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/assets/<path:filepath>")
def serve_asset(filepath):
    global ASSETS_DIR
    """
    Serve static files from the assets directory.
    """
    try:
        return send_from_directory(ASSETS_DIR, filepath)
    except Exception as e:
        print(f"Error serving asset {filepath}: {str(e)}")
        abort(404)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_page(path):
    global TEMPLATE_DIR
    global MUSEFILE_NAME
    """
    Dynamically serve pages by mapping routes to file paths.
    """
    # Start the timer for the overall render
    overall_start = time.time()
    # If no specific path is provided, default to main board loaded with cli loader
    chosen_board = path

    print(f"Serving from {MUSEFILE_NAME} : {path}")
    # Construct the full file path
    board_path = Path(chosen_board).resolve()

    # Check if the board exists
    if not board_path.exists():
        print('aborted board does not exist')
        abort(404)  # Return 404 if file is not found

    base_directory = Path(".").resolve()
    if not board_path.is_relative_to(base_directory):
        print('aborted board path outside base', board_path, base_directory)
        abort(404) # Return 404 user tried to escape current directory

    # Write the blank render in tmp for css gen
    tmp_render_path:str = "/tmp/rendered_template.html"
    # TODO: embed the board's files and context data here
    blank_render:str = render_template('board.html')
    with open(tmp_render_path, "w") as file:
        file.write(blank_render)

    # Build the css and embed it in itself
    inline_css:str = build_css(
            styles_filepath = f"partials/styles.css",
            tailwindconfig_filepath = f"partials/tailwind.config.js",
            content_filepath = tmp_render_path,
            call_options=["--minify"],
            )

    # TODO: embed the board's files and context data here
    result = render_template('board.html', inline_css = inline_css)
    print(f"Completed render took : {time.time() - overall_start:.2f}s")
    return result


def build_css(styles_filepath, tailwindconfig_filepath, content_filepath, call_options):
    """
    A function to rebuild CSS files.
    Replace the command with your actual CSS build process.
    """
    print("Rebuilding CSS...")
    try:
        # Example: Build using Tailwind CLI (modify as needed)
        css:str = sh.tailwindcss("-i", styles_filepath, "--config", tailwindconfig_filepath,
                   "--content", content_filepath, *call_options)

        # check if css was rendered correctly, or else send error 
        if "MIT License" not in css: # did not output the styles
            raise ValueError(f"could not build css successfully cssoutput : {css}")

        print("CSS built successfully.")
        return css
    except Exception as e:
        print(f"Error building CSS: {e}")


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate static site pages")
    parser.add_argument("--export", type=bool, help="Specify if export to build dir needed", default=False)
    parser.add_argument("--musefile", type=str, help="Current theme to render", default='')
    args = parser.parse_args()

    if args.musefile == '':
        print("Please select a musefile with --musefile")
        sys.exit(1)
    else:
        # check if musefile exists in that path
        musefile_path = Path(args.musefile)
        if musefile_path.exists():
            MUSEFILE_NAME = musefile_path.stem
            ASSETS_DIR = f"build/{MUSEFILE_NAME}/files"
        else:
            print(f"The musefile '{args.musefile}' does NOT exist at that location")
            sys.exit(1)

    # Assign jinja template dir
    app.template_folder = TEMPLATE_DIR
    # Create a Livereload server
    server = Server(app)

    if args.export:
        # TODO: Export the whole project to build/ dont run server.watch
        print('Exported the app to build/ dir, you can host it now !')
        raise NotImplementedError()
    else:
        # TODO: reload and build the custom pagefind index
        # Watch the components directory for changes
        server.watch(TEMPLATE_DIR)
        # Start the server
        server.serve(port=1414, debug=True)



    



