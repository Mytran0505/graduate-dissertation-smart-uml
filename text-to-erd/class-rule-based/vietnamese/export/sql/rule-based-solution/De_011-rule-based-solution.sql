CREATE TABLE loai_hinh_tai_nang (
	ma_loai_hinh_tai_nang INT CONSTRAINT PK_loai_hinh_tai_nang PRIMARY KEY,
	ten_loai_hinh VARCHAR(100),
	so_thi_sinh_dang_ky_tham_gia INT
);

CREATE TABLE huan_luyen_vien (
	ma_huan_luyen_vien INT CONSTRAINT PK_huan_luyen_vien PRIMARY KEY,
	ho_ten VARCHAR(100),
	gioi_tinh VARCHAR(255),
	so_dien_thoai INT
);

CREATE TABLE thi_sinh (
	ma_so_du_thi INT CONSTRAINT PK_thi_sinh PRIMARY KEY,
	ho_ten VARCHAR(100),
	gioi_tinh VARCHAR(255),
	ngay_sinh DATE,
	dia_chi VARCHAR(255)
);

CREATE TABLE duoc_dang_ky (
	ma_loai_hinh_tai_nang INT,
	CONSTRAINT FK_duoc_dang_ky_loai_hinh_tai_nang FOREIGN KEY(ma_loai_hinh_tai_nang) REFERENCES loai_hinh_tai_nang(ma_loai_hinh_tai_nang),
	ma_so_du_thi INT,
	CONSTRAINT FK_duoc_dang_ky_thi_sinh FOREIGN KEY(ma_so_du_thi) REFERENCES thi_sinh(ma_so_du_thi),
	CONSTRAINT PK_duoc_dang_ky PRIMARY KEY(ma_loai_hinh_tai_nang, ma_so_du_thi)
);

