# Reference — Decision records

An adopter's Architecture Decision Records live under
[`constitution/decisions/`](../../../constitution/decisions/) after the first decision is recorded.
The directory is instance-owned; the copied kit does not seed the method repository's historical
ADR log into a product.

## When to record one

Record an ADR when:

- the human authorizes a Mission or Constraints change;
- a governance/strategy correction changes the slow governing law;
- a selected delivery makes a load-bearing architectural decision.

Routine implementation details, reversible local choices, reviews, and test setup are lifecycle
work, not standalone strategic outcomes.

## Minimum shape

An ADR identifies the trigger and status, describes the context, states one decision, weighs at
least two alternatives, and records consequences including a negative trade-off. A load-bearing
design also receives a terse design-under-test and independent architecture review before code.

The autonomy gate checks only the required recorded-decision relationship for Mission/Constraints
changes. It does not prove authorization or architectural merit; those remain independent-review
and human judgments.

## See also

- [Course correction](../how-to/course-correct.md)
- [Review a design](../how-to/review-a-design.md)
- [Autonomy and architecture gates](gates.md)
