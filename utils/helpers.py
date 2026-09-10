import math
import random

def format_currency(amount):
    """
    Formats a numeric amount into Indian Rupee format.
    Example: 2485000 -> ₹24,85,000
    """
    try:
        val = int(round(amount))
        s = str(val)
        if len(s) <= 3:
            return f"₹{s}"
        last_three = s[-3:]
        other = s[:-3]
        res = ""
        while len(other) > 2:
            res = "," + other[-2:] + res
            other = other[:-2]
        res = other + res + "," + last_three
        return f"₹{res}"
    except Exception:
        return f"₹{amount:,}"

def calculate_market_range(predicted_price, percentage=0.055):
    """
    Calculates approximate market range (+/- 5.5%).
    Returns min_price and max_price rounded to nearest ₹5,000.
    """
    delta = predicted_price * percentage
    min_p = int(round((predicted_price - delta) / 5000.0) * 5000)
    max_p = int(round((predicted_price + delta) / 5000.0) * 5000)
    return {
        "min": min_p,
        "max": max_p,
        "formatted_min": format_currency(min_p),
        "formatted_max": format_currency(max_p)
    }

def generate_price_explanation(input_data, predicted_price):
    """
    Generates a clear human-readable explanation of key factors driving
    the predicted price based on vehicle parameters. No external LLM required.
    """
    year = int(input_data.get("year", 2020))
    km = int(input_data.get("km_driven", 50000))
    transmission = str(input_data.get("transmission", "Manual"))
    fuel = str(input_data.get("fuel_type", "Petrol"))
    ownership = str(input_data.get("ownership", "1st Owner"))
    condition = str(input_data.get("condition", "Good"))
    brand = str(input_data.get("brand", "Vehicle"))
    model = str(input_data.get("model", ""))
    
    current_year = 2026
    age = current_year - year

    positives = []
    negatives = []

    # Age impact
    if age <= 3:
        positives.append("recent manufacturing year")
    elif age >= 8:
        negatives.append("higher vehicle age")

    # Mileage/KM impact
    if km <= 35000:
        positives.append("exceptionally low kilometers driven")
    elif km > 85000:
        negatives.append("accumulated high mileage/kilometers")

    # Transmission impact
    if transmission == "Automatic":
        positives.append("automatic transmission preference in the used car market")

    # Fuel Type impact
    if fuel in ["Diesel", "Hybrid"]:
        positives.append(f"{fuel} engine fuel efficiency and resale demand")
    elif fuel == "Electric":
        positives.append("electric drivetrain market adoption")

    # Ownership impact
    if ownership == "1st Owner":
        positives.append("single-owner vehicle history")
    elif ownership in ["3rd Owner", "4+ Owners"]:
        negatives.append("multiple previous ownership transfers")

    # Condition impact
    if condition == "Excellent":
        positives.append("top-tier vehicle condition rating")
    elif condition in ["Fair", "Poor"]:
        negatives.append(f"{condition.lower()} vehicle physical condition rating")

    # Build coherent narrative
    if positives and negatives:
        pos_str = ", ".join(positives)
        neg_str = ", ".join(negatives)
        explanation = (
            f"The estimated value for your {brand} {model} is positively influenced by its {pos_str}. "
            f"However, factors such as {neg_str} slightly reduce the overall market resale value."
        )
    elif positives:
        pos_str = ", ".join(positives)
        explanation = (
            f"Your {brand} {model} holds strong market value due to key positive drivers including its {pos_str}."
        )
    elif negatives:
        neg_str = ", ".join(negatives)
        explanation = (
            f"The valuation reflects market depreciation primarily driven by {neg_str}."
        )
    else:
        explanation = (
            f"The estimated value aligns with standard market depreciation metrics for a {year} {brand} {model} "
            f"with {km:,} km driven."
        )

    return explanation

def generate_image_price_explanation(detected_specs, predicted_price):
    """
    Generates explanation text for AI camera scan prediction.
    """
    brand = detected_specs.get("brand", "Vehicle")
    model = detected_specs.get("model", "")
    body_type = detected_specs.get("body_type", "SUV")
    condition = detected_specs.get("condition", "Good")
    confidence = detected_specs.get("visual_confidence", 92)

    return (
        f"DriveValue AI Vision engine scanned the captured image with {confidence}% confidence, identifying a "
        f"{brand} {model} ({body_type}) in {condition.lower()} visual exterior condition. Valuation was computed "
        f"using trained market regression features calibrated for this vehicle class."
    )
