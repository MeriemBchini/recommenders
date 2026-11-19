# Lab #6 – Investigation Record

**Team / student(s):** [meriem bchini]  
**Mode:** Individual  
**Approved upstream project:** TensorFlow Recommenders  
**Repository:**https://github.com/MeriemBchini/recommenders
**Working branch:** main
**Baseline SHA:*abdbe4319718f2c6ad5ac681ede78a37aa508c9a* 
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

## Task 2 – Detect and Investigate Code Smells

### Preliminary Findings



| Candidate | Location | Observation |
|---|---|---|
| C1 | `tensorflow_recommenders/tasks/
retrieval.py` | Maximum Line Length: line exceeds the configured 80-character limit. |
| C2 | `Streaming.call` | Method combines query handling, candidate scoring, top-K reduction, and result assembly. |
| C3 | `ScaNN` and `Streaming` | Classes manage several responsibilities, including indexing and querying. |
| C4 | Ranking/factorized tests | Repeated dataset creation and model setup patterns. |

### Selected Issue: C1 – Maximum Line Length

**File:**' tensorflow_recommenders/tasks/
retrieval.py'
**Location:** Line84-87

**Tool finding:**
- Rule: Enforce Maximum Line Length
- Severity: Minor
- Category: Code style
- Reported line length: 87/80
- Estimated fixing time: 3 minutes

**Problem:**

The error message contains a line exceeding the configured maximum length of 80 characters. Long lines can reduce readability and make the code harder to maintain.

**Planned improvement:**

Reformat the string across shorter lines while preserving the exact error message and behavior.

## Task 3 – Prioritize Technical Debt and Plan Refactoring

| Candidate | Expected impact | Effort | Decision |
|---|---|---|---|
| C1 – Maximum Line Length | Improves readability with minimal changes. | Very low | Prioritize now. |
| C2 – Long Method | Improves method organization. | Medium | Defer. |
| C3 – Large Class | Could improve modularity. | High | Defer. |
| C4 – Duplicated Code | Reduces repeated logic. | Medium | Defer. |

|---|---|---|---|---|
| [Your name / GitHub handle] | C1 | Split the long string into shorter lines without changing its content. | Improved readability and compliance with the 80-character limit. | Ruff check and relevant tests. |

## Task 4 – Refactor, Verify, and Commit

### Before Refactoring

self._loss = loss if loss is not None else tf.keras.losses.CategoricalCrossentropy(
    from_logits=True, reduction=tf.keras.losses.Reduction.SUM)
"true_candidate_ids`, which will be checked against "
```

### Planned Refactoring

Reformat the affected code while preserving the original error message. 



### Verification

PS C:\Users\Asus\OneDrive\Bureau\lab5\recommenders> git diff
diff --git a/tensorflow_recommenders/tasks/retrieval.py b/tensorflow_recommenders/tasks/retrieval.py
index cfba04f..fcc0c3e 100644
--- a/tensorflow_recommenders/tasks/retrieval.py
+++ b/tensorflow_recommenders/tasks/retrieval.py
@@ -1,3 +1,4 @@
+
 # Copyright 2026 The TensorFlow Recommenders Authors.
 #
 # Licensed under the Apache License, Version 2.0 (the "License");
:

- Confirm that the line-length warning is resolved.
PS C:\Users\Asus\OneDrive\Bureau\lab5\recommenders> ruff check --select E501 tensorflow_recommenders/tasks/retrieval.py
All checks passed!
- Run relevant tests for `tensorflow_recommenders/tasks/
retrieval.py`.

### Results

| Measurement | Before | After |
|---|---|---|
| Maximum line length | 87 characters | [Result] |
| Line-length warning | 7 | [Result] |
| Relevant tests | [Baseline result] | [Result] |

### GQM Answers

**Q1:** The investigation identified readability concerns, including a line exceeding the configured 80-character limit. The selected refactoring aims to improve readability through consistent formatting.

**Q2:** Other potential duplication patterns were observed in ranking/factorized tests and retrieval classes. Further analysis with jscpd is required to quantify and confirm them.

### Conclusion

The selected issue is a small, low-risk maintainability improvement. The refactoring aims to improve code readability without changing the software's behavior. GitHub analysis and relevant tests will provide evidence of the result.


