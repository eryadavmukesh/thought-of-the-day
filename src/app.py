from utils.thought_generator import ThoughtGenerator
import json

def main():
    print("Welcome to Thought of the Day!")
    generator = ThoughtGenerator()

    # Interaction 1: Motivation theme
    print("\nGenerating thought for theme: 'motivation'")
    result1 = generator.get_thought("motivation")
    print(json.dumps(result1, indent=2))

    # Interaction 2: Random theme
    print("\nGenerating thought with random theme")
    result2 = generator.get_thought()
    print(json.dumps(result2, indent=2))

    # Interaction 3: Peace theme
    print("\nGenerating thought for theme: 'peace'")
    result3 = generator.get_thought("peace")
    print(json.dumps(result3, indent=2))

if __name__ == "__main__":
    main()