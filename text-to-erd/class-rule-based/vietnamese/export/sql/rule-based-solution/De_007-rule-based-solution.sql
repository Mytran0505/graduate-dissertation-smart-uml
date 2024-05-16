CREATE TABLE trang_phuc (
	ma_trang_phuc INT CONSTRAINT PK_trang_phuc PRIMARY KEY,
	ten_trang_phuc VARCHAR(100),
	kich_co FLOAT,
	mau_sac VARCHAR(255),
	gia_cho_thue VARCHAR(255)
);

CREATE TABLE khach_hang (
	ma_khach_hang INT CONSTRAINT PK_khach_hang PRIMARY KEY,
	ho_ten VARCHAR(100),
	dia_chi VARCHAR(255),
	so_dien_thoai INT
);

CREATE TABLE hop_dong (
	ma_hop_dong INT CONSTRAINT PK_hop_dong PRIMARY KEY,
	ngay_bat_dau_hop_dong DATE,
	ngay_ket_thuc_hop_dong DATE,
	tri_gia_hop_dong VARCHAR(255)
);

CREATE TABLE thue (
	ma_hop_dong INT,
	CONSTRAINT FK_thue_hop_dong FOREIGN KEY(ma_hop_dong) REFERENCES hop_dong(ma_hop_dong),
	ma_trang_phuc INT,
	CONSTRAINT FK_thue_trang_phuc FOREIGN KEY(ma_trang_phuc) REFERENCES trang_phuc(ma_trang_phuc),
	CONSTRAINT PK_thue PRIMARY KEY(ma_hop_dong, ma_trang_phuc)
);

