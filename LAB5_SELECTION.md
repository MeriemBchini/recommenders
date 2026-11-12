# Lab #5 - System Selection and Reproducibility Record

## People and collaboration

- **Working mode:**  Solo  [ ] 
- **Student A (name / GitHub):** Meriem Bchini / MeriemBchini
- **Student B (name / GitHub; if pair):** N/A unless working in a pair
- **Fork owner:** To be completed after creating the fork
- **Collaborator invitation accepted?** Not applicable if solo
- **Individual work differentiation:** `QUALITY_INVESTIGATION.md` in the selected repository. Add the GitHub link after committing the file.

---

## First shortlist - catalogue only

| Candidate | Catalogue-based reason | One concern to investigate |
|---|---|---|
| LightFM | Python library implementing hybrid recommendation algorithms combining collaborative and content-based filtering. | Older project activity and possible installation issues related to Cython and OpenMP. |
| TensorFlow Recommenders (TFRS) | TensorFlow-based framework supporting recommendation model development, training, evaluation and deployment. | TensorFlow/Keras version compatibility and computational requirements. |
| Ultralytics YOLO | Popular Python computer-vision framework supporting object detection, classification and other vision tasks. | AGPL-3.0 licensing and potentially higher computational requirements. |
| N/A | Third candidate shortlist is sufficient for individual work. | N/A |

---

## Evidence-based candidate assessment

**Legend:** Y = Yes; P = Partial; N = No; U = Unknown.

| Criterion | Candidate A: TensorFlow Recommenders | Candidate B: LightFM | Candidate C: Ultralytics YOLO | Candidate D |
|---|---|---|---|---|
| **C1 Public repository / licence / data rights** | **Y** – Public GitHub repository, Apache-2.0 licence. MovieLens dataset has research-use conditions that must be respected. Evidence: https://github.com/tensorflow/recommenders | **Y** – Public repository, Apache-2.0 licence. MovieLens dataset available for research under its usage conditions. Evidence: https://github.com/lyst/lightfm | **P** – Public repository, AGPL-3.0 licence or commercial enterprise licence. COCO dataset licensing must also be checked. Evidence: https://github.com/ultralytics/ultralytics | N/A |
| **C2 Pinned revision / runtime** | **Y** – Select release v0.7.7 and pin its commit. Requires Python environment and TensorFlow 2.x. Evidence: https://github.com/tensorflow/recommenders/releases | **P** – Python package available, but compatibility with Python, Cython and compiler versions needs verification. | **Y** – Python >=3.8 and PyTorch >=1.8 according to the repository installation instructions. A specific revision must be pinned. | N/A |
| **C3 Nontrivial source + refactoring** | **Y** – Contains model implementations, retrieval tasks, ranking tasks, evaluation metrics and feature-processing components. Suitable for investigating and refactoring nontrivial source code. | **Y** – Contains recommendation algorithms, feature representations and evaluation utilities. | **Y** – Contains model architecture, training, prediction and evaluation components. | N/A |
| **C4 Tests and expected-output oracle** | **P** – Repository tests are available. The MovieLens tutorial provides a reproducible execution procedure and evaluation output, but exact expected metric values must be established. | **P** – Tests and evaluation functions are available, including Precision@K and AUC. | **P** – Tests and validation procedures are available. Expected results depend on model weights, dataset and configuration. | N/A |
| **C5 AI/recommender ground-truth source and terms** | **Y** – MovieLens 100K provides real user ratings as recommendation ground truth. The tutorial uses an 80,000/20,000 train/test split. GroupLens research-use conditions apply. | **Y** – MovieLens ratings provide interaction labels for recommendation evaluation. Its examples use train/test data and Precision@K and AUC. | **Y** – COCO provides annotated object categories and bounding boxes as ground-truth labels for object detection. Dataset terms must be checked. | N/A |
| **C6 Evaluation procedure and metrics** | **Y** – Retrieval evaluation using FactorizedTopK and top-K recommendation metrics. The tutorial includes training and testing. | **Y** – Precision@K and ROC AUC are directly supported. | **Y** – Detection evaluation includes precision, recall and mAP. | N/A |
| **C7 Upstream GitHub history** | **Y** – Public history, issues, pull requests, releases and multiple contributors. Repository snapshot previously inspected: 243 issues, 37 open PRs, 308 closed PRs. Evidence: https://github.com/tensorflow/recommenders | **P** – Public history with 483 commits in the inspected repository snapshot, but less recent development activity than the other candidates. | **Y** – Public repository with extensive development history, issues, pull requests and releases. | N/A |
| **C8 CI/DevOps possibility** | **Y** – GitHub Actions workflows and automated testing provide a basis for CI investigation. | **Y** – Existing CI configuration includes CircleCI, Travis CI and AppVeyor. | **Y** – GitHub Actions and automated testing provide opportunities for CI investigation. | N/A |
| **C9 Laptop setup feasibility** | **P** – Installation through pip is documented. TensorFlow and Keras compatibility must be checked, and training may require additional resources. | **P** – Relatively lightweight recommendation framework, but native dependencies such as Cython and OpenMP can complicate installation. | **P** – Installation is documented, but training object-detection models can require substantial computational resources. | N/A |
| **C10 Continuation to Labs 6-9 / credible question** | **Y** – Strong opportunities for source-code investigation, refactoring, unit testing, CI, reproducibility and recommendation evaluation. | **Y** – Also suitable for recommendation evaluation, testing and refactoring, although its development activity is a concern. | **P** – Suitable for software quality and testing investigations, but less aligned with the recommendation-system evaluation focus. | N/A |

---

## Ground-truth verification notes

### Candidate A: TensorFlow Recommenders

- **Functional test assertion or specification URL:**
  - https://github.com/tensorflow/recommenders
  - https://github.com/tensorflow/recommenders/tree/main/tensorflow_recommenders
  - https://github.com/tensorflow/recommenders/tree/main/tensorflow_recommenders/layers
- **Recommendation ground-truth source:** MovieLens 100K dataset.
  - https://grouplens.org/datasets/movielens/100k/
- **Ground-truth labels:** Explicit user movie ratings and observed user-item interactions.
- **Evaluation metric:** FactorizedTopK, including top-K retrieval evaluation.
- **Train/test protocol:** The official tutorial shuffles the 100,000 ratings using seed 42 and separates them into 80,000 training examples and 20,000 test examples.
- **Data terms:** Research use is permitted under GroupLens conditions. Acknowledge the dataset, do not imply endorsement, and do not redistribute it without permission.
  - https://files.grouplens.org/datasets/movielens/ml-100k-README.txt
- **Official tutorial:** https://github.com/tensorflow/recommenders/blob/main/README.md

### Candidate B: LightFM

- **Functional test assertion or specification URL:**
  - https://github.com/lyst/lightfm
  - https://github.com/lyst/lightfm/tree/master/tests
- **Recommendation ground-truth source:** MovieLens dataset.
- **Ground-truth labels:** User-item ratings and interactions.
- **Evaluation metrics:** Precision@K and ROC AUC.
- **Train/test protocol:** The MovieLens example separates ratings into training and testing matrices and evaluates recommendations against the test interactions.
- **Data terms:** GroupLens research-use conditions apply.
- **Evaluation example:** https://github.com/lyst/lightfm/blob/master/examples/movielens/readme.md

### Candidate C: Ultralytics YOLO

- **Functional test assertion or specification URL:**
  - https://github.com/ultralytics/ultralytics
  - https://github.com/ultralytics/ultralytics/tree/main/tests
- **Ground-truth source:** COCO object-detection dataset.
- **Ground-truth labels:** Annotated object categories and bounding boxes.
- **Evaluation metrics:** Precision, recall and mean Average Precision (mAP).
- **Evaluation procedure:** Train or load a model, perform predictions on a validation dataset and compare predicted bounding boxes with annotated ground truth.
- **Data terms:** Check the COCO dataset terms separately from the Ultralytics AGPL-3.0 software licence.
- **Documentation:** https://docs.ultralytics.com/

---

## Decision

### Final SUT and short description

**Selected SUT: TensorFlow Recommenders (TFRS)**

Repository: https://github.com/tensorflow/recommenders

TensorFlow Recommenders is an open-source Python library built on TensorFlow and Keras for developing recommendation systems.

It supports the complete recommendation workflow, including:

- Data preparation and feature processing.
- User and item representation models.
- Model training and optimization.
- Retrieval and ranking tasks.
- Recommendation evaluation.
- Model deployment.

The project will focus on investigating the source code, its testing infrastructure, evaluation procedures and reproducibility.

### Why it is better suited than rejected alternatives

TensorFlow Recommenders is the most appropriate candidate because it offers a good combination of software engineering complexity and measurable AI functionality.

Compared with LightFM, TFRS provides a broader TensorFlow-based architecture with several components that can be investigated and refactored.

Compared with Ultralytics YOLO, TFRS is more aligned with the recommendation-system evaluation task. It also provides an accessible benchmark using MovieLens data and built-in retrieval metrics.

Other advantages include:

1. A public GitHub repository.
2. An Apache-2.0 licence.
3. Existing tests and CI infrastructure.
4. A documented MovieLens recommendation example.
5. Quantitative evaluation through top-K recommendation metrics.
6. Opportunities to investigate software quality and reproducibility.

### Rejected alternatives and reasons

**1. LightFM**

LightFM is a valid alternative because it supports hybrid recommendation algorithms and has evaluation metrics such as Precision@K and AUC.

However, its older development activity and potential Cython/OpenMP installation difficulties make it a less attractive choice for this investigation.

**2. Ultralytics YOLO**

Ultralytics YOLO is a mature computer-vision framework with extensive source code, testing possibilities and evaluation metrics.

However, it focuses on object detection rather than recommendation systems. Its AGPL-3.0 licensing and computational requirements are additional considerations.

### Backup SUT and trigger for switching

**Backup: Ultralytics YOLO**

Switch to Ultralytics only if TensorFlow Recommenders cannot be installed reproducibly, its dependencies cannot be stabilized, or its tests cannot be executed successfully in the available laptop environment.

LightFM remains another possible alternative if the installation and evaluation requirements can be satisfied.

### Biggest unresolved risk / mitigation

**Risk:** TensorFlow/Keras version compatibility and reproducibility across environments.

**Mitigation:**

- Pin the selected TFRS release and its exact Git commit.
- Create an isolated Python virtual environment.
- Record the Python, TensorFlow and TFRS versions.
- Save the dependency list in `requirements.txt`.
- Set random seeds for reproducible experiments.
- Keep the training/test split fixed.
- Run the existing tests before modifying source code.
- Record installation errors and test results.
- Document the hardware and execution environment.

---

## Repository provenance and pair access

- **Original upstream repo URL:** https://github.com/tensorflow/recommenders
- **Selected original tag:** `v0.7.7`
- **Release commit shown by GitHub:** `cf1dafa` (short SHA; record the full SHA locally).
- **Selected branch:** Release tag `v0.7.7`, rather than an unpinned `main` branch.
- **Fork URL:** To be completed after creating your GitHub fork.
- **Fork owner:** To be completed.
- **Collaborator access:** Not applicable if working individually.

### Reproducibility commands

After creating your fork, use the following commands to establish the exact repository revision:

```bash
# Clone the upstream repository
git clone https://github.com/tensorflow/recommenders.git

cd recommenders

# Inspect available releases
git tag -l

# Check out the selected release
git checkout v0.7.7

# Record the exact revision
git rev-parse HEAD

# Record the current repository state
git status

# Create a Python virtual environment
python -m venv .venv
```

Activate the environment:

**Windows:**

```powershell
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

Install the framework:

```bash
python -m pip install --upgrade pip
pip install tensorflow
pip install tensorflow-recommenders==0.7.7
```

Record the installed versions:

```bash
python --version
pip show tensorflow
pip show tensorflow-recommenders
```

After installation, execute the repository's existing tests using the documented test procedure and record the actual results. Do not report tests as passing until they have been executed.

---

## Final investigation direction

**Proposed research question:**

How can software refactoring and automated testing improve the maintainability and reproducibility of TensorFlow Recommenders without changing its recommendation evaluation results?

Possible investigation areas for subsequent laboratories:

- Source-code complexity and maintainability.
- Identification of refactoring opportunities.
- Unit and integration testing.
- Regression testing of recommendation metrics.
- CI automation using GitHub Actions.
- Reproducibility of model training and evaluation.
- Comparison of results before and after refactoring.

**Expected outcome:** A reproducible investigation showing whether selected software quality improvements can be introduced while preserving the functional behavior and recommendation evaluation results of TensorFlow Recommenders.