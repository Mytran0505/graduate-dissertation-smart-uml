CREATE TABLE thanh_vien (
	ma_thanh_vien INT CONSTRAINT PK_thanh_vien PRIMARY KEY,
	ho_ten VARCHAR(100),
	gioi_tinh VARCHAR(255),
	ngay_sinh DATE,
	mat_khau VARCHAR(255)
);

CREATE TABLE bai_viet (
	ma_bai_viet INT CONSTRAINT PK_bai_viet PRIMARY KEY,
	tieu_de VARCHAR(255),
	ngay_dang DATE,
	noi_dung_cua_bai_viet VARCHAR(255)
);

CREATE TABLE chu_de (
	ma_chu_de INT CONSTRAINT PK_chu_de PRIMARY KEY,
	ten_cua_chu_de VARCHAR(100)
);

CREATE TABLE binh_luan (
	ma_bai_viet INT,
	CONSTRAINT FK_binh_luan_bai_viet FOREIGN KEY(ma_bai_viet) REFERENCES bai_viet(ma_bai_viet),
	ma_thanh_vien INT,
	CONSTRAINT FK_binh_luan_thanh_vien FOREIGN KEY(ma_thanh_vien) REFERENCES thanh_vien(ma_thanh_vien),
	thoi_gian_binh_luan INT,
	CONSTRAINT PK_binh_luan PRIMARY KEY(ma_bai_viet, ma_thanh_vien)
);

