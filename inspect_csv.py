import sys

# The name of the file to inspect
file_name = "casefeed.csv"

print(f"--- Inspecting the first 30 lines of '{file_name}' ---")

try:
    with open(file_name, 'r', encoding="latin1") as f:
        for i, line in enumerate(f):
            if i >= 30:
                break
            # We add the line number (starting from 1) for clarity
            print(f"Line {i+1}: {line.strip()}")

except FileNotFoundError:
    print(f"\nError: The file '{file_name}' was not found in this directory.")
    sys.exit(1)
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")
    sys.exit(1)

print("\n--- End of inspection ---")
print("Please copy all the text above and paste it in your reply.")

