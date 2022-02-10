donor, recipient = input().split()

valid_types = ['A', 'B', 'O', 'AB']

if donor not in valid_types or recipient not in valid_types:
    print('Invalid Input')

if donor == recipient or donor == 'O' or recipient == 'AB':
    print('Donation is Valid')
else:
    print('Donation is Invalid')

