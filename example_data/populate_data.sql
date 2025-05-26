BEGIN TRANSACTION;

-- Prédios
INSERT INTO building (name) VALUES
  ('Prédio A'),
  ('Prédio B');

-- Salas
INSERT INTO room (name, building_id) VALUES
  ('Sala 101', 1),
  ('Sala 102', 1),
  ('Sala 201', 2),
  ('Laboratório', 2);

-- Professores
INSERT INTO professor (name) VALUES
  ('Ana Silva'),
  ('Bruno Costa'),
  ('Carla Souza'),
  ('Daniel Almeida'),
  ('Evelyn Pereira');

-- Disciplinas
INSERT INTO subject (code, name, professor_id) VALUES
  ('MAT101','Matemática Básica',    1),
  ('FIS101','Física I',             2),
  ('QUI101','Química Geral',        3),
  ('POR101','Português',            4),
  ('HIS101','História',             5),
  ('MAT201','Matemática Avançada',  1);

-- Turmas
INSERT INTO class (subject_id, year, semester, code) VALUES
  (1, 2025, 1, 'MATH-B1'),
  (2, 2025, 1, 'PHYS-A1'),
  (3, 2025, 1, 'CHEM-C1'),
  (4, 2025, 2, 'PORT-B2'),
  (5, 2025, 2, 'HIST-D2'),
  (6, 2025, 2, 'MATH-ADV2');

-- Horários das turmas
INSERT INTO class_schedule (class_id, room_id, day_of_week, start_time, end_time) VALUES
  -- Matemática Básica: seg & qua 08:00–10:00 na Sala 101
  (1, 1, 1, '08:00', '10:00'),
  (1, 1, 3, '08:00', '10:00'),

  -- Física I: ter & qui 10:00–12:00 na Sala 102
  (2, 2, 2, '10:00', '12:00'),
  (2, 2, 4, '10:00', '12:00'),

  -- Química Geral: qua & sex 14:00–16:00 na Sala 201
  (3, 3, 3, '14:00', '16:00'),
  (3, 3, 5, '14:00', '16:00'),

  -- Português: seg & qua 16:00–18:00 na Sala 201
  (4, 3, 1, '16:00', '18:00'),
  (4, 3, 3, '16:00', '18:00'),

  -- História: ter & qui 08:00–10:00 no Laboratório
  (5, 4, 2, '08:00', '10:00'),
  (5, 4, 4, '08:00', '10:00'),

  -- Matemática Avançada: sex 10:00–12:00 na Sala 102
  (6, 2, 5, '10:00', '12:00');

COMMIT;
