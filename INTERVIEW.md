# FraudDetect Interview Preparation

## 1. One-minute explanation

FraudDetect is an end-to-end fraud-detection system built on the PaySim synthetic mobile-money dataset. It predicts whether a transaction is fraudulent using transaction type, amount, and sender/receiver balance information.

The pipeline versions data with DVC, performs domain feature engineering, preprocesses numerical and categorical data, trains an XGBoost classifier, tunes the decision threshold using validation data, evaluates with fraud-appropriate metrics, and saves the model and preprocessing pipeline as artifacts.

The model uses scale_pos_weight for class imbalance. Instead of using the default threshold of 0.5, it uses a low threshold selected to maximize recall while targeting at least 65% precision. The model is served through FastAPI, consumed by a static HTML/CSS/JavaScript frontend, tracked with MLflow/DagsHub, and containerized with Docker.

## 2. Complete process

    PaySim dataset
          ↓
    DVC-versioned raw data
          ↓
    Data loading
          ↓
    Stratified train/test split
          ↓
    Train/validation split
          ↓
    Feature engineering
          ↓
    Imputation + scaling + one-hot encoding
          ↓
    XGBoost training
          ↓
    Validation probability predictions
          ↓
    Threshold optimization
          ↓
    Test evaluation
          ↓
    Save model, preprocessor, metrics and plots
          ↓
    MLflow tracking and model selection
          ↓
    FastAPI inference

The main training orchestrator is src/pipelines/training_pipeline.py.

## 3. Dataset

The project uses the PaySim synthetic financial transaction dataset, commonly known as “Synthetic Financial Datasets for Fraud Detection” on Kaggle. It simulates mobile-money transactions.

### Dataset statistics

- Rows: approximately 6,362,620
- Original columns: 11
- Fraudulent transactions: 8,213
- Fraud rate: approximately 0.129%
- Legitimate rate: approximately 99.871%
- Test-set size: 1,272,524 transactions
- Actual fraud cases in the test set: 1,643

### Columns

| Column | Meaning | Treatment |
|---|---|---|
| step | Time step/hour | Dropped |
| type | Transaction type | One-hot encoded |
| amount | Transaction amount | Used |
| nameOrig | Sender identifier | Dropped |
| oldbalanceOrg | Sender balance before transaction | Used |
| newbalanceOrig | Sender balance after transaction | Used |
| nameDest | Receiver identifier | Dropped |
| oldbalanceDest | Receiver balance before transaction | Used |
| newbalanceDest | Receiver balance after transaction | Used |
| isFraud | Target: 0 legitimate, 1 fraud | Target |
| isFlaggedFraud | Existing rule-based flag | Dropped |

Fraud is concentrated in TRANSFER and CASH_OUT. The report states that no fraud was observed in CASH_IN, DEBIT, or PAYMENT.

## 4. EDA

EDA covered:

- Dataset shape, data types, and descriptive statistics
- Missing-value checks
- Duplicate checks
- Class distribution
- Transaction-type distribution
- Transaction amount distributions
- Fraud by transaction type
- Numerical correlation matrix
- Feature relationships and feature importance

Important findings:

- The data is extremely imbalanced: approximately 99.87% legitimate and 0.13% fraud.
- Transaction amounts are heavily right-skewed.
- The reported mean transaction amount is approximately 179,861, with a standard deviation around 603,858.
- Fraud is mainly associated with TRANSFER and CASH_OUT.
- Balance-error features are among the strongest fraud signals.
- The report states that no exact duplicates were found.
- PaySim generally has no missing values, but the production pipeline still supports imputation.

Because of the imbalance, accuracy is not sufficient. A model predicting every row as legitimate could achieve approximately 99.87% accuracy while detecting no fraud.

## 5. Feature engineering

The pipeline creates two domain features:

    errorBalanceOrig = oldbalanceOrg - amount - newbalanceOrig
    errorBalanceDest = oldbalanceDest + amount - newbalanceDest

The first measures whether the sender balance changed consistently with the transaction. The second measures whether the receiver balance changed consistently. Large discrepancies can indicate anomalous transfers.

Implementation: src/pipelines/feature_engineering_pipeline.py.

Important accuracy note: the report describes these as absolute errors, but the current code stores signed residuals. A future improvement would be to use abs(...) so positive and negative discrepancies are treated equally.

## 6. Preprocessing

Dropped columns:

    step, nameOrig, nameDest, isFlaggedFraud

Identifiers are dropped because they are high-cardinality values that do not generalize well and can encourage memorization. isFlaggedFraud is dropped because it could leak an existing rule-based fraud decision.

Numerical features:

    amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest,
    newbalanceDest, errorBalanceOrig, errorBalanceDest

Numerical pipeline:

    Median imputation → StandardScaler

Categorical pipeline:

    Most-frequent imputation → OneHotEncoder(handle_unknown="ignore")

The preprocessor is fitted only on training data:

    X_train_t = preprocessor.fit_transform(X_train)
    X_val_t = preprocessor.transform(X_val)
    X_test_t = preprocessor.transform(X_test)

This prevents preprocessing leakage. The complete fitted preprocessor is serialized and reused during inference.

## 7. Splitting strategy

The project performs:

1. Stratified 80/20 train-test split.
2. A further stratified split of the training data into training and validation sets.

Configuration includes test_size 0.2, cross_validation 3, stratify true, and seed 42. Stratification preserves the fraud ratio in every split.

Important implementation note: the configuration contains cross_validation: 3, and the README mentions cross-validation, but the current training code does not call StratifiedKFold or cross_val_score. It uses a stratified holdout validation set for threshold tuning. Model selection is performed across timestamped artifact runs using PR-AUC, with a recall filter.

Accurate interview wording:

> The project was designed around stratified validation and reserves a three-fold cross-validation configuration, but the current implementation uses a stratified holdout validation set for threshold tuning. The final model is selected from experiment artifacts using PR-AUC.

## 8. Model selection

### Logistic Regression

A simple, fast, interpretable baseline. Its limitation is a mostly linear decision boundary.

### Decision Tree

Captures nonlinear relationships and is easy to interpret, but a single tree can overfit and be unstable.

### Random Forest

More robust than one tree and captures nonlinear relationships, but can use more memory and may be less efficient than boosting.

### XGBoost

Selected because it performs strongly on tabular data, learns nonlinear interactions, supports class weighting and subsampling, handles large datasets efficiently, supports GPU training, and produces probability scores for threshold optimization.

Repository note: the current source contains the final XGBoost implementation but not separate Logistic Regression, Decision Tree, or Random Forest implementations. If those models were run separately, present them as baseline experiments; otherwise, describe them as candidates considered during selection.

## 9. Final model and hyperparameters

    n_estimators: 263
    max_depth: 11
    learning_rate: 0.081554
    subsample: 0.556441
    colsample_bytree: 0.563919
    scale_pos_weight: 7.452034
    objective: binary:logistic
    eval_metric: logloss
    tree_method: hist
    device: cuda
    n_jobs: 1
    random_state: 42

Parameter meanings:

- n_estimators=263: number of boosting trees.
- max_depth=11: maximum depth; more depth captures complex interactions but increases overfitting risk.
- learning_rate=0.081554: contribution of each tree.
- subsample=0.5564: approximately 55.6% of rows used for each tree.
- colsample_bytree=0.5639: approximately 56.4% of features used for each tree.
- scale_pos_weight=7.452: increases the importance of fraud examples.
- objective=binary:logistic: binary classification with probability output.
- tree_method=hist: fast histogram-based tree construction.
- device=cuda: GPU acceleration where CUDA is available.

## 10. Handling class imbalance

The project combines:

1. Stratified train/test and train/validation splits.
2. Cost-sensitive learning through scale_pos_weight=7.452034.
3. Precision-recall metrics rather than relying on accuracy.
4. Threshold optimization to prioritize recall.

scale_pos_weight changes the loss contribution of fraud cases; it does not create synthetic fraud samples. The current implementation does not use SMOTE, ADASYN, oversampling, or undersampling. For this very large dataset, class weighting is simpler and computationally practical.

## 11. Threshold optimization

A model probability is not automatically a business decision. The threshold determines when a transaction becomes fraud.

The default 0.5 threshold is unsuitable because fraud is rare. Genuine fraud cases can have probabilities below 0.5, so a 0.5 threshold would miss too many cases.

On the validation set, the system:

1. Generates fraud probabilities.
2. Computes the precision-recall curve.
3. Finds candidate thresholds.
4. Keeps thresholds where precision is at least 65%.
5. Selects the threshold with maximum recall.
6. Falls back to maximum F1-score if no threshold meets the precision constraint.

Selected threshold: 0.001149877, approximately 0.115%.

The threshold is learned on validation data and held fixed for test evaluation and API inference. Implementation: src/evaluation/metrics.py.

## 12. Evaluation

| Metric | Score |
|---|---:|
| Accuracy | 99.93% |
| Precision | 64.81% |
| Recall | 99.76% |
| F1-score | 78.57% |
| ROC-AUC | 99.94% |
| PR-AUC | 98.77% |
| Threshold | 0.001149877 |

Confusion matrix:

    TN = 1,269,991
    FP = 890
    FN = 4
    TP = 1,639

Interpretation:

- Recall 99.76%: almost all fraud cases were detected; only 4 were missed.
- Precision 64.81%: approximately 64.8% of fraud alerts were actual fraud.
- Accuracy is reported but not primary because of severe imbalance.
- PR-AUC 98.77% indicates excellent ranking performance for the fraud class.

The threshold was optimized on validation data, so test precision can differ slightly from the 65% validation constraint. The final test precision of 64.81% is close, while recall remains 99.76%.

## 13. Artifact management

Each training run creates:

    artifacts/xgboost/<timestamp>/
    ├── xgboost_model.pkl
    ├── preprocessor.pkl
    ├── params.json
    ├── metrics.json
    └── plots/
        ├── confusion_matrix.png
        ├── auc_curve.png
        └── pr_auc.png

The model picker scans artifact runs, ignores incompatible schema versions, requires recall of at least 0.70, and chooses the run with the highest PR-AUC. It copies the selected files to models/best_model.pkl, models/best_preprocessor.pkl, and models/best_metrics.json.

## 14. MLOps tools

### DVC

DVC versions large datasets. Git stores pointer files such as data/raw/data.csv.dvc, while DVC tracks the actual data. This provides reproducibility and allows experiments to be tied to a specific dataset version.

### MLflow

MLflow records model parameters, metrics, plots, and model artifacts. Tracked metrics include accuracy, precision, recall, F1-score, ROC-AUC, PR-AUC, and threshold.

### DagsHub

DagsHub provides the remote MLflow tracking server and a UI for comparing experiment runs.

### Joblib

Joblib serializes the fitted XGBoost model and preprocessing pipeline.

### Docker and Render

Docker makes the backend environment reproducible. The frontend and backend are deployed on Render.

### Logging

Logging covers data loading, dataset shapes, training, threshold selection, metrics, API failures, and artifact-loading failures.

## 15. Backend API flow

The backend is built with FastAPI.

At startup, the application loads models/best_model.pkl and models/best_preprocessor.pkl. They are kept in global variables and reused, avoiding model loading for every request.

Endpoint:

    POST /predict/

Example request:

    {
      "type": "TRANSFER",
      "amount": 100000,
      "oldbalanceOrg": 50000,
      "newbalanceOrig": 0,
      "oldbalanceDest": 10000,
      "newbalanceDest": 110000
    }

Pydantic validates required fields, transaction type, and non-negative amounts and balances. Invalid requests receive HTTP 422.

Prediction steps:

1. Load the model and preprocessor.
2. Load the optimized threshold from best_metrics.json.
3. Convert the request to a one-row pandas DataFrame.
4. Apply the saved preprocessing pipeline, including feature engineering.
5. Generate the fraud probability.
6. Compare it with the optimized threshold.
7. Return prediction, probability, threshold, and risk factors.

Core logic:

    probability = model.predict_proba(processed_data)[0][1]
    prediction = int(probability >= threshold)

Example response:

    {
      "prediction": 1,
      "prediction_label": "Fraud",
      "fraud_probability": 0.8537,
      "risk_factors": [
        "Sender balance equals transaction amount",
        "Sender balance drained to zero",
        "Transaction type commonly used in fraud"
      ],
      "threshold": 0.001149877
    }

Risk factors are simple rule-based explanations. They check whether the sender balance equals the amount, the sender balance becomes zero, the receiver balance remains unchanged, or the type is TRANSFER/CASH_OUT. They are not SHAP explanations.

Prediction exceptions become structured HTTP 500 responses. CORS is enabled so the static frontend can call the backend.

## 16. Frontend flow

The frontend uses HTML, CSS, and vanilla JavaScript:

1. User enters transaction details.
2. JavaScript sends a POST request to /predict/.
3. The result displays the fraud label, probability, threshold, and risk factors.
4. The artifacts page calls GET /artifacts/ and displays the latest run, metrics, confusion matrix, ROC curve, and PR curve.

## 17. Common interview questions

### Why is fraud detection imbalanced?

Fraud is rare compared with legitimate transactions. Here it represents only about 0.13% of rows.

### Why is accuracy insufficient?

A model predicting every transaction as legitimate could get approximately 99.87% accuracy while detecting no fraud.

### Why is recall important?

Recall = TP / (TP + FN). It measures the percentage of actual fraud caught. Missing fraud causes financial loss.

### Why is precision important?

Precision = TP / (TP + FP). It measures how many fraud alerts are correct. Low precision causes too many false alerts and customer friction.

### Why PR-AUC instead of ROC-AUC?

ROC-AUC can look excellent when the majority class is extremely large. PR-AUC focuses more directly on performance for the rare fraud class.

### Why XGBoost?

It is strong for tabular data, learns nonlinear interactions, supports class weighting and subsampling, scales well, supports GPU training, and outputs probabilities for threshold tuning.

### Why not SMOTE?

The dataset is very large, and synthetic oversampling could be expensive or create unrealistic transactions. Cost-sensitive learning is simpler here.

### Why drop account names?

They are high-cardinality identifiers that do not generalize well and may cause memorization.

### Why drop isFlaggedFraud?

It is an existing rule-based flag and could leak target information.

### Why is the threshold so low?

Severe imbalance and class weighting affect probability distributions. A threshold of 0.5 would miss too many fraud cases. The threshold was selected to maximize recall under a precision constraint.

### How did you avoid preprocessing leakage?

The preprocessor was fitted only on training data; validation and test data were transformed using that fitted pipeline.

### What happens with an unseen category?

OneHotEncoder(handle_unknown="ignore") prevents inference from failing.

### Training versus threshold tuning?

Training learns the feature-to-target relationship. Threshold tuning converts probability scores into business decisions. The model can remain unchanged while the threshold changes.

### What would you monitor in production?

- Fraud rate
- Probability distribution
- Precision and recall after labels arrive
- False-positive and false-negative rates
- Input-data drift
- Transaction-type distribution
- API latency and errors
- Threshold performance over time

### Current limitations?

- Dataset is synthetic rather than real banking data.
- No explicit production drift-monitoring system is implemented.
- Current training uses holdout validation, not implemented k-fold CV.
- Risk factors are rule-based, not SHAP-based.
- No online learning.
- Authentication and rate limiting are not implemented.
- Balance-error features could use absolute residuals.
- Test precision is slightly below the validation constraint.

## 18. Strong closing answer

The key design decision was treating this as a rare-event detection problem rather than a normal accuracy-based classification problem. I combined domain feature engineering, stratified splitting, cost-sensitive XGBoost training, PR-AUC-based evaluation, and validation-based threshold optimization. The final model catches 99.76% of fraud cases on the held-out test set while maintaining approximately 64.8% precision. I then packaged the preprocessing and model together, tracked experiments with MLflow and DVC, and exposed the model through a FastAPI service for real-time inference.
