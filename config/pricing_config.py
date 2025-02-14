from dataclasses import dataclass


@dataclass(frozen=True)
class TokenPricing:
    input_price: float
    output_price: float


# Centralized mapping of model names to pricing details
MODEL_PRICING_MAP = {
    "claude-3-5-haiku-latest": TokenPricing(
        input_price=0.8 / 1000000,  # $0.80 per million input tokens
        output_price=4 / 1000000,  # $4.00 per million output tokens
    ),
    "claude-3-5-sonnet-latest": TokenPricing(
        input_price=3 / 1000000,  # $3 per million input tokens
        output_price=15 / 1000000,  # $15 per million output tokens
    ),
    "gpt-4o-mini": TokenPricing(
        input_price=0.15 / 1000000,  # $0.15 per million input tokens
        output_price=0.6 / 1000000,  # $0.60 per million output tokens
    ),
    "gpt-4o": TokenPricing(
        input_price=2.5 / 1000000,  # $2.5 per million input tokens
        output_price=10 / 1000000,  # $10 per million output tokens
    ),
    "gemini-2.0-flash": TokenPricing(
        input_price=0.1 / 1000000,  # $0.10 per million input tokens
        output_price=0.4 / 1000000,  # $0.40 per million output tokens
    ),
    "gemini-2.0-flash-thinking-exp": TokenPricing(
        input_price=0.1 / 1000000,  # pricing not available...
        output_price=0.4 / 1000000,  # pricing not available...
    ),
}


def get_pricing(model_name: str) -> TokenPricing:
    """Fetches the pricing configuration for the given model."""
    if model_name not in MODEL_PRICING_MAP:
        raise ValueError(f"Model {model_name} not found in pricing map")

    return MODEL_PRICING_MAP[model_name]
