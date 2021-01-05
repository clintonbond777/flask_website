from flask_website import db
from flask_website.models import User, Program, Model, Case, Project, RideMap
from datetime import datetime

### Temporary load in data: drop when connected to flask app
db.drop_all()
db.create_all()


print("Add in users Jeff and Jeff1")
u1 = User(username="Jeff", email="jeff@123.com", password="123")
u2 = User(username="Jeff1", email="jeff1@123.com", password="1234")

db.session.add(u1)
db.session.add(u2)
db.session.commit()

print("This is the u1.id call")
print(u1.id)

print("Adding some programs to the mix")

p1 = Program(name="MERCURY MARAUDER", description="It was a car", created_by=u1.id)

p2 = Program(name="TOYOTA PRIUS", description="Make less drag!", created_by=u2.id)

p3 = Program(
    name="FERRARI MONDEO", description="Speed is the name of the game", created_by=u1.id
)

list_programs = [p1, p2, p3]

for prog in list_programs:
    db.session.add(prog)

db.session.commit()

print("Adding some geometry to the mix")

m1 = Model(name="Baseline-1", description="asdf", created_by=u2.id, program_id=p1.id)
m2 = Model(
    name="Baseline-2",
    description="testing the cooling",
    created_by=u1.id,
    program_id=p1.id,
)
m3 = Model(
    name="Baseline-3",
    description="expanded front wheel liner",
    created_by=u1.id,
    program_id=p1.id,
)

m4 = Model(
    name="Baseline-4",
    description="changes to underbody",
    created_by=u2.id,
    program_id=p2.id,
)
m5 = Model(
    name="Baseline-5",
    description="change in splitter",
    created_by=u2.id,
    program_id=p2.id,
)
m6 = Model(
    name="Baseline-6", description="new rear wing", created_by=u1.id, program_id=p2.id
)

m7 = Model(
    name="Baseline-7", description="added wicker", created_by=u2.id, program_id=p3.id
)
m8 = Model(
    name="SPL-01",
    description="Front Splitter Extension (-x)",
    created_by=u1.id,
    program_id=p3.id,
)

list_models = [m1, m2, m3, m4, m5, m6, m7, m8]

for mod in list_models:
    db.session.add(mod)
db.session.commit()

### Ridemap
r1 = RideMap(name="AA", description="A bumpy ride on gravel", program_id=p1.id)
r2 = RideMap(name="BB", description="shorter track", program_id=p1.id)
r3 = RideMap(name="CC", description="rrh sweep", program_id=p1.id)

r4 = RideMap(name="DD", description="simulator map", program_id=p2.id)
r5 = RideMap(name="EE", description="corner exit map", program_id=p2.id)
r6 = RideMap(name="FF", description="gravel map 32", program_id=p2.id)

r7 = RideMap(name="GG", description="Short-track-550", program_id=p3.id)
r8 = RideMap(name="HH", description="Short-track-650", program_id=p3.id)
r9 = RideMap(name="II", description="Short-track-750", program_id=p3.id)

list_rm = [r1, r2, r3, r4, r5, r6, r7, r8, r9]

for mod in list_rm:
    db.session.add(mod)
db.session.commit()

c1 = Case(
    name="baseline run",
    description="2022 baseline preliminary run",
    created_by=u1.id,
    project_id=p1.id,
    model_id=m1.id,
    baseline_id=m1.id,
    ridemap_id=r1.id,
)

c2 = Case(
    name="Test part swap",
    description="2022 part swap",
    created_by=u1.id,
    project_id=p1.id,
    model_id=m2.id,
    baseline_id=m1.id,
    ridemap_id=r2.id,
)

c3 = Case(
    name="baseline run",
    description="2022 baseline preliminary run",
    created_by=u1.id,
    project_id=p1.id,
    model_id=m3.id,
    baseline_id=m1.id,
    ridemap_id=r1.id,
)

c4 = Case(
    name="Test part swap",
    description="2022 part swap",
    created_by=u1.id,
    project_id=p3.id,
    model_id=m4.id,
    baseline_id=m2.id,
    ridemap_id=r4.id,
)

c5 = Case(
    name="baseline run",
    description="2022 baseline preliminary run",
    created_by=u1.id,
    project_id=p1.id,
    model_id=m3.id,
    baseline_id=m1.id,
    ridemap_id=r5.id,
)

c6 = Case(
    name="Test part swap",
    description="2022 part swap",
    created_by=u1.id,
    project_id=p3.id,
    model_id=m4.id,
    baseline_id=m2.id,
    ridemap_id=r5.id,
)

c7 = Case(
    name="Test part swap",
    description="2022 part swap",
    created_by=u1.id,
    project_id=p3.id,
    model_id=m7.id,
    baseline_id=m2.id,
    ridemap_id=r7.id,
)

c8 = Case(
    name="baseline run",
    description="2022 baseline preliminary run",
    created_by=u1.id,
    project_id=p1.id,
    model_id=m8.id,
    baseline_id=m7.id,
    ridemap_id=r8.id,
)

c9 = Case(
    name="Test part swap",
    description="2022 part swap",
    created_by=u1.id,
    project_id=p3.id,
    model_id=m8.id,
    baseline_id=m2.id,
    ridemap_id=r9.id,
)

list_models = [c1, c2, c3, c4, c5, c6, c7, c8, c9]

for mod in list_models:
    db.session.add(mod)
db.session.commit()

print("Print all users formatted")
user_formatted = [u.username for u in User.query.all()]

print(user_formatted)


print("Print all User names")
for u in User.query.all():
    print(u.username)

print("Print all Program names")
for p in Program.query.all():
    print(p.name)

print("Loop and print Geometry names")
for g in Model.query.all():
    print(g.name)

print("Print all case names")
for c in Case.query.all():
    print(c.name)

user = User.query.filter_by(id="2").first()
print(p1.created_by)

print("Add in a few projects")
pp1 = Project(
    name="Cooling",
    description="Brake Cooling",
    created_by=u2.id,
    program_id=p1.id,
)

pp2 = Project(
    name=" ASDFFF",
    description="Random project",
    created_by=u1.id,
    program_id=p1.id,
)

pp3 = Project(
    name="Baseline-1 dev",
    description="Development from June 15 onward",
    created_by=u2.id,
    program_id=p2.id,
)

pp4 = Project(
    name=" asdfasfdaa",
    description="ffasdf",
    created_by=u1.id,
    program_id=p2.id,
)

pp5 = Project(
    name="Baseline-aaasdf dev",
    description="quick work here tires",
    created_by=u2.id,
    program_id=p3.id,
)

pp6 = Project(
    name=" ffdjjjgpsa",
    description="sdafgfff",
    created_by=u1.id,
    program_id=p3.id,
)

list_projects = [pp1, pp2, pp3, pp4, pp5, pp6]

for mod in list_projects:
    db.session.add(mod)
db.session.commit()

program_select = "WRC"
project_select = "Cooling"

program_validate = Program.query.filter_by(name=program_select).first()

print("\n" * 3)

if program_validate:
    print(program_validate.name)
    print("\n" * 3)
    print(program_validate.project)
    for proj in program_validate.project:
        if project_select == proj.name:
            print(project_select)

    print([(str(u.id), u.name) for u in Program.query.all()])