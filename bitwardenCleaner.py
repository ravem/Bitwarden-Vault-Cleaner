from urllib.parse import urlsplit, urlunsplit
import json
import re
import datetime
import os

# ------------------------------------------------------------------------
# Ask user for input/output files
# ------------------------------------------------------------------------
default_input_file = "bitwarden_export_file.json"
default_output_file = "bitwarden_export_file_output.json"

input_file_name = input(f"Enter the input file name [{default_input_file}]: ").strip()
if not input_file_name:
    input_file_name = default_input_file

output_file_name = input(f"Enter the output file name [{default_output_file}]: ").strip()
if not output_file_name:
    output_file_name = default_output_file

deleted_file_name = f"{os.path.splitext(output_file_name)[0]}_deleted.json"
log_file_name = f"{os.path.splitext(output_file_name)[0]}_merge_log.txt"

# ------------------------------------------------------------------------
# Initialize log
# ------------------------------------------------------------------------
def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file_name, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")
    print(message)

# Clear log file at start
open(log_file_name, "w").close()
log("=== Bitwarden Merge Script Started ===")

# ------------------------------------------------------------------------
# Load input data
# ------------------------------------------------------------------------
with open(input_file_name, 'r', encoding='utf-8') as input_file:
    data = json.load(input_file)

# ------------------------------------------------------------------------
# Initialize variables
# ------------------------------------------------------------------------
processed_items = 0
total_items = len(data['items'])
duplicates = {}  # key: (username, password), value: item
deleted_items = []
merge_summary = []

# ------------------------------------------------------------------------
# MAIN PROCESSING LOOP
# ------------------------------------------------------------------------
items_copy = data['items'][:]

for item in items_copy:
    item_name = item.get('name', '<Unnamed>')
    item_type = item.get('type', 0)

    # Analizza solo i Login (type=1)
    if item_type != 1:
        log(f"Skipping item '{item_name}' (type={item_type}) – not a Login")
        continue

    log(f"Processing item ({processed_items + 1}/{total_items}): {item_name}")

    login_data = item.get('login', {})
    uris = login_data.get('uris') or []  # empty list if None
    username = login_data.get('username')
    password = login_data.get('password')

    if username is None or password is None:
        log(f"> Skipping: missing username/password")
        processed_items += 1
        continue

    corrected_uris = []
    uri_keys = []
    for uri_data in uris:
        uri = uri_data.get('uri')
        if uri:
            corrected_uris.append({"uri": uri})
            uri_keys.append(uri)

    # Keep empty URI accounts
    item['login']['uris'] = corrected_uris

    # --- Duplicate merge logic ---
    reason_for_deletion = ""
    found_duplicate = None
    for key, existing_item in duplicates.items():
        existing_username, existing_password = key
        if existing_username == username and existing_password == password:
            existing_uris = {u['uri'] for u in existing_item['login']['uris']}
            current_uris = set(uri_keys)

            # Merge if at least one URI in common or if one account has empty URIs
            if (existing_uris & current_uris) or (not existing_uris and current_uris) or (existing_uris and not current_uris):
                found_duplicate = existing_item
                merged_uris = existing_uris.union(current_uris)
                merged_uri_list = [{"uri": u} for u in sorted(merged_uris)]
                found_duplicate['login']['uris'] = merged_uri_list

                log(f"> MERGE: '{item_name}' merged into '{found_duplicate['name']}' with {len(merged_uris)} URI(s)")
                merge_summary.append(f"{item_name} → merged with {found_duplicate['name']}")
                break

    if found_duplicate:
        reason_for_deletion = f"Merged with {found_duplicate['name']}"
    else:
        duplicates[(username, password)] = item

    if reason_for_deletion:
        log(f"> Removing item: {item_name} ({reason_for_deletion})")
        deleted_items.append({**item, "reasonForDeletion": reason_for_deletion})
        data['items'].remove(item)

    # Save after each iteration
    with open(output_file_name, 'w', encoding='utf-8') as output_file:
        json.dump(data, output_file, indent=2, ensure_ascii=False)

    with open(deleted_file_name, 'w', encoding='utf-8') as deleted_file:
        json.dump(deleted_items, deleted_file, indent=2, ensure_ascii=False)

    processed_items += 1

# ------------------------------------------------------------------------
# Final save & summary
# ------------------------------------------------------------------------
with open(output_file_name, 'w', encoding='utf-8') as output_file:
    json.dump(data, output_file, indent=2, ensure_ascii=False)

log(f"\n=== Processing Complete ===")
log(f"Processed items: {processed_items}/{total_items}")
log(f"Deleted items: {len(deleted_items)}")

if merge_summary:
    log("\n--- Merge Summary ---")
    for line in merge_summary:
        log(line)
else:
    log("\nNo merges performed.")

log("=== Bitwarden Merge Script Finished ===")
