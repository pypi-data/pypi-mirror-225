# Juno Platform

## Description

This is a library providing AI algo runtime and package management cli

## Quick Start

### install

```bash
pip install junoplatform
```

#### junocli 
##### login first before every other subcommands
```bash
junocli login <your_op_user> <your_op_password>
```

##### create a project
```bash
junocli init my_algo_project
```

##### test run
```bash
junocli run
```

##### package

```
junocli package <plant_name> <ALGO_MODULE_NAME>
```

#### upload, deploy, list & status