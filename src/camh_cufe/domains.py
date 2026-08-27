"""Central domain-separation registry for CAMH-CUFE version 1.

Security-critical hashes, hash-to-curve calls, and derived public contexts must
use a unique constant from this module.  Adding a new purpose requires a new
constant; reusing an existing purpose for a semantically different statement is
forbidden.
"""

PROTOCOL_FAMILY = b"CAMH-CUFE"
PROTOCOL_VERSION = 1

# Hash-to-curve / proof context.
PI4_BASES = b"CAMH-CUFE/PI4/BASES/v1"

# Hash commitments over canonical protocol objects.
HISTORY_INIT = b"CAMH-CUFE/HISTORY/INIT/v1"
HISTORY_LINK = b"CAMH-CUFE/HISTORY/LINK/v1"

# Symbolic/differential-oracle-only derivation.  This domain must never be
# reused by the real cryptographic backend.
SYMBOLIC_TAG = b"CAMH-CUFE/SYMBOLIC/TAG/v1"

# Reserved names for concrete backend implementations.  Their algorithms are
# not implemented yet; the constants are reserved now so future code does not
# invent incompatible ad-hoc labels.
REAL_STATE_HASH = b"CAMH-CUFE/REAL/STATE/v1"
REAL_TOKEN_ID = b"CAMH-CUFE/REAL/TOKEN-ID/v1"
CHECKPOINT_SIGNATURE = b"CAMH-CUFE/CHECKPOINT/SIGN/v1"
FINAL_RESULT_STATEMENT = b"CAMH-CUFE/PI4/STATEMENT/v1"


REGISTERED = {
    "pi4-bases": PI4_BASES,
    "history-init": HISTORY_INIT,
    "history-link": HISTORY_LINK,
    "symbolic-tag": SYMBOLIC_TAG,
    "real-state-hash-reserved": REAL_STATE_HASH,
    "real-token-id-reserved": REAL_TOKEN_ID,
    "checkpoint-signature-reserved": CHECKPOINT_SIGNATURE,
    "final-result-statement-reserved": FINAL_RESULT_STATEMENT,
}


def assert_unique_domains() -> None:
    """Raise if two semantic purposes accidentally share a domain label."""
    values = tuple(REGISTERED.values())
    if len(values) != len(set(values)):
        raise RuntimeError("duplicate CAMH-CUFE domain-separation label")


assert_unique_domains()
