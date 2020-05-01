from flask_website import db
from flask_website.models import User, Program


for u in User.query.all():
    print(u)


print('\n')

for p in Program.query.all():
    print(p)

user = User.query.filter_by(id = '3').first()
print(user.program)


print(user)