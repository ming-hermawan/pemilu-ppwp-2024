from module.db.base.sql.sqlite import BaseDbSqlite


class DbSqlite(BaseDbSqlite):

    # Constructor
    def __init__(self,
                 db_filename: str):
        super().__init__(
          db_filename=db_filename)

    # Destructor
    def __del__(self):
        super().__del__()

    # PROTECTED Begin

    # ppwps

    def __create_table_ppwps(self):
        self._execute(
          '''
CREATE TABLE ppwps(
ppwp_code TEXT PRIMARY KEY,
dt TEXT,
name TEXT,
color TEXT,
order_number INT)
;''')

    def __insert_into_ppwps(self,
                            ppwps: dict):
        parameters = list(
          (key,
           value['ts'],
           value['nama'],
           value['warna'],
           value['nomor_urut']) for key, value in ppwps.items()
        )
        self._executemany(
          '''
INSERT INTO ppwps(
ppwp_code,
dt,
name,
color,
order_number)
VALUES(
?,
?,
?,
?,
?)
;''',
          parameters)

    # regions

    def __create_table_regions(self):
        self._execute(
          '''
CREATE TABLE regions(
region_code TEXT PRIMARY KEY,
region_id INT,
name TEXT,
level INT,
prefix TEXT)
;''')

    def __insert_into_regions(self,
                              regions: list):
        parameters = list(
          (x['kode'],
           x['id'],
           x['nama'],
           x['tingkat'],
           x['prefix']) for x in regions
        )
        self._executemany(
          '''
INSERT INTO regions(
region_code,
region_id,
name,
level,
prefix)
VALUES(
?,
?,
?,
?,
?)
;''',
          parameters)

    # hhcw_ppwps

    def __create_table_hhcw_ppwps(self):
        self._execute(
          '''
CREATE TABLE hhcw_ppwps(
hhcw_code TEXT PRIMARY KEY,
dt TEXT,
prefix TEXT,
vote_status INT,/* status_suara */
adm_status INT,/* status_adm */
valid_vote INT,/* administrasi.suara_sah */
unvalid_vote INT,/* administrasi.suara_tidak_sah */
total_vote INT,/* administrasi.suara_total */
dpt_j_voter INT,/* administrasi.pemilih_dpt_j */
dpt_l_voter INT,/* administrasi.pemilih_dpt_l */
dpt_p_voter INT,/* administrasi.pemilih_dpt_p */
dpt_j_user INT,/* administrasi.pengguna_dpt_j */
dpt_l_user INT,/* administrasi.pengguna_dpt_l */
dpt_p_user INT,/* administrasi.pengguna_dpt_p */
dptb_j_user INT,/* administrasi.pengguna_dptb_j */
dptb_l_user INT,/* administrasi.pengguna_dptb_l */
dptb_p_user INT,/* administrasi.pengguna_dptb_p */
non_dpt_j_user INT,/* administrasi.pengguna_non_dpt_j */
non_dpt_l_user INT,/* administrasi.pengguna_non_dpt_l */
non_dpt_p_user INT,/* administrasi.pengguna_non_dpt_p */
total_j_user INT,/* administrasi.pengguna_total_j */
total_l_user INT,/* administrasi.pengguna_total_l */
total_p_user INT,/* administrasi.pengguna_total_p */
psu TEXT)
;''')

    def __create_table_hhcw_ppwp_empty_administration(self):
        self._execute(
          '''
CREATE TABLE hhcw_ppwp_empty_administration(
hhcw_code TEXT PRIMARY KEY)
;''')

    def __create_table_hhcw_ppwp_charts(self):
        self._execute(
          '''
CREATE TABLE hhcw_ppwp_charts(
hhcw_code TEXT,
ppwp_code TEXT,
value INT,
PRIMARY KEY (hhcw_code, ppwp_code))
;''')

    def __create_table_hhcw_ppwp_empty_chart(self):
        self._execute(
          '''
CREATE TABLE hhcw_ppwp_empty_chart(
hhcw_code TEXT PRIMARY KEY)
;''')

    def __create_table_hhcw_ppwp_images(self):
        self._execute(
          '''
CREATE TABLE hhcw_ppwp_images(
hhcw_code TEXT,
n INT,
link TEXT,
PRIMARY KEY (hhcw_code, n))
;''')

    def __create_table_hhcw_ppwp_empty_image(self):
        self._execute(
          '''
CREATE TABLE hhcw_ppwp_empty_image(
hhcw_code TEXT PRIMARY KEY)
;''')

    def __get_hhcw_ppwp_charts(self,
                               hhcw_code: list,
                               ppwp_codes: list,
                               chart: dict) -> list:
        output = []
        if chart is not None:
            for key, value in chart.items():
                if key in ppwp_codes:
                    output.append(
                      (
                        hhcw_code,
                        key,
                        value)
                    )
        return output

    def __get_hhcw_ppwp_images(self,
                               hhcw_code: list,
                               images: list):
        output = []
        if (images is not None):
            filtered_images = list(
              filter(
                lambda x2: x2 is not None, images
              )
            )
            for n in range(0, len(filtered_images)):
                output.append(
                  (
                    hhcw_code,
                    n,
                    filtered_images[n])
                )
        return output

    def __insert_into_hhcw_ppwps(self,
                                 hhcw_ppwps: list,
                                 ppwp_codes: list):
        hhcw_ppwps_parameters = []
        hhcw_ppwp_empty_administration_parameters = []
        hhcw_ppwp_charts_parameters = []
        hhcw_ppwp_empty_chart_parameters = []
        hhcw_ppwp_images_parameters = []
        hhcw_ppwp_empty_image_parameters = []
        for x in hhcw_ppwps:
            hhcw_code = x['code']
            dt = x['ts']
            prefix = x['prefix']
            vote_status = x['status_suara']
            adm_status = x['status_adm']
            valid_vote = unvalid_vote = total_vote = dpt_j_voter = \
                dpt_l_voter = dpt_p_voter = dpt_j_user = \
                dpt_l_user = dpt_p_user = dptb_j_user = \
                dptb_l_user = dptb_p_user = non_dpt_j_user = \
                non_dpt_l_user = non_dpt_p_user = total_j_user = \
                total_l_user = total_p_user = None
            if 'administrasi' in x.keys():
                administration = x['administrasi']
                if administration is not None:
                    valid_vote = \
                        administration['suara_sah']
                    unvalid_vote = \
                        administration['suara_tidak_sah']
                    total_vote = \
                        administration['suara_total']
                    dpt_j_voter = \
                        administration['pemilih_dpt_j']
                    dpt_l_voter = \
                        administration['pemilih_dpt_l']
                    dpt_p_voter = \
                        administration['pemilih_dpt_p']
                    dpt_j_user = \
                        administration['pengguna_dpt_j']
                    dpt_l_user = \
                        administration['pengguna_dpt_l']
                    dpt_p_user = \
                        administration['pengguna_dpt_p']
                    dptb_j_user = \
                        administration['pengguna_dptb_j']
                    dptb_l_user = \
                        administration['pengguna_dptb_l']
                    dptb_p_user = \
                        administration['pengguna_dptb_p']
                    non_dpt_j_user = \
                        administration['pengguna_non_dpt_j']
                    non_dpt_l_user = \
                        administration['pengguna_non_dpt_l']
                    non_dpt_p_user = \
                        administration['pengguna_non_dpt_p']
                    total_j_user = \
                        administration['pengguna_total_j']
                    total_l_user = \
                        administration['pengguna_total_l']
                    total_p_user = \
                        administration['pengguna_total_p']
                else:
                    hhcw_ppwp_empty_administration_parameters.append(
                      [hhcw_code]
                    )
            psu = x['psu']
            hhcw_ppwps_parameters.append(
              (
                hhcw_code,
                dt,
                prefix,
                vote_status,
                adm_status,
                valid_vote,
                unvalid_vote,
                total_vote,
                dpt_j_voter,
                dpt_l_voter,
                dpt_p_voter,
                dpt_j_user,
                dpt_l_user,
                dpt_p_user,
                dptb_j_user,
                dptb_l_user,
                dptb_p_user,
                non_dpt_j_user,
                non_dpt_l_user,
                non_dpt_p_user,
                total_j_user,
                total_l_user,
                total_p_user,
                psu)
            )
            if 'chart' in x.keys():
                hhcw_ppwp_charts = self.__get_hhcw_ppwp_charts(
                  hhcw_code=hhcw_code,
                  ppwp_codes=ppwp_codes,
                  chart=x['chart'])
                if len(hhcw_ppwp_charts) > 0:
                    hhcw_ppwp_charts_parameters.extend(
                      hhcw_ppwp_charts
                    )
                else:
                    hhcw_ppwp_empty_chart_parameters.append(
                      [hhcw_code]
                    )
            if 'images' in x.keys():
                hhcw_ppwp_images = self.__get_hhcw_ppwp_images(
                  hhcw_code=hhcw_code,
                  images=x['images'])
                if len(hhcw_ppwp_images) > 0:
                    hhcw_ppwp_images_parameters.extend(
                      hhcw_ppwp_images
                    )
                else:
                    hhcw_ppwp_empty_image_parameters.append(
                      [hhcw_code]
                    )
        self._executemany(
          '''
INSERT INTO hhcw_ppwps(
hhcw_code,
dt,
prefix,
vote_status,
adm_status,
valid_vote,
unvalid_vote,
total_vote,
dpt_j_voter,
dpt_l_voter,
dpt_p_voter,
dpt_j_user,
dpt_l_user,
dpt_p_user,
dptb_j_user,
dptb_l_user,
dptb_p_user,
non_dpt_j_user,
non_dpt_l_user,
non_dpt_p_user,
total_j_user,
total_l_user,
total_p_user,
psu)
VALUES(
?,
?,
?,
?,
?,
?,
?,
?,
?,
?,
?,
?,
?,
?,
?,
?,
?,
?,
?,
?,
?,
?,
?,
?)
;''',
          hhcw_ppwps_parameters)
        self._executemany(
          '''
INSERT INTO hhcw_ppwp_empty_administration(
hhcw_code)
VALUES(
?)
;''',
          hhcw_ppwp_empty_administration_parameters)
        self._executemany(
          '''
INSERT INTO hhcw_ppwp_charts(
hhcw_code,
ppwp_code,
value)
VALUES(
?,
?,
?)
;''',
          hhcw_ppwp_charts_parameters)
        self._executemany(
          '''
INSERT INTO hhcw_ppwp_empty_chart(
hhcw_code)
VALUES(
?)
;''',
          hhcw_ppwp_empty_chart_parameters)
        self._executemany(
          '''
INSERT INTO hhcw_ppwp_images(
hhcw_code,
n,
link)
VALUES(
?,
?,
?)
;''',
          hhcw_ppwp_images_parameters)
        self._executemany(
          '''
INSERT INTO hhcw_ppwp_empty_image(
hhcw_code)
VALUES(
?)
;''',
          hhcw_ppwp_empty_image_parameters)

    # hhcw_ppwps End

    # PROTECTED End

    # PUBLIC Begin

    def process(self,
                ppwps: dict,
                regions: list,
                hhcw_ppwps: list):
        self.__create_table_ppwps()
        self.__create_table_regions()
        self.__create_table_hhcw_ppwps()
        self.__create_table_hhcw_ppwp_empty_administration()
        self.__create_table_hhcw_ppwp_charts()
        self.__create_table_hhcw_ppwp_empty_chart()
        self.__create_table_hhcw_ppwp_images()
        self.__create_table_hhcw_ppwp_empty_image()
        self.__insert_into_ppwps(
          ppwps=ppwps)
        self.__insert_into_regions(
          regions=regions)
        self.__insert_into_hhcw_ppwps(
          hhcw_ppwps=hhcw_ppwps,
          ppwp_codes=list(ppwps.keys()))
        self._commit()

    # PUBLIC End
