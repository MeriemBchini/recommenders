# Lab #7 — From Code to Operation: Investigation Record

**Team:** [Team name]  
**Student(s) / GitHub handle(s):** [Name — @handle; Name — @handle]  
**Fork / working branch:** [Link]  
**Upstream project and pinned version:** [Link / tag / SHA]

## 1. Stakeholder, goal and selected functionality

**Stakeholder concern:** [What does the release engineer need to trust?]

**GQM goal:** Analyze **[component/process]** for the purpose of **[evaluation/improvement]**, with respect to **[delivery/operational quality focus]**, from the viewpoint of **[stakeholder]**, in the context of **[fork and GitHub-hosted Ubuntu environment]**.

| Question | Question in your own words | Evidence / measurement and why it helps |
|---|---|---|
| Q1 | | |
| Q2 | | |

**Selected function/component:** [Name and direct GitHub source link]  
**Why this represents the software's purpose:** [1–3 sentences]  
**Representative input and baseline expectation:** [Input and specific expected result/behavior]  
**Planned small behavior change:** [What will intentionally differ, and why?]  
**What must still work unchanged?** [Regression check/invariant]

## 2. Baseline: deploy and execute on GitHub

| Evidence | Baseline |
|---|---|
| Baseline commit SHA and link | |
| Actions workflow file link | |
| Ubuntu/runtime and relevant dependency versions | |
| How the fork's code is installed/built and verified as the executed code | |
| Functional case executed (command/script/test or local endpoint) | |
| Expected vs observed behavior | |
| Check result and meaningful measurement(s), if any | |
| Exact GitHub Actions run URL | |

**What does this establish, and what does it not establish?** [2–3 sentences]

## 3. Controlled change and verification

**Source/function changed:** [GitHub code link]  
**Reason for change:** [Why a stakeholder might want this behavior]  
**Code-change commit(s):** [Direct GitHub URL(s)]

| Item | Before change | After change |
|---|---|---|
| Same input/case | | |
| Expected behavior under each version's stated contract | | |
| Observed behavior on GitHub runner | | |
| Automated case check/result | | |
| Unchanged regression/invariant check | | |
| Exact Actions run URL | | |
| Commit SHA | | |

**How do your checks distinguish the two versions?** [Explain the assertion(s); include any informative failed check and its interpretation, if observed.]

**Did anything fail unexpectedly? What did you learn or fix?** [Briefly explain, or write "None observed".]

## 4. Engineering judgment and submission

**Answer Q1:** [Evidence-based answer]  
**Answer Q2:** [Evidence-based answer]

**Release decision:** [Accept changed version / request changes / insufficient evidence — and why]  
**One important limitation or missing check:** [What your experiment cannot prove]

| GitHub evidence | Link |
|---|---|
| Lab #7 pull request (within your fork) | |
| **Merged commit** on `semester-investigation` | |
| Final `LAB7_ANALYSIS.md` on merged branch | |
| Student 1 meaningful commit(s) | |
| Student 2 meaningful commit(s), if a pair | |

**LLM assistance (if used):** [What did it help generate, and what did you independently verify?]

**Submission reminder:** Each student submits `Lab7_YOUR_GITHUB_HANDLE.txt` to the Lab #7 MS Teams submit folder, containing their name, fork URL, merged-commit URL and final analysis URL.
