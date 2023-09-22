<div align="center">

<a href="https://mechmania.org"><img width="25%" src="https://github.com/MechMania-29/Website/blob/main/images/mm29_logo.png" alt="MechMania 29"></a>

### [website](https://mechmania.org) | python-starterpack | [java-starterpack](https://github.com/MechMania-29/java-starterpack) | [visualizer](https://github.com/MechMania-29/visualizer) | [engine](https://github.com/MechMania-29/engine) | [wiki](https://github.com/MechMania-29/Wiki)

# MechMania Python Starterpack

Welcome to MechMania! The python starterpack will allow you to write a python bot to compete against others.
Two bots will be faced against each other, and then the [engine](https://github.com/MechMania-29/engine) will run a simulation to see who wins!
After the engine runs you'll get a gamelog (a large json file) that you can use in the [visualizer](https://github.com/MechMania-29/visualizer) to
visualize the game's progress and end result.

</div>

---

## Installation

To begin, make sure you have Java 17+ installed. You can test this by running:

```sh
java --version
```

Also, you'll need python 3.9+, and you can make sure you have it by running:

```sh
python --version
```

Make sure you're using 3.9+, or things will break!

To install the engine, you can simply run:

```
python engine.py
```

and you should see an engine.jar appear in engine/engine.jar!

If you don't, you can manually install it by following the instructions on the [engine](https://github.com/MechMania-29/engine) page.

## Usage

To modify your strategy, you'll want to edit `strategy/choose_strategy.py`.
You should only need to edit files in the strategy directory.

To run your client, you can use the following commands:

### Run your bot against itself

```sh
python main.py run self
```

### Run your bot against the human computer (your bot plays zombies)

```sh
python main.py run humanComputer
```

### Run your bot against the zombie computer (your bot plays humans)

```sh
python main.py run zombieComputer
```

### Serve your bot to a port

You shouldn't need to do this, unless none of the other methods work.
<details>
<summary>Expand instructions</summary>

To serve your bot to a port, you can run it like this:

```sh
python main.py serve [port]
```

Where port is the port you want to serve to, like 9001 for example:

```sh
python main.py serve 9001
```

A full setup with the engine might look like (all 3 commands in separate terminal windows):

```sh
python main.py serve 9001
python main.py serve 9002
java -jar engine.jar 9001 9002
```

</details>
