CREATE TABLE mon_hoc (
	ma_so_mon_hoc INT CONSTRAINT PK_mon_hoc PRIMARY KEY,
	ten_mon_hoc VARCHAR(100),
	so_tin_chi_ly_thuyet INT,
	so_tin_chi_thuc_hanh INT
);

CREATE TABLE do_an (
	ma_so_do_an INT CONSTRAINT PK_do_an PRIMARY KEY,
	ten_do_an VARCHAR(100),
	ngay_nop DATE,
	ma_so_mon_hoc INT,
	CONSTRAINT FK_do_an_mon_hoc FOREIGN KEY(ma_so_mon_hoc) REFERENCES mon_hoc(ma_so_mon_hoc)
);

CREATE TABLE sinh_vien (
	ma_so_sinh_vien INT CONSTRAINT PK_sinh_vien PRIMARY KEY,
	ho_ten_sinh_vien VARCHAR(100),
	dia_chi VARCHAR(255),
	so_dien_thoai INT
);

CREATE TABLE thuc_hien (
	ma_so_sinh_vien INT,
	CONSTRAINT FK_thuc_hien_sinh_vien FOREIGN KEY(ma_so_sinh_vien) REFERENCES sinh_vien(ma_so_sinh_vien),
	ma_so_do_an INT,
	CONSTRAINT FK_thuc_hien_do_an FOREIGN KEY(ma_so_do_an) REFERENCES do_an(ma_so_do_an),
	CONSTRAINT PK_thuc_hien PRIMARY KEY(ma_so_sinh_vien, ma_so_do_an)
);

