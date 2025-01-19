# Point Cloud Verticality Segmentation Script

This repository contains a Python script for segmenting point cloud data into upper and lower portions based on verticality values and height thresholds. The script is designed to process `.xyz` files and uses the `jakteristics` library to compute verticality for each point in the cloud.

## Features

- **Verticality Calculation**: Computes verticality for each point using the `jakteristics` library.
- **Height Thresholding**: Segments the point cloud based on height and verticality differences.
- **Customizable Thresholds**: Allows setting thresholds for:
  - Starting height (`threshold_zstart`)
  - Minimum verticality difference (`threshold_verticality`)
  - Minimum branch separation (`threshold_wrong_branch`)
- **Batch Processing**: Automatically processes all `.xyz` files in a specified directory.
- **Output Organization**: Saves segmented point clouds into `lower` and `upper` subdirectories.

## Requirements

- Python 3.8 or later
- Libraries:
  - `numpy`
  - `os`
  - `jakteristics`

Install the required libraries using:
```bash
pip install numpy jakteristics
```

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/moonis-ali/Hybrid-model.git
   cd Hybrid-model
   ```

2. Place your `.xyz` point cloud files in the `data` directory or any folder of your choice.

3. Update the `directory` variable in the script to point to your data folder:
   ```python
   directory = "path/to/your/point-cloud-files/"
   ```

4. Run the script:
   ```bash
   python verticality_segmentation.py
   ```

5. Segmented point clouds will be saved in:
   - `<directory>/lower/` (points below the threshold)
   - `<directory>/upper/` (points above the threshold)

## Input File Format

The input files should be `.xyz` files containing:
- **X**, **Y**, **Z** coordinates (one point per line).

The script appends a verticality value to each point during processing.

## Example Workflow

1. **Input**:
   - Point cloud file `tree1.xyz`:
     ```
     1.0 2.0 3.0
     1.1 2.1 3.1
     ...
     ```
2. **Output**:
   - `lower/tree1.xyz`:
     ```
     1.0 2.0 3.0 0.123
     1.1 2.1 3.1 0.234
     ...
     ```
   - `upper/tree1.xyz`:
     ```
     1.5 2.5 4.0 0.345
     1.6 2.6 4.1 0.456
     ...
     ```

## Parameters

You can customize the following parameters in the script:

- `threshold_zstart`: Starting height above the ground to analyze points. Default: `2`.
- `threshold_verticality`: Minimum difference in verticality between consecutive points. Default: `0.3`.
- `threshold_wrong_branch`: Minimum Z-difference between detected branches. Default: `0.5`.

## Notes

- The script is designed for `.xyz` files with three columns (X, Y, Z). If additional columns are present, the script will ignore them.
- The verticality computation uses a default search radius of `0.2`, which can be adjusted based on your data.
