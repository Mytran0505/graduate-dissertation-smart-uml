CREATE TABLE chung_chi (
	ma_chung_chi INT CONSTRAINT PK_chung_chi PRIMARY KEY,
	ten_chung_chi VARCHAR(100),
	tong_so_tin_chi INT,
	muc_hoc_phi VARCHAR(255)
);

CREATE TABLE mon_hoc (
	ma_mon_hoc INT CONSTRAINT PK_mon_hoc PRIMARY KEY,
	ten_mon_hoc VARCHAR(100),
	so_tin_chi_mon_hoc INT
);

CREATE TABLE lop_hoc (
	ma_lop INT CONSTRAINT PK_lop_hoc PRIMARY KEY,
	ten_lop VARCHAR(100),
	ngay_bat_dau_hoc DATE,
	ngay_ket_thuc DATE,
	so_hoc_vien_toi_da_du_kien INT,
	ma_chung_chi INT,
	CONSTRAINT FK_lop_hoc_chung_chi FOREIGN KEY(ma_chung_chi) REFERENCES chung_chi(ma_chung_chi)
);

CREATE TABLE bao_gom (
	ma_chung_chi INT,
	CONSTRAINT FK_bao_gom_chung_chi FOREIGN KEY(ma_chung_chi) REFERENCES chung_chi(ma_chung_chi),
	ma_mon_hoc INT,
	CONSTRAINT FK_bao_gom_mon_hoc FOREIGN KEY(ma_mon_hoc) REFERENCES mon_hoc(ma_mon_hoc),
	CONSTRAINT PK_bao_gom PRIMARY KEY(ma_chung_chi, ma_mon_hoc)
);

