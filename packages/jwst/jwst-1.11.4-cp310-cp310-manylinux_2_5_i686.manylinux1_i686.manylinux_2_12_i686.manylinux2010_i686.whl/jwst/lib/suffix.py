"""Suffix manipulation

API
---
`remove_suffix`
    Main function used to remove suffixes from
    file base names.

Notes
-----

`KNOW_SUFFIXES` is the list used by `remove_suffix`. This
list is generated by the function `combine_suffixes`. The function uses
`SUFFIXES_TO_ADD` to add other suffixes that it would otherwise not
discover or should absolutely be in the list. The function uses
'SUFFIXES_TO_DISCARD` for strings found that are not to be considered
suffixes.

Hence, to update `KNOW_SUFFIXES`, update both `SUFFIXES_TO_ADD` and
`SUFFIXES_TO_DISCARD` as necessary, then use the output of
`find_suffixes`.
"""
from importlib import import_module
import itertools
import logging
from os import (listdir, path)
import re

__all__ = ['remove_suffix']

# Configure logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# Suffixes that are hard-coded or otherwise
# have to exist. Used by `find_suffixes` to
# add to the result it produces.
SUFFIXES_TO_ADD = [
    'ami', 'amiavg', 'aminorm',
    'blot', 'bsub', 'bsubints',
    'c1d', 'cal', 'calints', 'cat', 'crf', 'crfints',
    'dark',
    'i2d',
    'median',
    'phot', 'psf-amiavg', 'psfalign', 'psfstack', 'psfsub',
    'ramp', 'rate', 'rateints', 'residual_fringe',
    's2d', 's3d', 'snr',
    'uncal',
    'wfscmb', 'whtlt',
    'x1d', 'x1dints',
]

# Suffixes that are discovered but should not be considered.
# Used by `find_suffixes` to remove undesired values it has found.
SUFFIXES_TO_DISCARD = ['engdblogstep', 'functionwrapper', 'pipeline', 'rscd_step', 'step', 'systemcall']


# Calculated suffixes.
# This is produced by the `find_suffixes` function below
_calculated_suffixes = {
    'masterbackgroundmosstep',
    'ami3pipeline',
    'whitelightstep',
    'ami_average',
    'spec3pipeline',
    'wfscombine',
    'fringe',
    'resamplestep',
    'resample_spec',
    'saturationstep',
    'firstframestep',
    'cat',
    'systemcall',
    'alignrefsstep',
    'functionwrapper',
    'darkcurrentstep',
    'imprintstep',
    'source_catalog',
    'straylight',
    'amiaveragestep',
    'ami_normalize',
    'jumpstep',
    'resample',
    'sourcetypestep',
    'spec2pipeline',
    'tweakreg',
    'msaflagopenstep',
    'outlierdetectionstep',
    'saturation',
    'pathloss',
    'groupscalestep',
    'ramp_fit',
    'lastframe',
    'darkpipeline',
    'image2pipeline',
    'outlierdetectionstackstep',
    'tso3pipeline',
    'straylightstep',
    'sourcecatalogstep',
    'dark_current',
    'mrs_imatch',
    'assignwcsstep',
    'skymatch',
    'extract_2d',
    'cubebuildstep',
    'residualfringestep',
    'residual_fringe',
    'spec2nrslamp',
    'ipc',
    'refpix',
    'image3pipeline',
    'superbiasstep',
    'hlspstep',
    'reset',
    's2d',
    'ami_analyze',
    'flatfieldstep',
    'tsophotometrystep',
    'combine_1d',
    'step',
    'cubeskymatchstep',
    'i2d',
    'group_scale',
    'rscdstep',
    'stackrefsstep',
    'flat_field',
    'guidercdsstep',
    'mrsimatchstep',
    'align_refs',
    'dqinitstep',
    'outlierdetectionscaledstep',
    'superbias',
    'assign_wcs',
    'guider_cds',
    'firstframe',
    'masterbackgroundstep',
    'master_background',
    'skymatchstep',
    'white_light',
    'persistencestep',
    'amianalyzestep',
    'backgroundstep',
    'photomstep',
    'background',
    'photom',
    'extract_1d',
    'cube_build',
    'wfscombinestep',
    'lastframestep',
    'aminormalizestep',
    'linearity',
    'rscd',
    'rampfitstep',
    'pipeline',
    'engdblog',
    'resamplespecstep',
    'persistence',
    'klip',
    'dq_init',
    'barshadowstep',
    'klipstep',
    'linearitystep',
    'hlsp',
    'pathlossstep',
    'refpixstep',
    'gainscalestep',
    'extract2dstep',
    'detector1pipeline',
    'fringestep',
    'dark',
    'whtlt',
    'guiderpipeline',
    'stackrefs',
    'imprint',
    'coron3pipeline',
    'resetstep',
    'combine1dstep',
    'outlier_detection_scaled',
    'outlier_detection_stack',
    'srctype',
    'outlier_detection',
    'engdblogstep',
    'gain_scale',
    'ipcstep',
    'jump',
    'extract1dstep',
    'tweakregstep',
    'assignmtwcsstep',
    'assign_mtwcs',
    'wavecorrstep',
    'wfsscontamstep',
    'undersamplingcorrectionstep',
    'pixelreplacestep',
}


# ##########
# Suffix API
# ##########
def remove_suffix(name):
    """Remove the suffix if a known suffix is already in name"""
    separator = None
    match = REMOVE_SUFFIX_REGEX.match(name)
    try:
        name = match.group('root')
        separator = match.group('separator')
    except AttributeError:
        pass
    if separator is None:
        separator = '_'
    return name, separator


def replace_suffix(name, new_suffix):
    """Replace suffix on name

    Parameters
    ----------
    name: str
        The name to replace the suffix of.
        Expected to be only the basename; no extensions.

    new_suffix:
        The new suffix to use.
    """
    no_suffix, separator = remove_suffix(name)
    return no_suffix + separator + new_suffix


# #####################################
# Functions to generate `KNOW_SUFFIXES`
# #####################################
def combine_suffixes(
        to_add=(_calculated_suffixes, SUFFIXES_TO_ADD),
        to_remove=(SUFFIXES_TO_DISCARD,)
):
    """Combine the suffix lists into a single list

    Parameters
    ----------
    to_add: [iterable[, ...]]
        List of iterables to add to the combined list.

    to_remove: [iterable[, ...]]
        List of iterables to remove from the combined list.

    Returns
    -------
    suffixes: list
        The list of suffixes.
    """
    combined = set(itertools.chain.from_iterable(to_add))
    combined.difference_update(itertools.chain.from_iterable(to_remove))
    combined = list(combined)
    combined.sort()

    return combined


def find_suffixes():
    """Find all possible suffixes from the jwst package

    Returns
    -------
    suffixes: set
        The set of all programmatically findable suffixes.

    Notes
    -----
    This will load all of the `jwst` package. Consider if this
    is worth doing dynamically or only as a utility to update
    a static list.
    """
    from jwst.stpipe import Step
    from jwst.stpipe.utilities import all_steps

    jwst = import_module('jwst')
    jwst_fpath = path.split(jwst.__file__)[0]

    # First traverse the code base and find all
    # `Step` classes. The default suffix is the
    # class name.
    suffixes = set(
        klass_name.lower()
        for klass_name, klass in all_steps().items()
    )

    # Instantiate Steps/Pipelines from their configuration files.
    # Different names and suffixes can be defined in this way.
    # Note: Based on the `collect_pipeline_cfgs` script
    config_path = path.join(jwst_fpath, 'pipeline')
    for config_file in listdir(config_path):
        if config_file.endswith('.cfg'):
            try:
                step = Step.from_config_file(
                    path.join(config_path, config_file)
                )
            except Exception as err:
                logger.debug(f'Configuration {config_file} failed: {str(err)}')
            else:
                suffixes.add(step.name.lower())
                if step.suffix is not None:
                    suffixes.add(step.suffix.lower())

    # That's all folks
    return list(suffixes)


# --------------------------------------------------
# The set of suffixes used by the pipeline.
# This set is generated by `combine_suffixes`.
# Only update this list by `combine_suffixes`.
# Modify `SUFFIXES_TO_ADD` and `SUFFIXES_TO_DISCARD`
# to change the results.
# --------------------------------------------------
KNOW_SUFFIXES = combine_suffixes()

# Regex for removal
REMOVE_SUFFIX_REGEX = re.compile(
    '^(?P<root>.+?)((?P<separator>_|-)(' +
    '|'.join(KNOW_SUFFIXES) + '))?$'
)


# ############################################
# Main
# Find and report differences from known list.
# ############################################
if __name__ == '__main__':
    print('Searching code base for calibration suffixes...')
    calculated_suffixes = find_suffixes()
    found_suffixes = combine_suffixes(
        to_add=(calculated_suffixes, SUFFIXES_TO_ADD),
        to_remove=(SUFFIXES_TO_DISCARD, )
    )
    print(
        'Known list has {known_len} suffixes.'
        ' Found {new_len} suffixes.'.format(
            known_len=len(KNOW_SUFFIXES),
            new_len=len(found_suffixes)
        )
    )
    print(
        'Suffixes that have changed are {}'.format(
            set(found_suffixes).symmetric_difference(KNOW_SUFFIXES)
        )
    )
