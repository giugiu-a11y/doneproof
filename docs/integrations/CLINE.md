# Cline Integration

Use DoneProof for Cline handoffs that modify code, docs, or configuration.

## Add To Instructions

Copy `.doneproof/templates/cline.md` into the project instructions Cline reads.

## Required Check

```bash
doneproof check --receipt .doneproof/receipts/latest.json
```

If a verification command was skipped, record the reason in the receipt risk section.
