# Quickstart — your first LIGHT tower

1. **Copy the LIGHT core.** From a canonical Control Tower checkout:

   ```powershell
   & 'C:\path\to\control-tower\framework\adoption\scripts\bootstrap.ps1' `
     -Target 'C:\path\to\your-repo'
   ```

   Use `-Profile Full` only when the project needs Full-only specialization, Authority/GOVERNED
   extensions, or framework-development material. The installer preserves existing product CI; it
   does not generate product build/test workflows.
2. **Run THIN inception.** Open the target and invoke `bootstrap-tower`. Answer Scope, Decisions,
   and Context + constraints before the main Tower writes `constitution/mission.md`,
   `constitution/constraints.md`, and `constitution/roadmap.md`.
3. **Gate readiness independently.** Run the existing readiness check and obtain a fresh
   `inception-readiness` PASS.
4. **Plan the first observable capability.** Invoke `plan-slice`; for eligible LIGHT work, the main
   Tower writes requirements, plan, and validation without automatic specialist handoffs.
5. **Implement, review, and record.** Produce product-native evidence, obtain a fresh no-edit
   Reviewer verdict, record the returned PROMOTE, pass merge readiness, and run `record-closeout`.

That is one complete turn of the loop. When reality contradicts an artifact, correct the nearest
authoritative artifact first rather than letting code drift.
