import os
import sys
sys.path.append('..')
from glob import glob
from DeepBrainSeg.registration import Coregistration
from DeepBrainSeg.helpers.dcm2niftii import convertDcm2nifti
from DeepBrainSeg.brainmask.hdbetmask import get_bet_mask, bet_skull_stripping
from DeepBrainSeg.tumor import tumorSeg

coreg = Coregistration()
segmentor = tumorSeg()
# dcm_subject_root = '../sample_volume/dcm/all_patients'
dcm_subject_root = '/Users/admintmun/datasets/rsna-miccai-radiogenomics-classification/train'
dcm_subjects = [os.path.join(dcm_subject_root, sub) for sub in os.listdir(dcm_subject_root)]

for subject in dcm_subjects:
    seqs = os.listdir(subject)
    json = {}
    
    for seq in seqs:
        if seq.__contains__('T1wCE'):
            json['t1c'] = os.path.join(subject, seq)
        elif seq.__contains__('FLAIR'):
            json['flair'] =  os.path.join(subject, seq)
        elif seq.__contains__('T1w'):
            json['t1'] = os.path.join(subject, seq)
        elif seq.__contains__('T2w'):
            json['t2'] =  os.path.join(subject, seq)

    
    # convert dcm to nifty
    convertDcm2nifti(path_json = json,
                    output_dir = os.path.join('../rsna_miccai_results/nifty/', subject.split('/').pop()),
                    verbose = True)

    # HD-BET mask extraction

    for key in json.keys():
        # get_bet_mask(os.path.join('../sample_results/nifty/', subject.split('/').pop(), key+'t1c.nii.gz.gz'),
		# 	os.path.join('../sample_results/skull_strip/{}/'.format(subject.split('/').pop())),
        #                 device = 'cpu')
        get_bet_mask(os.path.join('../rsna_miccai_results/nifty/', subject.split('/').pop(), key + '.nii.gz'),
                     device='cpu')

        # Don't need to worry about skull stripping for the Kaggle challenge
        # bet_skull_stripping(os.path.join('../rsna_miccai_results/nifty/', subject.split('/').pop(), key+'t1c.nii.gz.gz'),
        #                     os.path.join('../rsna_miccai_results/skull_strip/{}/'.format(subject.split('/').pop()))
        #                     )
		# 	os.path.join('../sample_results/skull_strip/{}/'.format(subject.split('/').pop())))
        # get_bet_mask(os.path.join('../sample_results/nifty/', subject.split('/').pop(), key+'t1c.nii.gz.gz'),
        #     os.path.join('../sample_results/skull_strip/{}/'.format(subject.split('/').pop()))
        #              )

    # Coregistration
    moving_imgs = {'t1': os.path.join('../rsna_miccai_results/nifty/{}/{}.nii.gz'.format(subject.split('/').pop(), 't1')),
                    't2': os.path.join('../rsna_miccai_results/nifty/{}/{}.nii.gz'.format(subject.split('/').pop(), 't2')),
                    'flair':os.path.join('../rsna_miccai_results/nifty/{}/{}.nii.gz'.format(subject.split('/').pop(), 'flair'))
                    }
    fixed_img =  os.path.join('../rsna_miccai_results/nifty/{}/{}.nii.gz'.format(subject.split('/').pop(), 't1c'))
    coreg.register_patient(moving_images = moving_imgs,
                            fixed_image  = fixed_img,
                            save_path  = os.path.join('../rsna_miccai_results/coreg/{}'.format(subject.split('/').pop())))

    # # Segmentation
    segmentor.get_segmentation(os.path.join('../rsna_miccai_results/coreg/{}/isotropic/t1.nii.gz'.format(subject.split('/').pop())),
                                os.path.join('../rsna_miccai_results/coreg/{}/isotropic/t2.nii.gz'.format(subject.split('/').pop())),
                                os.path.join('../rsna_miccai_results/coreg/{}/isotropic/t1c.nii.gz'.format(subject.split('/').pop())),
                                os.path.join('../rsna_miccai_results/coreg/{}/isotropic/flair.nii.gz'.format(subject.split('/').pop())),
                                os.path.join('../rsna_miccai_results/segmentations/{}/'.format(subject.split('/').pop())))
    # segmentor = tumorSeg(quick=True)
    # segmentor.get_segmentation_brats(os.path.join('../rsna_miccai_results/nifty/', subject.split('/').pop()))

