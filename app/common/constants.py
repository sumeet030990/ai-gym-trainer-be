AI_PROVIDERS = {
  "OpenAI": "OpenAI",
  "Groq": "Groq",
  "Claude": "Claude",
  "Ollama": "Ollama",
}

REGENERATE_AFTER_DAYS = 30
REGENERATE_AFTER_LONG_BREAK = 7

# Progress plateau/spike detection: flag when an exercise's logged weight hasn't
# moved (or has jumped too fast) over its last few sessions.
PLATEAU_LOOKBACK_DAYS = 30
PLATEAU_MIN_SESSIONS = 3
PLATEAU_SPIKE_THRESHOLD_PERCENT = 20

# Adherence rate: flag when the user is logging far fewer sessions than the
# plan's weekly training days would expect.
ADHERENCE_LOOKBACK_DAYS = 14
ADHERENCE_MIN_RATE = 0.5