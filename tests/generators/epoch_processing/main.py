from eth2spec.gen_helpers.gen_from_tests.gen import run_state_test_generators
from eth2spec.phase0 import spec as spec_phase0
from eth2spec.altair import spec as spec_altair
from eth2spec.test.helpers.constants import PHASE0, ALTAIR


specs = (spec_phase0, spec_altair)


if __name__ == "__main__":
    phase_0_mods = {key: 'eth2spec.test.phase0.epoch_processing.test_process_' + key for key in [
        'justification_and_finalization',
        'rewards_and_penalties',
        'registry_updates',
        'slashings',
        'eth1_data_reset',
        'effective_balance_updates',
        'slashings_reset',
        'randao_mixes_reset',
        'historical_roots_update',
        'participation_record_updates',
    ]}
    altair_mods = {
        **{key: 'eth2spec.test.altair.epoch_processing.test_process_' + key for key in [
            'sync_committee_updates',
        ]},
        **phase_0_mods,
    }  # also run the previous phase 0 tests

    # TODO Custody Game testgen is disabled for now
    # custody_game_mods = {**{key: 'eth2spec.test.custody_game.epoch_processing.test_process_' + key for key in [
    #     'reveal_deadlines',
    #     'challenge_deadlines',
    #     'custody_final_updates',
    # ]}, **phase_0_mods}  # also run the previous phase 0 tests (but against custody game spec)

    all_mods = {
        PHASE0: phase_0_mods,
        ALTAIR: altair_mods,
    }

    run_state_test_generators(runner_name="epoch_processing", specs=specs, all_mods=all_mods)
