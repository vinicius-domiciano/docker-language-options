#!/bin/bash

### reload_aliases
alias reload_aliases="source /home/alexandrino/projects/docker-options-config/sources/bin/aliases.sh"

### Image run function
__docker_image_run__() {
	container="$1"
	path="$(pwd)"
	shift
	docker run --rm -v "$path":/app -w /app "$container" "$@"
}


# __start_aliases_from_languages__
alias java='__docker_image_run__ docker-options_ee27f618-ea3d-4cfc-bac4-b465d17c385a java'
alias javac='__docker_image_run__ docker-options_ee27f618-ea3d-4cfc-bac4-b465d17c385a javac'
# __end_aliases_from_languages__