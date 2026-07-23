"""Static reference data used to seed the database.

Most of this is real, hand-curated reference data (roles, muscle groups,
standard gym equipment, common exercises, onboarding questions, and AI
provider/model catalogs). USERS is the exception: synthetic placeholder
data for local dev/testing, not a real person.
"""

ROLES = ["Admin", "Trainer", "User", "Gym Owner"]

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
    ("Air Bike", "Fan-resisted air bike for cardio conditioning"),
    ("Spin Bike", "Indoor cycling / spin bike"),
    ("Recumbent Bike", "Seated, low-impact recumbent cardio bike"),
    ("Leg Curl / Leg Extension Machine", "Seated machine for hamstring curls and quad extensions"),
    ("Pec Fly / Rear Delt Machine", "Selectorized machine for chest fly and rear delt work"),
    ("Shoulder Press Machine", "Selectorized machine for overhead shoulder pressing"),
    ("Chest Press Machine", "Selectorized machine for horizontal chest pressing"),
    ("Inner/Outer Thigh Machine", "Seated adductor/abductor machine"),
    ("Preacher Curl Machine", "Selectorized machine for isolated bicep curls"),
    ("Iso-Lateral Row Machine", "Plate-loaded independent-arm rowing machine"),
    ("Chest Press & Lat Pulldown Combo", "Dual-station machine combining chest press and lat pulldown"),
    ("Abdominal Machine", "Selectorized machine for weighted ab crunches"),
    ("Cable Crossover Machine", "Dual-tower adjustable cable crossover station"),
    ("Functional Trainer", "Dual-adjustable pulley station for functional movements"),
    ("Standing Deltoid / Multi Flight Machine", "Selectorized machine for standing shoulder/deltoid work"),
    ("Super Squat Machine", "Plate-loaded hack/squat style machine"),
    ("Lat Pull / Seated Row Machine", "Dual-station machine combining lat pulldown and seated row"),
    ("Wrist Curl Machine", "Selectorized machine for forearm/wrist curls"),
    ("Weight Lifting Platform", "Reinforced platform for olympic lifts"),
    ("Adjustable Bench", "Multi-position adjustable weight bench"),
    ("Draw Muscle Machine", "Selectorized machine for weighted torso/ab flexion"),
    ("Multi-Functional Bench", "Multi-purpose adjustable training bench"),
    ("Utility Bench", "Flat/upright utility bench"),
    ("Adjustable Ab Board", "Adjustable incline board for core/decline work"),
    ("Seated Calf Machine", "Selectorized machine for seated calf raises"),
    ("Hip Thrust Machine", "Machine for weighted hip thrust/glute bridge"),
    ("Sissy Squat Machine", "Machine for isolated sissy squats targeting quads"),
    ("Dumbbell Rack", "Tiered storage rack for dumbbells"),
    ("Weight Plate Tree", "Vertical storage tree for weight plates"),
    ("Weight Plate Rack", "Horizontal storage rack for weight plates"),
    ("Barbell Rack", "Storage rack/stand for barbells"),
    ("T-Bar Row", "Landmine-style T-bar row station"),
    ("Hyperextension Bench", "Bench for lower back hyperextensions"),
    ("Handle Rack", "Storage rack for cable attachment handles"),
    ("EZ Barbell", "Fixed-weight EZ curl barbell"),
    ("Weight Plates", "Standard olympic weight plates"),
    ("Bumper Weight Plates", "Rubber-coated bumper plates for olympic lifts"),
    ("Twister", "Sitting/standing rotational core twister machine"),
    ("Dip Stand", "Stand for parallel bar dips and hanging leg raises"),
    ("Biceps Handle", "Cable attachment for bicep curls"),
    ("Aerobic Stepper", "Adjustable-height step platform for aerobic training"),
    ("Tricep Bar", "Angled cable attachment for tricep pushdowns"),
    ("Revolving Rowing Handle", "Rotating cable attachment for rowing movements"),
    ("Tricep Rope", "Rope cable attachment for tricep pushdowns"),
]

# (exercise name, description, muscle name, primary equipment name or None,
#  extra equipment names usable for exercise_equipment join table, exercise level)
# exercise level must match db.schemas.exercises.LEVEL: "beginner" | "intermediate" | "advanced"
#
# Storage/rack-only equipment (Dumbbell Rack, Weight Plate Tree, Weight Plate Rack, Barbell Rack,
# Handle Rack) holds gear rather than being used to perform a movement, so it's intentionally not
# referenced by any exercise below.
EXERCISES = [
    ("Barbell Bench Press", "Flat barbell press for chest development.", "Chest", "Flat Bench", ["Barbell", "Weight Plates"], "intermediate"),
    ("Incline Dumbbell Press", "Incline press targeting upper chest.", "Chest", "Incline Bench", ["Dumbbell"], "intermediate"),
    ("Back Squat", "Barbell back squat for lower body strength.", "Quadriceps", "Squat Rack", ["Barbell", "Weight Plates", "Weight Lifting Platform"], "intermediate"),
    ("Deadlift", "Barbell deadlift for posterior chain strength.", "Back", "Barbell", ["Weight Plates", "Bumper Weight Plates", "Weight Lifting Platform"], "advanced"),
    ("Overhead Press", "Standing barbell shoulder press.", "Shoulders", "Barbell", ["Weight Plates"], "intermediate"),
    ("Dumbbell Bicep Curl", "Standing dumbbell curl for biceps.", "Biceps", "Dumbbell", [], "beginner"),
    ("Cable Tricep Pushdown", "Cable pushdown for triceps.", "Triceps", "Cable Machine", ["Tricep Rope", "Tricep Bar"], "beginner"),
    ("Lat Pulldown", "Seated cable lat pulldown.", "Lats", "Lat Pulldown Machine", [], "beginner"),
    ("Leg Press", "Machine leg press for quads and glutes.", "Quadriceps", "Leg Press Machine", [], "beginner"),
    ("Plank", "Isometric core hold.", "Abs", None, [], "beginner"),
    ("Pull-up", "Bodyweight vertical pull.", "Lats", "Pull-up Bar", [], "intermediate"),
    ("Kettlebell Swing", "Hip-hinge ballistic swing for glutes and hamstrings.", "Glutes", "Kettlebell", [], "intermediate"),
    ("Treadmill Run", "Steady-state or interval cardio run.", "Cardio", "Treadmill", [], "beginner"),
    ("Rowing Machine", "Full body cardio and pulling exercise.", "Full Body", "Rowing Machine", [], "beginner"),
    ("Standing Calf Raise", "Smith machine calf raise.", "Calves", "Smith Machine", [], "beginner"),
    ("Stair Climbing", "Steady-state cardio on the stair climber.", "Cardio", "Stair Climber", [], "beginner"),
    ("Elliptical Cardio Session", "Low-impact cardio on the elliptical trainer.", "Cardio", "Elliptical Trainer", [], "beginner"),
    ("Air Bike Sprints", "High-intensity interval sprints on the air bike.", "Cardio", "Air Bike", [], "intermediate"),
    ("Spin Bike Ride", "Steady-state or interval ride on the spin bike.", "Cardio", "Spin Bike", [], "beginner"),
    ("Recumbent Bike Ride", "Seated, low-impact cardio ride.", "Cardio", "Recumbent Bike", [], "beginner"),
    ("Step Aerobics", "Cardio stepping routine on the aerobic stepper.", "Cardio", "Aerobic Stepper", [], "beginner"),
    ("Battle Rope Slams", "Alternating rope slams for conditioning.", "Full Body", "Battle Ropes", [], "intermediate"),
    ("Seated Leg Curl", "Seated machine curl for hamstring isolation.", "Hamstrings", "Leg Curl / Leg Extension Machine", [], "beginner"),
    ("Leg Extension", "Seated machine extension for quad isolation.", "Quadriceps", "Leg Curl / Leg Extension Machine", [], "beginner"),
    ("Machine Pec Fly", "Selectorized fly for chest isolation.", "Chest", "Pec Fly / Rear Delt Machine", [], "beginner"),
    ("Machine Rear Delt Fly", "Selectorized reverse fly for rear delts.", "Shoulders", "Pec Fly / Rear Delt Machine", [], "beginner"),
    ("Machine Shoulder Press", "Seated machine press for shoulders.", "Shoulders", "Shoulder Press Machine", [], "beginner"),
    ("Machine Chest Press", "Seated machine press for chest.", "Chest", "Chest Press Machine", [], "beginner"),
    ("Hip Adduction/Abduction", "Seated machine work for inner/outer thigh.", "Glutes", "Inner/Outer Thigh Machine", [], "beginner"),
    ("Machine Preacher Curl", "Selectorized preacher curl for biceps isolation.", "Biceps", "Preacher Curl Machine", [], "beginner"),
    ("Iso-Lateral Row", "Plate-loaded independent-arm row.", "Back", "Iso-Lateral Row Machine", [], "intermediate"),
    ("Combo Machine Chest Press", "Chest press on the combo chest press/lat pulldown station.", "Chest", "Chest Press & Lat Pulldown Combo", [], "beginner"),
    ("Machine Ab Crunch", "Weighted crunch on the abdominal machine.", "Abs", "Abdominal Machine", [], "beginner"),
    ("Cable Crossover Fly", "Standing cable fly on the crossover station.", "Chest", "Cable Crossover Machine", [], "intermediate"),
    ("Functional Trainer Cable Chop", "Dual-pulley diagonal chop for core and full body.", "Full Body", "Functional Trainer", [], "intermediate"),
    ("Standing Machine Lateral Raise", "Standing machine raise for deltoids.", "Shoulders", "Standing Deltoid / Multi Flight Machine", [], "beginner"),
    ("Machine Squat", "Guided squat pattern on the hack/squat-style machine.", "Quadriceps", "Super Squat Machine", [], "intermediate"),
    ("Seated Cable Row", "Seated row on the lat pull/seated row station.", "Back", "Lat Pull / Seated Row Machine", [], "beginner"),
    ("Machine Wrist Curl", "Selectorized curl for forearm isolation.", "Forearms", "Wrist Curl Machine", [], "beginner"),
    ("Adjustable Bench Dumbbell Press", "Dumbbell press on an adjustable bench.", "Chest", "Adjustable Bench", ["Dumbbell"], "beginner"),
    ("Standing Draw-In Ab Crunch", "Weighted torso flexion on the draw muscle machine.", "Abs", "Draw Muscle Machine", [], "beginner"),
    ("Multi-Functional Bench Step-Up", "Weighted step-up using a multi-functional bench.", "Quadriceps", "Multi-Functional Bench", ["Dumbbell"], "beginner"),
    ("Seated Dumbbell Shoulder Press", "Seated dumbbell press on a utility bench.", "Shoulders", "Utility Bench", ["Dumbbell"], "beginner"),
    ("Decline Sit-Up", "Decline sit-up on an adjustable ab board.", "Abs", "Adjustable Ab Board", [], "beginner"),
    ("Seated Calf Raise", "Seated machine raise for calf isolation.", "Calves", "Seated Calf Machine", [], "beginner"),
    ("Machine Hip Thrust", "Guided hip thrust for glute development.", "Glutes", "Hip Thrust Machine", [], "beginner"),
    ("Machine Sissy Squat", "Isolated quad squat on the sissy squat machine.", "Quadriceps", "Sissy Squat Machine", [], "intermediate"),
    ("T-Bar Row", "Landmine-style row for back thickness.", "Back", "T-Bar Row", [], "intermediate"),
    ("Back Hyperextension", "Lower back extension on a hyperextension bench.", "Back", "Hyperextension Bench", [], "beginner"),
    ("EZ Bar Curl", "Standing curl using an EZ barbell.", "Biceps", "EZ Barbell", [], "beginner"),
    ("Standing Twist", "Rotational core movement on the twister.", "Abs", "Twister", [], "beginner"),
    ("Tricep Dip", "Bodyweight dip on a dip stand.", "Triceps", "Dip Stand", [], "intermediate"),
    ("Cable Bicep Curl", "Standing cable curl for biceps.", "Biceps", "Cable Machine", ["Biceps Handle"], "beginner"),
    ("Cable Seated Row", "Seated cable row using a rowing handle.", "Back", "Cable Machine", ["Revolving Rowing Handle"], "beginner"),
    ("Band Pull-Apart", "Resistance band pull-apart for rear delt and upper back activation.", "Shoulders", "Resistance Bands", [], "beginner"),
    ("Barbell Shrug", "Standing barbell shrug for trap development.", "Traps", "Barbell", ["Weight Plates"], "beginner"),
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
