# Attribution Quality

This package was designed to both generate explanations for deep learning segmentation models as well as to provide comprehensive metrics for evaluating new explanation methods.

We have included our novel explanation method, Kernel-Weighted Contribution, as well as a number of other XAI methods adapted for use with segmentation models. With the additional use of our [explanation ground-truth dataset](https://github.com/Mullans/NoduleSeg), we can evaluate the quality of these methods and provide a comprehensive comparison of their performance.

<!-- The paper describing the methods and dataset is available as [Kernel-Weighted Contribution: A Novel Method of Visual Attribution for 3D Deep Learning Segmentation in Medical Imaging](link forthcoming). -->


## Startup Instructions

Note - We use [mamba](https://github.com/mamba-org/mamba) to install packages, but you can use [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) in the same way if you prefer.

1. Install `attribution_quality` requirements
   1. Either [install torch or build from source](https://pytorch.org/get-started/locally/)
   2. `mamba install -c conda-forge numpy scikit-image tqdm`
2. Install `attribution_quality`
   1. METHOD 1 (recommended)
      1. `pip install attribution_quality --no-deps`
   2. METHOD 2 (for local development)
      1. `git clone git@github.com:Mullans/AttributionQuality.git`
      2. `cd AttributionQuality`
      3. `pip install -e . --no-deps`
3. (Optional) Install SimpleITK and matplotlib for the example notebooks and for some evaluation metrics
   1. `mamba install -c simpleitk -c conda-forge simpleitk matplotlib`

## nnUNet Setup Instructions (optional)

*Note: We used nnUNet for the experiments described in our paper. You can skip this section unless you want to reproduce our results.*

1. Install nnUNet requirements
   1. `mamba install -c conda-forge -c simpleitk dicom2nifti medpy scikit-learn simpleitk pandas nibabel matplotlib`
   2. `pip install batchgenerators`
2. Install nnUNet v1
   1. `git clone -b nnunetv1 --single-branch git@github.com:MIC-DKFZ/nnUNet.git`
   2. `cd nnunet`
   3. `pip install -e . --no-deps`
3. Finish setting up nnUNet
   1. Set `nnUNet_raw_data_base`, `nnUNet_preprocessed`, and `RESULTS_FOLDER` environment variables

## Attribution Quality Example Notebooks

1. `examples/SingleLayer_Example.ipynb` - Example Jupyter notebook showing how to use this package to generate explanations for a single layer of a segmentation model
2. `examples/Full_KWC_Example.ipynb` - Example Jupyter notebook showing how to run Kernel-Weighted Contribution on all layers of a segmentation model and evaluate the resulting attribution map

Currently included methods of explanation:
| | | |
| -- | -- | -- |
| Kernel-Weighted Contribution | ScoreCAM | |
| GradCAM | GradCAM++ | LayerCAM |
| XGradCAM | Element-wise GradCAM | HiResCAM|
| | | |

