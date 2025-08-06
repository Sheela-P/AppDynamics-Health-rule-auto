# ✅ Loads and analyzes CPU usage 
# ✅ Logs activity to health_rule_log.txt 
# ✅ Shows last saved threshold from threshold_config.txt 
# ✅ Saves new threshold to both threshold_config.txt and suggested_threshold.txt 
# ✅ Commits both files to GitHub with timestamped messages 
# ✅ Prints everything clearly in the terminal



# import pandas as pd
# import logging
# import subprocess

# # Configure logging
# logging.basicConfig(
#     filename='health_rule_log.txt',
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

# # Show last saved threshold
# try:
#     with open('threshold_config.txt', 'r') as f:
#         last_threshold = f.read().strip()
#     print(f"\n📁 Last saved threshold: {last_threshold}")
# except FileNotFoundError:
#     print("\n📁 No previous threshold found. Starting fresh.")

# # Load data
# df = pd.read_csv('performance_metrics.csv')
# df['timestamp'] = pd.to_datetime(df['timestamp'])

# # Basic stats
# avg_cpu = df['cpu_usage'].mean()
# high_usage_count = len(df[df['cpu_usage'] > 85])
# high_usage_ratio = high_usage_count / len(df)

# # Decision logic
# print("\n📊 AppDynamics Health Rule Model\n")
# print(f"✅ Loaded {len(df)} data points.")
# print(f"📉 Average CPU usage: {round(avg_cpu, 2)}%")
# print(f"⚠️ High usage instances (>85%): {high_usage_count} ({round(high_usage_ratio*100, 2)}%)")

# cpu_threshold = None
# if avg_cpu > 70 or high_usage_ratio > 0.3:
#     cpu_threshold = round(df['cpu_usage'].quantile(0.95), 2)
#     print(f"\n📈 Suggested Health Rule threshold: {cpu_threshold}% (95th percentile)")
#     print("🚨 CPU usage is high. Consider updating Health Rule and investigating.")
    
#     # Save threshold
#     with open('threshold_config.txt', 'w') as f:
#         f.write(f"CPU Threshold: {cpu_threshold}%\n")
#     logging.info(f"Suggested CPU threshold: {cpu_threshold}% based on high usage.")
    
#     # Git commit
#     subprocess.run(['git', 'add', 'threshold_config.txt'], check=True)
#     subprocess.run(['git', 'commit', '-m', f'Update CPU threshold to {cpu_threshold}%'], check=True)
#     subprocess.run(['git', 'push'], check=True)
#     logging.info("Threshold committed and pushed to GitHub.")
# else:
#     print("\n✅ CPU usage is within normal range. No threshold update needed.")
#     logging.info("No threshold update needed. CPU usage is normal.")


import pandas as pd
import logging
import subprocess
from datetime import datetime

# 🪵 Configure logging
logging.basicConfig(
    filename='health_rule_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 📁 Show last saved threshold
try:
    with open('threshold_config.txt', 'r') as f:
        last_threshold = f.read().strip()
    print(f"\n📁 Last saved threshold: {last_threshold}")
except FileNotFoundError:
    print("\n📁 No previous threshold found. Starting fresh.")

# 📥 Load data
try:
    df = pd.read_csv('performance_metrics.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
except Exception as e:
    print(f"❌ Error loading CSV: {e}")
    logging.error(f"Failed to load CSV: {e}")
    exit()

# 📊 Basic stats
avg_cpu = df['cpu_usage'].mean()
high_usage_count = len(df[df['cpu_usage'] > 85])
high_usage_ratio = high_usage_count / len(df)

# 🧠 Decision logic
print("\n📊 AppDynamics Health Rule Model\n")
print(f"✅ Loaded {len(df)} data points.")
print(f"📉 Average CPU usage: {round(avg_cpu, 2)}%")
print(f"⚠️ High usage instances (>85%): {high_usage_count} ({round(high_usage_ratio*100, 2)}%)")

cpu_threshold = None
if avg_cpu > 70 or high_usage_ratio > 0.3:
    cpu_threshold = round(df['cpu_usage'].quantile(0.95), 2)
    print(f"\n📈 Suggested Health Rule threshold: {cpu_threshold}% (95th percentile)")
    print("🚨 CPU usage is high. Consider updating Health Rule and investigating.")

    # 📝 Save threshold to both files
    with open('threshold_config.txt', 'w') as f:
        f.write(f"CPU Threshold: {cpu_threshold}%\n")
    with open("suggested_threshold.txt", "w") as f:
        f.write(f"Suggested Threshold: {cpu_threshold:.2f}%\n")

    logging.info(f"Suggested CPU threshold: {cpu_threshold}% based on high usage.")

    # 🕒 Git commit with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        subprocess.run(['git', 'add', 'threshold_config.txt', 'suggested_threshold.txt'], check=True)
        subprocess.run(['git', 'commit', '-m', f'Updated threshold at {timestamp}'], check=True)
        subprocess.run(['git', 'push'], check=True)
        logging.info("Threshold committed and pushed to GitHub.")
        print("🚀 Git update successful.")
    except subprocess.CalledProcessError as e:
        print("⚠️ Git update failed. Check your repo and authentication.")
        logging.error(f"Git error: {e}")
else:
    print("\n✅ CPU usage is within normal range. No threshold update needed.")
    logging.info("No threshold update needed. CPU usage is normal.")
