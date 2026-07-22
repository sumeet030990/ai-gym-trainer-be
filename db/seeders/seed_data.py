"""Static reference data used to seed the database.

Most of this is real, hand-curated reference data (roles, muscle groups,
standard gym equipment, common exercises, onboarding questions, and AI
provider/model catalogs). USERS is the exception: synthetic placeholder
data for local dev/testing, not a real person.
"""

ROLES = ["Admin", "Trainer", "User"]

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

CATEGORIES = [
    "Goals",
    "Profile",
    "Training Experience",
    "Availability",
    "Environment/Equip",
    "Lifestyle",
    "Medical & Injury",
    "Diet",
    "Preferences",
    "AI Personalization",
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

# Synthetic dev/test user -- placeholder contact details, not a real person.
# Password is hashed by the seeder before insert; never store plaintext.
USERS = [
    {
        "email": "sumeet@example.com",
        "mobile_no": "9999999999",
        "password": "password",
        "first_name": "Test",
        "last_name": "User",
        "birth_date": "1990-01-01",
        "diet_type": "non_vegetarian",
        "role_name": "User",
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
#  category [must match a name in CATEGORIES], sort_order, [options])
#
# Fields already captured elsewhere are intentionally NOT repeated here:
#   age (users.birth_date), height/weight/chest/waist/hips/arms/thighs/neck/body_fat
#   (all on body_measurements), diet_type base value (users.diet_type).
GOAL_QUESTIONS = [
    # Goals
    (
        "What is your primary fitness goal?",
        "checkbox",
        "Goals",
        1,
        [
            "Lose Weight", "Lose Body Fat", "Build Muscle", "Gain Weight", "Increase Strength",
            "Improve Endurance", "Body Recomposition (Lose Fat + Gain Muscle)", "Improve Athletic Performance",
            "General Fitness", "Prepare for an Event", "Lean Body", "Custom Goal",
        ],
    ),
    (
        "Any secondary goals?",
        "checkbox",
        "Goals",
        2,
        ["Improve Flexibility", "Improve Posture", "Better Sleep", "Stress Reduction", "Toning"],
    ),
    (
        "When do you want to achieve your goal?",
        "radio",
        "Goals",
        3,
        ["1 Month", "3 Months", "6 Months", "12 Months", "No Specific Timeline"],
    ),
   
    # Profile
    ("What is your gender?", "radio", "Profile", 4, ["Male", "Female", "Prefer not to say"]),
    ("What is your target weight?", "text", "Profile", 5, []),

    # Training Experience
    (
        "What is your workout experience?",
        "radio",
        "Training Experience",
        6,
        ["Beginner (0-6 months)", "Intermediate (6 months - 3 years)", "Advanced (3+ years)"],
    ),
    (
        "Have you trained consistently before?",
        "radio",
        "Training Experience",
        7,
        ["Never", "Occasionally", "Regularly", "Very Consistently"],
    ),

    # Availability
    (
        "How many days per week can you train?",
        "radio",
        "Availability",
        8,
        ["2 Days", "3 Days", "4 Days", "5 Days", "6 Days", "7 Days"],
    ),
    (
        "Which days work best for you?",
        "checkbox",
        "Availability",
        9,
        ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    ),
    (
        "Preferred workout time",
        "radio",
        "Availability",
        10,
        ["Early Morning", "Morning", "Afternoon", "Evening", "Late Night", "Flexible"],
    ),

    # Environment & Equipment
    (
        "Where will you train?",
        "radio",
        "Environment/Equip",
        11,
        ["Commercial Gym", "Home Gym", "Outdoor", "Other"],
    ),
    (
        "What equipment do you have access to?",
        "checkbox",
        "Environment/Equip",
        12,
        [
            "Treadmill", "Bike", "Rowing Machine", "Dumbbells", "Adjustable Dumbbells", "Barbells",
            "Weight Plates", "Bench", "Squat Rack", "Power Rack", "Smith Machine", "Cable Machine",
            "Leg Press", "Hack Squat", "Pull-up Bar", "Dip Station", "Resistance Bands",
            "Kettlebells", "TRX", "Medicine Ball",
        ],
    ),
    ("Any other equipment you have access to?", "text", "Environment/Equip", 13, []),

    # Lifestyle
    (
        "What best describes your daily activity?",
        "radio",
        "Lifestyle",
        14,
        ["Sedentary (Desk Job)", "Lightly Active", "Moderately Active", "Very Active", "Athlete / Physical Job"],
    ),
    ("How stressful is your daily life?", "radio", "Lifestyle", 15, ["Low", "Moderate", "High", "Very High"]),
    (
        "Average sleep duration",
        "radio",
        "Lifestyle",
        16,
        ["Less than 5 Hours", "5-6 Hours", "6-7 Hours", "7-8 Hours", "8+ Hours"],
    ),
    ("Sleep quality", "radio", "Lifestyle", 17, ["Poor", "Average", "Good", "Excellent"]),
    (
        "Average daily water intake",
        "radio",
        "Lifestyle",
        18,
        ["Less than 1L", "1-2L", "2-3L", "3-4L", "4L+"],
    ),

    # Medical & Injury
    (
        "Do you have any medical conditions?",
        "checkbox",
        "Medical & Injury",
        19,
        ["None", "Diabetes", "High Blood Pressure", "Asthma", "Heart Condition", "Thyroid Condition", "Arthritis", "Other"],
    ),
    ("Additional details on any medical condition", "text", "Medical & Injury", 20, []),
    (
        "Do you have any injuries or physical limitations?",
        "checkbox",
        "Medical & Injury",
        21,
        [
            "None", "Lower Back Pain", "Shoulder Pain", "Knee Pain", "Elbow Pain", "Wrist Pain",
            "Hip Pain", "Neck Pain", "Previous Surgery", "Other",
        ],
    ),
    ("Describe your injuries or physical limitations", "text", "Medical & Injury", 22, []),

    # Diet
    (
        "What is your diet preference?",
        "radio",
        "Diet",
        23,
        ["Vegetarian", "Vegan", "Eggetarian", "Non Vegetarian", "Pescatarian", "Keto", "Low Carb", "Mediterranean", "Other"],
    ),
    (
        "Do you have any food allergies?",
        "checkbox",
        "Diet",
        24,
        ["None", "Dairy", "Eggs", "Gluten", "Peanuts", "Tree Nuts", "Soy", "Seafood", "Shellfish", "Other"],
    ),
    ("Any other allergies?", "text", "Diet", 25, []),
    ("How many meals do you usually eat per day?", "radio", "Diet", 26, ["2", "3", "4", "5", "6+"]),
    ("Are there any foods you dislike?", "text", "Diet", 27, []),
    (
        "Do you currently take any supplements?",
        "checkbox",
        "Diet",
        28,
        ["Whey Protein", "Creatine", "Pre Workout", "Multivitamin", "Fish Oil", "BCAA", "None", "Other"],
    ),
    ("Any other supplements?", "text", "Diet", 29, []),

    # AI Personalization
    ("How aggressive should your program be?", "radio", "AI Personalization", 30, ["Conservative", "Moderate", "Aggressive"]),
    (
        "How often should we check in on your progress?",
        "radio",
        "AI Personalization",
        32,
        ["Weekly", "Every 2 Weeks", "Every 3 Weeks", "Monthly"],
    ),
]
