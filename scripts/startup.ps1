param (
    [Parameter(Mandatory=$false, HelpMessage="The AiiDAlab docker image to run.")]
    [Alias("i")]
    [string]$image = "aiidalab/full-stack:latest",
    [Parameter(Mandatory=$false, HelpMessage="The path to mount the containers home directory into.")]
    [Alias("v")]
    [string]$homeBind = "$HOME",
    [Parameter(Mandatory=$false, HelpMessage="GPU support: auto (default), on/nvidia, or off.")]
    [Alias("g")]
    [string]$gpu = "auto"
)

# --- GPU DETECTION ---
# Detect an NVIDIA GPU and enable Docker GPU passthrough (--gpus all).
# On Windows, Docker Desktop only supports NVIDIA GPUs (through WSL2/CUDA); AMD
# ROCm containers are not supported, so only NVIDIA is auto-detected here.
# Use -gpu off to force CPU-only, or -gpu on to force GPU passthrough.
Write-Host "Checking for GPU support..." -ForegroundColor Cyan
$gpuArgs = @()
switch ($gpu.ToLower()) {
    { $_ -in @("0", "off", "none", "false") } {
        Write-Host "GPU support disabled - running on CPU only." -ForegroundColor Cyan
    }
    { $_ -in @("on", "nv", "nvidia", "true") } {
        Write-Host "Forcing NVIDIA GPU support (--gpus all)." -ForegroundColor Cyan
        $gpuArgs = @("--gpus", "all")
    }
    default {
        $nvidiaSmi = Get-Command nvidia-smi -ErrorAction SilentlyContinue
        if ($nvidiaSmi -and (& nvidia-smi -L 2>$null)) {
            Write-Host "NVIDIA GPU detected - enabling GPU support (--gpus all)." -ForegroundColor Cyan
            $gpuArgs = @("--gpus", "all")
        } else {
            Write-Host "No NVIDIA GPU detected - running on CPU only." -ForegroundColor Cyan
        }
    }
}
# --- END GPU DETECTION ---

$dockerArgs = @(
    "run", "--rm", "-p", "8888:8888", "-v", "$($homeBind):/home/jovyan"
)

$dockerArgs += $gpuArgs

[string]$aiidaConfig = "$($homeBind)\.aiida\config.json"

if (Test-Path -Path $aiidaConfig) {
    Write-Host "Existing AiiDA user profile configuration found. No new user will be created." -ForegroundColor Cyan
    $dockerArgs += "--env"
    $dockerArgs += "SETUP_DEFAULT_AIIDA_PROFILE=false"
} else {
    Write-Host "Enter AiiDA User Profile Configuration: " -ForegroundColor Cyan
    [string]$userName = Read-Host -Prompt "    - Username "
    [string]$firstName = Read-Host -Prompt "    - First Name "
    [string]$lastName = Read-Host -Prompt "    - Last Name "
    [string]$emailAddress = Read-Host -Prompt "    - Email Address "
    [string]$institution = Read-Host -Prompt "    - Institution "

    $dockerArgs += @(
        "--env", "AIIDA_PROFILE_NAME=$userName",
        "--env", "AIIDA_USER_FIRST_NAME=$firstName",
        "--env", "AIIDA_USER_LAST_NAME=$lastName",
        "--env", "AIIDA_USER_EMAIL=$emailAddress",
        "--env", "AIIDA_USER_INSTITUTION=$institution"
    )
}

Write-Host "Starting Image: $image" -ForegroundColor Cyan
$dockerArgs += $image

# Run the container and stream its output so the first Jupyter URL can be opened
# automatically in the user's default browser. The URL is still printed so it can
# be opened manually if the browser launch fails.
$script:opened = $false
& docker @dockerArgs 2>&1 | ForEach-Object {
    Write-Host $_
    if (-not $script:opened) {
        $match = [regex]::Match([string]$_, 'https?://(127\.0\.0\.1|localhost)[^\s]+')
        if ($match.Success) {
            Write-Host "Opening AiiDAlab in your default browser: $($match.Value)" -ForegroundColor Green
            Start-Process $match.Value
            $script:opened = $true
        }
    }
}
