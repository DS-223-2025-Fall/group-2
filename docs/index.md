# Welcome to MkDocs

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml                  # The MkDocs configuration file.
    docs/
        index.md                # Documentation homepage.
        backend.md              # Backend documentation.
        frontend.md             # Frontend documentation.
        problem_definition.md   # Project problem definition.
        ...                     # Other markdown pages, images, or files.
    backend/                     # Backend service code.
        ...                     # Your Python code or APIs.
    frontend/                    # Frontend service code.
        ...                     # Your HTML/CSS/JS or framework code.
    problem_definition/          # Project problem definition files.
        ...                     # Any additional supporting files.
    venv/                        # Python virtual environment (optional).
    docker-compose.yml            # Docker Compose configuration for project services.
    requirements.txt             # Python dependencies.
    .gitignore                   # Files/folders to ignore in git.
