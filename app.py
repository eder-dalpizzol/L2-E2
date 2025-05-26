from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///horarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- modelos (igual ao antes) ---
class Building(db.Model):
    __tablename__ = 'building'
    id    = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String, nullable=False)
    rooms = db.relationship('Room', backref='building')

class Room(db.Model):
    __tablename__ = 'room'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))
    schedules   = db.relationship('ClassSchedule', backref='room')

class Professor(db.Model):
    __tablename__ = 'professor'
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String, nullable=False)
    subjects  = db.relationship('Subject', backref='professor')

class Subject(db.Model):
    __tablename__ = 'subject'
    id           = db.Column(db.Integer, primary_key=True)
    code         = db.Column(db.String, nullable=False)
    name         = db.Column(db.String, nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'))
    classes      = db.relationship('Class', backref='subject')

class Class(db.Model):
    __tablename__ = 'class'
    id          = db.Column(db.Integer, primary_key=True)
    subject_id  = db.Column(db.Integer, db.ForeignKey('subject.id'))
    year        = db.Column(db.Integer)
    semester    = db.Column(db.Integer)
    code        = db.Column(db.String)
    schedules   = db.relationship('ClassSchedule', backref='class')

class ClassSchedule(db.Model):
    __tablename__ = 'class_schedule'
    id           = db.Column(db.Integer, primary_key=True)
    class_id     = db.Column(db.Integer, db.ForeignKey('class.id'))
    room_id      = db.Column(db.Integer, db.ForeignKey('room.id'))
    day_of_week  = db.Column(db.Integer)  # 1=segunda ... 7=domingo
    start_time   = db.Column(db.Time)
    end_time     = db.Column(db.Time)

with app.app_context():
    db.create_all()
    if Building.query.first() is None:
        # 1) prédios
        b1 = Building(name='Prédio A')
        b2 = Building(name='Prédio B')
        db.session.add_all([b1, b2])
        db.session.commit()

        # 2) salas
        r1 = Room(name='Sala 101', building=b1)
        r2 = Room(name='Sala 102', building=b1)
        r3 = Room(name='Sala 201', building=b2)
        r4 = Room(name='Laboratório', building=b2)
        db.session.add_all([r1, r2, r3, r4])
        db.session.commit()

        # 3) professores
        p1 = Professor(name='Ana Silva')
        p2 = Professor(name='Bruno Costa')
        p3 = Professor(name='Carla Souza')
        p4 = Professor(name='Daniel Almeida')
        p5 = Professor(name='Evelyn Pereira')
        db.session.add_all([p1, p2, p3, p4, p5])
        db.session.commit()

        # 4) disciplinas
        s1 = Subject(code='MAT101', name='Matemática Básica',   professor=p1)
        s2 = Subject(code='FIS101', name='Física I',            professor=p2)
        s3 = Subject(code='QUI101', name='Química Geral',       professor=p3)
        s4 = Subject(code='POR101', name='Português',           professor=p4)
        s5 = Subject(code='HIS101', name='História',            professor=p5)
        s6 = Subject(code='MAT201', name='Matemática Avançada', professor=p1)
        db.session.add_all([s1, s2, s3, s4, s5, s6])
        db.session.commit()

        # 5) turmas
        c1 = Class(subject=s1, year=2025, semester=1, code='MATH-B1')
        c2 = Class(subject=s2, year=2025, semester=1, code='PHYS-A1')
        c3 = Class(subject=s3, year=2025, semester=1, code='CHEM-C1')
        c4 = Class(subject=s4, year=2025, semester=2, code='PORT-B2')
        c5 = Class(subject=s5, year=2025, semester=2, code='HIST-D2')
        c6 = Class(subject=s6, year=2025, semester=2, code='MATH-ADV2')
        db.session.add_all([c1, c2, c3, c4, c5, c6])
        db.session.commit()

        # 6) horários
        slots = [
            (c1, r1, 1, time(8,0),  time(10,0)),  # seg 08–10
            (c1, r1, 3, time(8,0),  time(10,0)),  # qua 08–10
            (c2, r2, 2, time(10,0), time(12,0)),  # ter 10–12
            (c2, r4, 4, time(10,0), time(12,0)),  # qui 10–12
            (c3, r3, 3, time(14,0), time(16,0)),  # qua 14–16
            (c3, r3, 5, time(14,0), time(16,0)),  # sex 14–16
            (c4, r3, 1, time(16,0), time(18,0)),  # seg 16–18
            (c4, r3, 3, time(16,0), time(18,0)),  # qua 16–18
            (c5, r4, 2, time(8,0),  time(10,0)),  # ter 08–10
            (c5, r4, 4, time(8,0),  time(10,0)),  # qui 08–10
            (c6, r2, 5, time(10,0), time(12,0)),  # sex 10–12
        ]
        for cls, room, dow, start, end in slots:
            db.session.add(
                ClassSchedule(
                    class_id=cls.id,
                    room_id=room.id,
                    day_of_week=dow,
                    start_time=start,
                    end_time=end
                )
            )
        db.session.commit()

        print("Banco populado com dados de exemplo.")    

WORK_START = time(8, 0)
WORK_END   = time(18, 0)

def calcula_livres(ocupados):
    livres = []
    cursor = WORK_START
    for s, e in ocupados:
        if cursor < s:
            livres.append((cursor, s))
        cursor = max(cursor, e)
    if cursor < WORK_END:
        livres.append((cursor, WORK_END))
    return livres

@app.route('/')
def index():
    # página inicial com dois links
    return render_template('home.html')

@app.route('/horas_por_professor')
def horas_por_professor():
    q = (
        db.session.query(
            Professor.name.label('professor'),
            func.sum(
              (func.strftime('%s', ClassSchedule.end_time)
             - func.strftime('%s', ClassSchedule.start_time)) / 3600.0
            ).label('horas')
        )
        .join(Subject).join(Class).join(ClassSchedule)
        .group_by(Professor.id)
    )
    data = [{'professor': row.professor, 'horas': row.horas or 0} for row in q]
    return render_template('horas_por_professor.html', data=data)

@app.route('/salas_horarios')
def salas_horarios():
    salas = []
    for sala in Room.query.all():
        por_dia = {}
        for d in range(1, 8):
            oc = (ClassSchedule.query
                  .filter_by(room_id=sala.id, day_of_week=d)
                  .order_by(ClassSchedule.start_time).all())
            ocup = [(c.start_time, c.end_time) for c in oc]
            livres = calcula_livres(ocup)
            por_dia[d] = {
                'ocupados': [(s.strftime('%H:%M'), e.strftime('%H:%M')) for s,e in ocup],
                'livres':   [(s.strftime('%H:%M'), e.strftime('%H:%M')) for s,e in livres]
            }
        salas.append({
            'room_id':   sala.id,
            'room_name': sala.name,
            'schedule':  por_dia
        })
    return render_template('salas_horarios.html', salas=salas)

if __name__ == '__main__':
    app.run(debug=True)
