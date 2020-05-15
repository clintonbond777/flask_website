from flask_website import db
from flask_website.models import User, Program, Geometry, Case

### Temporary load in data: drop when connected to flask app
db.drop_all()
db.create_all()

u1 = User(username = 'Jeff', email = 'jeff@123.com', password = '123')
u2 = User(username = 'Jeff1', email = 'jeff1@123.com', password = '1234')

db.session.add(u1)
db.session.add(u2)
db.session.commit()

print(u1.id)

p1 =Program(name = 'WRC', 
    description = 'WRC CAR', 
    created_by = u1.id) 

p2 =Program(name = 'NIGHTHAWK', 
    description = 'NASCAR', 
    created_by = u2.id)

db.session.add(p1)
db.session.add(p2)
db.session.commit()

g1 = Geometry(name = 'Baseline-1-04', 
    description = '2022 baseline car', 
    created_by = u2.id)

g2 = Geometry(name = 'Baseline-1-04-WA-FF-01', 
    description = 'Front Splitter Extension (-x)', 
    created_by = u1.id)

db.session.add(g1)
db.session.add(g2)
db.session.commit() 

c1 =Case(name = 'baseline run', 
    description = '2022 baseline preliminary run', 
    created_by = u1.id, 
    project_id = p1.id,  
    geometry_id = g2.id
    )

c2 =Case(name = 'WA-FF-01 Part Swap ', 
    description = '2022 part swap', 
    created_by = u1.id, 
    project_id = p1.id, 
    geometry_id = g2.id 
    )

db.session.add(c1)
db.session.add(c2)
db.session.commit()

for u in User.query.all():
    print(u.username)
    
for p in Program.query.all():
    print(p.name)

for g in Geometry.query.all():
    print(g.name)

for c in Case.query.all():
    print(c.name)

user = User.query.filter_by(id = '2').first()
print(p1.created_by)

