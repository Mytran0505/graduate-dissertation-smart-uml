CREATE TABLE mon_the_thao (
	ma_mon INT CONSTRAINT PK_mon_the_thao PRIMARY KEY,
	ten_mon VARCHAR(100),
	loai_mon VARCHAR(255)
);

CREATE TABLE noi_dung_thi_dau (
	ma_noi_dung INT CONSTRAINT PK_noi_dung_thi_dau PRIMARY KEY,
	ten_noi_dung VARCHAR(100),
	le_phi_tham_gia VARCHAR(255)
);

CREATE TABLE van_dong_vien (
	ma_van_dong_vien INT CONSTRAINT PK_van_dong_vien PRIMARY KEY,
	ho_ten VARCHAR(100),
	gioi_tinh VARCHAR(255),
	ngay_sinh DATE,
	thong_tin_lien_he VARCHAR(255)
);

CREATE TABLE tham_gia (
	ma_van_dong_vien INT,
	CONSTRAINT FK_tham_gia_van_dong_vien FOREIGN KEY(ma_van_dong_vien) REFERENCES van_dong_vien(ma_van_dong_vien),
	ma_noi_dung INT,
	CONSTRAINT FK_tham_gia_noi_dung_thi_dau FOREIGN KEY(ma_noi_dung) REFERENCES noi_dung_thi_dau(ma_noi_dung),
	CONSTRAINT PK_tham_gia PRIMARY KEY(ma_van_dong_vien, ma_noi_dung)
);

