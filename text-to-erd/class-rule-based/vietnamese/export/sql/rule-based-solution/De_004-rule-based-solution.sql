CREATE TABLE loai_giao_trinh (
	ma_loai_giao_trinh INT CONSTRAINT PK_loai_giao_trinh PRIMARY KEY,
	ten_loai_giao_trinh VARCHAR(100),
	chu_de VARCHAR(255)
);

CREATE TABLE giao_trinh (
	ma_giao_trinh INT CONSTRAINT PK_giao_trinh PRIMARY KEY,
	ten_giao_trinh VARCHAR(100),
	so_trang INT,
	nam_xuat_ban VARCHAR(255)
);

CREATE TABLE tac_gia (
	ma_tac_gia INT CONSTRAINT PK_tac_gia PRIMARY KEY,
	ho_ten_tac_gia VARCHAR(100),
	ngay_thang_nam_sinh DATE,
	que_quan VARCHAR(255),
	chuyen_nganh VARCHAR(255)
);

CREATE TABLE viet (
	ma_tac_gia INT,
	CONSTRAINT FK_viet_tac_gia FOREIGN KEY(ma_tac_gia) REFERENCES tac_gia(ma_tac_gia),
	ma_giao_trinh INT,
	CONSTRAINT FK_viet_giao_trinh FOREIGN KEY(ma_giao_trinh) REFERENCES giao_trinh(ma_giao_trinh),
	CONSTRAINT PK_viet PRIMARY KEY(ma_tac_gia, ma_giao_trinh)
);

