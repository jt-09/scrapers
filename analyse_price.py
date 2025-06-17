import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the CSV file
csv_path = os.path.join(os.path.dirname(__file__), "price_history.csv")
df = pd.read_csv(csv_path)

# Convert timestamp column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Clean any missing or bad data
df = df.dropna(subset=['price', 'title'])

# Group by title
grouped = df.groupby('title')

# Show summary stats for each product
print("\n--- Price Statistics by Product ---\n")
for title, group in grouped:
    print(f"{title}")
    print(f"  Min: ${group['price'].min():.2f}")
    print(f"  Max: ${group['price'].max():.2f}")
    print(f"  Avg: ${group['price'].mean():.2f}")
    print(f"  Entries: {len(group)}\n")

# Plot price history for each product
for title, group in grouped:
    plt.figure(figsize=(8, 4))
    plt.plot(group['timestamp'], group['price'], marker='o')
    plt.title(f"Price History: {title[:50]}")  # truncate long titles
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()
