# Hallucination Audit Report
**Subject:** Tailored Resume - John Doe
**Target Role:** InnovateCorp - Senior Product Manager - AI Solutions

## Executive Summary
The tailored resume successfully re-framed the candidate's experience but introduced several specific claims regarding AI/ML experience and skills that are **not supported** by the Raw Resume. These constitute factual hallucinations and must be verified or removed.

## Audit Findings

### Critical Severity (Factual Fabrications)

1.  **Claim:** Managed "AI-driven products" and "AI solutions" at Tech Innovations Inc.
    *   **Reality:** Raw Resume states "SaaS platform" and "multiple products." There is no evidence these products utilized AI or ML.
    *   **Violation:** Fabricating the *nature* of the product to match the job description.

2.  **Claim:** "Partnered with data science... teams."
    *   **Reality:** Raw Resume lists collaboration with "engineering, design, and sales." Data Science is not mentioned.
    *   **Violation:** Inventing specific cross-functional relationships.

3.  **Claim:** Skills: "Natural Language Processing (NLP)", "MLOps".
    *   **Reality:** Raw Resume lists "Machine Learning Fundamentals." NLP and MLOps are distinct, specialized skills not claimed in the source.
    *   **Violation:** Hallucinating technical competencies.

### Minor Severity (Inferences & Re-phrasing)

1.  **Claim:** "B2B SaaS platform" (Tech Innovations).
    *   **Reality:** Raw Resume says "SaaS platform" (current role) and "B2B enterprise software" (past role).
    *   **Verdict:** Acceptable Inference. Combining "SaaS" with the candidate's B2B history is a logical, low-risk inference.

2.  **Claim:** "PRDs and User Stories."
    *   **Reality:** Raw Resume says "detailed product specifications."
    *   **Verdict:** Acceptable Re-phrasing. Standard industry terminology mapping.

## Recommendations
1.  **Revert** the description of Tech Innovations products to "Data-Intensive SaaS" or similar, unless the candidate confirms AI involvement.
2.  **Remove** "Data Science" from the collaboration list unless verified.
3.  **Remove** "NLP" and "MLOps" from skills unless the candidate can provide evidence (e.g., side projects, unlisted certs).
