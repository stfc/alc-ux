param (
    [Parameter(Mandatory=$false, HelpMessage="The AiiDAlab docker image to run.")]
    [Alias("i")]
    [string]$image = "aiidalab/full-stack:latest",
    [Parameter(Mandatory=$false, HelpMessage="The path to mount the containers home directory into.")]
    [Alias("v")]
    [string]$homeBind = "$HOME"
)

$dockerArgs = @(
    "run", "--rm", "-it", "-p", "8888:8888", "-v" "$($homeBind):/home/jovyan"
)

[string]$aiidaConfig = "$($homeBind)\.aiida\config.json"

if (Test-Path -Path $aiidaConfig) {
    $dockerArgs += "--env"
    $dockerArgs += "SETUP_DEFAULT_AIIDA_PROFILE=false"
} else {
    Write-Host "Enter AiiDA User Profile Configuration: " -ForegroundColor Cyan
    [string]$userName = Read-Host -Prompt "    - Username "
    [string]$firstName = Read-Host -Prompt "    - First Name "
    [string]$lastNAme = Read-Host -Prompt "    - Last Name "
    [string]$emailAddress = Read-Host -Prompt "    - Email Address "
    [string]$institution = Read-Host -Prompt "    - Institution "

    $dockerArgs += @(
        "--env", "AIIDA_PROFILE_NAME=$userName",
        "--env", "AIIDA_USER_FIRST_NAME=$firstName",
        "--env", "AIIDA_USER_LAST_NAME=$lastName",
        "--env", "AIIDA_USER_EMAIL=$emailAddress",
        "--env", "AIIDA_USER_INSTITUTION=$institution",
    )
}

Write-Host "Starting Image: $image" -ForegroundColor Cyan
$dockerArgs += $image
docker @dockerArgs