# VS-TEST: Cloud Connectivity Check

## Metadata
```yaml
metadata:
  story_id: "VS-TEST"
  provider: "google-gemini"
  preferred_model: "gemini-2.5-flash"
```

## Goal
```yaml
goal:
  as_a: "Cloud Connectivity Tester"
  i_want: "To verify that the AVS Toolkit can successfully route this prompt to Google Gemini."
  so_that: "I can confidently run strategic workloads in the cloud."
```

## Instructions
```yaml
instructions:
  execution_steps:
    - step: 1
      action: "Reply with the exact phrase: 'Connection Successful: Hello from Google Gemini!'"
      validation_rule: "The response matches the phrase."
```

## Context Manifest
```yaml
context_manifest: []
```
