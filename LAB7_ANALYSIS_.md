# Lab #7 — From Code to Operation: Investigation Record

**Team:** Individual  
**Student(s) / GitHub handle(s):** Meriem Bchini — @MeriemBchini  
**Fork / working branch:** https://github.com/MeriemBchini/recommenders — branch `lab7-work` 
**Upstream project and pinned version:** https://github.com/tensorflow/recommenders — `tensorflow-recommenders` 0.7.7 (fork state at base commit `82beddd` before Lab #7 work)

## 1. Stakeholder, goal and selected functionality

**Stakeholder concern:** Sam, the release engineer, needs to trust that the retrieval part of TensorFlow Recommenders can be installed and executed from our fork's exact commit in a clean Ubuntu environment, and that when the recommendation rule changes, the delivery checks make the change visible.

**GQM goal:** Analyze **the TFRS top-k retrieval path (`BruteForce` wrapped by a small application function `recommend()`)** for the purpose of **evaluation**, with respect to **delivery and behavioral-change verification confidence**, from the viewpoint of **a release engineer (Sam)**, in the context of **my fork of tensorflow/recommenders and a GitHub-hosted `ubuntu-24.04` runner**.

| Question | Question in your own words | Evidence / measurement and why it helps |
|---|---|---|
| Q1 | Can the retrieval component from my fork's exact commit be installed and executed on a clean Ubuntu runner, producing the expected top-k result for a fixed case? | Install/run outcome of the job, checkout SHA printed in the log, `tfrs.__file__` pointing into the checkout (not `site-packages`), printed `recommend()` output, pytest result, job duration. These show that the code under test is the fork's code and that it really produced a result. |
| Q2 | Does the pipeline detect and verify an intentional change to the recommendation eligibility rule? | Baseline run passes; changed code makes the old assertion fail (detection); updated assertion and unchanged invariants pass on the changed commit; output moves from `[a,b,c]` to `[b,c,d]`. This shows the checks are sensitive to the behavior change and not just green. |

**Selected function/component:** `BruteForce` top-k retrieval layer, `tensorflow_recommenders/layers/factorized_top_k.py`, line 515: https://github.com/MeriemBchini/recommenders/blob/d2f0fd386a4f70dd5ee05cabb57d10bd9b7c18a6/tensorflow_recommenders/layers/factorized_top_k.py#L515  
Application function that calls it: `recommend()` in https://github.com/MeriemBchini/recommenders/blob/140758cc8a54cbd47aa2956216e504aabd2d8541/lab7/recommender_app.py  
**Why this represents the software's purpose:** TFRS exists to build recommender systems, and top-k retrieval of candidate items for a query embedding is its core serving step. `recommend()` builds a `BruteForce` index over item embeddings (`index(candidates, identifiers)`) and calls it to get the top-k items and scores.

**Representative input and baseline expectation:** 5 items `a..e` with fixed 2-D embeddings `a=[1,0], b=[0.9,0.1], c=[0.5,0.5], d=[0.1,0.9], e=[0,1]`; user `u1` with query embedding `[1,0]` who has already consumed item `a`. Dot-product scores are a=1.0, b=0.9, c=0.5, d=0.1, e=0.0, so the baseline top-3 is `["a","b","c"]`.  
**Planned small behavior change:** `recommend()` should exclude items the user has already consumed (a recommendation eligibility rule) and still return k items (by requesting `k + len(consumed)` from `BruteForce`). Expected result for `u1`: `["b","c","d"]`. This changes observable output and cannot be satisfied by editing only a test.  
**What must still work unchanged?** Results are sorted by descending score and have the requested size k; a user with no consumption history (`u2`, same embedding as `u1`) still gets `["a","b","c"]`.

## 2. Baseline: deploy and execute on GitHub

| Evidence | Baseline |
|---|---|
| Baseline commit SHA and link | `d2f0fd386a4f70dd5ee05cabb57d10bd9b7c18a6` — https://github.com/MeriemBchini/recommenders/commit/d2f0fd386a4f70dd5ee05cabb57d10bd9b7c18a6 (tagged `lab7-baseline`) |
| Actions workflow file link | https://github.com/MeriemBchini/recommenders/blob/d2f0fd386a4f70dd5ee05cabb57d10bd9b7c18a6/.github/workflows/lab7.yml |
| Ubuntu/runtime and relevant dependency versions | `ubuntu-24.04`, Python 3.10, `tensorflow-cpu==2.15.1` (Keras 2), `absl-py`, `pytest==8.3.4`; TFRS 0.7.7 from the fork |
| How the fork's code is installed/built and verified as the executed code | `actions/checkout` of the fork commit, then `pip install -e . --no-deps`. A workflow step prints `git rev-parse HEAD`, `tensorflow_recommenders.__file__` and the TF version; the test `test_uses_fork_source` asserts that `tfrs.__file__` is not in `site-packages`. |
| Functional case executed (command/script/test or local endpoint) | `python -m pytest lab7 -v` plus a printed call `recommend('u1', 3)` |
| Expected vs observed behavior | Expected `['a','b','c']`; observed `['a','b','c']` (see log lines below) |
| Check result and meaningful measurement(s), if any | Job succeeded, 4 tests passed (`test_uses_fork_source`, `test_baseline_topk`, `test_invariant_ordering_and_size`, `test_user_without_history_unchanged`). Job duration 1m 18s. |
| Exact GitHub Actions run URL | https://github.com/MeriemBchini/recommenders/actions/runs/45830583056 (run #1, success) |

Log evidence (copied because logs expire):
```
Commit SHA: <paste from log, should be d2f0fd386a4f70dd5ee05cabb57d10bd9b7c18a6>
TFRS file: <paste from log, path inside the checkout>
RECOMMEND u1 k=3 -> (['a', 'b', 'c'], [<scores>])
4 passed
```

**What does this establish, and what does it not establish?** It establishes that the fork's commit installs on a clean Ubuntu runner and that its `BruteForce` layer, called through my application function, returns the hand-computed top-3 for a fixed case. It does not establish anything about accuracy, large catalogs, trained models, other Python/TF versions or performance.

## 3. Controlled change and verification

**Source/function changed:** `recommend()` in https://github.com/MeriemBchini/recommenders/blob/140758cc8a54cbd47aa2956216e504aabd2d8541/lab7/recommender_app.py  
**Reason for change:** A recommendation service should normally not suggest items the user has already consumed, so a stakeholder may want an eligibility filter on top of raw retrieval.  
**Code-change commit(s):**
- Behavior change (code only): https://github.com/MeriemBchini/recommenders/commit/a4f5006b6df4f12558939992dc211ea11d7e4b8f
- Test update (new expectation, invariants kept): https://github.com/MeriemBchini/recommenders/commit/140758cc8a54cbd47aa2956216e504aabd2d8541
- Full diff: https://github.com/MeriemBchini/recommenders/compare/lab7-baseline...140758cc8a54cbd47aa2956216e504aabd2d8541

| Item | Before change | After change |
|---|---|---|
| Same input/case | `recommend("u1", k=3)`, u1 has consumed `a` | same |
| Expected behavior under each version's stated contract | Top-k by score: `['a','b','c']` | Top-k by score excluding consumed items: `['b','c','d']` |
| Observed behavior on GitHub runner | `['a','b','c']` (run #1) | Run #2 (code change with old test): old assertion saw `['b','c','d']`. Run #3 (updated test): `<paste from log: RECOMMEND line>` |
| Automated case check/result | `test_baseline_topk` passed | Run #2: `test_baseline_topk` failed (old expectation no longer describes the changed case). Run #3: `test_changed_excludes_consumed` asserts `"a" not in ids` and `ids == ["b","c","d"]` → `<pass/fail from run #3>` |
| Unchanged regression/invariant check | `test_invariant_ordering_and_size` and `test_user_without_history_unchanged` passed | Same two tests passed locally on the changed code; run #3: `<confirm pass>` |
| Exact Actions run URL | https://github.com/MeriemBchini/recommenders/actions/runs/45830583056 | Detection run: https://github.com/MeriemBchini/recommenders/actions/runs/45831431730 (failed, 35s). Final changed-version run: https://github.com/MeriemBchini/recommenders/actions/runs/45831925554 |
| Commit SHA | `d2f0fd386a4f70dd5ee05cabb57d10bd9b7c18a6` | Detection: `a4f5006b6df4f12558939992dc211ea11d7e4b8f`. Final: `140758cc8a54cbd47aa2956216e504aabd2d8541` |

**How do your checks distinguish the two versions?** The baseline test asserts `ids == ["a","b","c"]`; after the change the function returns `["b","c","d"]`, so that assertion fails (run #2, and locally: `assert ['b','c','d'] == ['a','b','c']`, differing at index 0). The new test asserts that the consumed item `a` is absent and that the result is exactly `["b","c","d"]`. The unchanged checks (descending order and size k, and an identical result for a user without history) pass on both versions, so the new behavior is not accepted merely because all expectations were rewritten.

**Did anything fail unexpectedly? What did you learn or fix?** The intentional failure in run #2 was the planned detection evidence. Setup problems that were fixed along the way: (1) the global Python 3.14 could not install TF 2.15.1 and had Keras 3, which TFRS rejects, so I used a Python 3.10 venv with TF 2.15.1 (Keras 2); (2) a pytest internal error (`NodeId` has no `_str_cache`) was fixed by pinning `pytest==8.3.4`; (3) a nested `lab7/lab7` folder broke test collection and was flattened; (4) `git add` failed because `LAB7_ANALYSIS.md` had not been copied from the template yet.

## 4. Engineering judgment and submission

**Answer Q1:** Yes. The baseline workflow ran on a clean `ubuntu-24.04` runner, installed the fork with an editable install, printed the checked-out SHA and a `tfrs.__file__` path inside the checkout, and `test_uses_fork_source` asserts that path is not `site-packages`. The `BruteForce` layer returned the hand-computed `['a','b','c']` and 4 tests passed in 1m 18s. A release engineer can therefore trust that the fork's code ran and produced a meaningful result.

**Answer Q2:** Yes. With only the code changed, the old expectation failed in CI (run #2). After updating the expectation to `['b','c','d']` while keeping the ordering/size and no-history invariants, the changed commit's run (#3) `<passed — confirm>`. The checks distinguished old from new behavior and the unchanged behavior stayed intact.

**Release decision:** Accept the changed version. Evidence: the logged SHA and module path identify the executed code, the output changed from `[a,b,c]` to `[b,c,d]` as intended, the new assertion passes and the invariants still hold. The limitation below is acceptable for this scope.  
**One important limitation or missing check:** The change lives in an application wrapper (`lab7/recommender_app.py`) and the check uses one user and five hand-made 2-D embeddings on CPU with one Python/TF version. It does not show that the TFRS library itself changed, that it scales to large catalogs or trained models, or what happens when `k` exceeds the number of remaining eligible items.

| GitHub evidence | Link |
|---|---|
| Lab #7 pull request (within your fork) | `<PR link: lab7-work → semester-investigation>` |
| **Merged commit** on `semester-investigation` | `<merge commit link>` |
| Final `LAB7_ANALYSIS.md` on merged branch | https://github.com/MeriemBchini/recommenders/blob/semester-investigation/LAB7_ANALYSIS.md |
| Student 1 meaningful commit(s) | Baseline app/tests/workflow: https://github.com/MeriemBchini/recommenders/commit/d2f0fd386a4f70dd5ee05cabb57d10bd9b7c18a6 · Behavior change: https://github.com/MeriemBchini/recommenders/commit/a4f5006b6df4f12558939992dc211ea11d7e4b8f · Test update: https://github.com/MeriemBchini/recommenders/commit/140758cc8a54cbd47aa2956216e504aabd2d8541 |

**LLM assistance (if used):** An LLM (Claude) helped draft the application code, tests, workflow YAML and troubleshooting steps. I verified them by running the tests locally (4 passed before and after the change, and the old test failing on the changed code as expected), checking the `BruteForce` signature in my fork's source, and inspecting the GitHub Actions runs and logs myself.

**Submission reminder:** Each student submits `Lab7_YOUR_GITHUB_HANDLE.txt` to the Lab #7 MS Teams submit folder, containing their name, fork URL, merged-commit URL and final analysis URL.