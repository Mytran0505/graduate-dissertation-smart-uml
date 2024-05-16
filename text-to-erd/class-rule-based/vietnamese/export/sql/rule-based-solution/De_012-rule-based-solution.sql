CREATE TABLE benh_vien (
	ma_benh_vien INT CONSTRAINT PK_benh_vien PRIMARY KEY,
	ten_benh_vien VARCHAR(100),
	so_giuong_benh INT
);

CREATE TABLE quoc_gia (
	ma_quoc_gia INT CONSTRAINT PK_quoc_gia PRIMARY KEY,
	ten_quoc_gia VARCHAR(100),
	so_luong_ca_nhiem_benh INT,
	so_luong_nguoi_da_chet INT
);

CREATE TABLE benh_nhan (
	ma_benh_nhan INT CONSTRAINT PK_benh_nhan PRIMARY KEY,
	ten_benh_nhan VARCHAR(100),
	gioi_tinh VARCHAR(255),
	ngay_sinh DATE,
	dia_chi VARCHAR(255)
);

CREATE TABLE duoc_dieu_tri (
	ma_benh_nhan INT,
	CONSTRAINT FK_duoc_dieu_tri_benh_nhan FOREIGN KEY(ma_benh_nhan) REFERENCES benh_nhan(ma_benh_nhan),
	ma_benh_vien INT,
	CONSTRAINT FK_duoc_dieu_tri_benh_vien FOREIGN KEY(ma_benh_vien) REFERENCES benh_vien(ma_benh_vien),
	CONSTRAINT PK_duoc_dieu_tri PRIMARY KEY(ma_benh_nhan, ma_benh_vien)
);

