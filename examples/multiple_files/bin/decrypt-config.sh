#!/usr/bin/env bash
# Exit on first error
set -e

# Define our secret extenssion
secret_ext=".json"

# If there is a config directory, then move it to a backup
if test -d config; then
  if test -d config.bak; then
    rm -r config.bak
  fi
  mv config/ config.bak/
fi

# Create our new config directory
mkdir config

# For each of our files in our encrypted config
for file in $(ls config.enc); do
  # Determine src and target for our file
  src_file="config.enc/$file"
  target_file="config/$file"

  # If the file is our secret, then decrypt it
  if echo "$file" | grep -E "${secret_ext}$" &&
      test "$CONFIG_COPY_ONLY" != "TRUE"; then
    sops --decrypt "$src_file" > "$target_file"
  # Otherwise, symlink to the original file
  else
    ln -s "../$src_file" "$target_file"
  fi
done
