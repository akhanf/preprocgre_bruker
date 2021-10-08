#!/usr/bin/env python

import numpy as np
import nibabel as nib
import json

imag_nii = snakemake.input.imag_nii
real_nii = snakemake.input.real_nii

imag_img = nib.load(imag_nii)
real_img = nib.load(real_nii)

print(f'Computing phase with Siemens dicom convention from {imag_nii} and {real_nii} as (arctan2(imag,real) / Pi +1 )*2048')
phase = np.arctan2(imag_img.get_fdata(),real_img.get_fdata());
phase = ((phase/np.pi) +1.0 )*2048;
phase = nib.casting.float_to_int(phase, 'int16')

phase_nii = snakemake.output.phase_nii
print(f'Saving as {phase_nii}')
phase_nib = nib.Nifti1Image(phase, real_img.affine, real_img.header)
nib.save(phase_nib, phase_nii)

imag_json = snakemake.input.imag_json
phase_json = snakemake.output.phase_json

print(f'Creating json from {imag_json}, replacing IMAGINARY with PHASE in image type, saving as {phase_json}')
with open(imag_json) as f:
    json_dict = json.load(f)

if 'ImageType' in json_dict:
    json_dict['ImageType'][5] = 'PHASE'

with open(phase_json, 'w') as outfile:
    json.dump(json_dict, outfile,indent=4)


