# About
Lucrezia is a storytelling engine written in Panda3D with a PyQT5 editor that aims to narrates immersive 3D stories blending 2D art style with cinematic effects.

Current builds are very experimental and are subject to change rapidly, shipping mostly broken and half-baked features.

# Dependencies
TODO

# Run
Clone the repo:

```
git clone https://github.com/snizzo/lucrezia.git
```

Navigate inside the directory:
```
cd lucrezia
```

Launch the game:

```
python3 src/main.py
```

Launch the editor:
```
python3 src/editor.py
```

# Test
Lucrezia is shipped with many functional tests for single features / scenarios / behaviours. 

List all tests:
```
python3 src/main.py -lt
```

Launch a single test:
```
python3 src/main -t TestName
```
