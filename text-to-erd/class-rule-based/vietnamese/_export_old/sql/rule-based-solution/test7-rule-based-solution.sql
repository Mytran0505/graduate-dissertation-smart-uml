CREATE TABLE phong_may_tinh (
	ma_phong INT CONSTRAINT PK_phong_may_tinh PRIMARY KEY,
	ten_phong VARCHAR(100),
	ten_nguoi_quan_ly_phong VARCHAR(100)
);

CREATE TABLE may_tinh (
	ma_may_tinh INT CONSTRAINT PK_may_tinh PRIMARY KEY,
	toc_do_CPU FLOAT,
	dung_luong_RAM FLOAT,
	dung_luong_o_cung FLOAT,
	ma_phong INT,
	CONSTRAINT FK_may_tinh_phong_may_tinh FOREIGN KEY(ma_phong) REFERENCES phong_may_tinh(ma_phong)
);

CREATE TABLE mon_hoc (
	ma_mon_hoc INT CONSTRAINT PK_mon_hoc PRIMARY KEY,
	ten_mon_hoc VARCHAR(100),
	thoi_luong_mon_hoc VARCHAR(255)
);

CREATE TABLE dang_ky (
	ma_mon_hoc INT,
	CONSTRAINT FK_dang_ky_mon_hoc FOREIGN KEY(ma_mon_hoc) REFERENCES mon_hoc(ma_mon_hoc),
	ma_phong INT,
	CONSTRAINT FK_dang_ky_phong_may_tinh FOREIGN KEY(ma_phong) REFERENCES phong_may_tinh(ma_phong),
	ngay_dang_ky DATE,
	CONSTRAINT PK_dang_ky PRIMARY KEY(ma_mon_hoc, ma_phong)
);

