CREATE TABLE bao (
	ma_bao INT CONSTRAINT PK_bao PRIMARY KEY,
	ten_bao VARCHAR(100),
	don_gia VARCHAR(255)
);

CREATE TABLE khach_hang (
	ma_khach_hang INT CONSTRAINT PK_khach_hang PRIMARY KEY,
	ten_khach_hang VARCHAR(100),
	dia_chi VARCHAR(255)
);

CREATE TABLE hoa_don (
	so_hoa_don INT CONSTRAINT PK_hoa_don PRIMARY KEY,
	ngay_dat_mua DATE,
	tri_gia_hoa_don VARCHAR(255)
);

CREATE TABLE thong_tin_chi_tiet (
	so_hoa_don INT,
	CONSTRAINT FK_thong_tin_chi_tiet_hoa_don FOREIGN KEY(so_hoa_don) REFERENCES hoa_don(so_hoa_don),
	ma_bao INT,
	CONSTRAINT FK_thong_tin_chi_tiet_bao FOREIGN KEY(ma_bao) REFERENCES bao(ma_bao),
	so_luong_dat_mua INT,
	CONSTRAINT PK_thong_tin_chi_tiet PRIMARY KEY(so_hoa_don, ma_bao)
);

