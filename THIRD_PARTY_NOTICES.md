# Third-party notices

The project's original code and original diagrams are licensed under MIT, copyright Max Blunden-Slusarski. That licence does not cover third-party packages, pretrained models or datasets. They retain the terms linked below. No third-party model weights or source tree is vendored. Packages are installed separately; retain their bundled notices if redistributing an environment or binary.

## Direct dependencies and tooling

| Component | Use | Licence / source |
|---|---|---|
| Python | Runtime and offline HTML dashboard | [PSF licence](https://docs.python.org/3/license.html) |
| NumPy | Array operations and geometry | [BSD-3-Clause](https://numpy.org/doc/stable/license.html) |
| SciPy | Statistical bounds and numerical evaluation | [BSD-3-Clause](https://github.com/scipy/scipy/blob/main/LICENSE.txt) |
| PyYAML | Configuration loading | [MIT](https://github.com/yaml/pyyaml/blob/main/LICENSE) |
| Matplotlib | Aggregate charts and original diagrams | [Matplotlib licence, based on PSF](https://matplotlib.org/stable/project/license.html) |
| Pillow | PNG output and local synthetic media | [MIT-CMU / HPND and bundled-library notices](https://pillow.readthedocs.io/en/stable/about.html) |
| pytest | CPU tests | [MIT](https://github.com/pytest-dev/pytest/blob/main/LICENSE) |
| Ruff | Linting and formatting | [MIT](https://github.com/astral-sh/ruff/blob/main/LICENSE) |
| pre-commit | Optional developer hooks | [MIT](https://github.com/pre-commit/pre-commit/blob/main/LICENSE) |
| setuptools | Build backend | [MIT](https://github.com/pypa/setuptools/blob/main/LICENSE) |
| pip | Installation tooling | [MIT and vendored notices](https://github.com/pypa/pip/blob/main/LICENSE.txt) |

## Transitive Python dependencies

These names cover the numerical/plotting/test environment; optional model environments add their own dependency licences. A package's bundled native libraries may have additional notices, which remain supplied in its wheel.

| Component | Licence / source |
|---|---|
| cfgv | [MIT](https://github.com/asottile/cfgv/blob/main/LICENSE) |
| distlib | [PSF-2.0 and retained historical Python terms](https://github.com/pypa/distlib/blob/master/LICENSE.txt) |
| filelock | [MIT](https://github.com/tox-dev/filelock/blob/main/LICENSE) |
| identify | [MIT](https://github.com/pre-commit/identify/blob/main/LICENSE); also verified in the installed wheel |
| nodeenv | [BSD-3-Clause](https://github.com/ekalinin/nodeenv/blob/master/LICENSE) |
| platformdirs | [MIT](https://github.com/tox-dev/platformdirs/blob/main/LICENSE) |
| python-discovery | [MIT](https://github.com/tox-dev/python-discovery/blob/main/LICENSE) |
| virtualenv | [MIT](https://github.com/pypa/virtualenv/blob/main/LICENSE) |
| contourpy | [BSD-3-Clause](https://github.com/contourpy/contourpy/blob/main/LICENSE) |
| cycler | [BSD-3-Clause](https://github.com/matplotlib/cycler/blob/main/LICENSE) |
| fonttools | [MIT](https://github.com/fonttools/fonttools/blob/main/LICENSE) |
| kiwisolver | [BSD-3-Clause](https://github.com/nucleic/kiwi/blob/main/LICENSE) |
| packaging | [Apache-2.0 OR BSD-2-Clause](https://github.com/pypa/packaging/blob/main/LICENSE) |
| pyparsing | [MIT](https://github.com/pyparsing/pyparsing/blob/master/LICENSE) |
| python-dateutil | [Apache-2.0 OR BSD-3-Clause](https://github.com/dateutil/dateutil/blob/master/LICENSE) |
| six | [MIT](https://github.com/benjaminp/six/blob/master/LICENSE) |
| iniconfig | [MIT](https://github.com/pytest-dev/iniconfig/blob/main/LICENSE) |
| pluggy | [MIT](https://github.com/pytest-dev/pluggy/blob/main/LICENSE) |
| Pygments | [BSD-2-Clause](https://github.com/pygments/pygments/blob/master/LICENSE) |
| DejaVu fonts, used by Matplotlib output | [Bitstream Vera-derived licence; DejaVu additions public domain](https://dejavu-fonts.github.io/License.html) |

## Research models and external inference libraries

| Component | Research use | Licence / source |
|---|---|---|
| RF-DETR-L / RF-DETR | Fine-tuned weapon detector | [Apache-2.0 for the open RF-DETR package and Large model](https://github.com/roboflow/rf-detr). Newer Plus model families have separate terms and are not interchangeable with the named research model |
| DINOv2 | RF-DETR vision backbone | [Apache-2.0](https://github.com/facebookresearch/dinov2/blob/main/LICENSE) |
| Qwen3-VL-8B-Instruct | Frozen vision-language verification | [Apache-2.0 model card](https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct) |
| Transformers | Qwen model loading/inference | [Apache-2.0](https://github.com/huggingface/transformers/blob/main/LICENSE) |
| Accelerate | Optional model placement/runtime support | [Apache-2.0](https://github.com/huggingface/accelerate/blob/main/LICENSE) |
| safetensors | External model serialisation | [Apache-2.0](https://github.com/huggingface/safetensors/blob/main/LICENSE) |
| Hugging Face Hub | External model access | [Apache-2.0](https://github.com/huggingface/huggingface_hub/blob/main/LICENSE) |
| PyTorch / torchvision | Neural-network runtime and image operators | [BSD-style PyTorch terms](https://github.com/pytorch/pytorch/blob/main/LICENSE), [BSD-3-Clause torchvision](https://github.com/pytorch/vision/blob/main/LICENSE) |
| Ultralytics YOLO26 pose and its BoT-SORT integration | Research person/pose inference and tracking | **[AGPL-3.0](https://github.com/ultralytics/ultralytics/blob/main/LICENSE)**, or a separately obtained commercial licence |
| lap | Assignment solver in the optional tracking runtime | [BSD-2-Clause](https://github.com/gatagat/lap/blob/master/LICENSE) |
| supervision | Detection containers and optional model adapter utilities | [MIT](https://github.com/roboflow/supervision/blob/develop/LICENSE.md) |
| Original BoT-SORT | Tracking method used through the Ultralytics integration | [MIT upstream](https://github.com/NirAharon/BoT-SORT/blob/main/LICENSE); upstream MIT does not replace the Ultralytics integration's terms |
| OpenCV | Optional video decoding and image operations | [Apache-2.0](https://github.com/opencv/opencv/blob/4.x/LICENSE) |
| OmniFall package | Research data preparation and annotation access | [Apache-2.0 package](https://pypi.org/project/omnifall/) and component-specific dataset terms; not required for the public CPU examples |

**Copyleft boundary:** the research inference adapter invokes Ultralytics as an external dependency for pose/tracking. It is not installed for the public CPU tests or synthetic dashboard, and neither its source nor its weights are distributed here. AGPL obligations can apply to a combined application and network service; separation or an optional import does not automatically remove those obligations. The MIT notice applies to original project contributions only. Resolve the external model/software terms before distributing or operating a complete inference deployment; no commercial Ultralytics licence is claimed.

The FB0 head and event/evaluation implementation are original project code. Data-derived models may have separate dataset-use restrictions even when their implementation uses a permissive software licence. See [data terms](docs/data.md). No dependency licence is accepted on the user's behalf by the examples.
