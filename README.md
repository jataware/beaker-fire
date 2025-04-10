# beaker-fire 

A beaker agent for wildfire analysis.

<div align="center">
    <img src="assets/output_20x.gif" alt="Beaker demo" width="100%">
</div>

# quickstart

```
git lfs fetch
pip install -e .
```

Then, start the notebook with:

```
cd src/beaker_fire
beaker beaker-fire
```

It will be available at localhost:8888.

> Note: if you don't run the app from `src/beaker_fire` the agent will be unable to find the `data`.

## configuration

You can configure Beaker with the `beaker config` CLI command. You can set the language model provider, API keys, etc.
