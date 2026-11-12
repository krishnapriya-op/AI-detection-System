# AI Style Classifier

## Project Overview

AI Style Classifier is a Python-based application designed to analyze programming assignments and investigate coding patterns associated with human-written and AI-assisted source code.

## Problem Statement

The increasing use of AI coding assistants makes it difficult for educators to distinguish independently developed programming assignments from AI-assisted submissions.

## Proposed Solution

The application analyzes Python source code using Abstract Syntax Trees (AST) and extracts structural and stylistic features, including:

- Number of functions, classes and loops
- Code complexity and nesting depth
- Identifier naming conventions
- Comment frequency
- Function length and code structure

These features form the foundation for developing a machine learning-based classification system.

## Technology Stack

- Python
- Streamlit
- AST
- Pandas
- Scikit-learn

## Current Prototype

The current prototype provides Python file uploads, syntax validation, code feature extraction and preliminary heuristic-based style indicators.

## Future Scope

- Train and integrate a machine learning classifier using labelled human-written and AI-generated code.
- Generate calibrated confidence scores.
- Add explainable predictions.
- Extend support to additional programming languages.

## Important Limitation

The current heuristic indicators cannot establish the authorship of code. Human-written and AI-assisted code can exhibit similar structural and stylistic characteristics. Results should not be used as definitive evidence of academic misconduct.

## Acknowledgement

This project is adapted from the existing AI Detection System repository. Original project attribution and MIT license are retained.