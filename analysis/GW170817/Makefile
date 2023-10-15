
.PHONY : submit_l1_l2
submit_l1_l2 : 
	bilby_pipe GW170817_low_spin_reweight_cal_fix_sky_l1_l2.ini --submit
	bilby_pipe GW170817_low_spin_sample_cal_fix_sky_l1_l2.ini --submit
	bilby_pipe GW170817_high_spin_reweight_cal_fix_sky_l1_l2.ini --submit
	bilby_pipe GW170817_high_spin_sample_cal_fix_sky_l1_l2.ini --submit

.PHONY : submit_priors
submit_priors : 
	bilby_pipe GW170817_low_spin_reweight_cal_fix_sky_priors.ini --submit
	bilby_pipe GW170817_low_spin_sample_cal_fix_sky_priors.ini --submit
	bilby_pipe GW170817_high_spin_reweight_cal_fix_sky_priors.ini --submit
	bilby_pipe GW170817_high_spin_sample_cal_fix_sky_priors.ini --submit
