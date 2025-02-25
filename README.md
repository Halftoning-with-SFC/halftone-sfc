# Digital halftoning with space filling curves
> Repository for `Digital halftoning with space filling curves` code.

## ⚙️ Setting Up and Running Digital Halftoning with Space Filling Curves
### 📦 Prerequisites
Before starting, make sure that:
- You have [git](https://git-scm.com) installed on your machine.
- You have [Python](https://www.python.org/downloads) installed on your machine.

### 🏗️ Installing the Application
To install the application using git, follow these steps:
1. Clone the project to a directory of your choice (HTTPS):
    ```bash
    git clone https://github.com/Halftoning-with-SFC/halftone-sfc.git
    ```
    or (SSH)
    ```bash
    git clone git@github.com:Halftoning-with-SFC/halftone-sfc.git
    ```
2. After cloning the project, navigate to it:
    ```bash
    cd halftone-sfc
    ```
3. Create a virtual environment `.venv` in Python:
    ```bash
    python -m venv .venv
    ```
4. Activate your virtual environment:
    ```bash
    source .venv/bin/activate
    ```
5. Then, install the dependencies in your new Python virtual environment:
    ```bash
    pip install -r requirements.txt
    ```

### 🚀 Running the Application
1. Run it using Python:
    ```bash
    python3 -m halftonesfc.cli --help
    ```

## 🎉 Making Changes to the Project
After installing the application on your machine, make sure you are in the project directory ("halftone-sfc").

### 🔖 Making Updates
1. After selecting your task, use branch "develop" (or create a new branch if you want)
    ```bash
    git pull origin develop
    git switch develop
    ```
2. After making your changes, add them:
    ```bash
    git add [file]
    ```
    or add all files:
    ```bash
    git add .
    ```
3. Commit your changes with a BRIEF description of the modifications made:
    ```bash
    git commit -m "[emoji] type(directory): [brief description]"
    ```
    Example:
    ```bash
    git commit -m "✨ feat(code): add method for generating curves"
    ```
    Note: You can get emojis from [Gitmoji](https://gitmoji.dev/)
4. Push your local changes to GitHub:
    ```bash
    git push -u origin develop
    ```
    Note: the branch name of the example above is "develop".
    
5. (After completing all changes in this branch, i.e., finishing the feature),
   create a Pull Request (PR) [here](https://github.com/Halftoning-with-SFC/halftone-sfc/compare).
   Describe your changes (attach screenshots if necessary) and request a merge.
   Done! Now just wait for someone to review your code and merge it into the main branch.