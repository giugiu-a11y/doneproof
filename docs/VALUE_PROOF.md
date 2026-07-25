# Value Proof

This file defines the value claim that DoneProof must earn before Captured Proof
is released.

## Category

Local check evidence for AI code changes.

## Promise

Run the check. Get a shareable receipt tied to the current Git change.

## Who Gets Value First

Repository maintainers and senior reviewers handling AI-authored changes. Their
problem is not a missing agent summary; it is uncertainty about what check
actually ran, which Git change it covered, and what remains unapproved.

## Named Mechanism

Captured Proof:

- executes one argument-vector command without a shell;
- records the observed exit code and duration;
- resolves the selected changed Git scope;
- stores privacy-safe digests instead of raw command output or diff content;
- integrity-binds the captured fields inside the receipt;
- leaves the successful workflow in `awaiting_review`.

## What It Proves

The receipt is evidence that DoneProof observed a specific command result and
bound it to a selected Git scope on that machine.

## What It Does Not Prove

It does not prove:

- semantic correctness or adequate test coverage;
- security, authorship, or an uncompromised machine;
- signed or remote attestation;
- approval to merge, deploy, or publish;
- that redaction can recognize every possible secret.

Human review remains final.

## Why It Is Not Just A Checklist

A prompt checklist can be claimed without execution. Captured Proof runs the
command and produces a machine-readable, schema-validatable artifact that a
reviewer can inspect or automate against.

## Activation Proof

The candidate demonstration:

1. runs `git diff --check`;
2. captures the observed result against the changed Git scope;
3. validates the receipt and JSON Schema;
4. renders the review state and privacy boundary;
5. completes the visible story in a 10.4-second demonstration.

The measured demo command path completed in 0.50 seconds on one development
machine. This is evidence that the under-60-second activation target is
feasible, not a universal performance claim.

## Market Proof

Market proof is still pending. It requires:

- two qualified maintainer pain confirmations;
- one receipt from an external real change;
- one repeat external use.

Until those events occur, DoneProof has a verified candidate and a testable
value hypothesis, not demonstrated adoption.

## Relevance Test

Every core feature must improve the answer to:

> What check actually ran against this Git change, and what still requires
> human review?

Features that do not improve that answer remain outside the core.
