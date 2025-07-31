# password_strength_checker.py

import argparse
from zxcvbn import zxcvbn

def analyze_password(password):
    result = zxcvbn(password)
    score = result['score']
    feedback = result['feedback']

    print(f"\nPassword Strength Score: {score} / 4")

    if feedback['warning']:
        print("⚠️ Warning:", feedback['warning'])
    if feedback['suggestions']:
        print("💡 Suggestions:")
        for suggestion in feedback['suggestions']:
            print(f"  - {suggestion}")

    strength_levels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
    print(f"\n🔐 Password Strength: {strength_levels[score]}")

def main():
    parser = argparse.ArgumentParser(description="Password Strength Analyzer")
    parser.add_argument("-p", "--password", type=str, help="Password to analyze")

    args = parser.parse_args()

    if args.password:
        analyze_password(args.password)
    else:
        password = input("Enter password to check strength: ")
        analyze_password(password)

if __name__ == "__main__":
    main()
