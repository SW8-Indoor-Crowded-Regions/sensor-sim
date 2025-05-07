import pytest
from app.utils.heuristics import p_stay
from app.test.factories.visitor_factory import VisitorFactory


# Skulpturgaden is the largest area with 2915.98 square meters
# The restrooms are among the smallest with 18 square meters
@pytest.mark.parametrize(
	"popularity, area, alpha, beta",
	[
		(0, 18, 0.5, 0.5),          # Minimum values
		(2.0, 2915.98, 0.5, 0.5),    # Maximum values
		(1.0, 900.0, 0.5, 0.5),     # Mid-range values
		(2.0, 18.0, 0.7, 0.3),        # Max popularity, min area
		(0, 2915.98, 0.3, 0.7),      # Min popularity, max area
		(2.5, 3000.0, 0.5, 0.5),    # Out of bounds (should be clamped)
		(-1.0, -50.0, 0.5, 0.5)    # Negative values (should be clamped to 0)
	]
)


def test_p_stay_normalization_bounds(popularity, area, alpha, beta):
    """Test that p_stay() returns values within 0-1 regardless of input."""
    visitor = VisitorFactory(popularity_factor=popularity, area=area).create()
    stay_prob = p_stay(visitor, alpha=alpha, beta=beta)
    assert 0.0 <= stay_prob <= 1.0, f"Stay probability {stay_prob} is out of bounds for input: {popularity}, {area}"


def test_p_stay_comparison():
    """Test that a small, low-popularity room gets a lower stay probability than a large, high-popularity room."""
    # Small, low-popularity room
    visitor_small_low = VisitorFactory(popularity_factor=0.2, area=18).create()
    stay_prob_small_low = p_stay(visitor_small_low, alpha=0.5, beta=0.5)

    # Large, high-popularity room
    visitor_large_high = VisitorFactory(popularity_factor=2.0, area=2915.98).create()
    stay_prob_large_high = p_stay(visitor_large_high, alpha=0.5, beta=0.5)

    assert stay_prob_small_low < stay_prob_large_high, (
        f"Expected smaller stay probability for small/low room. Got {stay_prob_small_low} vs {stay_prob_large_high}"
    )