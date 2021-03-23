## Requirements
- The `azureuser` ssh key must be available at `~/.ssh/id_rsa_azure`
- Python3 and `venv` module

## Setup

Create a virtual environment and install the dependencies.

```
python3 -m venv venv
source ./venv/bin/activate
python -m pip install -r requirements.txt
```

## Scan the ssh keys of the VMs
```
ansible -i ./inventory.ini all -a true --ssh-extra-args="-o UpdateHostKeys=yes -o StrictHostKeyChecking=accept-new"
```

## Run the only playbook as a dryrun showing changes
```
ansible-playbook -i inventory.ini playbook.yml --diff --check
```

## Run the only playbook, perform the changes and show the diffs
```
ansible-playbook -i inventory.ini playbook.yml --diff
```

## Generate inventory - TODO: replace this

I had trouble getting the Azure inventory module authenticated, so we're just using a script for now.

```
# Get the groups
az group list --query "[?starts_with(name, 'space')]".name -o tsv > groups.txt
# Rebuild the inventory.ini
cat <<EOM > inventory.ini
[all:vars]
ansible_python_interpreter=/usr/bin/python3
ansible_ssh_private_key_file=~/.ssh/id_rsa_azure
ansible_user=azureuser
EOM
for group in $(cat groups.txt );do 
  group_host=$(echo $group | cut -d_ -f1)
  echo [${group}]; 
  echo -n ${group_host} ansible_host=;az vm list-ip-addresses --resource-group ${group} --query "[?starts_with(virtualMachine.name, 'space')]".virtualMachine.network.publicIpAddresses[0].ipAddress | grep -Eo '[0-9.]+' | tr -d '\n';
  echo -n " private_ip=";az vm list-ip-addresses --resource-group ${group} --query "[?starts_with(virtualMachine.name, 'space')]".virtualMachine.network.privateIpAddresses[0] | grep -Eo '[0-9.]+'
  echo;
  done >> inventory.ini
```