CREATE TABLE tieu_chuan (
	ma_tieu_chuan INT CONSTRAINT PK_tieu_chuan PRIMARY KEY,
	ten_tieu_chuan VARCHAR(100),
	thong_tin_mo_ta VARCHAR(255)
);

CREATE TABLE tieu_chi (
	ma_tieu_chi INT CONSTRAINT PK_tieu_chi PRIMARY KEY,
	noi_dung VARCHAR(255),
	thong_tin_goi_y_tieu_chi VARCHAR(255)
);

CREATE TABLE minh_chung (
	ma_minh_chung INT CONSTRAINT PK_minh_chung PRIMARY KEY,
	ten_minh_chung VARCHAR(100),
	tom_tat_noi_dung VARCHAR(255),
	loai_minh_chung VARCHAR(255),
	tap_tin_chua_minh_chung VARCHAR(255)
);

CREATE TABLE minh_hoa (
	ma_minh_chung INT,
	CONSTRAINT FK_minh_hoa_minh_chung FOREIGN KEY(ma_minh_chung) REFERENCES minh_chung(ma_minh_chung),
	ma_tieu_chi INT,
	CONSTRAINT FK_minh_hoa_tieu_chi FOREIGN KEY(ma_tieu_chi) REFERENCES tieu_chi(ma_tieu_chi),
	CONSTRAINT PK_minh_hoa PRIMARY KEY(ma_minh_chung, ma_tieu_chi)
);

