import pickle



t1_seg_radiomics = pickle.load(open("/Users/admintmun/dev/DeepBrainSeg/sample_volume/brats/Brats18_2013_11_1/DBSRadFeatures/Seq_t1_Class_whole/all_features.pickle", "rb"))

print(t1_seg_radiomics)