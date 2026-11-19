# Lab #6 – Investigation Record

**Team / student(s):** Meriem Bchini  
**Mode:** Individual  
**Approved upstream project:** TensorFlow Recommenders  
**Repository:** https://github.com/MeriemBchini/recommenders  
**Working branch:** `main`

---

## Task 1 – Stakeholder, GQM, and Code Smell Selection

### Stakeholder: Alex – Software Maintainer

Alex wants to improve code readability and make the software easier to understand, modify, and maintain.

### GQM Goal

Analyze the Python source code of TensorFlow Recommenders to evaluate its maintainability, with respect to code readability, complexity, and duplication, from the viewpoint of a software maintainer.

### Measurement Questions

| Question | Description | Metrics |
|---|---|---|
| Q1 | To what extent does the source code contain readability and complexity issues? | Line length, method length, cyclomatic complexity. |
| Q2 | To what extent does the source code contain duplicated code that increases maintenance effort? | Duplication percentage and repeated code fragments. |

### Selected Code Smells

| Code Smell | Motivation | Investigation |
|---|---|---|
| Long Method | Complex methods are harder to understand and maintain. | Method length and complexity analysis. |
| Large Class | Excessive responsibilities reduce modularity. | Manual class inspection. |
| Duplicated Code | Repeated code increases maintenance effort. | jscpd analysis. |
| Long Parameter List | Too many parameters make functions harder to understand. | Parameter count and source inspection. |

**Primary tool:** Codacy Cloud  
**Complementary tool:** Ruff

---

## Task 2 – Detect and Investigate Code Smells

### Preliminary Findings

| Candidate | Location | Observation |
|---|---|---|
| C1 | `tensorflow_recommenders/tasks/retrieval.py` | Maximum Line Length: line exceeds the configured 80-character limit. |
| C2 | `Streaming.call` | Method combines query handling, candidate scoring, top-K reduction, and result assembly. |
| C3 | `ScaNN` and `Streaming` | Classes manage several responsibilities, including indexing and querying. |
| C4 | Ranking/factorized tests | Repeated dataset creation and model setup patterns. |

### Selected Issue: C1 – Maximum Line Length

**File:** `tensorflow_recommenders/tasks/retrieval.py`  
**Location:** Line 86

**Tool finding:**
- Rule: Enforce Maximum Line Length
- Severity: Minor
- Category: Code style
- Reported line length: 87/80
- Estimated fixing time: 3 minutes

**Problem:**

The assignment of the `CategoricalCrossentropy` loss function exceeds the configured maximum line length of 80 characters. Long lines can reduce readability and make code harder to understand and maintain.

**Original code:**

```python
self._loss = loss if loss is not None else tf.keras.losses.CategoricalCrossentropy(
    from_logits=True, reduction=tf.keras.losses.Reduction.SUM)
```

**Proposed refactoring:**

```python
self._loss = (
    loss
    if loss is not None
    else tf.keras.losses.CategoricalCrossentropy(
        from_logits=True,
        reduction=tf.keras.losses.Reduction.SUM,
    )
)
```

**Expected improvement:**

Reformat the conditional expression and constructor arguments across shorter lines while preserving the original behavior.

---

## Task 3 – Prioritize Technical Debt and Plan Refactoring

| Candidate | Expected impact | Effort | Decision |
|---|---|---|---|
| C1 – Maximum Line Length | Improves readability with minimal changes. | Very low | Prioritize now. |
| C2 – Long Method | Improves method organization. | Medium | Defer. |
| C3 – Large Class | Could improve modularity. | High | Defer. |
| C4 – Duplicated Code | Reduces repeated logic. | Medium | Defer. |

### Refactoring Assignment

| Student | Selected issue | Planned change | Expected result | Verification |
|---|---|---|---|---|
| Meriem Bchini | C1 – Maximum Line Length | Split the conditional expression and constructor arguments across shorter lines. | Improved readability and compliance with the 80-character limit. | Ruff check and relevant tests. |

---

## Task 4 – Refactor, Verify, and Commit

### Before Refactoring

The original code contained a long conditional assignment:

```python
self._loss = loss if loss is not None else tf.keras.losses.CategoricalCrossentropy(
    from_logits=True, reduction=tf.keras.losses.Reduction.SUM)
```

The first line exceeded the configured 80-character limit.

### After Refactoring

The proposed change formats the conditional expression and constructor arguments across multiple lines:

```python
self._loss = (
    loss
    if loss is not None
    else tf.keras.losses.CategoricalCrossentropy(
        from_logits=True,
        reduction=tf.keras.losses.Reduction.SUM,
    )
)
```

### Verification

**Git diff**

The recorded `git diff` output showed an additional blank line at the beginning of `retrieval.py`. The actual formatting change still needs to be verified in the committed version.

**Ruff check**

Command:

```bash
ruff check --select E501 tensorflow_recommenders/tasks/retrieval.py
```

Result:

```text
All checks passed!
```

This confirms that Ruff did not report any E501 line-length violations in the checked file.

**Relevant tests**

Command:

```bash
python -m pytest tensorflow_recommenders/tasks/
```




### GQM Answers

**Q1: To what extent does the source code contain readability and complexity issues?**

The investigation identified several potential maintainability concerns, including long methods, large classes, and a line exceeding the configured 80-character limit. The selected issue focuses on improving readability through consistent formatting.

**Q2: To what extent does the source code contain duplicated code that increases maintenance effort?**

Potential duplication patterns were observed in ranking and factorized tests. 

---

## Commit Information


**Latest commit SHA:** `abdbe4319718f2c6ad5ac681ede78a37aa508c9a`

**Commit message:** `Fix long line in retrieval task`

**Repository:** https://github.com/MeriemBchini/recommenders

**Commit link:** https://github.com/MeriemBchini/recommenders/commit/abdbe4319718f2c6ad5ac681ede78a37aa508c9a



**Codacy before:** https://app.codacy.com/gh/MeriemBchini/recommenders/issues/current?categories=CodeStyle

**Codacy after:**https://app.codacy.com/gh/MeriemBchini/recommenders/issues/current?categories=CodeStyle
---

## Conclusion

The investigation identified a minor code-style issue in TensorFlow Recommenders. The selected issue was prioritized because it is localized, requires minimal effort, and offers an opportunity to improve code readability without changing program behavior.

The proposed refactoring separates the conditional expression and constructor arguments into shorter lines. Ruff reported no E501 violations in the checked file. The final evaluation should also confirm that the intended modification is present in the committed code, that relevant tests pass, and that the Codacy result reflects the improvement.