tracking = ['you guys','hey']
tokens = ['hey', 'yall']

passed_filter = "N/A"
for p in tracking:
    print (p)
    print (set(p))
    print(set(tokens))
    if set(p).issubset(set(tokens)):
        print ('yup')
        passed_filter = p
        print("passed filter: " + passed_filter)
        break

print(passed_filter)
