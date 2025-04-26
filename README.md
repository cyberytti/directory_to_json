# 🗂️ Codebase to JSON Converter

This Python script allows you to convert an entire codebase directory—including all subdirectories and files—into a structured, minified JSON file. It’s specifically designed to help you package and upload your full project structure to any chatbot for analysis, assistance, or documentation generation.

## 🚀 Features

- Recursively scans and captures all files and subdirectories
- Reads and includes file contents in the output JSON
- Outputs a compact, minified `.json` file
- Displays progress with colorful CLI feedback
- Handles permission errors and file read issues gracefully

## 📦 Why Use This?

Most chatbots don't allow uploading entire folders or codebases directly. This tool solves that problem by transforming your full project directory into a single `.json` file, which you can easily upload to a chatbot for processing, refactoring, or analysis.

## 🛠️ Usage

### 1. Install [uv](https://github.com/astral-sh/uv)

If you haven’t already, install `uv`, a fast Python package manager:

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

### 2. Run the script

Use `uv` to execute the script with the following command:

```bash
uv run directory_to_json.py --help
```

### 3. Convert your project

To convert your project, run:

```bash
uv run directory_to_json.py -d ./path/to/your/project
```

This will generate a file like `your_project.json` in the current directory.

## 📂 Output JSON Structure

The output JSON represents the full folder tree, including each file's contents.

Example structure:

```json
{
  "name": "project_folder",
  "type": "directory",
  "path": "./project_folder",
  "children": [
    {
      "name": "main.py",
      "type": "file",
      "path": "./project_folder/main.py",
      "content": "print('Hello, world!')"
    },
    {
      "name": "submodule",
      "type": "directory",
      "path": "./project_folder/submodule",
      "children": [
        {
          "name": "helper.py",
          "type": "file",
          "path": "./project_folder/submodule/helper.py",
          "content": "def helper():\n    pass"
        }
      ]
    }
  ]
}
```

- `name`: Name of the file or folder
- `type`: `"file"` or `"directory"`
- `path`: Relative or absolute path
- `content`: File content (only for files)
- `children`: Nested list of subdirectories and files (only for directories)

## 📌 Notes

- Python 3.12 or newer is required.
- The output JSON includes both structure and contents, making it ideal for AI tools to parse and understand your codebase.
- The resulting file is compact and shareable.

## 🧑‍💻 Example

```bash
uv run directory_to_json.py -d ./my_project
```

This creates `my_project.json`, containing all files, folders, and code content inside `./my_project`.

---

**Version:** 1.0.0  
**Author:** *Sagnik Bose*  
**License:** MIT ([LICENSE](LICENSE))

Happy coding!

