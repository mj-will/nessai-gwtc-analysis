.PHONY : submit_all
submit_all : submit_bbh, submit_bns

.PHONY : submit_bbh, submit_bns
submit_bbh : 
	bilby_pipe GW150914.ini --submit
	bilby_pipe GW151012.ini --submit
	bilby_pipe GW151226.ini --submit
	bilby_pipe GW170104.ini --submit
	bilby_pipe GW170608.ini --submit
	bilby_pipe GW170729.ini --submit
	bilby_pipe GW170809.ini --submit
	bilby_pipe GW170814.ini --submit
	bilby_pipe GW170818.ini --submit
	bilby_pipe GW170823.ini --submit

submit_bns : 
	bilby_pipe GW170817_low_spin.ini --submit
	bilby_pipe GW170817_high_spin.ini --submit