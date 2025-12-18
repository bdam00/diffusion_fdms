# diffusion_fdms : Information Diffusion Analysis on GitHub

## Project Overview

This project is a Python-based tool for analyzing information diffusion on GitHub repositories. It scrapes data from GitHub, builds a network graph of developers and their interactions, and then simulates information spread using two common models:

*   **Independent Cascade (IC):** A probabilistic model where nodes have a chance to "activate" their neighbors.
*   **Linear Threshold (LT):** A model where a node is activated if the cumulative influence of its active neighbors exceeds a certain threshold.

The project is structured as a command-line application that allows for interactive analysis and visualization of the diffusion process.

### Core Technologies

*   **Python 3:** The primary programming language.
*   **Pandas:** For data manipulation and analysis.
*   **NetworkX:** For graph creation, manipulation, and analysis.
*   **Matplotlib & Plotly:** For data visualization.
*   **PyGithub:** For scraping data from the GitHub API.

## Building and Running

### 1. Installation

First, install the necessary Python packages using pip:

```bash
pip3 install -r requirements.txt
```

### 2. Running the Application

The main entry point for the application is `code/main.py`. To run it, use the following command:

```bash
python3 code/main.py
```

The script will guide you through an interactive menu to:

1.  **Choose a GitHub repository:** Select from a predefined list of popular repositories.
2.  **Regenerate the dataset:** You can choose to re-scrape the data from GitHub or use the existing data in the `data_github/` directory.
3.  **Choose a visualization method:** Select between a simple Matplotlib visualization, an interactive Plotly visualization, or an export to Gephi.
4.  **Choose a simulation mode:** You can run an Independent Cascade simulation, a Linear Threshold simulation, or perform a series of more in-depth analyses.

## Development Conventions

*   **Project Structure:** The project is organized into three main directories:
    *   `code/`: Contains the core logic for data scraping, graph building, and the diffusion models.
    *   `analysis/`: Contains scripts for more in-depth analysis of the diffusion models.
    *   `data_github/`: Stores the scraped data in JSON format.
*   **Modularity:** The code is well-structured, with different functionalities separated into different files (e.g., `github_scraper.py`, `graph_builder.py`, `ic_model.py`, `lt_model.py`).
*   **Interactivity:** The main application is designed to be interactive, with clear prompts and menus to guide the user.
*   **Visualization:** The project provides multiple options for visualizing the graph and the results of the simulations, including static plots, interactive plots, and exports to external tools.
