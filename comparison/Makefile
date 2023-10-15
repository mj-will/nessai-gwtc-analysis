CONFIG = config.mk
include ${CONFIG}

BBH_EVENTS = GW150914 GW151012 GW151226 GW170104 GW170608 GW170729 GW170809 GW170814 GW170818 GW170823
BBH_EVENTS_XPHM = GW150914_XPHM GW151012_XPHM GW151226_XPHM GW170104_XPHM GW170608_XPHM GW170729_XPHM GW170809_XPHM GW170814_XPHM GW170818_XPHM GW170823_XPHM
BBH_EVENTS_LI = GW150914_LI GW151012_LI GW151226_LI GW170104_LI GW170608_LI GW170729_LI GW170809_LI GW170814_LI GW170818_LI GW170823_LI

SKYMAPS = GW150914_SKYMAP GW151012_SKYMAP GW151226_SKYMAP GW170104_SKYMAP GW170608_SKYMAP GW170729_SKYMAP GW170809_SKYMAP GW170814_SKYMAP GW170818_SKYMAP GW170823_SKYMAP

GWTC2p1_EVENTS = GW190412 GW190521 
GWTC3_EVENTS = GW191109

INESSAI = GW170823_INESSAI

$(BBH_EVENTS) : 
	python submit_pe_summary.py \
		--submit-dir submit/ \
		--job-label $@_$(ANAYLSIS_LABEL) \
		-w $(WEBDIR)/$@/ \
		-s $(GWTC1_SAMPLES)/$@_GWTC-1.hdf5 \
		   $(GWTC2p1_SAMPLES)/$@_GWTC_2p1_IMRPhenomXPHM.dat \
		   $(wildcard $(ANALYSISDIR)/outdir_nessai_gwtc_1_$@_$(ANAYLSIS_LABEL)/final_result/*.hdf5) \
		   $(wildcard $(ANALYSISDIR_XP)/outdir_nessai_gwtc_1_$@_$(ANAYLSIS_LABEL_XP)/final_result/*.hdf5) \
		--labels GWTC-1 GWTC-2 nessai-Pv2 nessai-XP \
		--gw --disable_corner --disable_remnant --disable_interactive --no_ligo_skymap


$(BBH_EVENTS_XPHM) :
	$(eval EVENT := $(shell echo $@ | grep -o "GW[0-9]\{6\}"))
	echo $(EVENT)
	python submit_pe_summary.py \
		--submit-dir submit/ \
		--job-label $@_summary \
		--add_to_existing \
		-e $(WEBDIR)/$(EVENT)/ \
		-s $(wildcard $(ANALYSISDIR_XPHM)/outdir_nessai_gwtc_1_$(EVENT)_$(ANAYLSIS_LABEL_XPHM)/final_result/*.hdf5) \
		--labels nessai-XPHM \
		--gw --disable_corner --disable_remnant --disable_interactive --no_ligo_skymap

$(BBH_EVENTS_LI) : 
	$(eval EVENT := $(shell echo $@ | grep -o "GW[0-9]\{6\}"))
	echo $(EVENT)
	python submit_pe_summary.py \
		--submit-dir submit/ \
		--job-label $(EVENT)_LIPrior_summary \
		-w $(WEBDIR_LI)/$(EVENT)/ \
		-s $(GWTC1_SAMPLES)/$(EVENT)_GWTC-1.hdf5 \
		   $(wildcard $(ANALYSISDIR)/outdir_nessai_gwtc_1_$(EVENT)_$(ANAYLSIS_LABEL)/final_result/*.hdf5) \
		   $(wildcard $(ANALYSISDIR_LI)/outdir_nessai_gwtc_1_$(EVENT)_$(ANAYLSIS_LABEL_LI)/final_result/*.hdf5) \
		--labels GWTC-1 nessai-Pv2 nessai-Pv2-LIPrior \
		--gw --disable_corner --disable_remnant --disable_interactive --no_ligo_skymap

$(GWTC2p1_EVENTS) : 
	$(eval EVENT := $(shell echo $@ | grep -o "GW[0-9]\{6\}"))
	echo $(EVENT)
	python submit_pe_summary.py \
		--submit-dir submit/ \
		--job-label $(EVENT)_PESummary \
		--memory 8GB \
		-w $(WEBDIR_O3)/$@/ \
		-s $(GWTC2p1_SAMPLES)/$(EVENT)_GWTC_2p1_IMRPhenomXPHM.dat \
		   $(wildcard $(ANALYSISDIR_O3)/outdir_$(EVENT)_IMRPhenomXPHM/final_result/*.hdf5) \
		--labels GWTC-2.1 nessai \
		--gw --disable_corner --disable_remnant --disable_interactive --no_ligo_skymap

$(GWTC3_EVENTS) : 
	$(eval EVENT := $(shell echo $@ | grep -o "GW[0-9]\{6\}"))
	echo $(EVENT)
	python submit_pe_summary.py \
		--submit-dir submit/ \
		--job-label $(EVENT)_PESummary \
		--memory 8GB \
		-w $(WEBDIR_O3)/$(EVENT)/ \
		-s $(GWTC3_SAMPLES)/$(EVENT)_GWTC_3_IMRPhenomXPHM.dat \
		   $(wildcard $(ANALYSISDIR_O3)/outdir_$(EVENT)_IMRPhenomXPHM/final_result/*.hdf5) \
		--labels GWTC-2.1 nessai \
		--gw --disable_corner --disable_remnant --disable_interactive --no_ligo_skymap


$(INESSAI) : 
	$(eval EVENT := $(shell echo $@ | grep -o "GW[0-9]\{6\}"))
	echo $(EVENT)
	python submit_pe_summary.py \
		--submit-dir submit/ \
		--job-label $(EVENT)_PESummary \
		--memory 8GB \
		-w $(INESSAI_WEBDIR)/$(EVENT)/ \
		-s  $(wildcard $(ANALYSISDIR)/outdir_nessai_gwtc_1_$(EVENT)_$(ANAYLSIS_LABEL)/final_result/*.hdf5) \
		    $(wildcard $(INESSAI_ANALYSISDIR)/outdir_inessai_gwtc_1_$(EVENT)_$()/final_result/*.hdf5) \
		--labels GWTC-1 GWTC-2 nessai-Pv2 nessai-XP \
		--labels GWTC-2.1 nessai \
		--gw --disable_corner --disable_remnant --disable_interactive --no_ligo_skymap


GW150914_phase : 
	$(eval EVENT := $(shell echo $@ | grep -o "GW[0-9]\{6\}"))
	echo $(EVENT)
	python submit_pe_summary.py \
		--submit-dir submit/ \
		--job-label $(EVENT)_PESummary \
		-w $(WEBDIR)/$(EVENT)_phase/ \
		-s $(GWTC1_SAMPLES)/$(EVENT)_GWTC-1.hdf5 \
		   $(wildcard /home/michael.williams/git_repos/nessai-gwtc-1/analysis/original_priors/outdir_nessai_gwtc_1_$(EVENT)_no_phase_marg/final_result/*.hdf5) \
		--labels GWTC-1 nessai-Pv2-no-marg \
		--gw --disable_corner --disable_remnant --disable_interactive --no_ligo_skymap

GW170817_low_spin : 
	$(eval EVENT := $(shell echo $@ | grep -o "GW[0-9]\{6\}"))
	echo $(EVENT)
	python submit_pe_summary.py \
		--submit-dir submit/ \
		--job-label $@_summary_pages \
		-w $(GW170817_WEBDIR)/$(EVENT)_low_spin_sample_calibration/ \
		-s $(GWTC1_SAMPLES)/$(EVENT)_GWTC-1.hdf5 \
		   $(wildcard $(GW170817_DIR)/outdir_nessai_gwtc_1_$(EVENT)_low_spin_sample_calibration/final_result/*.hdf5) \
		--path_to_samples /IMRPhenomPv2NRT_lowSpin_posterior None \
		--labels GWTC-1 nessai \
		--gw --disable_corner --disable_remnant --disable_interactive --no_ligo_skymap

GW190425_low_spin : 
	python submit_pe_summary.py \
		--submit-dir submit/ \
		--job-label $@_summary_pages \
		--memory 10GB \
		--add_to_existing \
		-e $(GW190425_WEBDIR)/low_spin/ \
		-s /home/michael.williams/git_repos/nessai-gwtc-1/analysis/GW190425/outdir_GW190425_low_spin_reweight/final_result/GW190425_low_spin_data0_1240215503-017_analysis_L1V1_merge_result.hdf5 \
		--labels nessai_reweight \
		--gw --disable_corner --disable_remnant --disable_interactive --no_ligo_skymap

GW190425_high_spin : 
	python submit_pe_summary.py \
		--submit-dir submit/ \
		--job-label $@_summary_pages \
		--memory 10GB \
		--add_to_existing \
		-e $(GW190425_WEBDIR)/high_spin/ \
		-s /home/michael.williams/git_repos/nessai-gwtc-1/analysis/GW190425/outdir_GW190425_high_spin_reweight/final_result/GW190425_high_spin_data0_1240215503-017_analysis_L1V1_merge_result.hdf5 \
		--labels nessai_high_spin_reweight \
		--gw --disable_corner --disable_remnant --disable_interactive --no_ligo_skymap



$(SKYMAPS) : 
	$(eval EVENT := $(shell echo $@ | grep -o "GW[0-9]\{6\}"))
	echo $(EVENT)
	python submit_skymap.py \
		--event $(EVENT) \
		--job-label $(EVENT)_skymap \
		--submit-dir submit/


.PHONY : thesis_plots
thesis_plots : corner_plots_gwtc1 corner_plots_gwtc2p1 inessai_results gwtc1_chirp_mass_plot gwtc2p1_skymaps timing_plots GW190412_plots GW190425_plots GW190521_plots GW191109_plots


.PHONY : corner_plots_gwtc1
corner_plots_gwtc1:
	python plot_corner_o1o2.py --event GW150914 --event GW170809 \
	--label gwtc_1 \
	--analysis GWTC-1 --analysis nessai-Pv2 --analysis nessai-XP \
	--parameter chirp_mass --parameter mass_ratio --parameter chi_p --parameter chi_eff \
	--parameter theta_jn --parameter ra --parameter dec --parameter luminosity_distance

.PHONY : corner_plots_gwtc2p1
corner_plots_gwtc2p1:
	python plot_corner_o1o2.py --event GW170729 --event GW170814 \
	--label gwtc_2p1 \
	--analysis GWTC-2 --analysis nessai-XPHM --analysis nessai-XP \
	--parameter chirp_mass --parameter mass_ratio --parameter chi_p --parameter chi_eff \
	--parameter theta_jn --parameter ra --parameter dec --parameter luminosity_distance

.PHONY : calibration_plots
calibration_plots : 
	jupyter nbconvert --execute compare_calibration.ipynb --to notebook --inplace

.PHONY : js_comparison_gwtc1
js_comparison_gwtc1 :
	python js_comparison.py --catalogue GWTC-1

.PHONY : js_comparison_gwtc2p1
js_comparison_gwtc2p1 :
	python js_comparison.py --catalogue GWTC-2.1

.PHONY : gwtc1_chirp_mass_plot
gwtc1_chirp_mass_plot : 
	python gwtc1_chirp_mass_plot.py

.PHONY : gwtc2p1_skymaps
gwtc2p1_skymaps : 
	jupyter nbconvert --execute skymap_comparison.ipynb --to notebook --inplace

.PHONY : timing_plots
timing_plots : 
	jupyter nbconvert --execute timing.ipynb --to notebook --inplace

.PHONY : GW170817_plots
GW170817_plots : 
	jupyter nbconvert --execute GW170817.ipynb --to notebook --inplace

.PHONY : GW190412_plots
GW190412_plots : 
	jupyter nbconvert --execute GW190412.ipynb --to notebook --inplace

.PHONY : GW190425_plots
GW190425_plots : 
	jupyter nbconvert --execute GW190425.ipynb --to notebook --inplace

.PHONY : GW190521_plots
GW190521_plots : 
	jupyter nbconvert --execute GW190521.ipynb --to notebook --inplace

.PHONY : GW191109_plots
GW191109_plots : 
	jupyter nbconvert --execute GW191109.ipynb --to notebook --inplace

.PHONY : O3_plots
O3_plots : GW190412_plots GW190425_plots GW190521_plots GW191109_plots

.PHONY : inessai_results
inessai_results : 
	jupyter nbconvert --execute inessai_comparison.ipynb --to notebook --inplace#

.PHONY : prep_download
prep_download :
	tar -zcvf results.tar.gz \
		figures/calibration \
		figures/GW150914 \
		figures/GW170809 \
		figures/GW170729 \
		figures/GW170814 \
		figures/js_comparison \
		figures/gwtc1 \
		figures/skymaps \
		figures/timing \
		figures/GW170817 \
		figures/GW190412 \
		figures/GW190521 \
		figures/GW191109 \
		figures/GW190425 \
		figures/inessai \
		results/
	