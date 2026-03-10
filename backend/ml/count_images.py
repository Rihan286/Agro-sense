import os

BASE_PATH = "../../data/Chilli"

total_all = 0

for split in ["train", "val", "test"]:
    split_path = os.path.join(BASE_PATH, split)
    split_total = 0

    print(f"\n--- {split.upper()} ---")

    for cls in os.listdir(split_path):
        cls_path = os.path.join(split_path, cls)

        if os.path.isdir(cls_path):
            count = len([
                f for f in os.listdir(cls_path)
                if f.lower().endswith(('.jpg','.jpeg','.png'))
            ])

            split_total += count
            print(f"{cls}: {count}")

    print(f"Total {split}: {split_total}")
    total_all += split_total

print("\n======================")
print(f"TOTAL DATASET: {total_all} images")