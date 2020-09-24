from flask_website import db
from flask_website.models import User, Program, Geometry, Case, Project
from datetime import datetime

### Temporary load in data: drop when connected to flask app
db.drop_all()
db.create_all()


print('Add in users Jeff and Jeff1')
u1 = User(username = 'Jeff', email = 'jeff@123.com', password = '123')
u2 = User(username = 'Jeff1', email = 'jeff1@123.com', password = '1234')

db.session.add(u1)
db.session.add(u2)
db.session.commit()

print('This is the u1.id call')
print(u1.id)

print('Adding some programs to the mix')

p1 =Program(name = 'WRC', 
    description = 'WRC CAR', 
    created_by = u1.id) 

p2 =Program(name = 'NIGHTHAWK', 
    description = 'NASCAR', 
    created_by = u2.id)

db.session.add(p1)
db.session.add(p2)
db.session.commit()

print('Adding some geometry to the mix')

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
 
print('Print all users formatted')
jjj = [u.username for u in User.query.all()]

print(jjj)


print('Print all User names')
for u in User.query.all():
    print(u.username)

print('Print all Program names')    
for p in Program.query.all():
    print(p.name)

print('Loop and print Geometry names')
for g in Geometry.query.all():
    print(g.name)

print('Print all case names')
for c in Case.query.all():
    print(c.name)

user = User.query.filter_by(id = '2').first()
print(p1.created_by)

print('Add in two projects')
pp1 = Project(name = 'Cooling',
    description = 'Brake Cooling',
    created_by = u1.id, 
    program_id = p1.id,
    )

pp2 = Project(name = ' ASDFFF',
    description = 'Random project',
    created_by = u1.id, 
    program_id = p1.id,
    )

db.session.add(pp1)
db.session.add(pp2)
db.session.commit()


program_select = "WRC"
project_select = "Cooling"

program_validate = Program.query.filter_by(name = program_select).first()

print('\n'*3)
print(program_validate.name)
print('\n'*3)
print(program_validate.project)
for proj in program_validate.project:
    if project_select == proj.name:
        print('got em')


##



print([(str(u.id),u.name) for u in Program.query.all()])