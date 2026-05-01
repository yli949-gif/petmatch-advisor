# Pet Adoption Risk Decision System

## Project Summary

This project is a data-driven decision system designed to reduce high-risk pet adoption mismatches.
Instead of relying on emotion alone, it compares a user's lifestyle constraints with pet care demands
and returns a risk level, explanation, and behavior guidance.

## Business Problem

Many people choose pets emotionally, but daily lifestyle constraints often create a poor long-term fit.
That mismatch can lead to stress, neglect, or failed adoption outcomes.

The goal of this project is to identify high-risk adoption scenarios before the decision is made.

## Why This Is a Data Analyst Project

This is not a reporting-only project. The core work is:

- defining risk as a measurable target
- designing interpretable features
- converting domain knowledge into decision logic
- identifying the key drivers of mismatch
- translating analytical output into user action

## Target Variable

`mismatch_risk`

- `high`
- `low`

The system is designed to minimize false negatives, because missing a high-risk case is more costly than
flagging an extra medium-risk situation for review.

## Features

Primary features:

- `hours_away`
- `activity_level`
- `housing_type`
- `pet_type`

Supporting behavioral feature:

- `pet_energy_level`

## Data Source

The dataset is synthetic. It is generated from realistic lifestyle constraints and pet-care assumptions,
then labeled with transparent rule-based logic.

## Analytical Logic

The analysis compares user lifestyle against pet requirements to detect mismatch risk.

Key insight:

- time availability is one of the strongest predictors of mismatch
- high-energy pets create more risk when paired with low-activity users
- apartments are not inherently risky, but become riskier for high-energy dogs

## Model Choice

The project uses a rule-based classification model instead of a black-box model.

Why:

- interpretability matters more than marginal accuracy
- each decision must be explainable to a user
- the output should support action, not just prediction

## Output

For each user-pet match, the system returns:

- risk score
- risk label
- explanation
- behavior guidance

Example:

> Risk: High  
> Explanation: The adopter is away for long hours and selected a high-energy dog while reporting low daily activity.  
> Guidance: Consider a lower-energy pet or reduce time away before adopting.

## Validation Approach

Because the data is synthetic, validation is scenario-based rather than production-based.

This project validates value by:

- simulating adoption cases
- comparing high-risk vs low-risk decisions
- adjusting user behavior inputs and checking whether risk drops

## Project Structure

```text
.
├── assets/
│   ├── cat.svg
│   ├── golden.svg
│   ├── husky.svg
│   └── small-dog.svg
├── index.html
├── README.md
├── PROJECT_CN.md
├── data/
│   └── synthetic_pet_adoption.csv
└── src/
    └── risk_model.py
```

## How To Run

```bash
python3 src/risk_model.py
```

To open the interactive front-end demo, open `index.html` in a browser.

## Interview Version

One-line description:

> A data-driven decision system that reduces high-risk pet adoption mismatches.

Core problem:

> People often make adoption decisions emotionally, which leads to poor lifestyle-pet fit.

Most important insight:

> Time availability and pet energy level are the strongest predictors of mismatch risk.

Impact:

> The system improves decisions by surfacing risk early and guiding users toward lower-risk choices.

## Next Improvement

If expanded further, the next step would be to replace synthetic labels with real adoption outcome data and
train a predictive model for better calibration.
