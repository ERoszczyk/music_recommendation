# Music recommendation

Music recommendation using artificial intelligence methods

```
├── .gitignore                <- GitHub's excellent Python .gitignore customized for this project
├── LICENSE                   <- Your project's license.
├── Pipfile                   <- The Pipfile for reproducing the analysis environment
├── README.md                 <- The top-level README for developers using this project.
│
├── data
│   ├── 0_raw                 <- The original, immutable data dump.
│   ├── 0_external            <- Data from third party sources.
│   ├── 1_interim             <- Intermediate data that has been transformed.
│   └── 2_final               <- The final, canonical data sets for modeling.
│
├── docs                      <- GitHub pages website
│   ├── data_dictionaries     <- Data dictionaries
│   └── references            <- Papers, manuals, and all other explanatory materials.
│
├── notebooks                 <- Jupyter notebooks. Naming convention is a number (for ordering),
│                                the creator's initials, and a short `_` delimited description, e.g.
│                                `01_cp_exploratory_data_analysis.ipynb`.
│
├── output
│   ├── features              <- Fitted and serialized features
│   ├── models                <- Trained and serialized models, model predictions, or model summaries
│   └── reports               <- Generated analyses as HTML, PDF, LaTeX, etc.
│       └── figures           <- Generated graphics and figures to be used in reporting
│
├── pipelines                 <- Pipelines and data workflows.
│   ├── Pipfile               <- The Pipfile for reproducing the pipelines environment
│   ├── pipelines.py          <- The CLI entry point for all the pipelines
│   ├── <repo_name>           <- Code for the various steps of the pipelines
│   │   ├──  __init__.py
│   │   ├── etl.py            <- Download, generate, and process data
│   │   ├── visualize.py      <- Create exploratory and results oriented visualizations
│   │   ├── features.py       <- Turn raw data into features for modeling
│   │   └── train.py          <- Train and evaluate models
│   └── tests
│       ├── fixtures          <- Where to put example inputs and outputs
│       │   ├── input.json    <- Test input data
│       │   └── output.json   <- Test output data
│       └── test_pipelines.py <- Integration tests for the HTTP API
│
└── serve                     <- HTTP API for serving predictions
    ├── Dockerfile            <- Dockerfile for HTTP API
    ├── Pipfile               <- The Pipfile for reproducing the serving environment
    ├── app.py                <- The entry point of the HTTP API
    └── tests
        ├── fixtures          <- Where to put example inputs and outputs
        │   ├── input.json    <- Test input data
        │   └── output.json   <- Test output data
        └── test_app.py       <- Integration tests for the HTTP API
```
