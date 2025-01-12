# Psychological support bot

## Links
- [Used template](https://github.com/Latand/tgbot_template_v3)


## Development

### Setup

```sh
python3.12 -m venv venv
source ./venv/bin/activate.fish
make setup
```

### Running
#### Run (after setup)
```sh
make run
```

#### Run with docker
```sh
make docker
```

### Correct errors
#### Lint

```sh
make lint
```

#### Format + fix

```sh
make format
```

#### Type Check

```sh
make type-check
```

### Migrations
#### New revision
```sh
make rev
```

#### Upgrade db to latest revision
```sh
make upgrade
```