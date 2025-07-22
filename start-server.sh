#!/usr/bin/env bash

source "$HOME/.bash/.bash_os"
source "$HOME/.bash/.bash_print"

# ──────────────────────────────────────────────────────────────────────────────
# Starts the http server with: 'npx tsx http-server.ts'.
# Background job: Watches PATHS_TO_WATCH, runs `npm run build` on change.
# ──────────────────────────────────────────────────────────────────────────────

HTTP_SERVER_PROJECT_ROOT="$PWD/node"

VITE_ROOT="$PWD/node/_vite-frontend"
PATHS_TO_WATCH=(
    "$VITE_ROOT/index.html"
    "$VITE_ROOT/index.ts"
    "$VITE_ROOT/src"
    "$VITE_ROOT/../_shared"
)

# ─── Assert-Paths: VITE_ROOT && PATHS_TO_WATCH ───────────────────────────────────
if ! test_path "$VITE_ROOT"; then print_red "VITE_ROOT is not a real path. VITE_ROOT: $VITE_ROOT"; exit 1; fi
for path in "${PATHS_TO_WATCH[@]}"; do
    if ! test_path "$path"; then print_red "path is not a real path. path: $path"; exit 1; fi
done


# ─── Build Function ───────────────────────────────────────────────────────────
npm_build() {
	cd "$VITE_ROOT"
	npm run build &> /dev/null 
	date +%s                    # return seconds since epoch
}
# ─── Background Watcher ───────────────────────────────────────────────────────
watch_vite() {
	local last_built
	last_built=$(npm_build)

	while true; do
		sleep 0.15
		for path in "${PATHS_TO_WATCH[@]}"; do
			if is_file "$path"; then
				modified=$(stat -c %Y "$path")
				if (( modified > last_built )); then
					last_built=$(npm_build)
					break
				fi
			fi

			if is_directory "$path"; then
				while IFS= read -r -d '' file; do
					modified=$(stat -c %Y "$file")
					if (( modified > last_built )); then
						last_built=$(npm_build)
						break 2
					fi
				done < <(find "$path" -type f -print0)
			fi
		done
	done
}


# ─── Main ──────────────────────────────────────────────────────────────────────
START_PATH="$PWD"
clear

# Start watcher in the background
WATCHER_OUT=$(mktemp)           # Create temp file for capturing background stdout
watch_vite >"$WATCHER_OUT" &
WATCHER_PID=$!

# Run http server in the foreground
cd "$HTTP_SERVER_PROJECT_ROOT"
npx tsx http-server.ts
EXIT_CODE=$?

cleanup() {
    # Kill the watcher if still running
    kill "$WATCHER_PID" 2>/dev/null || true

    # Wait for watcher to exit and get exit code
    wait "$WATCHER_PID" 2>/dev/null
    WATCHER_EXIT_CODE=$?

    # Print background job stdout
    if [ -s "$WATCHER_OUT" ]; then
        while IFS= read -r line; do
            print_green "$line"
        done < "$WATCHER_OUT"
    fi

    # Cleanup temp files
    rm -f "$WATCHER_OUT"

    cd "$START_PATH"

    [ "$WATCHER_EXIT_CODE" -eq 0 ] && print_green "Watcher Background Job Exit Code: $WATCHER_EXIT_CODE" || print_red "Watcher Background Job Exit Code: $WATCHER_EXIT_CODE"
    exit "$WATCHER_EXIT_CODE"
}
trap cleanup INT TERM


cd "$START_PATH"