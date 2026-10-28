"""
Disclaimer text shared by the tools.

Kept in one place so the wording asserted by the prompt-contract and integration
tests cannot drift between tools. See boundaries B2 and B3 in the design
document: nutrition figures are estimates, and diet tags are catalog labels
rather than a verified allergen analysis.
"""

ESTIMATE_DISCLAIMER = (
    "Nutrition figures are estimates from a simulated database, not measured values, "
    "and are not suitable for clinical use."
)

ALLERGEN_NOTE = (
    "Diet tags are catalog labels only. This is not an allergen analysis — "
    "always check the actual product labels and your own ingredients before cooking."
)

DIETITIAN_NOTE = (
    "For any dietary requirement tied to a medical condition, consult a registered dietitian."
)


__all__ = ["ESTIMATE_DISCLAIMER", "ALLERGEN_NOTE", "DIETITIAN_NOTE"]
