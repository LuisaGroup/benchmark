# Benchmark

Python scripts to automatically benchmark the performance of **LuisaRender**, **Mitsuba3**, and **PBRT-v4**.

## Usage
- Please edit `run_config.py` before running the benchmarks. The dictionary `target_settings` specifies the renderers and the corresponding settings. You will have to fill in the `renderer_settings["<renderer>"]["exe"]["path"]` fields for the scripts to successfully find the executables for the renderers.

  > Please note that for **PBRT-v4**, the `rr_depth` option is ineffective, since the parameter is hard coded in the renderer's source. You will have to modify the source code and recompile it to change `rr_depth`.

- After configuration, please execute the `run.py` script with Python 3 to start the benchmarks. The script generates modified scene description files under `<renderer>/scenes` and creates the `outputs` folder to hold the results. For example, the renderings are stored in `outputs/pictures` and timings in `outputs/results.csv`.
