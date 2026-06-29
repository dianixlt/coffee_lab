import sqlite3, os

DB = os.path.join(os.path.dirname(__file__), 'coffeelab.db')

def run():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.executescript("DELETE FROM sesiones; DELETE FROM recetas; DELETE FROM cafes; DELETE FROM equipo;")

    # ── EQUIPO ─────────────────────────────────────────────────────────────
    equipo = [
        ('V60 Mugen',               'Hario',        'brewer',  None,         'Plástico — método principal taza individual.'),
        ('V60 + Garrafa',           'Hario',        'brewer',  None,         'Batch hasta 40g.'),
        ('Chemex',                  'Chemex',       'brewer',  None,         'Batch 40g+. Doblar filtro siempre. Nunca meter nada al filtro si se apelmaza.'),
        ('UFO Dripper',             None,           'brewer',  None,         'Plástico — en aprendizaje. Máximo 15g. Solo naturales/honeys. Flujo lento constante.'),
        ('Aeropress',               'Aeropress',    'brewer',  None,         'Dosis pequeñas 10–18g.'),
        ('French Press',            None,           'brewer',  None,         'Naturales con cuerpo, cafés viejos.'),
        ('Epeios Essence',          'Epeios',       'grinder', None,         'Molino eléctrico dial 0–80. ⚠️ Dando señales de falla — dividir en máx 2 porciones de 25g por ciclo.'),
        ('Greater Goods Scale',     'Greater Goods','otro',    None,         'Báscula con timer.'),
        ('Instastings Kettle',      'Instastings',  'otro',    None,         'Control de temperatura.'),
        ('Filtros Cafec Abaca',     'Cafec',        'otro',    None,         'Upgrade reciente. Usar siempre para florales, Geshas y etíopes washed.'),
        ('Origami Sensory Cup',     'Origami',      'otro',    None,         'Blanca — para Geshas y florales delicados. Prueba definitiva Origami vs taza normal pendiente (Elida ASD 2a bolsa).'),
    ]
    con.executemany('INSERT INTO equipo (nombre,marca,tipo,fecha_adquisicion,notas) VALUES (?,?,?,?,?)', equipo)
    print(f'  ✓ {len(equipo)} equipos')

    # ── CAFÉS ──────────────────────────────────────────────────────────────
    # (nombre, roaster, pais_origen, proceso, perfil_taza, fecha_compra, estado, puntuacion)
    cafes = [
        # ABIERTOS
        ('Javier Salas El Renacer',         'Prodigal',     'Colombia',      'lavado',  'Anaerobic washed Gesha. Mol 40 · 90°C.',                                                         None,         'en_stock', None),
        ('Mutana',                           'La Cabra',     'Burundi',       'lavado',  'Washed Bourbon Burundi. Mol 38 · 93°C.',                                                          None,         'en_stock', None),
        ('Dabid Berrio La Casita',           'Sey',          'Colombia',      'lavado',  'Washed Chiroso. Mol 38 · 93°C.',                                                                  None,         'en_stock', None),
        ('Lovely Day',                       'Dark Arts',    'Myanmar',       'natural', 'Carbonic maceration natural Myanmar. Mol 42 · 88°C.',                                             None,         'en_stock', None),
        ('Ninga',                            'Flower Child', 'Burundi',       'lavado',  'Washed Red Bourbon. Apricot, persimmon, berries. Mol 38 · 93°C.',                                None,         'en_stock', None),
        ('Las Margaritas',                   'Passenger',    'Costa Rica',    'honey',   'Honey H3 CR. Cacao y dulce. Próxima: mol 37, 92°C.',                                              None,         'en_stock', 3.0),
        ('El Oasis Fernando Bocanegra',      'Moonwake',     'Colombia',      'lavado',  '60hr washed Gesha. Peach presente, jazmín faint. CENTER POURS crítico.',                         None,         'en_stock', 3.0),
        ('Echemo',                           'Tim Wendelboe','Etiopía',       'lavado',  'Washed Ethiopian Heirloom. Tostado muy claro — molienda un paso más gruesa que referencia.',     None,         'en_stock', None),
        ('Sumava',                           'La Cabra',     'Costa Rica',    'honey',   'Honey SL28 Costa Rica. Plano — viejo. Convertir a Cold Brew con jamaica. Mol 75.',              None,         'en_stock', 2.0),
        ('Habtamu Fekadu Aga Landrace',      'Hydrangea',    'Etiopía',       'lavado',  'Washed Yirgacheffe. 4 meses post tueste. Mol 38 · 93°C.',                                       None,         'en_stock', None),
        ('Melese Wolde Anaerobic Natural',   'Hydrangea',    'Etiopía',       'natural', 'Anaerobic natural Sidama. Landrace 74158, Bombe Sidama. Mol 40 · 89°C.',                        None,         'en_stock', None),
        ('Daniel Tunsisa',                   'La Cabra',     'Etiopía',       'natural', 'Natural Heirloom Sidama. Mol 39 · 89°C. Funciona bien para cold brew con jamaica.',              None,         'en_stock', None),
        ('Las Perlitas Lot 7',               'Prodigal',     'Colombia',      'lavado',  'Washed Colombia. Tea-like, cítrico, berries. Mol 40 · 93°C.',                                   None,         'en_stock', 4.0),
        ('Colombie Frank Hoyos',             'Tanat',        'Colombia',      'natural', 'Anaerobic yeast 60h. Muffin, tropical, vainilla. Mol 40 · 89°C.',                               None,         'en_stock', None),
        ('Elida Estate Geisha ASD',          'Elida Estate', 'Panamá',        'natural', 'Natural ASD. Manzana, pera, ciruela, vainilla, brown sugar, chocolate, cítrico. RECETA MAESTRA: mol 44 · 87°C · filtro Abaca · center pours · enfriar a ~60°C.', None, 'en_stock', 5.0),
        ('Elida Estate Catuai',              'Elida Estate', 'Panamá',        'natural', 'Natural Catuai. Dulzura aromática, acidez media, nuez. Mol 38 · 92°C. Ideal para UFO.',         None,         'en_stock', 3.0),
        ('El Pergamino Geisha Honey',        'El Pergamino', 'Colombia',      'honey',   'Geisha Honey Colombia. Chemex recomendado. Mol 41 · 90°C.',                                      None,         'en_stock', None),
        ('Ayla Bombe — Yisak Ketema',        'Corvus',       'Etiopía',       'natural', 'Natural Heirloom. Frambuesa, fresa, floral. Ratio 1:17. Dejar enfriar a ~60°C. Mol 41 · 91°C.',None,         'en_stock', None),
        ('Sadayana Kongsi Winey Anaerobic',  'Corvus',       'Indonesia',     'natural', 'Anaerobic natural Indonesia. Cuerpo velvety, aftertaste chocolate oscuro. Ratio 1:16. Muy soluble — mol 37 · 89°C.', None, 'en_stock', None),
        ('Castillo Tropical Strawberry Wave','Hydrangea',    'Colombia',      'natural', 'Cofermentado fresa. Mol 38 · 91°C.',                                                              None,         'en_stock', None),
        ('La Papaya Yunguilla Natural',      'Hydrangea',    'Ecuador',       'natural', 'Natural Ecuador. Mol 40 · 89°C.',                                                                 None,         'en_stock', None),
        ('Finca Potosi XO Natural',          'Hydrangea',    'Colombia',      'natural', 'XO Natural Colombia. Ron, piña, roble. Mol 40 · 89°C.',                                          None,         'en_stock', None),
        ('Andrés Martinez Pink Bourbon',     'September',    'Colombia',      'lavado',  'Semi lavado Pink Bourbon. Pink lemonade, kiwi, watermelon candy. Mol 40 · 90°C.',                None,         'en_stock', None),
        # POR ABRIR
        ('Yunyun Nannan',                    'Tanat',        'China (Yunnan)','natural', 'Anaerobic natural Yunnan. ⚠️ Urgente — muy viejo (tostado Feb 2026).',                          '2026-02-01', 'en_stock', None),
        ('Sidra Prime',                      'Prodigal',     'Colombia',      'lavado',  'Washed Sidra. No es su perfil — muy ácido/tropical. Candidato a donar.',                        '2026-03-02', 'en_stock', 2.0),
        ('Panama Finca Carmen Caturra',      'Rogue Wave',   'Panamá',        'lavado',  'Washed Caturra Panamá.',                                                                           '2026-04-21', 'en_stock', None),
        ('Elida Estate Geisha ASD 2a Bolsa', 'Elida Estate', 'Panamá',        'natural', 'Natural ASD — en congelador. Prueba Origami vs taza normal pendiente.',                          None,         'en_stock', None),
        ('El Burro Lot E',                   'September',    'Panamá',        'natural', 'Natural Gesha Panamá. ⚠️ Abrir ya — casi 2 meses de tueste.',                                   '2026-04-29', 'en_stock', None),
        ('Sugar Dust',                       'September',    'Etiopía',       'lavado',  'Anaerobic washed Gesha. Fruit loops, cereal, lavanda leve. ★5 en sesión previa.',               '2026-04-28', 'en_stock', 5.0),
        ('Gerba Dogo',                       'Datura',       'Etiopía',       'lavado',  'Washed Heirloom Guji. En peak. Abaca filter. Mol 38 · 92°C.',                                   '2026-04-27', 'en_stock', None),
        # TERMINADOS
        ('Kirimahiga AB',                    'September',    'Kenya',         'lavado',  'Kenya washed — referencia máxima. Tea-like, berry, cítrico.',                                    None,         'terminado', 5.0),
        ('Gatuya AA',                        'Hydrangea',    'Kenya',         'lavado',  'Kenya washed — referencia máxima.',                                                               None,         'terminado', 5.0),
        ('El Burro Lot F',                   'September',    'Panamá',        'natural', 'Natural Gesha Panamá. Pasado peak a 3 meses. Flores faint, vainilla leve. Flat y ácido al enfriar — lección de frescura.', None, 'terminado', 3.0),
        ('Jairo Arcila',                     'FIL',          'Colombia',      'natural', 'Aerobic natural 5 meses. Pineapple, dark chocolate.',                                            None,         'terminado', None),
    ]
    con.executemany('INSERT INTO cafes (nombre,roaster,pais_origen,proceso,perfil_taza,fecha_compra,estado,puntuacion) VALUES (?,?,?,?,?,?,?,?)', cafes)
    print(f'  ✓ {len(cafes)} cafés')

    def cid(nombre):
        row = con.execute("SELECT id FROM cafes WHERE nombre LIKE ?", (f'%{nombre}%',)).fetchone()
        return row['id'] if row else None

    # ── RECETAS AFINADAS ───────────────────────────────────────────────────
    recetas = [
        (cid('Elida Estate Geisha ASD'),  'V60',      15.0, 225, 87, '3:00–3:30',
         'RECETA MAESTRA ★5. Filtro Abaca. Ratio 1:15. Bloom 30ml · 50 seg. 2 pulsos ~97ml CENTER POURS. '
         'Dejar enfriar a ~60°C — manzana, pera, ciruela, vainilla, brown sugar. Molienda Epeios: 44.'),
        (cid('Ayla Bombe'),               'V60',      20.0, 340, 91, '3:15',
         'Receta Corvus oficial. Filtro Abaca. Ratio 1:17. Bloom 40ml · 45 seg. 2 pulsos ~150ml. Mol 41. '
         'Si thin/lemon sin dulzura → mol 40. Si amargo/papery → mol 43. Enfriar — frambuesa, fresa, floral.'),
        (cid('Sadayana'),                 'V60',      20.0, 320, 89, '2:30–3:00',
         'Receta Corvus oficial. Filtro Abaca. Ratio 1:16. Bloom 40ml · 45 seg. 2 pulsos ~140ml. Mol 37. '
         'Muy soluble — drena rápido. Si thin/sour → mol fino. Si flat/amargo → mol grueso. Cuerpo velvety, aftertaste chocolate oscuro.'),
        (cid('Las Perlitas'),             'V60',      25.0, 375, 93, '3:00–3:30',
         'Plantilla V60 25g washed. Bloom 50ml · 45s. 3 pulsos ~108ml. Mol 38.'),
        (cid('Las Perlitas'),             'V60',      30.0, 450, 93, '3:15–3:45',
         'Plantilla V60 30g washed. Bloom 60ml · 45s. 3 pulsos ~130ml. Mol 40.'),
    ]
    con.executemany('INSERT INTO recetas (cafe_id,metodo,dosis_cafe,agua_ml,temperatura,tiempo_total,notas) VALUES (?,?,?,?,?,?,?)', recetas)
    print(f'  ✓ {len(recetas)} recetas')

    # ── SESIONES (Recipe Log) ───────────────────────────────────────────────
    sesiones = [
        (cid('Las Perlitas'),             'V60',       '2026-05-02', '25g/375ml · mol 38 · 93°C · 3:49. Tea-like, cítrico, berries. 3 meses post tueste.',              4.0),
        (cid('Las Perlitas'),             'V60',       '2026-05-02', '30g/450ml · mol 40 · 93°C · 4:00. Buen cuerpo, sabores ligeros.',                                 4.0),
        (cid('Elida Estate Geisha ASD'),  'V60',       '2026-05-08', '15g/225ml · mol 42 · 89°C · 3:30. Chocolate, vainilla, manzana/pera. Amargor leve — bajar temp.', 3.0),
        (cid('Elida Estate Geisha ASD'),  'V60',       '2026-05-10', '15g/225ml · mol 44 · 87°C · 3:15. RECETA AFINADA — manzana, pera, ciruela, chocolate, vainilla, cítrico, brown sugar.', 5.0),
        (cid('Elida Estate Catuai'),      'V60',       '2026-05-10', '20g/300ml · mol 38 · 92°C · 3:00. Dulzura aromática, acidez media, nuez.',                        3.0),
        (cid('Ninga'),                    'V60',       '2026-05-12', '30g/450ml · mol 38 · 93°C · 3:30. Apricot, persimmon, berries.',                                  None),
        (cid('Echemo'),                   'V60',       '2026-05-14', '20g/300ml · mol 40 · 92°C · 3:00. Ethiopian Heirloom washed. Tostado muy claro.',                  None),
        (cid('Mutana'),                   'V60',       '2026-05-15', '25g/375ml · mol 38 · 93°C · 3:15. Washed Bourbon Burundi.',                                        None),
        (cid('Sumava'),                   'V60',       '2026-05-15', '25g/375ml · mol 40 · 91°C · 3:20. Plano — viejo. Derivar a cold brew.',                            2.0),
        (cid('El Oasis'),                 'V60',       '2026-05-16', '25g/375ml · mol 38 · 89°C · 3:30. Outer pours apelmazaron. Peach presente, jazmín no.',            3.0),
        (cid('Javier Salas'),             'V60',       '2026-05-18', '35g/525ml · mol 41 · 90°C · 3:45 (garrafa). Ácido, sin mango/cítrico.',                           None),
        (cid('Sidra Prime'),              'V60',       '2026-05-19', '40g/600ml · mol 38 · 93°C · 3:30 (garrafa). Muy ácido, plano. No es su perfil.',                  2.0),
        (cid('Dabid Berrio'),             'V60',       '2026-05-20', '40g/600ml · mol 38 · 93°C · 3:45 (garrafa). Chiroso washed Colombia.',                             None),
        (cid('Lovely Day'),               'V60',       '2026-05-21', '35g/525ml · mol 42 · 88°C · 3:45 (garrafa). Carbonic maceration natural Myanmar.',                 None),
        (cid('Las Margaritas'),           'V60',       '2026-05-22', '35g/525ml · mol 39 · 91°C · 3:30 (garrafa). Honey H3 CR. Cacao y dulce. Próxima: mol 37 · 92°C.',3.0),
        (cid('Colombie Frank Hoyos'),     'V60',       '2026-05-22', '11g/165ml · mol 40 · 89°C · 2:50. Anaerobic yeast 60h. Muffin, tropical, vainilla.',              None),
        (cid('Yunyun Nannan'),            'V60',       '2026-05-23', '40g/600ml · mol 41 · 88°C · 3:45 (garrafa). Anaerobic natural Yunnan.',                           None),
        (cid('Melese Wolde'),             'V60',       '2026-05-25', '27g/405ml · mol 40 · 89°C · 3:15. Landrace 74158, Bombe Sidama.',                                 None),
        (cid('Melese Wolde'),             'UFO-V2',    '2026-05-26', '15g/225ml · mol 37 · 88°C · 3:10. Flujo lento y constante.',                                      None),
        (cid('Habtamu Fekadu'),           'V60',       '2026-05-27', '25g/375ml · mol 38 · 93°C · 3:20. Washed Yirgacheffe. 4 meses post tueste.',                      None),
        (cid('Daniel Tunsisa'),           'V60',       '2026-05-28', '25g/375ml · mol 39 · 89°C · 3:15. Natural Heirloom Sidama.',                                      None),
        (cid('Javier Salas'),             'AeroPress', '2026-05-30', '18g/270ml · mol 38 · 90°C · 2:20. Presión lenta y suave.',                                        None),
        (cid('Sumava'),                   'Switch',    '2026-06-01', '80g/800ml · mol 75 · fría · 17h refri. Cold Brew reconvertido. Ratio 1:10.',                       None),
        (cid('Andrés Martinez'),          'V60',       '2026-06-10', '25g/375ml · mol 40 · 90°C · 3:00. Pink lemonade, kiwi, watermelon candy. Semi lavado.',           None),
        (cid('Sugar Dust'),               'V60',       '2026-06-12', '25g/375ml · mol 39 · 91°C · 3:00 (Mugen). Fruit loops, cereal, lavanda leve. Anaerobic washed Gesha.', 5.0),
        (cid('Gerba Dogo'),               'V60',       '2026-06-13', '25g/375ml · mol 38 · 92°C · 3:00. Washed Heirloom Guji. Abaca filter.',                           None),
        (cid('Ayla Bombe'),               'V60',       '2026-06-15', '20g/340ml · mol 41 · 91°C · 3:15. Ratio 1:17. Faint frambuesa, floral. Mejorar próxima vez.',     None),
        (cid('Sadayana'),                 'V60',       '2026-06-16', '20g/320ml · mol 37 · 89°C · 2:45. Ratio 1:16. Muy soluble. Abaca filter.',                        None),
        (cid('El Burro Lot F'),           'V60',       '2026-06-17', '25g/375ml · mol 39 · 89°C · 3:35. Pasado peak 3 meses. Flores faint, vainilla leve. Flat y ácido al enfriar.', 3.0),
        (cid('El Burro Lot E'),           'V60',       '2026-06-18', '25g/375ml · mol 40 · 89°C · 3:00. Gesha natural Panamá. Abrir pronto — misma fecha tueste que Lot F.', None),
        (cid('Finca Potosi XO'),          'V60',       '2026-06-20', '20g/300ml · mol 40 · 89°C · 3:00. XO Natural Colombia. Ron, piña, roble.',                        None),
        (cid('Jairo Arcila'),             'AeroPress', '2026-06-22', '18g/270ml · mol 40 · 91°C · 2:20. 5 meses — aerobic natural. Pineapple, dark chocolate.',         None),
    ]
    con.executemany('INSERT INTO sesiones (cafe_id,metodo,fecha,notas,puntuacion) VALUES (?,?,?,?,?)', sesiones)
    print(f'  ✓ {len(sesiones)} sesiones')

    con.commit()
    con.close()
    print('\nSeed completado.')

if __name__ == '__main__':
    run()
