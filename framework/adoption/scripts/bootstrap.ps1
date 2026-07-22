#!/usr/bin/env pwsh
<#
.SYNOPSIS
  Bootstrap a Control Tower profile into a target repository.
.DESCRIPTION
  Copies only source-controlled files selected by an explicit profile:

  - Light (default): the executable lifecycle core, two agents, four governance
    workflows, required gates/contracts/doctrine, and adopter documentation.
  - Full: the complete tracked kit copied by the original unprofiled installer.

  It does NOT create a constitution. Existing files are preserved unless -Force
  is supplied, and files outside the selected profile are never deleted.
.EXAMPLE
  ./bootstrap.ps1 -Target C:\path\to\your\repo
.EXAMPLE
  ./bootstrap.ps1 -Target C:\path\to\your\repo -Profile Full
#>
param(
  [Parameter(Mandatory = $true)][string]$Target,
  [ValidateSet('Light', 'Full')][string]$Profile = 'Light',
  [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# repo root = 4 levels up: framework/adoption/scripts/bootstrap.ps1 -> repo root
$method = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSCommandPath)))

$lightPaths = @(
  '.github/skills/README.md',
  '.github/skills/bootstrap-tower',
  '.github/skills/inception-readiness',
  '.github/skills/plan-slice',
  '.github/skills/architecture-review',
  '.github/skills/review-slice',
  '.github/skills/replan-and-correct',
  '.github/skills/record-closeout',
  '.github/agents/README.md',
  '.github/agents/architect-agent.agent.md',
  '.github/agents/reviewer-agent.agent.md',
  '.github/workflows/docs.yml',
  '.github/workflows/autonomy.yml',
  '.github/workflows/provenance.yml',
  '.github/workflows/merge.yml',
  '.github/copilot-instructions.md',
  'AGENTS.md',
  'CLAUDE.md',
  '.gitattributes',
  'framework/contracts/change-record.md',
  'framework/doctrine',
  'framework/docs',
  'framework/adoption/install.md',
  'framework/adoption/quickstart.md',
  'framework/adoption/scripts/bootstrap.ps1',
  'framework/scripts/constraint_model.py',
  'framework/scripts/change_record.py',
  'framework/scripts/check_change_record.py',
  'framework/scripts/check_docs.py',
  'framework/scripts/check_autonomy.py',
  'framework/scripts/check_provenance.py',
  'framework/scripts/check_merge_ready.py'
)

$fullPaths = @(
  '.github/skills',
  '.github/agents',
  '.github/instructions',
  '.github/workflows',
  '.github/copilot-instructions.md',
  'AGENTS.md',
  'CLAUDE.md',
  'framework',
  '.gitattributes'
)

$lightRequired = @(
  '.github/copilot-instructions.md',
  '.github/skills/bootstrap-tower/SKILL.md',
  '.github/skills/architecture-review/SKILL.md',
  '.github/skills/review-slice/SKILL.md',
  '.github/agents/architect-agent.agent.md',
  '.github/agents/reviewer-agent.agent.md',
  '.github/workflows/docs.yml',
  '.github/workflows/merge.yml',
  'framework/contracts/change-record.md',
  'framework/doctrine/operating-model.md',
  'framework/adoption/install.md',
  'framework/scripts/check_docs.py',
  'framework/scripts/change_record.py',
  'framework/scripts/check_change_record.py',
  'framework/scripts/check_merge_ready.py',
  'AGENTS.md',
  'CLAUDE.md',
  '.gitattributes'
)

$requiredByProfile = @{
  Light = $lightRequired
  Full = $lightRequired + @(
    '.github/skills/run-slice-evals/SKILL.md',
    '.github/skills/authority-policy-reconciliation/SKILL.md',
    '.github/agents/requirements-agent.agent.md',
    '.github/agents/planner-agent.agent.md',
    '.github/instructions/agent-skills.instructions.md',
    '.github/workflows/evals.yml',
    '.github/workflows/agents.yml',
    'framework/evals/run_evals.py',
    'framework/scripts/check_agents.py',
    'framework/scripts/check_regression.py',
    'framework/scripts/check_verification.py'
  )
}

function Get-TrackedFiles {
  param([string[]]$Pathspecs)

  $gitArgs = @('-C', $method, 'ls-files', '--') + $Pathspecs
  $files = @(& git @gitArgs)
  if ($LASTEXITCODE -ne 0) {
    throw "Unable to enumerate source-controlled Control Tower assets from $method."
  }

  return @($files | Where-Object { $_ } | Sort-Object -Unique)
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw 'Control Tower bootstrap requires Git to enumerate source-controlled assets.'
}

$sourceRoot = @(& git -C $method rev-parse --show-toplevel 2>$null)
if ($LASTEXITCODE -ne 0 -or $sourceRoot.Count -ne 1) {
  throw "Control Tower $Profile profile source is not a Git checkout: $method"
}

$resolvedMethod = (Resolve-Path -LiteralPath $method).Path.TrimEnd('\', '/')
$resolvedSource = (Resolve-Path -LiteralPath $sourceRoot[0]).Path.TrimEnd('\', '/')
if (-not [string]::Equals($resolvedMethod, $resolvedSource, [System.StringComparison]::OrdinalIgnoreCase)) {
  throw "Control Tower $Profile profile source must be the repository root: $resolvedMethod"
}

$pathspecs = if ($Profile -eq 'Light') { $lightPaths } else { $fullPaths }
$files = Get-TrackedFiles -Pathspecs $pathspecs
$missingRequired = @($requiredByProfile[$Profile] | Where-Object { $_ -notin $files })
$missingTracked = @($files | Where-Object {
  $platformPath = $_.Replace('/', [System.IO.Path]::DirectorySeparatorChar)
  -not (Test-Path -LiteralPath (Join-Path $resolvedMethod $platformPath) -PathType Leaf)
})
$missing = @(($missingRequired + $missingTracked) | Sort-Object -Unique)
if ($missing.Count -gt 0) {
  throw "Control Tower $Profile profile source is incomplete; missing tracked asset(s): $($missing -join ', '). Run Full from a canonical Control Tower checkout."
}

$targetRoot = [System.IO.Path]::GetFullPath($Target).TrimEnd('\', '/')
if ([string]::Equals($resolvedMethod, $targetRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
  throw 'Control Tower bootstrap target must differ from the method source.'
}

New-Item -ItemType Directory -Force -Path $targetRoot | Out-Null
$copied = 0
$preserved = 0

foreach ($relativePath in $files) {
  $platformPath = $relativePath.Replace('/', [System.IO.Path]::DirectorySeparatorChar)
  $source = Join-Path $resolvedMethod $platformPath
  $destination = Join-Path $targetRoot $platformPath

  if ((Test-Path -LiteralPath $destination) -and -not $Force) {
    $preserved++
    continue
  }

  $parent = Split-Path -Parent $destination
  if ($parent) {
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
  }
  Copy-Item -LiteralPath $source -Destination $destination -Force
  $copied++
}

Write-Host "Control Tower $Profile profile copied into $targetRoot ($copied copied, $preserved preserved)."
Write-Host 'No constitution was seeded. Open the target in an agent editor and run bootstrap-tower inception.'
if ($Profile -eq 'Light') {
  Write-Host 'To add Full assets later, rerun this command from a canonical Control Tower checkout with -Profile Full.'
}
