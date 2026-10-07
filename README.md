# Claim evidence gate

I built this after reading Cozmo's Forward Deployed Engineer prompt about entering a water damage estimate into Xact from a call transcript and 40 photos.

I kept getting stuck on one question:

**If the transcript says something that the photos do not actually support, what stops the agent from turning that statement into an estimate?**

So this is a small experiment around that boundary. It is not an Xactimate integration and it is not meant to be a replica of Cozmo.

## What I tried

The first version of the thought process was basically:

`transcript + photos -> estimate`

I changed that to:

`transcript + photos -> evidence checks -> estimate OR human review`

The gate currently checks a few things that seemed easy to get wrong:

* the room in the transcript actually has usable photo evidence
* a measurement in the transcript has supporting visual evidence
* a reported measurement does not disagree with the available measurement
* the usable evidence is above a simple confidence threshold
* duplicate or irrelevant photos do not become extra evidence
* an unavailable estimate tool does not result in a successful action

The data is synthetic. There is no Cozmo, customer, carrier, or proprietary data in this repo.

## The part I care about

I don't think a model's confidence should be the permission to change a claim.

The system needs a separate decision about whether it has enough evidence to act.

That is the boundary I wanted to make inspectable in code instead of just describing it in a README.

## Failure cases

The test set includes cases such as:

* transcript says 6 ft, photo evidence says 9 ft
* transcript identifies a kitchen but the usable photo is from a hall
* the only matching photo is low confidence
* the transcript contains a measurement but no photo supports it
* repeated / irrelevant photos are present
* the downstream estimate tool is unavailable

For each case the code returns the reason for the decision and a small trace showing where the claim went.

## Run it

```bash
python -m pytest -q
python run_lab.py
```

The tests are intentionally small. I wanted the policy to be easy to inspect rather than hiding it behind an LLM call.

## What I would do next

If this were going into a real claims workflow, the simple checks here would not be enough. I would want photo provenance, better room/entity linking, calibrated uncertainty, immutable audit events, idempotent tool calls, retries with clear limits, and a review queue.

The interesting question for me is where those controls should sit. My current answer is that the model can propose an action, but a separate evidence layer should decide whether the action is allowed to happen.
