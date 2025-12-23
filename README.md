# Music Recommendation System 🎵

## Overview
This is a Python-based music recommendation system that allows users to:
- Load and analyze a music dataset.
- Calculate similarity between tracks or artists using multiple similarity metrics.
- View recommendations for tracks or artists.
- Interact with a user-friendly GUI built using Tkinter.

The system is designed with modularity in mind, separating dataset loading, similarity calculation, statistical analysis, and the user interface.

---

## Modules

### 1. Dataset Loader
Handles loading and parsing of music datasets in CSV format.
- Features include filtering invalid rows, extracting required features, and providing helper methods to retrieve tracks/artists.
- **Key skills demonstrated:** Data handling, CSV parsing, dictionary management.

### 2. Similarity Calculator
Implements multiple similarity metrics:
- Euclidean, Cosine, Pearson, Manhattan.
- Computes similarity between tracks or artists.
- Efficient caching and optimization for large datasets.
- **Key skills demonstrated:** Mathematics, linear algebra, algorithm optimization.

### 3. Statistics Calculator
Provides statistical insights on dataset features:
- Mean, median, mode, variance, standard deviation, min, max, range.
- **Key skills demonstrated:** Data analysis, statistical reasoning.

### 4. User Interface (GUI)
- Tkinter-based interface for entering items and viewing similarity/recommendations.
- Dynamic selection of similarity metrics and comparison type.
- Clean, visually structured layout with results highlighting.
- **Key skills demonstrated:** GUI development, user interaction design.

### 5. Main Module
- Integrates all modules and launches the GUI.
- Performs initial dataset validation and displays dataset statistics in the console.
- **Key skills demonstrated:** Software design, modular integration, user experience.

---

## Screenshots
*<img width="2496" height="1664" alt="image" src="https://github.com/user-attachments/assets/5f0b7c47-0144-4798-bfd1-b59797c8c940" />
*


---

## Installation and Usage
1. Clone the repository:
```bash
git clone https://github.com/giddiesboom/music-recommendation-system.git
