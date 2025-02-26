# Ethereum 2.0 The Merge

**Warning:** This document is currently based on [Phase 0](../phase0/validator.md) but will be rebased to [Altair](../altair/validator.md) once the latter is shipped.

**Notice**: This document is a work-in-progress for researchers and implementers.

## Table of contents

<!-- TOC -->
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Beacon chain responsibilities](#beacon-chain-responsibilities)
  - [Block proposal](#block-proposal)
    - [Constructing the `BeaconBlockBody`](#constructing-the-beaconblockbody)
      - [Execution Payload](#execution-payload)
        - [`get_pow_chain_head`](#get_pow_chain_head)
        - [`produce_execution_payload`](#produce_execution_payload)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->
<!-- /TOC -->

## Introduction

This document represents the changes to be made in the code of an "honest validator" to implement executable beacon chain proposal.

## Prerequisites

This document is an extension of the [Phase 0 -- Validator](../phase0/validator.md). All behaviors and definitions defined in the Phase 0 doc carry over unless explicitly noted or overridden.

All terminology, constants, functions, and protocol mechanics defined in the updated Beacon Chain doc of [The Merge](./beacon-chain.md) are requisite for this document and used throughout. Please see related Beacon Chain doc before continuing and use them as a reference throughout.

## Beacon chain responsibilities

All validator responsibilities remain unchanged other than those noted below. Namely, the transition block handling and the addition of `ExecutionPayload`.

### Block proposal

#### Constructing the `BeaconBlockBody`

##### Execution Payload

###### `get_pow_chain_head`

Let `get_pow_chain_head() -> PowBlock` be the function that returns the head of the PoW chain. The body of the function is implementation specific.

###### `produce_execution_payload`

Let `produce_execution_payload(parent_hash: Hash32, timestamp: uint64) -> ExecutionPayload` be the function that produces new instance of execution payload.
The body of this function is implementation dependent.

* Set `block.body.execution_payload = get_execution_payload(state)` where:

```python
def get_execution_payload(state: BeaconState) -> ExecutionPayload:
    if not is_transition_completed(state):
        pow_block = get_pow_chain_head()
        if not is_valid_transition_block(pow_block):
            # Pre-merge, empty payload
            return ExecutionPayload()
        else:
            # Signify merge via producing on top of the last PoW block
            timestamp = compute_time_at_slot(state, state.slot)
            return produce_execution_payload(pow_block.block_hash, timestamp)

    # Post-merge, normal payload
    execution_parent_hash = state.latest_execution_payload_header.block_hash
    timestamp = compute_time_at_slot(state, state.slot)
    return produce_execution_payload(execution_parent_hash, timestamp)
```
