import pandas as pd
import matplotlib.pyplot as plt
import os


# === Set mode here: "combined" or "individual"
PLOT_MODE = "combined"     # for one shared graph
# PLOT_MODE = "individual"   # for separate graphs per product


# === Load CSV ===
csv_path = os.path.join(os.path.dirname(__file__), "price_history.csv")
df = pd.read_csv(csv_path)

# === Clean and prepare ===
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.dropna(subset=['price', 'title'])

# === Print price stats per product ===
print("\n--- Price Statistics by Product ---\n")
grouped = df.groupby('title')

for title, group in grouped:
    print(f"{title}")
    print(f"  Min: ${group['price'].min():.2f}")
    print(f"  Max: ${group['price'].max():.2f}")
    print(f"  Avg: ${group['price'].mean():.2f}")
    print(f"  Entries: {len(group)}\n")

# === Plotting ===
if PLOT_MODE == "combined":
    plt.figure(figsize=(10, 6))
    for title, group in grouped:
        plt.plot(group['timestamp'], group['price'], marker='o', label=title[:50])  # Truncate title if too long
    plt.title("Price History (All Products)")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

elif PLOT_MODE == "individual":
    for title, group in grouped:
        plt.figure(figsize=(8, 4))
        plt.plot(group['timestamp'], group['price'], marker='o')
        plt.title(f"Price History: {title[:50]}")
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

else:
    print(f"Unknown PLOT_MODE: {PLOT_MODE}")