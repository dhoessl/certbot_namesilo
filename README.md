# certbot_namesilo
ansible role to create a container managing certificates for domains on namesilo

# How To Use

1. Add this role as submodule to your playbook.

```bash
git submodule add https://github.com/dhoessl/certbot_namesilo.git roles/certbot_namesilo
```
2. Add it to the play

```yaml
---
- hosts: 'all'
  roles:
    - role: 'certbot_namesilo'
      tags: 'certbot'
...
```

3. Add Email Variable to inventory file
```yaml
---
certbot_email: 'my.email@examle.com'
...
```

4. Add Namesilo Api Key to vault file
```yaml
---
certbot_namesilo_apikey: 'xxxxxxxxxxxxxx'
...
```

5. Run the play
```bash
ansible-playbook -D playbook.yaml -i path/to/inventory.yaml --tags 'certbot'
```

This will create an image with certbot installed and every file to manage namesilo dns records.

Then there will be a one time container deployed, mounting `/etc/letsencrypt` and checking for wildcard certificates.

If this certificates are close to expiry, it will be renewed.

This container need to be run manually every now and then or just use a pipeline to run it everyday and forget about it.

# Restarting Services and Container
If you want to restart a specific service or container after renewal add it to `certbot_restart_services` or `certbot_restart_container` list.

For service it will be checked if the services in running otherwise the service wont be started.

Containers wont be checked so make sure to set the correct names.
