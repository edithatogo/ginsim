#!/usr/bin/env python3
"""
Tests for game diagram generation functions.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from src.model.game_diagrams import (
    create_enforcement_diagram,
    create_module_a_diagram,
    create_module_c_diagram,
    create_module_d_diagram,
    create_module_e_diagram,
    create_module_f_diagram,
    generate_all_game_diagrams,
)


class TestModuleADiagram:
    """Test Module A: Behavior/Deterrence diagram."""

    def test_module_a_diagram_creation(self):
        """Test Module A diagram creates without errors."""
        params = {"baseline_uptake": 0.52, "deterrence_elasticity": 0.18}
        fig = create_module_a_diagram(params=params)
        assert fig is not None
        assert fig.get_size_inches() is not None

    def test_module_a_diagram_without_params(self):
        """Test Module A diagram works without parameters."""
        fig = create_module_a_diagram()
        assert fig is not None

    def test_module_a_diagram_export(self):
        """Test Module A diagram can be saved."""
        with TemporaryDirectory() as tmpdir:
            save_path = Path(tmpdir) / "module_a_test"
            fig = create_module_a_diagram()
            fig.savefig(save_path, dpi=150, bbox_inches="tight")
            assert save_path.with_suffix(".png").exists()


class TestModuleCDiagram:
    """Test Module C: Insurance Equilibrium diagram."""

    def test_module_c_diagram_creation(self):
        """Test Module C diagram creates without errors."""
        fig = create_module_c_diagram()
        assert fig is not None

    def test_module_c_diagram_without_params(self):
        """Test Module C diagram works without parameters."""
        fig = create_module_c_diagram()
        assert fig is not None


class TestModuleDDiagram:
    """Test Module D: Proxy Substitution diagram."""

    def test_module_d_diagram_creation(self):
        """Test Module D diagram creates without errors."""
        params = {"proxy_accuracy": 0.65}
        fig = create_module_d_diagram(params=params)
        assert fig is not None

    def test_module_d_diagram_without_params(self):
        """Test Module D diagram works without parameters."""
        fig = create_module_d_diagram()
        assert fig is not None


class TestModuleEDiagram:
    """Test Module E: Pass-Through diagram."""

    def test_module_e_diagram_creation(self):
        """Test Module E diagram creates without errors."""
        params = {"pass_through_rate": 0.75}
        fig = create_module_e_diagram(params=params)
        assert fig is not None

    def test_module_e_diagram_without_params(self):
        """Test Module E diagram works without parameters."""
        fig = create_module_e_diagram()
        assert fig is not None


class TestModuleFDiagram:
    """Test Module F: Data Quality diagram."""

    def test_module_f_diagram_creation(self):
        """Test Module F diagram creates without errors."""
        params = {"research_participation_rate": 0.45}
        fig = create_module_f_diagram(params=params)
        assert fig is not None

    def test_module_f_diagram_without_params(self):
        """Test Module F diagram works without parameters."""
        fig = create_module_f_diagram()
        assert fig is not None


class TestEnforcementDiagram:
    """Test Enforcement: Compliance diagram."""

    def test_enforcement_diagram_creation(self):
        """Test Enforcement diagram creates without errors."""
        params = {"enforcement_strength": 0.7, "penalty_rate": 0.5}
        fig = create_enforcement_diagram(params=params)
        assert fig is not None

    def test_enforcement_diagram_without_params(self):
        """Test Enforcement diagram works without parameters."""
        fig = create_enforcement_diagram()
        assert fig is not None


class TestGenerateAllDiagrams:
    """Test bulk diagram generation."""

    def test_generate_all_diagrams(self):
        """Test all diagrams can be generated and exported."""
        with TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            example_params = {
                "module_a_behavior": {"baseline_uptake": 0.52, "deterrence_elasticity": 0.18},
                "module_d_proxy": {"proxy_accuracy": 0.65},
                "module_e_passthrough": {"pass_through_rate": 0.75},
                "module_f_data_quality": {"research_participation_rate": 0.45},
            }
            results = generate_all_game_diagrams(output_dir, example_params)

            # Check all 6 diagrams generated
            assert len(results) == 6

            # Check each diagram has PNG and SVG
            for paths in results.values():
                assert len(paths) == 2  # PNG and SVG
                for path in paths:
                    assert path.exists()
                    assert path.stat().st_size > 0  # File not empty

    def test_generate_all_diagrams_minimal(self):
        """Test diagram generation with minimal parameters."""
        with TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            results = generate_all_game_diagrams(output_dir)
            assert len(results) == 6
