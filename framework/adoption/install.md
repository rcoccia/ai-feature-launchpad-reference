# Install — adopt Control Tower in a product repository

Run the installer from a canonical Control Tower Git checkout. It copies source-controlled files
only and never creates a constitution.

## LIGHT — default

```powershell
& 'C:\path\to\control-tower\framework\adoption\scripts\bootstrap.ps1' `
  -Target 'C:\path\to\your-repo'
```

LIGHT installs the executable default:

- bootstrap, inception-readiness, planning, conditional architecture review, final review,
  correction, and closeout Skills;
- Reviewer and Architect agents;
- docs, autonomy, provenance, and merge-ready workflows;
- the entry points, Change Record contract, required gates, doctrine, and human documentation.

Requirements/Planner specialization, Authority/GOVERNED Skills, framework-development evals, and
example-only CI are not copied. Existing product workflows remain the product's responsibility:
paths outside the four selected Control Tower workflow files are always preserved, and without
`-Force` a colliding path is preserved too. The installer does not synthesize a language-specific
workflow or configure branch protection.

## Full — explicit opt-in

```powershell
& 'C:\path\to\control-tower\framework\adoption\scripts\bootstrap.ps1' `
  -Target 'C:\path\to\your-repo' `
  -Profile Full
```

Full copies the complete method kit: every Skill and agent, authoring instructions, all Control
Tower workflows, framework-development eval/golden material, and the complete portable
`framework/`. Run this command from the canonical method checkout; a LIGHT target does not contain
the Full-only source assets.

Running canonical-source Full after LIGHT is additive. It installs the opt-in assets without
deleting product files.

## Repeat and update

- Without `-Force`, existing target files are preserved.
- With `-Force`, only files selected by the chosen profile are overwritten.
- Neither profile deletes files. Applying LIGHT to a Full target does not prune Full-only assets.
- Untracked source files are never copied.

After either profile completes, open the target in an agent editor. The entry point sees no
`constitution/` and routes the main Tower to interview-first `bootstrap-tower` inception. After the
independent readiness verdict passes, begin the first delivery with `plan-slice`.
