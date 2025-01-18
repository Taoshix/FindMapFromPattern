# FindMapFromPattern
Scans your osu! maps to see if you have any maps that matches the reference rhythm using the time difference between objects with a default leeway of +-1ms to account for osu! rounding errors.

# Example usecase
Recreate the rhythm in the osu! editor and then copy the contents of the .osu file into reference.osu in the same directory as the script
## Reference rhythm
It does not care about the type, which means that you can even substitude slider ends with hit circles if you want

[![Reference rhythm](https://github.com/user-attachments/assets/70faa5ad-22cb-4dab-8ff6-e58295d501e8)](https://github.com/user-attachments/assets/70faa5ad-22cb-4dab-8ff6-e58295d501e8)

## Running the program
```bash
python find_pattern.py
```
![image](https://github.com/user-attachments/assets/0191555d-054c-4da7-9797-95aabb1c6be8)

## Result
Side by side comparison

[![Result](https://github.com/user-attachments/assets/1e0c8ed9-598a-4f8b-b5cb-a6ed919a522b)](https://github.com/user-attachments/assets/1e0c8ed9-598a-4f8b-b5cb-a6ed919a522b)