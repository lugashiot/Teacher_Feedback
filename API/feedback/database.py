from django.contrib.auth import authenticate


user = authenticate(username='Stecher.Helmut', password='HTLbesteSchual123!')
if user is not None:
    print("Allah")
else:
    print("Bruh")
