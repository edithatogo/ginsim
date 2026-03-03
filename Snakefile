# Snakemake pipeline for genetic discrimination policy model
# Usage: snakemake --cores all --configfile configs/experiments/phase4_policy_sweep.yaml

configfile: "configs/experiments/default.yaml"

# =============================================================================
# TARGETS
# =============================================================================

rule all:
    input:
        # Model outputs
        expand("outputs/results/{experiment}/posterior_samples.npy", experiment=config["experiments"]),
        # Validation
        "outputs/validation/stress_tests/summary.yaml",
        "outputs/validation/ppc/summary.yaml",
        # VOI analysis
        "outputs/voi/{experiment}/evpi.yaml",
        "outputs/voi/{experiment}/evppi_by_group.csv",
        # Figures
        "outputs/figures/{experiment}/policy_comparison.png",
        "outputs/figures/{experiment}/testing_uptake.png",
        "outputs/figures/{experiment}/premium_divergence.png",

# =============================================================================
# MODEL EXECUTION
# =============================================================================

rule run_model:
    """Run the full model for a given experiment configuration."""
    input:
        config="configs/experiments/{experiment}.yaml",
        priors="configs/calibration_{jurisdiction}.yaml"
    output:
        "outputs/results/{experiment}/posterior_samples.npy"
    conda:
        "environment.yaml"
    log:
        "logs/model_{experiment}.log"
    benchmark:
        "benchmarks/model_{experiment}.tsv"
    script:
        "scripts/run_model.py"

# =============================================================================
# VALIDATION
# =============================================================================

rule stress_tests:
    """Run stress test scenarios."""
    input:
        "outputs/results/{experiment}/posterior_samples.npy"
    output:
        "outputs/validation/stress_tests/summary.yaml"
    conda:
        "environment.yaml"
    log:
        "logs/stress_tests_{experiment}.log"
    script:
        "scripts/run_stress_tests.py"

rule posterior_predictive_checks:
    """Run posterior predictive checks."""
    input:
        "outputs/results/{experiment}/posterior_samples.npy"
    output:
        "outputs/validation/ppc/summary.yaml"
    conda:
        "environment.yaml"
    log:
        "logs/ppc_{experiment}.log"
    script:
        "scripts/run_posterior_predictive.py"

# =============================================================================
# VALUE OF INFORMATION
# =============================================================================

rule compute_evpi:
    """Compute Expected Value of Perfect Information."""
    input:
        "outputs/results/{experiment}/posterior_samples.npy"
    output:
        "outputs/voi/{experiment}/evpi.yaml"
    conda:
        "environment.yaml"
    log:
        "logs/evpi_{experiment}.log"
    script:
        "scripts/run_voi.py"

rule compute_evppi:
    """Compute Expected Value of Partial Perfect Information by parameter group."""
    input:
        "outputs/results/{experiment}/posterior_samples.npy"
    output:
        "outputs/voi/{experiment}/evppi_by_group.csv"
    conda:
        "environment.yaml"
    log:
        "logs/evppi_{experiment}.log"
    script:
        "scripts/run_evppi_by_group.py"

# =============================================================================
# FIGURES
# =============================================================================

rule figure_policy_comparison:
    """Generate policy comparison figure."""
    input:
        "outputs/results/{experiment}/posterior_samples.npy"
    output:
        "outputs/figures/{experiment}/policy_comparison.png"
    conda:
        "environment.yaml"
    script:
        "scripts/figures/policy_comparison.py"

rule figure_testing_uptake:
    """Generate testing uptake figure."""
    input:
        "outputs/results/{experiment}/posterior_samples.npy"
    output:
        "outputs/figures/{experiment}/testing_uptake.png"
    conda:
        "environment.yaml"
    script:
        "scripts/figures/testing_uptake.py"

rule figure_premium_divergence:
    """Generate premium divergence figure."""
    input:
        "outputs/results/{experiment}/posterior_samples.npy"
    output:
        "outputs/figures/{experiment}/premium_divergence.png"
    conda:
        "environment.yaml"
    script:
        "scripts/figures/premium_divergence.py"

# =============================================================================
# REPORTING
# =============================================================================

rule generate_report:
    """Generate comprehensive results report."""
    input:
        results=expand("outputs/results/{experiment}/posterior_samples.npy", experiment=config["experiments"]),
        voi=expand("outputs/voi/{experiment}/evppi_by_group.csv", experiment=config["experiments"]),
        figures=expand("outputs/figures/{experiment}/policy_comparison.png", experiment=config["experiments"])
    output:
        "outputs/reports/{experiment}/results.html"
    conda:
        "environment.yaml"
    script:
        "scripts/generate_report.py"
