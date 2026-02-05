from app.scheduler import punch_in, punch_out

print("1 → Punch In")
print("2 → Punch Out")

choice = input("Select option: ")

if choice == "1":
    punch_in()
elif choice == "2":
    punch_out()
else:
    print("Invalid choice")
