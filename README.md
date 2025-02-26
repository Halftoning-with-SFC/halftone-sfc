# Digital halftoning with space filling curves
> Repository for `Digital halftoning with space filling curves` code.

![Description of the image](data/output/hilbert_1_araras.png)

## About this Application
This application implements **Digital Halftoning with Space-Filling Curves**, a technique described in the paper:
> *[Digital Halftoning with Space Filling Curves](https://www.visgraf.impa.br/Data/RefBib/PS_PDF/a91a/s91-velho.pdf)*, Luiz Velho and Jonas de Miranda Gomes, SIGGRAPH 1991.  

In this README, you will find setup instructions to **install and run the application locally**, technical details about the pipeline and supported features, parameter descriptions to customize the halftoning process, usage examples to help you get started quickly, and contribution guidelines for making changes to the project. We also have a web version of the application, which is currently under development and not yet publicly available. 

#### Technical Details:
- **Input**: Images from .png and .jpg format.
- **Output**: Halftoned images.
- **Supported Curves**: Hilbert, Peano, and Lebesgue.
- **Customization**: Users can adjust gamma correction, edge enhancement, cluster size, and distribution method.
- **Dependencies**: Built with Python, OpenCV, and NumPy.

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
Run it using Python:
    ```bash
    python3 -m halftonesfc.cli --help
    ```

### 📋 Parameters
The application accepts the following arguments:

#### Required Parameters:
- `--in_image`: Path to the input image file.  
  Example: `--in_image data/input/araras.png`

#### Optional Parameters:
- `--curve`: Type of space-filling curve to use. Options: `hilbert`, `peano`, `lebesgue`.  
  Default: `hilbert`  
  Example: `--curve peano`

- `--cluster_size`: Size of the cluster for halftoning.  
  Default: `4`  
  Example: `--cluster_size 8`

- `--out_image`: Path to save the output image. If not provided, the output will be saved in the current directory with a generated name.  
  Example: `--out_image output.png`

- `--distribution`: Method for distributing black pixels within the cluster. Options: `standard`, `ordered`, `random`.  
  Default: `standard`  
  Example: `--distribution random`

- `--strength`: Strength value for edge enhancement. Controls the strength of edge enhancement.  
  Default: `1.0`  
  Example: `--strength 1.5`

- `--blur`: Blur value for edge enhancement. Controls the scale of blurring.  
  Default: `1.0`  
  Example: `--blur 2.0`

- `--gamma`: Gamma value for gamma correction. Adjusts the brightness of the image.  
  Default: `1.0`  
  Example: `--gamma 0.8`

### 🛠️ Examples
Here are some examples of how to use the application with different parameters:

1. **Basic Usage**:
   ```bash
   python3 -m halftonesfc.cli --in_image data/input/araras.png --curve hilbert --cluster_size 4
   
2. **All Parameters**
   ```bash
   python3 -m halftonesfc.cli --in_image data/input/araras.png --curve peano --cluster_size 8 --out_image output/araras_halftoned.png --distribution ordered --strength 1.2 --blur 1.5 --gamma 0.9

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
