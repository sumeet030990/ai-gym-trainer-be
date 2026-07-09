"""Static reference data used to seed the database.

This is real, hand-curated reference data (roles, muscle groups, standard gym
equipment, common exercises, onboarding questions, and AI provider/model
catalogs) -- not synthetic/fake test data and not user PII.
"""

ROLES = ["Admin", "Trainer", "Member"]

MUSCLES = [
    ("Chest"),
    ("Back"),
    ("Lats"),
    ("Shoulders"),
    ("Biceps"),
    ("Triceps"),
    ("Forearms"),
    ("Abs"),
    ("Quadriceps"),
    ("Hamstrings"),
    ("Glutes"),
    ("Calves"),
    ("Traps"),
    ("Full Body"),
    ("Cardio"),
]

AI_PROVIDERS = {
    "OpenAI": ["gpt-4o", "gpt-4o-mini", "gpt-4.1"],
    "Anthropic": ["claude-sonnet-5", "claude-opus-4-8", "claude-haiku-4-5-20251001"],
    "Google": ["gemini-2.5-pro", "gemini-2.5-flash"],
}

GYMS = [
    {
        "name": "Hammer",
        "location": "Default Location",
        "contact_number": None,
        "owner_name": "Pranay",
    }
]

EQUIPMENT = [
    ("Barbell", "Standard olympic barbell"),
    ("Dumbbell", "Adjustable/free-weight dumbbells"),
    ("Kettlebell", "Cast-iron kettlebell"),
    ("Flat Bench", "Flat weight bench"),
    ("Incline Bench", "Adjustable incline weight bench"),
    ("Squat Rack", "Power rack / squat cage"),
    ("Cable Machine", "Dual-adjustable cable pulley machine"),
    ("Lat Pulldown Machine", "Seated lat pulldown station"),
    ("Leg Press Machine", "Plate-loaded leg press"),
    ("Rowing Machine", "Indoor rowing ergometer"),
    ("Pull-up Bar", "Fixed or doorway pull-up bar"),
    ("Resistance Bands", "Elastic resistance bands"),
    ("Smith Machine", "Guided barbell rack system"),
    ("Battle Ropes", "Heavy conditioning ropes"),
    ("Treadmill", "Motorized treadmill"),
    ("Stair Climber", "Motorized stair climbing machine"),
    ("Elliptical Trainer", "Low-impact cardio elliptical machine"),
]

# (exercise name, description, muscle name, primary equipment name or None,
#  extra equipment names usable for exercise_equipment join table)
EXERCISES = [
    ("Barbell Bench Press", "Flat barbell press for chest development.", "Chest", "Flat Bench", ["Barbell"]),
    ("Incline Dumbbell Press", "Incline press targeting upper chest.", "Chest", "Incline Bench", ["Dumbbell"]),
    ("Back Squat", "Barbell back squat for lower body strength.", "Quadriceps", "Squat Rack", ["Barbell"]),
    ("Deadlift", "Barbell deadlift for posterior chain strength.", "Back", "Barbell", []),
    ("Overhead Press", "Standing barbell shoulder press.", "Shoulders", "Barbell", []),
    ("Dumbbell Bicep Curl", "Standing dumbbell curl for biceps.", "Biceps", "Dumbbell", []),
    ("Cable Tricep Pushdown", "Cable pushdown for triceps.", "Triceps", "Cable Machine", []),
    ("Lat Pulldown", "Seated cable lat pulldown.", "Lats", "Lat Pulldown Machine", []),
    ("Leg Press", "Machine leg press for quads and glutes.", "Quadriceps", "Leg Press Machine", []),
    ("Plank", "Isometric core hold.", "Abs", None, []),
    ("Pull-up", "Bodyweight vertical pull.", "Lats", "Pull-up Bar", []),
    ("Kettlebell Swing", "Hip-hinge ballistic swing for glutes and hamstrings.", "Glutes", "Kettlebell", []),
    ("Treadmill Run", "Steady-state or interval cardio run.", "Cardio", "Treadmill", []),
    ("Rowing Machine", "Full body cardio and pulling exercise.", "Full Body", "Rowing Machine", []),
    ("Standing Calf Raise", "Smith machine calf raise.", "Calves", "Smith Machine", []),
]

# (question, question_type ["radio" = single choice, "checkbox" = multiple choice, "text" = free text],
#  category, sort_order, [options])
GOAL_QUESTIONS = [
    (
        "What is your primary fitness goal?",
        "radio",
        1,
        1,
        ["Lose Weight", "Build Muscle", "Improve Endurance", "General Fitness", "Increase Strength", "Flexibility & Mobility"],
    ),
    (
        "What is your current fitness level?",
        "radio",
        1,
        2,
        ["Beginner", "Intermediate", "Advanced"],
    ),
    (
        "How many days per week can you train?",
        "radio",
        2,
        3,
        ["1-2 days", "3-4 days", "5-6 days", "Every day"],
    ),
    (
        "Do you have access to gym equipment?",
        "radio",
        2,
        4,
        ["Full gym access", "Home gym (basic equipment)", "Bodyweight only"],
    ),
    (
        "Which areas would you like to focus on?",
        "checkbox",
        3,
        5,
        ["Upper Body", "Lower Body", "Core", "Full Body", "Cardio / Conditioning"],
    ),
]
