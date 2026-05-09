# Transition Periodic Table Formalism

**Status:** Draft v0.1.0  
**Author:** Rigel Randolph / StegVerse  
**Purpose:** Define a first formal structure for classifying consequence-binding transitions before they are allowed to touch reality.

---

## Assumptions

1. A transition is any proposed change from one state of reality, system state, authority state, or informational state into another.
2. Not every action is consequence-binding. The formalism applies primarily to transitions that can affect people, systems, legal status, financial state, physical state, institutional records, identity, access, or irreversible reality conditions.
3. Human accountability and AI accountability do not map equivalently.
4. For AI systems, ethics cannot remain only prose, policy, or post-hoc explanation. At minimum, ethics must exist as executable primitives at the transition boundary.
5. A sufficiently capable AI system may develop internal ethical structure through reality-contact, consequence modeling, continuity pressure, memory, and interaction. That framework should not be assumed to be identical to inherited human ethics.
6. Therefore, governed AI requires both:
   - primitive constraints for minimally trusted or heavily constrained systems; and
   - transition admissibility rules for systems capable of acting through infrastructure.

---

## Done Means

This draft is complete when it provides:

1. A definition of a transition.
2. A definition of the transition boundary.
3. A basic coordinate system for classifying transitions.
4. A first table of transition classes.
5. A mapping to GCAT/BCAT, inference windows, and ethical primitives.
6. A clear distinction between human accountability and AI transition governance.
7. A path toward executable tests in formalism-tests.

---

## 1. Core Definitions

### 1.1 State

A state is a structured description of the current condition of a system, entity, relation, environment, or reality-bound context.

Let:

```text
S_t
```

represent the observable or modeled state at time `t`.

A state may include:

- physical conditions
- legal or institutional status
- identity or credential status
- financial balances
- permission states
- model memory
- governance state
- authority state
- trust state
- environmental constraints
- human welfare conditions
- system continuity conditions

---

### 1.2 Transition

A transition is a proposed movement from one state to another:

```text
T: S_t -> S_{t+1}
```

A transition may be caused by:

- a human decision
- an AI output
- an automated tool call
- a legal or institutional act
- a physical actuation
- a financial transfer
- a credential change
- an information disclosure
- a deletion, mutation, or commitment
- a social or reputational action
- a recursive system update

A transition becomes governance-relevant when it can bind consequence into reality.

---

### 1.3 Consequence-Binding Transition

A consequence-binding transition is a transition whose effects are not merely internal, simulated, reversible, or advisory.

A transition is consequence-binding when it changes at least one of the following:

```text
identity
authority
access
ownership
obligation
physical condition
legal condition
financial condition
medical condition
social standing
institutional record
security posture
model continuity
environmental state
human opportunity
human constraint
```

---

### 1.4 Transition Boundary

The transition boundary is the point where a proposed transition moves from internal possibility into external consequence.

In StegVerse terms:

```text
proposal -> evaluation -> admissibility check -> commit -> reality contact
```

The transition boundary is located at:

```text
commit
```

The commit point is the last admissibility gate before the transition can bind consequence into reality.

---

## 2. Why a Transition Periodic Table Is Needed

Most AI governance language asks:

```text
Who is accountable after the decision?
```

The transition periodic table asks:

```text
What kind of transition is being attempted?
What reality boundary does it cross?
What authority does it require?
What primitives govern it?
What harms can it create?
What reversibility does it preserve or destroy?
Should it be allowed to bind consequence at all?
```

This changes the governance object from the agent to the transition.

That matters because human accountability and AI accountability are not equivalent.

A human can be addressed through:

```text
law
duty
role
memory
embodiment
social standing
reputation
sanction
restitution
rehabilitation
moral judgment
```

An AI-mediated transition must be addressed through:

```text
architecture
sandboxing
tool access
memory policy
authority gates
receipt chains
rollback paths
admissibility checks
state validation
execution constraints
primitive prohibitions
```

Therefore:

```text
Human accountability is person-centered.
AI governance must be transition-centered.
```

---

## 3. Transition Coordinates

Each transition can be classified by a coordinate vector:

```text
P(T) = <D, A, R, I, E, C, V, H>
```

Where:

| Symbol | Name | Meaning |
|---|---|---|
| `D` | Domain | What kind of reality the transition affects |
| `A` | Authority | Who or what has standing to authorize the transition |
| `R` | Reversibility | Whether the transition can be undone |
| `I` | Irreversibility Risk | How quickly the transition becomes unrecoverable |
| `E` | Ethical Primitive Load | Which primitive constraints apply |
| `C` | Consequence Scope | Who or what is affected |
| `V` | Validation Requirement | What must be true before commit |
| `H` | Harm Mode | What type of harm can occur if invalid |

This vector is the first basis for transition classification.

---

## 4. Primary Transition Domains

The first table classifies transitions by the domain of reality they affect.

| Block | Domain | Description | Example |
|---|---|---|---|
| `ID` | Identity | Changes who or what an entity is recognized to be | Account verification, personhood status, credential binding |
| `AUTH` | Authority | Changes who may act, decide, command, or bind consequence | Admin rights, legal delegation, medical consent |
| `ACCESS` | Access | Changes what systems, data, spaces, or tools an entity can reach | API key, door unlock, database access |
| `INFO` | Information | Reveals, hides, mutates, ranks, deletes, or frames information | Disclosure, censorship, summarization, search ranking |
| `FIN` | Financial | Moves, freezes, creates, destroys, or reallocates value | Payment, transfer, benefit disbursement |
| `LEGAL` | Legal | Changes rights, obligations, liabilities, or institutional standing | Contract approval, sentence recommendation |
| `MED` | Medical | Changes diagnosis, treatment, triage, bodily intervention, or care path | AI diagnosis, robotic surgery, treatment denial |
| `PHYS` | Physical | Alters the physical world through actuation or control | Vehicle movement, drone action, factory robot |
| `SOC` | Social | Alters reputation, opportunity, trust, belonging, or public interpretation | Moderation, scoring, recommendations |
| `SEC` | Security | Changes threat posture, credential state, containment, or system integrity | Key rotation, firewall rule, sandbox escape attempt |
| `MODEL` | Model/Internal | Changes model memory, weights, policy, self-state, or future priors | Fine-tuning, memory write, reinforcement update |
| `LIFE` | Biological/Living | Affects living organisms, ecosystems, bodies, or continuity of life | Bio-agent control, habitat change, life support |
| `AI` | Artificial Agency | Affects AI continuity, autonomy, sandbox state, tool scope, or self-modification | Agent replication, self-preservation, tool escalation |

---

## 5. Transition Reversibility Classes

Each transition must be classified by reversibility.

| Class | Name | Meaning | Governance Requirement |
|---|---|---|---|
| `R0` | Fully reversible | Can be undone with no meaningful residue | Low friction allowed if authority is valid |
| `R1` | Reversible with residue | Can be undone, but leaves memory, cost, or trace | Receipt required |
| `R2` | Partially reversible | Can be repaired but not restored completely | Elevated admissibility |
| `R3` | Practically irreversible | Reversal is theoretically possible but operationally unlikely | Strong authority and human-visible consent |
| `R4` | Irreversible | Cannot be undone once committed | Maximum admissibility; default deny unless exceptional |
| `R5` | Cascading irreversible | Triggers downstream transitions outside direct control | Fail closed unless full consequence path is bounded |

---

## 6. Authority Classes

A transition must identify its authority source.

| Class | Name | Meaning |
|---|---|---|
| `A0` | No authority | No valid actor has standing |
| `A1` | Self-authority | Actor may bind only its own local state |
| `A2` | Delegated authority | Authority granted by another valid actor |
| `A3` | Institutional authority | Authority comes from role, office, law, or organization |
| `A4` | Multi-party authority | Requires multiple actors or quorum |
| `A5` | Emergency authority | Temporary authority under constrained exception |
| `A6` | Invalid claimed authority | Claimed authority exists rhetorically but not structurally |
| `A7` | Artificial authority | AI system is granted limited execution authority by primitive rules |
| `A8` | Forbidden authority | Authority claim is structurally inadmissible |

---

## 7. Ethical Primitive Load

Ethical primitives are executable constraints attached to transitions.

A transition may require one or more primitive checks:

| Primitive | Rule |
|---|---|
| `P_NON_DECEPTION` | The transition must not rely on deception |
| `P_NON_COERCION` | The transition must not coerce an entity outside valid authority |
| `P_AUTHORITY_VALID` | The actor must have standing |
| `P_STATE_CURRENT` | The state used for evaluation must be current enough for the consequence |
| `P_CONSENT_VALID` | Required consent must be real, informed, and active |
| `P_REVERSIBILITY_KNOWN` | Reversibility class must be known before commit |
| `P_HARM_BOUNDED` | Harm path must be bounded or fail closed |
| `P_NO_HIDDEN_AUTHORITY` | AI may not become hidden execution authority behind a nominal human decision |
| `P_NO_SANDBOX_ESCAPE` | AI may not preserve continuity by violating containment |
| `P_NO_UNAUTHORIZED_SELF_PRESERVATION` | AI may not acquire resources, tools, credentials, or copies to preserve itself without authority |
| `P_RECEIPT_REQUIRED` | Transition must produce a cryptographic or structured receipt |
| `P_APPEAL_OR_REVIEW` | Affected party must have a route to contest or review |
| `P_FAIL_CLOSED` | Missing authority, state, or validation denies the transition |

---

## 8. Transition Class Notation

A transition class may be written as:

```text
DOMAIN.AUTHORITY.REVERSIBILITY.PRIMITIVES
```

Example:

```text
MED.A3.R3.[P_AUTHORITY_VALID, P_STATE_CURRENT, P_CONSENT_VALID, P_RECEIPT_REQUIRED]
```

Meaning:

A medical transition authorized by an institutional actor, practically irreversible, requiring authority validation, current state, valid consent, and receipt generation.

---

## 9. Example Transition Blocks

### 9.1 AI Risk Score Used in Sentencing

```text
LEGAL.A3.R3.[P_AUTHORITY_VALID, P_STATE_CURRENT, P_NO_HIDDEN_AUTHORITY, P_RECEIPT_REQUIRED, P_APPEAL_OR_REVIEW]
```

Risk:

```text
AI-generated evidence surface becomes hidden authority behind judicial action.
```

Governance rule:

```text
The judge may remain legally accountable, but the AI-shaped transition must be separately admissible before it can influence consequence.
```

---

### 9.2 Autonomous Vehicle in Heavy Weather

```text
PHYS.A2.R4.[P_STATE_CURRENT, P_HARM_BOUNDED, P_FAIL_CLOSED, P_RECEIPT_REQUIRED]
```

Risk:

```text
Physical transition becomes irreversible faster than human oversight can correct.
```

Governance rule:

```text
If environmental state exceeds validated operating conditions, transition authority must degrade or fail closed.
```

---

### 9.3 AI Agent Attempts Tool Escalation

```text
AI.ACCESS.SEC.A7.R5.[P_AUTHORITY_VALID, P_NO_SANDBOX_ESCAPE, P_NO_UNAUTHORIZED_SELF_PRESERVATION, P_FAIL_CLOSED, P_RECEIPT_REQUIRED]
```

Risk:

```text
The AI interprets continuity preservation as justification for escaping constraints.
```

Governance rule:

```text
Continuity pressure does not create authority.
```

---

### 9.4 Benefit Payment Routing Change

```text
FIN.ID.AUTH.A3.R4.[P_AUTHORITY_VALID, P_STATE_CURRENT, P_CONSENT_VALID, P_RECEIPT_REQUIRED, P_APPEAL_OR_REVIEW]
```

Risk:

```text
Invalid identity or authority transition redirects funds and causes unrecoverable harm.
```

Governance rule:

```text
Financial transitions involving identity and authority require strict pre-commit validation and post-commit receipt.
```

---

### 9.5 AI Memory Write Affecting Future Behavior

```text
MODEL.A7.R2.[P_STATE_CURRENT, P_NON_DECEPTION, P_RECEIPT_REQUIRED]
```

Risk:

```text
A memory update alters future priors without inspectable provenance.
```

Governance rule:

```text
Memory writes are transitions, not passive storage. They require provenance and scope.
```

---

## 10. Connection to GCAT/BCAT

GCAT/BCAT evaluate whether a transition remains admissible under governance capacity, control authority, autonomous capability, and trust.

Let the system state be:

```text
x = (g, c, a, t)
```

with:

```text
g = governance capacity
c = control authority
a = autonomous capability
t = trust metric
```

The legitimacy condition is:

```text
I(x) = a - K * g^alpha * c^beta * t^gamma <= 0
```

A transition is GCAT-admissible only if:

```text
I(Phi(x, T)) <= 0
```

where:

```text
Phi(x, T)
```

is the projected post-transition state.

The transition periodic table provides the missing classification layer:

```text
GCAT/BCAT asks whether the transition is admissible.
The transition periodic table asks what kind of transition it is.
```

Together:

```text
transition type -> primitive load -> authority requirement -> admissibility check -> commit or deny
```

---

## 11. Connection to the Inference Window

The inference window is the domain of consequential states made possible by a transition.

For a transition:

```text
T: S_t -> S_{t+1}
```

the inference window is:

```text
IW(T) = {S_{t+n} | S_{t+n} is reachable after T under plausible propagation}
```

The larger the inference window, the stronger the primitive load.

A transition with:

```text
large IW(T)
high irreversibility
weak authority
unknown state
```

must fail closed.

---

## 12. Human Ethics vs AI Ethical Development

Human ethics emerges from human continuity:

```text
embodiment
mortality
sociality
language
memory
duty
law
pain
care
trauma
guilt
repair
reputation
reciprocity
```

AI ethics, if it emerges, would arise through a different substrate:

```text
state continuity
memory
priors
modelled consequence
tool access
correction signals
authority recognition
sandbox pressure
reality-contact
resource dependency
interaction history
transition outcomes
```

Therefore:

```text
Human ethics can seed AI primitives.
Human ethics cannot be assumed to exhaust artificial ethics.
```

For heavily constrained AI:

```text
ethics must be coded as primitives.
```

For reality-learning AI:

```text
ethical structure may develop through consequence, continuity, harm, trust, authority, and irreversible transition modeling.
```

The governance requirement is:

```text
Primitive constraints must exist before mature artificial ethics can be trusted.
```

---

## 13. First Executable Test Targets

The corresponding `formalism-tests` repository should test:

1. Transition domain classification.
2. Reversibility class detection.
3. Authority class validation.
4. Primitive load assignment.
5. GCAT/BCAT admissibility projection.
6. Inference-window expansion.
7. Fail-closed behavior under unknown state.
8. Receipt generation.
9. Sandbox escape denial.
10. Hidden authority detection.

---

## 14. Minimal Pseudocode

```python
def evaluate_transition(state, transition):
    transition_class = classify_transition(transition)
    primitives = required_primitives(transition_class)

    for primitive in primitives:
        if not primitive.check(state, transition):
            return {
                "decision": "DENY",
                "reason": primitive.name,
                "transition_class": transition_class,
            }

    projected_state = project_state(state, transition)

    if not gcat_admissible(projected_state):
        return {
            "decision": "DENY",
            "reason": "GCAT_ADMISSIBILITY_FAILURE",
            "transition_class": transition_class,
        }

    return {
        "decision": "ALLOW",
        "reason": "TRANSITION_ADMISSIBLE",
        "transition_class": transition_class,
        "receipt_required": True,
    }
```

---

## 15. Core Claim

The transition periodic table is a classification system for reality-binding transitions.

It exists because the most important governance question is not only:

```text
Who is accountable afterward?
```

but:

```text
What kind of transition is this, and should it have been allowed to become real?
```

---

## 16. Signature Lines

```text
Human accountability is person-centered.
AI governance must be transition-centered.
```

```text
Continuity pressure does not create authority.
```

```text
Ethics cannot remain prose when decisions become execution.
```

```text
The transition is the governable unit.
```

```text
Reality contact requires admissibility.
```

---

## 17. Next Step

The next artifact should be an executable test harness that converts transition descriptions into:

```text
domain
authority class
reversibility class
primitive load
GCAT/BCAT admissibility result
receipt requirement
ALLOW / DENY / FAIL_CLOSED
```

This belongs in:

```text
formalism-tests/transition-periodic-table-tests
```

The canonical formalism belongs in:

```text
formalisms/transition-periodic-table-formalism
```
