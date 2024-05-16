CREATE TABLE bo_phim (
	ma_bo_phim INT CONSTRAINT PK_bo_phim PRIMARY KEY,
	ten_bo_phim VARCHAR(100),
	nam_phat_hanh VARCHAR(255),
	the_loai VARCHAR(255),
	so_tap INT,
	so_diem_IMDb INT
);

CREATE TABLE dao_dien (
	ma_dao_dien INT CONSTRAINT PK_dao_dien PRIMARY KEY,
	ho_ten VARCHAR(100),
	tuoi VARCHAR(255),
	nam_tot_nghiep VARCHAR(255),
	xep_hang VARCHAR(255)
);

CREATE TABLE dien_vien (
	ma_dien_vien INT CONSTRAINT PK_dien_vien PRIMARY KEY,
	ho_ten VARCHAR(100),
	gioi_tinh VARCHAR(255),
	tuoi VARCHAR(255),
	so_vai_chinh INT,
	so_vai_phu INT
);

CREATE TABLE duoc_dien (
	ma_bo_phim INT,
	CONSTRAINT FK_duoc_dien_bo_phim FOREIGN KEY(ma_bo_phim) REFERENCES bo_phim(ma_bo_phim),
	ma_dien_vien INT,
	CONSTRAINT FK_duoc_dien_dien_vien FOREIGN KEY(ma_dien_vien) REFERENCES dien_vien(ma_dien_vien),
	CONSTRAINT PK_duoc_dien PRIMARY KEY(ma_bo_phim, ma_dien_vien)
);

