#!/bin/sh
# first create an .app executable for Mac and then run this shell script
# to create a DMG distribution.
# prerequisite: create YIKES.app in ./build/

# Create a folder 'dist'
mkdir -p build
 
# Create a folder 'dmg' under dist and use it to prepare the DMG.
mkdir -p dist/dmg

# Empty the dmg folder.
rm -r dist/dmg/*

# Copy the app bundle to the dmg folder.
cp -r "build/YIKES.app" dist/dmg

# If the DMG already exists, delete it.
test -f "dist/YIKES.dmg" && rm "dist/YIKES.dmg"

# the following is the main command. if it does not work, reinstall create-dmg using Homebrew
create-dmg \
  --volname "[jaiks] Just Another IPA Keyboard - Simplified" \
  --volicon "icon.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "YIKES.app" 175 120 \
  --hide-extension "YIKES.app" \
  --app-drop-link 425 120 \
  "dist/YIKES.dmg" \
  "dist/dmg/"
