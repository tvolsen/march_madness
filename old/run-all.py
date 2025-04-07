import os

os.system("python3 stat-scraper.py")
print("Statistics scraper completed!")
os.system("python3 bracket-scraper.py")
print("Bracket scraper completed!")
os.system("python3 record-scraper.py")
print("Record scraper completed!")
os.system("python3 stats-prep.py")
print("Statistics preparation completed!")
os.system("python3 feature-vector-prep.py")
print("Feature vector preparation completed!")