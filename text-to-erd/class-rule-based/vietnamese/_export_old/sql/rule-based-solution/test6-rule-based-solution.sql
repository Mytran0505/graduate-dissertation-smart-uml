CREATE TABLE chuyen_de (
	ma_so_chuyen_de INT CONSTRAINT PK_chuyen_de PRIMARY KEY,
	ten_chuyen_de VARCHAR(100),
	hoc_phi_niem_yet VARCHAR(255)
);

CREATE TABLE hoc_vien (
	ma_so_hoc_vien INT CONSTRAINT PK_hoc_vien PRIMARY KEY,
	ho_ten VARCHAR(100),
	dia_chi VARCHAR(255),
	so_dien_thoai_lien_lac INT
);

CREATE TABLE phieu_dang_ky (
	ma_so_phieu_dang_ky INT CONSTRAINT PK_phieu_dang_ky PRIMARY KEY,
	ngay_lap_phieu DATE,
	tong_hoc_phi VARCHAR(255),
	ma_so_hoc_vien INT,
	CONSTRAINT FK_phieu_dang_ky_hoc_vien FOREIGN KEY(ma_so_hoc_vien) REFERENCES hoc_vien(ma_so_hoc_vien)
);

CREATE TABLE dang_ky (
	ma_so_phieu_dang_ky INT,
	CONSTRAINT FK_dang_ky_phieu_dang_ky FOREIGN KEY(ma_so_phieu_dang_ky) REFERENCES phieu_dang_ky(ma_so_phieu_dang_ky),
	ma_so_chuyen_de INT,
	CONSTRAINT FK_dang_ky_chuyen_de FOREIGN KEY(ma_so_chuyen_de) REFERENCES chuyen_de(ma_so_chuyen_de),
	CONSTRAINT PK_dang_ky PRIMARY KEY(ma_so_phieu_dang_ky, ma_so_chuyen_de)
);

