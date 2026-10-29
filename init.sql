DELETE FROM job_classes;
DELETE FROM visits;
DELETE FROM classes;

INSERT INTO classes (title, value) VALUES ('Kohdetyyppi', 'kerrostalo');
INSERT INTO classes (title, value) VALUES ('Kohdetyyppi', 'omakotitalo');
INSERT INTO classes (title, value) VALUES ('Kohdetyyppi', 'liikekiinteistö');
INSERT INTO classes (title, value) VALUES ('Kohdetyyppi', 'julkinen rakennus');

INSERT INTO classes (title, value) VALUES ('Palvelu', 'ikkunanpesu');
INSERT INTO classes (title, value) VALUES ('Palvelu', 'parvekelasit');
INSERT INTO classes (title, value) VALUES ('Palvelu', 'julkisivupesu');
INSERT INTO classes (title, value) VALUES ('Palvelu', 'kattopuhdistus');

INSERT INTO classes (title, value) VALUES ('Vaihe', 'uusi');
INSERT INTO classes (title, value) VALUES ('Vaihe', 'tarjottu');
INSERT INTO classes (title, value) VALUES ('Vaihe', 'sovittu');
INSERT INTO classes (title, value) VALUES ('Vaihe', 'pesty');
