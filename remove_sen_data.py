import os
import shutil
import tarfile
import json
import yaml
import sys

# for i in range(1, len(sys.argv)):
path = f"{sys.argv[1]}"
print(path)


tar = tarfile.open(path)
extract_path = "/".join(path.split("/")[:-1])
print(extract_path)
tar.extractall(extract_path)
tar.close()
path = "".join(path.split(".")[:-2])
print(path)

config_db = f"{path}/etc/sonic/config_db.json"
snmp = f"{path}/etc/sonic/snmp.yml"
tacplus = f"{path}/etc/tacplus_nss.conf"


config_db_dir = f"{path}/etc/sonic"
for file in os.listdir(config_db_dir):
    if file.startswith("config_db.json"):
        config_data = ""
        print("-------")

        config_db = f"{path}/etc/sonic/{file}"
        print(config_db)
        # Open the JSON file for reading  #etc/sonic/config.json
        with open(config_db, "r") as json_file:
            # Load the contents of the file into a dictionary
            config_data = json.load(json_file)

        # Remove the desired key-value pair from the dictionary
        config_data["TACPLUS"]["global"].pop("passkey", None)

        # Open the JSON file for writing
        # write_pretty_json_to_file(data, json_file, indent=4)
        with open(config_db, "w") as json_file:
            # Write the modified dictionary back to the JSON file
            json.dump(config_data, json_file, indent=4)


yaml_data = ""
# Open the YAML file for reading
with open(snmp, "r") as yaml_file:
    # Load the contents of the file into a dictionary
    yaml_data = yaml.safe_load(yaml_file)

# Search for the desired string
yaml_data.pop("snmp_rocommunity", None)
yaml_data.pop('snmp_rocommunity6', None)

# Open the YAML file for writing
with open(snmp, "w") as yaml_file:
    # Write the modified dictionary back to the YAML file
    yaml.dump(yaml_data, yaml_file)


tac_data = ""
# Open the file in read mode
with open(tacplus, 'r') as conf_file:
    # Read the file contents into a list
    tac_data = conf_file.readlines()

# Remove the desired data from the list
conf_lines = [line for line in tac_data if not line.startswith('server')]

# Open the file in write mode
with open(tacplus, 'w') as conf_file:
    # Write the modified contents to the file
    for item in conf_lines:
        conf_file.write(item)
print(path)
if os.path.exists(f"{path}.tar.gz"):
    os.remove(f"{path}.tar.gz")
# def make_tarfile(output_filename, source_dir):
with tarfile.open(f"{path}.tar.gz", "w:gz") as tar:
    tar.add(path, arcname=os.path.basename(path))

shutil.rmtree(path)

print(f"file with removed sensitive data: {path}.tar.gz")
