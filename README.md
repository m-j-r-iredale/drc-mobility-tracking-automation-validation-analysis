# DRC Mobility Tracking Data Validation & Automated Analysis

A Python workflow for validating and analysing humanitarian mobility-tracking data from the Democratic Republic of the Congo.

This project was developed because humanitarian data in the field can change very quickly as new information is received and records are corrected or updated. As a result, the UN's Analytics Knowledge and Output team needed a fast, verifiable and repeatable process for reporting.

The workflow combines two linked stages:

1. Validating the cleaned source data before analysis
2. Automating the main analytical process used for reporting

## Project Context

The data originated from field-level mobility tracking activities undertaken in the DRC's complex humanitarian context.

Because source datasets could change between reporting cycles, the first priority was to establish a repeatable validation process that could verify the integrity of the analytical input.

Once the dataset had passed validation, the second stage automated the main calculations, transformations and outputs required for reporting.

The resulting workflow was designed to make the analytical process more consistent, reproducible and easier to rerun when updated data became available.

## Workflow

**Field-cleaned data → validation checks → exception review → validated dataset → automated analysis → reporting outputs**

## What the Project Does

### 1. Validate Incoming Data

The validation stage checks the cleaned dataset before any automated analysis is performed.

The workflow is used to:

- Identify missing or unexpected values
- Test logical consistency between variables
- Verify analytical and aggregation outputs
- Flag records or results requiring investigation
- Establish a validated dataset for downstream reporting

### 2. Investigate Exceptions

Records or outputs that fail validation checks can be reviewed before the main analysis is rerun. This creates a clear distinction between data that has passed validation and data that still requires investigation and/or cleaning.

### 3. Automate the Analytical Workflow

Once the data has been verified, the second stage automates the main analysis used for reporting.

This includes:

- Applying repeatable transformations
- Reproducing core calculations programmatically
- Generating consistent analytical outputs
- Reducing reliance on repeated manual processing
- Allowing the workflow to be rerun efficiently when updated field data becomes available

## Technologies

- Python
- Pandas
- NumPy
- Matplotlib

## Project Structure

```text
drc-mobility-tracking-automation-validation-analysis/
├── README.md
├── src/
│   ├── validation.py
│   └── analysis.py
├── images/
├── sample_data/
├── requirements.txt
└── .gitignore
```
