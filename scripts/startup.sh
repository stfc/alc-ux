#!/bin/bash -l 

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
        ssh_str="--bind $SSH_AUT_SOCK:$SSH_AUTH_SOCK --env $SSH_AUTH_SOCK=$SSH_AUTH_SOCK"
    else
        ssh_str="-v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK -e SSH_AUTH_SOCK=$SSH_AUTH_SOCK" 
    fi 
else 
    echo "Attempting to load default keys..." 
    ssh-add 
    if [ $? -eq 0 ]; then
        echo "Successfully added default keys." 
        if [[ $container_engine == "apptainer" ]]; then 
            ssh_str="--bind $SSH_AUT_SOCK:$SSH_AUTH_SOCK --env $SSH_AUTH_SOCK=$SSH_AUTH_SOCK"
        else
            ssh_str="-v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK -e SSH_AUTH_SOCK=$SSH_AUTH_SOCK" 
        fi 
    else 
        echo "SSH agent not running. SSH configuration will have to be managed from within the container."
        ssh_str=""
    fi  
fi 

# Run the container 
if [[ $container_engine == "apptainer" ]]; then 
    echo "Running apptainer with image $docker_image"
    apptainer run --compat --cleanenv --bind $home_bind:/home/jovyan --home /home/jovyan $env_str $ssh_str docker://$docker_image
else 
    echo "Running docker with image $docker_image" 
    docker run -it --rm -p 8888:8888 -v $home_bind:/home/jovyan $env_str $ssh_str $docker_image 
fi 