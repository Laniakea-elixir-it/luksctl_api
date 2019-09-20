# luksctl_api

An API to check the status of luks volumes and open it if needed.
No close method is provided.

Installation and configuration
==============================

1. Crete luksctl_api user
```
# useradd luksctl_api
```

2. Clone and install luksctl package

```
# sudo -i -u luksctl_api

$ git clone https://github.com/Laniakea-elixir-it/luksctl.git

$ cd lukctl

$ pip install .
```

3. Clone and install luksctl_api repository

```
# sudo -i -u luksctl_api

$ git clone https://github.com/Laniakea-elixir-it/luksctl_api.git
```

4. Install and enable systemd unit file 
