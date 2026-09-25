#!/bin/bash -l

check_for_executable() {
    local executable_name="$1"
    command -v "$executable_name" > /dev/null 2>&1
    return $?
}

# Open a URL in the user's default browser (best-effort, never fatal).
open_in_browser() {
    local url="$1"
    echo "Opening AiiDAlab in your default browser: $url"
    if check_for_executable xdg-open; then
        xdg-open "$url" >/dev/null 2>&1 &
    elif check_for_executable gio; then
        gio open "$url" >/dev/null 2>&1 &
    elif check_for_executable sensible-browser; then
        sensible-browser "$url" >/dev/null 2>&1 &
    elif check_for_executable open; then      # macOS
        open "$url" >/dev/null 2>&1 &
    else
        echo "No browser launcher (xdg-open/gio/sensible-browser/open) found."
        echo "Please open the URL above manually."
    fi
}


docker_image="aiidalab/full-stack:latest"
home_bind="${HOME}"
container_engine="apptainer"

# --- ARGUMENT PARSING LOOP ---
# Iterate through all passed arguments ($@)
while [ $# -gt 0 ]; do
    case "$1" in
        --docker-image=*)
            docker_image="${1#*=}"
            ;;
        --home-bind=*)
            home_bind="${1#*=}"
            ;;
        --use-docker*)
            container_engine="docker"
            ;;
        *)
            # Handle unrecognized arguments
            echo "Warning: Unknown argument or invalid format: '$1'"
            exit 1
            ;;
    esac
    # Move to the next argument
    shift
done
# --- END ARGUMENT PARSING ---

# Check for container engine executable
echo "Checking for requested container engine executable..."
if check_for_executable $container_engine; then
    echo "$container_engine found in PATH"
else
    echo "$container_engine not found! Please add the required executable to PATH or use a different engine"
    echo "Supported container engines are: apptainer, docker"
    exit 1
fi

# Check if provided bind path exists and create it if not
if [ ! -d $home_bind ]; then
    echo "Provided bind path doesn't exist, path will be created..."
    mkdir -p $home_bind
    if [ $? -eq 0 ]; then
        echo "Bind path successfully created"
    else
        echo "Unable to create new directory path at '$home_bind'"
        exit 1
    fi
fi

aiida_config="$home_bind/.aiida/config.json"
echo "Looking for existing AiiDA user profile at: $aiida_config"

# set -x ???

if [ ! -f "$aiida_config" ]; then

    echo "No existing AiiDA profile found. Setting up new user profile: "

    read -rp "Enter your AiiDA Username: " USER_INPUT
    read -rp "Enter your First Name: " FIRST_NAME_INPUT
    read -rp "Enter your Last Name: " LAST_NAME_INPUT
    read -rp "Enter your Email Address: " EMAIL_INPUT
    read -rp "Enter your Institution: " INSITUTION_INPUT

    env_str="--env AIIDA_PROFILE_NAME=$USER_INPUT --env AIIDA_USER_EMAIL=$EMAIL_INPUT --env AIIDA_USER_FIRST_NAME=$FIRST_NAME_INPUT --env AIIDA_USER_LAST_NAME=$LAST_NAME_INPUT --env AIIDA_USER_INSTITUTION=$INSITUTION_INPUT"

else
    echo "Existing AiiDA user profile configuration found. No new user will be created."
    env_str="--env SETUP_DEFAULT_AIIDA_PROFILE=false"
fi

# Check for SSH agent
echo "Checking for SSH Agent..."
ssh-add -l > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "SSH agent running and contains sshkey"
    if [[ $container_engine == "apptainer" ]]; then
        ssh_str="--bind $SSH_AUTH_SOCK:$SSH_AUTH_SOCK --env SSH_AUTH_SOCK=$SSH_AUTH_SOCK"
    else
        ssh_str="-v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK -e SSH_AUTH_SOCK=$SSH_AUTH_SOCK"
    fi
else
    echo "Attempting to load default keys..."
    ssh-add
    if [ $? -eq 0 ]; then
        echo "Successfully added default keys."
        if [[ $container_engine == "apptainer" ]]; then
            ssh_str="--bind $SSH_AUTH_SOCK:$SSH_AUTH_SOCK --env SSH_AUTH_SOCK=$SSH_AUTH_SOCK"
        else
            ssh_str="-v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK -e SSH_AUTH_SOCK=$SSH_AUTH_SOCK"
        fi
    else
        echo "SSH agent not running. SSH configuration will have to be managed from within the container."
        ssh_str=""
    fi
fi

# --- GPU DETECTION ---
# Detect a host GPU and enable the matching GPU support for the chosen engine.
# Set AIIDALAB_GPU=0 to force CPU-only, or AIIDALAB_GPU=nv|rocm to force a vendor.
echo "Checking for GPU support..."
gpu_vendor=""
case "${AIIDALAB_GPU:-auto}" in
    0|off|none|false)
        echo "GPU support disabled by AIIDALAB_GPU — running on CPU only."
        ;;
    nv|nvidia)
        echo "Forcing NVIDIA GPU support via AIIDALAB_GPU."
        gpu_vendor="nvidia"
        ;;
    rocm|amd)
        echo "Forcing AMD GPU support via AIIDALAB_GPU."
        gpu_vendor="amd"
        ;;
    *)
        if check_for_executable nvidia-smi && nvidia-smi -L >/dev/null 2>&1; then
            echo "NVIDIA GPU detected — enabling GPU support."
            gpu_vendor="nvidia"
        elif [ -e /dev/kfd ] && { check_for_executable rocminfo || check_for_executable rocm-smi; }; then
            echo "AMD GPU detected — enabling GPU support."
            gpu_vendor="amd"
        else
            echo "No GPU detected — running on CPU only."
        fi
        ;;
esac

# Map the detected vendor onto engine-specific run flags.
gpu_flag=""
if [[ $container_engine == "apptainer" ]]; then
    case "$gpu_vendor" in
        nvidia) gpu_flag="--nv" ;;
        amd)    gpu_flag="--rocm" ;;
    esac
else
    case "$gpu_vendor" in
        nvidia) gpu_flag="--gpus all" ;;
        amd)    gpu_flag="--device=/dev/kfd --device=/dev/dri --security-opt seccomp=unconfined" ;;
    esac
fi
# --- END GPU DETECTION ---

# Open the first Jupyter URL (loopback address) in the default browser the moment
# it appears in the container output. Only the first match triggers a launch.
opened=""
open_first_url() {
    [ -n "$opened" ] && return 0
    local url
    url=$(printf '%s' "$1" | grep -oE 'https?://(127\.0\.0\.1|localhost)[^[:space:]]+' | head -n 1)
    if [ -n "$url" ]; then
        open_in_browser "$url"
        opened=1
    fi
}

# Run the container, streaming its output so the URL can be detected and opened
# automatically. The URL is still printed so it can be opened manually if the
# browser launch fails. The while-loop runs in this shell (via process
# substitution) so 'opened' persists across iterations.
if [[ $container_engine == "apptainer" ]]; then
    echo "Running apptainer with image $docker_image"
    while IFS= read -r line; do
        printf '%s\n' "$line"
        open_first_url "$line"
    done < <(apptainer run --compat --cleanenv $gpu_flag --bind $home_bind:/home/jovyan --home /home/jovyan $env_str $ssh_str docker://$docker_image 2>&1)
else
    echo "Running docker with image $docker_image"
    while IFS= read -r line; do
        printf '%s\n' "$line"
        open_first_url "$line"
    done < <(docker run --rm -i -p 8888:8888 $gpu_flag -v $home_bind:/home/jovyan $env_str $ssh_str $docker_image 2>&1)
fi
