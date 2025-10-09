import pandas as pd
import random
import os

INTENTS = {
    # Maps to NeuroDesignOS / MetaDesign System
    "design_recommendation": [
        "Create a Y2K denim skirt for Asia, eco-friendly.",
        "Generate a streetwear hoodie with neon highlights.",
        "I need a visual prototype for a summer pastel dress.",
        "Design a modest outfit for the Middle East market.",
        "What does an asymmetrical satin gown look like?",
        "Show me a design sketch for a new t-shirt line.",
        "Generate a pattern for a casual shirt."
    ],
    # Maps to HoloShopOS / Retail & Commerce System / MirrorPersonaOS
    "outfit_recommendation": [
        "Suggest a new outfit for a summer wedding guest.",
        "What should I wear for a night out in Paris?",
        "Show me 5 outfits for a party that match my profile.",
        "Find me a business casual look for the office.",
        "Mix & match my items for a relaxed weekend.",
        "Give me styling advice for my black denim jacket.",
        "I need a mix and match for my date night."
    ],
    # Maps to SalesLiftOS / Retail & Commerce System
    "pricing_optimization": [
        "What is the optimal price for the new denim jacket?",
        "Predict the sales lift from a 15% discount.",
        "Generate a dynamic price recommendation for product P103.",
        "Should I adjust the price based on demand trend?",
        "What bundle should I offer with the boots and jacket?",
        "Analyze competitor pricing for my sneakers."
    ],
    # Maps to FabricVerseOS/GreenIndexOS / Sustainability System
    "fabric_selection": [
        "I need sustainable fabric suggestions for a t-shirt.",
        "Compare hemp vs organic cotton for eco-score.",
        "What materials are available for a product launch in EU?",
        "Give me the ESG score for polyester.",
        "Suggest greener alternatives to use in my new design.",
        "Find a low-carbon material for a winter coat."
    ],
    # Catch-all for non-fashion/non-operational queries
    "unclassified": [
        "What is the capital of France?",
        "Tell me a joke about Python.",
        "I need help with my Flask server deployment.",
        "Can you run a database migration for me?",
        "How does JWT authentication work?",
        "What's the weather like today?",
        "Summarize the news headlines."
    ]
}

def generate_labeled_data(intents_dict, num_samples_per_intent=100):
    """Generates a DataFrame of synthetic labeled data."""
    data = []
    for intent, prompts in intents_dict.items():
        for _ in range(num_samples_per_intent):
            # Pick a prompt
            prompt = random.choice(prompts)
            
            # Simple simulation: 30% chance of adding a conversational phrase to simulate user input
            if random.random() < 0.3:
                variations = ["Hey AI, ", "Can you help me: ", "I want to do this: ", "Please generate ", "Hi, ", "I have a question: "]
                prompt = random.choice(variations) + prompt.lower()
            
            # Simple simulation: 20% chance of adding punctuation variation
            if random.random() < 0.2:
                prompt = prompt.rstrip('?.') + random.choice(['.', '!', ''])
                
            data.append({'text_input': prompt, 'intent': intent})
            
    # Shuffle and reset index
    df = pd.DataFrame(data).sample(frac=1).reset_index(drop=True)
    return df


output_file = 'backend/app/neurocoreos/intent_data.csv'
df = generate_labeled_data(INTENTS, num_samples_per_intent=100)
df.to_csv(output_file, index=False)
