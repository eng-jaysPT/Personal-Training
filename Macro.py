def calculate_macros(current_weight, activity_level, body_fat_percentage, goal, muscle_gain_percentage, fat_loss_percentage, weeks):
    protein_per_kg = 2.0
    maintenance_fat_per_kg = 1.0
    fat_loss_fat_per_kg = 0.8
    muscle_gain_fat_per_kg = 1.2
    calories_per_gram_protein = 4
    calories_per_gram_fat = 9
    calories_per_gram_carbs = 4

    activity_multiplier = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9,
    }

    tdee = (88.4 + 13.4 * current_weight) * activity_multiplier.get(activity_level, 1.2)

    # Calculate weekly adjustments
    tdee_adjustment = (tdee * muscle_gain_percentage / 100 - tdee * (1 - fat_loss_percentage / 100)) / weeks
    protein_adjustment = protein_per_kg * current_weight * muscle_gain_percentage / (100 * weeks)
    fat_adjustment = (fat_loss_fat_per_kg * current_weight - fat_loss_fat_per_kg * current_weight * fat_loss_percentage / 100) / weeks

    macros = []
    for week in range(weeks + 1):
        adjusted_tdee = tdee + week * tdee_adjustment
        protein = protein_per_kg * current_weight + week * protein_adjustment

        if goal == "maintenance":
            fat = maintenance_fat_per_kg * current_weight
        elif goal == "fat_loss":
            fat = fat_loss_fat_per_kg * current_weight
        elif goal == "muscle_gain":
            fat = muscle_gain_fat_per_kg * current_weight
        elif goal == "recomposition":
            fat = (fat_loss_fat_per_kg + muscle_gain_fat_per_kg) / 2 * current_weight
        
        # Calculate carb intake with a 10% reduction from the previous week's total
        if week == 0:
            carbs = (adjusted_tdee - (protein * calories_per_gram_protein) - (fat * calories_per_gram_fat)) / calories_per_gram_carbs
        else:
            carbs = carbs * 1.05

        macros.append((protein, fat, carbs))

    return macros


if __name__ == "__main__":
    current_weight = float(input("Enter your current weight (kg): "))
    activity_level = input("Enter your activity level (sedentary, light, moderate, active, very_active): ")
    body_fat_percentage = float(input("Enter your current body fat percentage: "))
    goal = input("Enter your goal (muscle_gain, maintenance, fat_loss, recomposition): ")
    muscle_gain_percentage = float(input("Enter desired muscle gain percentage (applies only to muscle_gain goal): "))
    fat_loss_percentage = float(input("Enter desired fat loss percentage (applies only to fat_loss goal): "))
    weeks = int(input("Enter the desired timeframe in weeks: "))

    macros = calculate_macros(current_weight, activity_level, body_fat_percentage, goal, muscle_gain_percentage, fat_loss_percentage, weeks)

    for week, (protein, fat, carbs) in enumerate(macros):
        print(f"Week {week}:")
        print(f"  Protein: {protein:.2f} grams/day")
        print(f"  Fat: {fat:.2f} grams/day")
        print(f"  Carbohydrates: {carbs:.2f} grams/day")
        print()