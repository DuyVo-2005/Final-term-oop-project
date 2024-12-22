import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
import pandas as pd
from module import Account
from module import User
from module import Transfer, Trans
from module import readData, writeData
from module import GetPresentTime
import datetime
from PIL import Image, ImageTk
import numpy as np

# Tạo cửa sổ chính
root = tk.Tk()
root.geometry("600x800+50+50")
root.title("App Quản Lý Tài Chính Cá Nhân")
root.configure(bg="#66cdaa")
root.resizable(width=False, height=False)

# Biến toàn cục để lưu dữ liệu
user, cataLogList = readData()

import csv

txt_file = "data\\AccountList.txt"
csv_file = "data\\AccountList(1).csv"

txt_file2 = "data\\DebtList.txt"
csv_file2 = "data\\DebtList(1).csv"

def account_report(user):
    accountNameList = []
    incomeList = []  # Danh sách thu nhập
    expenseList = []  # Danh sách chi tiêu
    if len(user.Get_Account_List()) != 0:
        for account in user.Get_Account_List():
            accountNameList.append(account.Get_Account_Name())
            if account.Get_Acount_Type() == "ví điện tử":
                incomeList.append(account.Get_Balance())
                expenseList.append(0)
            else:
                incomeList.append(0)
                expenseList.append(account.Get_Balance())

        index = np.arange(len(accountNameList))  # Tạo index dựa trên số tài khoản
        bar_width = 0.35  # Độ rộng mỗi cột

        # Vẽ biểu đồ
        plt.bar(index, incomeList, bar_width, label="ví điện tử", color="green")
        plt.bar(
            index + bar_width, expenseList, bar_width, label="ngân hàng", color="red"
        )

        plt.title("Báo cáo Tình hình Tài chính Theo Tài khoản")
        plt.ylabel("Tổng số tiền")
        plt.xlabel("Tài khoản")
        plt.xticks(  #
            index + bar_width / 2, accountNameList, rotation=45
        )  # Đặt nhãn vào giữa các cặp cột
        plt.legend()  # Thêm chú thích
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showerror(
            "Thống kê",
            "Danh sách tài khoản rỗng, không thống kê được!",
        )

def chuyen_txt_sang_csv(txt_file, csv_file, header):
    # Đọc dữ liệu từ file .txt và ghi sang file .csv
    with open(txt_file, "r") as infile, open(csv_file, "w", newline="") as outfile:
        # Tạo đối tượng writer
        writer = csv.writer(outfile)
        row = header.strip().split("|")
        writer.writerow(row)
        # Lặp qua từng dòng trong file .txt
        for line in infile:
            # Tách các giá trị bằng dấu phẩy
            row = line.strip().split("|")
            writer.writerow(row)
    return txt_file, csv_file

def income_and_spending_report(data, period):
    if str(period) != "":
        data["Time"] = pd.to_datetime(data["Time"])
        if period == "theo ngày":
            data["Period"] = data["Time"].dt.date
        elif period == "theo tuần":
            data["Period"] = data["Time"].dt.to_period("W").astype(str)
        elif period == "theo tháng":
            data["Period"] = data["Time"].dt.to_period("M").astype(str)
        else:
            data["Period"] = data["Time"].dt.year
        # Nhóm dữ liệu theo thời gian và loại Fluctuation
        summary = (
            data.groupby(["Period", "Fluctuation"])["Amount"].sum().unstack().fillna(0)
        )

        # Vẽ biểu đồ
        summary.plot(kind="bar", figsize=(10, 6), stacked=True, color=["green", "red"])
        plt.title(f"Báo cáo Thu nhập và Chi tiêu ({period})")
        plt.ylabel("Tổng Amount")
        plt.xlabel("Thời gian")
        plt.legend(["Thu nhập", "Chi tiêu"])
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showerror(
            "Thống kê",
            "Vui lòng chọn khoảng thời gian cần báo cáo thu nhập và chi tiêu!",
        )


def loan_report(data):
    if data["Fluctuation"].isnull().all():
        messagebox.showerror(
            "Thống kê",
            "Danh sách khoản vay và cho vay rỗng! Không thống kê được!",
        )
    else:
        # Tính tổng Amount theo nhóm Fluctuation
        summary = data.groupby(["Fluctuation"])["Amount"].sum()

        # Xác định nhãn biểu đồ dựa trên nội dung Fluctuation
        labels = summary.index.map(
            lambda x: (
                "Vay"
                if x.lower() == "income"
                else "Cho Vay" if x.lower() == "spend" else x
            )
        )

        # Vẽ biểu đồ
        summary.plot(
            kind="pie",
            autopct="%1.2f%%",
            figsize=(8, 8),
            startangle=90,
            colors=["blue", "green"],
            labels=labels,
        )
        plt.title("Báo cáo Khoản vay và Cho vay")
        plt.ylabel("")
        plt.show()

def Statis_Page():
    # Chuyển giao diện tương tác
    Delete_Current_Info()

    txt_file2 = "data\\DebtList.txt"
    csv_file2 = "data\\DebtList(1).csv"
    header2 = "ID|Fluctuation|Amount|InterestRate|DueDate|Time|"
    txt_file2, csv_file2 = chuyen_txt_sang_csv(txt_file2, csv_file2, header2)

    TransactionData = pd.read_csv(
        "data\\TransactionData.csv",
        encoding="utf-8",
        sep=",",
    )
    DebtListData = pd.read_csv(
        "data\\DebtList(1).csv",
        sep=",",
        encoding="utf-8",
    )

    tk.Label(frame_Main, text="Thống kê tổng quan", font=("Arial", 12, "bold")).pack(
        pady=10
    )
    period = tk.StringVar()
    periodList = ["theo ngày", "theo tuần", "theo tháng", "theo năm"]
    combobox_chu_ky_thoi_gian = ttk.Combobox(
        frame_Main, textvariable=period, values=periodList, width=15
    )

    combobox_chu_ky_thoi_gian.pack(pady=10)

    tk.Button(
        frame_Main,
        text="Báo cáo Thu nhập và Chi tiêu",
        font=("Arial", 12),
        bg="#778899",
        width=32,
        command=lambda: income_and_spending_report(TransactionData, period.get()),
    ).pack(pady=10)

    tk.Button(
        frame_Main,
        text="Báo cáo Khoản vay và Cho vay",
        font=("Arial", 12),
        bg="#778899",
        width=32,
        command=lambda: loan_report(DebtListData),
    ).pack(pady=10)

    tk.Button(
        frame_Main,
        text="Báo cáo Tình hình Tài chính Theo Tài khoản",
        font=("Arial", 12),
        bg="#778899",
        width=32,
        command=lambda: account_report(user),
    ).pack(pady=10)
    

def Login_Programe():
    frame_DangNhap.pack_forget()
    
    # Tạo frame chính cho chương trình
    global frame_Main
    frame_Main = tk.Frame(root, bg="#66cdaa")
    frame_Main.pack(fill=tk.BOTH, expand=True)
    
    # Tạo menu các chức năng của App
    menu = tk.Menu(root)
    file_menu = tk.Menu(menu, tearoff=0) 
    file_menu.add_command(label="Trang Chủ", command=Home_Page)
    file_menu.add_command(label="Tài Khoản", command=Account_Page)
    file_menu.add_command(label="Giao Dịch", command=QuanLyThuChi)
    file_menu.add_command(label="Khoản Vay", command=Debt_Page)
    file_menu.add_command(label="Thống Kê", command=Statis_Page)
    file_menu.add_separator()
    file_menu.add_command(label="Thoát", command=root.quit)
    menu.add_cascade(label="Menu", menu=file_menu)
    root.config(menu=menu)
    
    # Hiển thị trang chủ mặc định khi đăng nhập
    Home_Page()

image_path1 = 'data\\image1.png'
image_path2 = 'data\\image2.png'
image_path3 = 'data\\image3.png'

def Home_Page():
    '''Xử lý giao diện cho trang chủ bao gồm các thông tin hiển thị về tổng thu nhập, tổng chi tiêu và số dư'''
    
    # Chuyển giao diện tương tác
    Delete_Current_Info()
    
    # Hiển thị các thông tin tổng quan của người dùng
    tk.Label(frame_Main, text="Tổng quan tài chính", font=("Arial", 18, "bold"), bg="#66cdaa").pack(pady=10)
    total_balnace = user.Get_Total_Balance()
    tk.Label(frame_Main, text=f"Tổng số dư: {total_balnace} VND", font=("Arial", 14), bg="#66cdaa").pack(pady=5)
    
    image = Image.open(image_path2)
    image = image.resize((500, 500))
    photo = ImageTk.PhotoImage(image)
    
    image_label = tk.Label(frame_Main, image=photo, bg="#66cdaa")
    image_label.image = photo
    image_label.pack(pady=10)

def Account_Page():
    '''Xử lý giao diện tài khoản khi người dùng nhấp vào từ menu chương trình'''

    # Xử lý cho chức năng xóa giao dịch
    def XoaChuyenKhoan():

        # Xử lý khi người dùng bấm xác nhận xóa sau khi nhập ID
        def XoaChuyenKhoanID():
            try:
                id = int(ID.get())
            except:
                messagebox.showerror("Lỗi", "Bạn chưa nhập ID hoặc ID không hợp lệ")
                return

            if user.Delete_Transfer(id):
                messagebox.showinfo("Xóa chuyển khoản", "Xóa thành công")
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy ID cần xóa")

            windown.destroy()
            writeData(user)
            LichSuChuyenKhoan()

        windown = tk.Toplevel()
        tk.Label(windown, text="Nhập ID mã giao dịch bạn muốn xóa", font=("Arial", 12, "bold")).pack(pady=10)
        ID = tk.Entry(windown, width=20)
        ID.pack(pady=10)
        tk.Button(windown, text="Xác nhận", font=("Arial", 12), bg="#778899", command=XoaChuyenKhoanID).pack(pady=10)

    # Xử lý cho chức năng chỉnh sửa giao dịch
    def ChinhSuaChuyenKhoan():  

        # Xử lý khi người dùng bấm xác nhận ID cần chỉnh sửa
        def ChinhSuaChuyenKhoanID():

            # Xử lý sao khi người dùng đã nhập xong thông tin chỉnh sửa
            def CapNhatChuyenKhoan():
                try:
                    soTien = int(ammount.get())
                except:
                    messagebox.showerror("Lỗi", "Vui lòng nhập số tiền hợp lệ")
                user.Edit_Transfer(id, soTien, newSourceAccount.get(), newDesAccount.get(), timeEdit.get(), note.get())
                writeData(user)
                messagebox.showinfo("Chỉnh sửa chuyển khoản", "Chỉnh sửa thành công")
                LichSuChuyenKhoan()

            try:
                id = int(ID.get())
            except:
                messagebox.showerror("Lỗi", "Bạn chưa nhập ID hoặc ID không hợp lệ")
                return

            if user.Get_Transfer_By_ID(id):
                windown.destroy()

                newWindown = tk.Toplevel()
                newWindown.geometry("300x500")
                tk.Label(newWindown, text="Cập nhật thông tin", font=("Arial", 12, "bold"), width=20).grid(row=0, column=0, columnspan=2, sticky="we")
                tk.Label(newWindown, text="Source Account", font=("Arial", 12), width=15).grid(row=1, column=0, padx=5, pady=10)
                newSourceAccount = ttk.Combobox(newWindown, values=[accout.Get_Account_Name() for accout in user.Get_Account_List()], width=15)
                newSourceAccount.grid(row=1, column=1, padx=5, pady=10)
                newSourceAccount.insert(0, user.Get_Transfer_By_ID(id).Get_Source_Account().Get_Account_Name())

                tk.Label(newWindown, text="Destination Account", font=("Arial", 12), width=15).grid(row=2, column=0, padx=5, pady=10)
                newDesAccount = ttk.Combobox(newWindown, values=[accout.Get_Account_Name() for accout in user.Get_Account_List()], width=15)
                newDesAccount.grid(row=2, column=1, padx=5, pady=10)
                newDesAccount.insert(0, user.Get_Transfer_By_ID(id).Get_Des_Account().Get_Account_Name())

                tk.Label(newWindown, text="Time", font=("Arial", 12), width=15).grid(row=3, column=0, padx=5, pady=10)
                timeEdit = tk.Entry(newWindown, width=20)
                timeEdit.grid(row=3, column=1)
                timeEdit.insert(0, user.Get_Transfer_By_ID(id).Get_Time())

                tk.Label(newWindown, text="Note", font=("Arial", 12), width=15).grid(row=4, column=0, padx=5, pady=10)
                note = tk.Entry(newWindown,  width=20)
                note.grid(row=4, column=1)
                note.insert(0, user.Get_Transfer_By_ID(id).Get_Note())

                tk.Label(newWindown, text="Amount", font=("Arial", 12), width=15).grid(row=5, column=0, padx=5, pady=10)
                ammount = tk.Entry(newWindown,  width=20)
                ammount.grid(row=5, column=1)
                ammount.insert(0, user.Get_Transfer_By_ID(id).Get_Amount())

                tk.Button(newWindown,text="Xác nhận", font=("Arial", 12), bg="#778899", command=CapNhatChuyenKhoan).grid(row=6, column=1, columnspan=2, pady=10)

                newWindown.columnconfigure(0, weight=1)
                newWindown.columnconfigure(1, weight=1)

            else:
                messagebox.showerror("Lỗi", "Không tìm thấy ID cần cập nhật")
                windown.destroy()

        windown = tk.Toplevel()
        tk.Label(windown, text="Nhập ID mã giao dịch bạn muốn chỉnh sửa", font=("Arial", 12, "bold")).pack(pady=10)
        ID = tk.Entry(windown, width=20)
        ID.pack(pady=10)
        tk.Button(windown, text="Xác nhận", font=("Arial", 12), bg="#778899", command=ChinhSuaChuyenKhoanID).pack(pady=10)

    # Xử lý cho chức năng xem giao dịch đã diễn ra
    def LichSuChuyenKhoan():

        # Chuyển màn hình giao dịch
        Delete_Current_Info()

        tree = ttk.Treeview(frame_Main, columns=("ID","Amount","SourceAccountName","DesAccountName","Time","Note"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Amount", text="Amount")
        tree.heading("SourceAccountName", text="SourceAccountName")
        tree.heading("DesAccountName", text="DesAccountName") 
        tree.heading("Time", text="Time")
        tree.heading("Note", text="Note")

        tree.column("ID", width=30, anchor="center")
        tree.column("Amount", width=20, anchor="center")
        tree.column("SourceAccountName", width=80, anchor="center")
        tree.column("DesAccountName", width=70, anchor="center")
        tree.column("Time", width=40, anchor="center")
        tree.column("Note", width=60, anchor="center")

        tree.pack(pady=10, fill=tk.BOTH, expand=True)
        for transfer in user.Get_Transfer_List():
            tree.insert("", tk.END, values=(transfer.Get_ID(), transfer.Get_Amount(), transfer.Get_Source_Account().Get_Account_Name(), transfer.Get_Des_Account().Get_Account_Name(), transfer.Get_Time(), transfer.Get_Note()))

        tk.Button(frame_Main, text="Xóa giao dịch", font=("Arial", 12, "bold"), bg="#778899", width=20, command=XoaChuyenKhoan).pack(pady=10)
        tk.Button(frame_Main, text="Chỉnh sửa giao dịch", font=("Arial", 12, "bold"), bg="#778899", width=20, command=ChinhSuaChuyenKhoan).pack(pady=10)

    # Xử lý cho chức năng tạo tài khoản mới
    def TaoTaiKhoan():
        def ThucHienTaoTaiKhoan():
            if user.Add_Account(Account(accountType.get(), nameAccount.get(), int(balnaceAccount.get()))):
                writeData(user)
                messagebox.showinfo("Tạo tài khoản", "Tài khoản được tạo thành công")
                newWindown.destroy()
                writeData(user)
                Account_Page()
            else:
                messagebox.showinfo("Tạo tài khoản", "Tạo tài khoản thất bại, vui lòng kiểm tra lại dữ liệu!")

        newWindown = tk.Toplevel()
        newWindown.geometry("300x500")
        tk.Label(newWindown, text="Tạo tài khoản mới", font=("Arial", 12, "bold"), width=25).grid(row=0, column=0, columnspan=2, sticky="we")
        tk.Label(newWindown, text="Chọn loại tài khoản", font=("Arial", 12), width=25).grid(row=1, column=0, padx=5, pady=10)
        accountType = ttk.Combobox(newWindown, values=["ngân hàng", "ví điện tử"], width=15)
        accountType.grid(row=1, column=1, padx=5, pady=10)

        tk.Label(newWindown, text="Nhập tên tài khoản", font=("Arial", 12), width=25).grid(row=2, column=0, padx=5, pady=10)
        nameAccount = tk.Entry(newWindown, font=("Arial", 12), width=20)
        nameAccount.grid(row=2, column=1, padx=5, pady=10)

        tk.Label(newWindown, text="Nhập số dư tài khoản", font=("Arial", 12), width=25).grid(row=3, column=0, padx=5, pady=10)
        balnaceAccount = tk.Entry(newWindown, font=("Arial", 12), width=20)
        balnaceAccount.grid(row=3, column=1, padx=5, pady=10)

        tk.Button(newWindown,text="Xác nhận", font=("Arial", 12), bg="#778899", command=ThucHienTaoTaiKhoan).grid(row=6, column=1, columnspan=2, pady=10)

        newWindown.columnconfigure(0, weight=1)
        newWindown.columnconfigure(1, weight=1)

    # Xử lý cho chức năng xóa tài khoản
    def XoaTaiKhoan():

        # Xử lý khi người dùng nhập tên tài khoản cần xóa
        def XoaTaiKhoanTheoTen():
            if user.Delete_Account(accountName.get()):
                messagebox.showinfo("Xóa tài khoản", "Xóa tài khoản thành công")
                writeData(user)
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy tên tài khoản cần xóa")
            newWindown.destroy()
            writeData(user)
            Account_Page()

        newWindown = tk.Toplevel()
        tk.Label(newWindown, text="Xóa tài khoản", font=("Arial", 12, "bold"), width=25).pack(pady=5)
        tk.Label(newWindown, text="Nhập tên tài khoản cần xóa").pack(pady=5)
        accountName = tk.Entry(newWindown, width=15)
        accountName.pack(pady=5)
        tk.Button(newWindown, text="Xác nhận",bg="#778899", command=XoaTaiKhoanTheoTen).pack(pady=10)

    # Xử lý chức năng chỉnh sửa tài khoản
    def ChinhSuaTaiKhoan():
        newWindown = tk.Toplevel()

        # Xử lý chỉnh sửa tài khoản khi người dùng đã nhập tên
        def ChinhSuaTaiKhoanTheoTen():

            # Xử lý khi ngươi dùng đã nhập đúng tên tài khoản cần cập nhật và thực hiện cập nhật
            def CapNhatTaiKhoan():
                try:
                    soTien = int(balnace.get())
                except:
                    messagebox.showerror("Lỗi", "Số tiền không hợp lệ")
                    return

                user.Edit_Account(accountName, typeAccount.get(), accountNameV1.get(), soTien)
                messagebox.showinfo("Cập nhật tài khoản", "Cập nhật thông tin tài khoản thành công")
                newWindown.destroy()
                writeData(user)
                Account_Page()

            nonlocal newWindown
            accountName = accountNameEdit.get()
            newWindown.destroy()
            if user.Get_Account_By_Name(accountName=accountName):
                newWindown = tk.Toplevel() 
                newWindown.geometry("500x500")
                tk.Label(newWindown, text="Cập nhật thông tin tài khoản", font=("Arial", 12, "bold"), width=20).grid(row=0, column=0, columnspan=2, sticky="we")

                tk.Label(newWindown, text="Loại tài khoản", font=("Arial", 12), width=15).grid(row=1, column=0, padx=5, pady=10)
                typeAccount = ttk.Combobox(newWindown, values=["ngân hàng", "ví điện tử"], width=15)
                typeAccount.grid(row=1, column=1, padx=5, pady=10)
                typeAccount.insert(0, user.Get_Account_By_Name(accountName).Get_Acount_Type())

                tk.Label(newWindown, text="Tên tài khoản", font=("Arial", 12), width=15).grid(row=2, column=0, padx=5, pady=10)
                accountNameV1 = tk.Entry(newWindown, width=20)
                accountNameV1.grid(row=2, column=1)
                accountNameV1.insert(0, user.Get_Account_By_Name(accountName).Get_Account_Name())

                tk.Label(newWindown, text="Số dư tài khoản", font=("Arial", 12), width=15).grid(row=3, column=0, padx=5, pady=10)
                balnace = tk.Entry(newWindown,  width=20)
                balnace.grid(row=3, column=1)
                balnace.insert(0, user.Get_Account_By_Name(accountName).Get_Balance())

                tk.Button(newWindown, text="Xác nhận", font=("Arial", 12), bg="#778899", command=CapNhatTaiKhoan).grid(row=4, column=0, columnspan=2, pady=15)

                newWindown.columnconfigure(0, weight=1)
                newWindown.columnconfigure(1, weight=1)

            else:
                messagebox.showerror("Lỗi", "Không tìm thấy tên tài khoản cần cập nhật")

        tk.Label(newWindown, text="Chỉnh sửa tài khoản", font=("Arial", 12, "bold"), width=25).pack(pady=5)
        tk.Label(newWindown, text="Nhập tên tài khoản chỉnh sửa").pack(pady=5)
        accountNameEdit = tk.Entry(newWindown, width=15)
        accountNameEdit.pack(pady=5)
        tk.Button(newWindown, text="Xác nhận", command=ChinhSuaTaiKhoanTheoTen, bg="#778899").pack(pady=10)

    # Xử lý cho chức năng tạo giao dịch mới
    def ChuyenKhoan():
        def SetSoDuTkChuyen(event=None):
            tk.Label(frame_Main, text=f"Số dư: {user.Get_Account_By_Name(var_tai_khoan_chuyen.get()).Get_Balance()}", font=("Arial", 12), width=20).grid(row=3, column=0, padx=5, pady=10)

        def SetSoDuTkNhan(event=None):
            tk.Label(frame_Main, text=f"Số dư: {user.Get_Account_By_Name(var_tai_khoan_nhan.get()).Get_Balance()}", font=("Arial", 12), width=20).grid(row=3, column=1, padx=5, pady=10)

        def ChuyenKhoan():
            try:
                soTienChuyenKhoan = int(soTien.get())
            except:
                messagebox.showerror("Lỗi", "Số tiền chuyển khoản không hợp lệ")
                return
            # Nếu số tiền chuyển khoản đã hợp lệ
            try:
                if user.Get_Account_By_Name(var_tai_khoan_chuyen.get()).Get_Balance() >= soTienChuyenKhoan:
                    user.Create_Transfer(sourceAccountName=var_tai_khoan_chuyen.get(), desAccountName=var_tai_khoan_nhan.get(), amount=soTienChuyenKhoan, note=note.get())
                    writeData(user)
                    messagebox.showinfo("Thêm chuyển khoản", "Chuyển khoản thành công")
                    SetSoDuTkChuyen()
                    SetSoDuTkNhan()
                else:
                    messagebox.showinfo("Thêm chuyển khoản", "Chuyển khoản thất bại, vui lòng kiểm tra lại số tiền!")
            except:
                messagebox.showinfo(
                    "Thêm chuyển khoản",
                    "Chuyển khoản thất bại, vui lòng kiểm tra dữ liệu!",
                )

        Delete_Current_Info()
        tk.Label(frame_Main, text="Tạo chuyển khoản", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, sticky="we", padx=5, pady=10)
        tk.Label(frame_Main, text="Chuyển từ tài khoản", font=("Arial", 12), width=20).grid(row=1, column=0, padx=5, pady=10)
        tk.Label(frame_Main, text="Chuyển vào tài khoản", font=("Arial", 12), width=20).grid(row=1, column=1, padx=5, pady=10)
        tk.Label(frame_Main, text="Số tiền chuyển khoản", font=("Arial", 12), width=20).grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        soTien = tk.Entry(frame_Main, width=15)
        soTien.grid(row=5, column=0, columnspan=2,  padx=5, pady=10)
        tk.Label(frame_Main, text="Ghi chú", font=("Arial", 12), width=20).grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        note = tk.Entry(frame_Main, width=30)
        note.grid(row=7, column=0, columnspan=2,  padx=5, pady=10)
        tk.Button(frame_Main, text="Thêm", font=("Arial", 12, "bold"), bg="#778899", command=ChuyenKhoan).grid(row=9, column=0, columnspan=2,  padx=10, pady=10)

        image = Image.open(image_path3)
        image = image.resize((350, 350))
        photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(frame_Main, image=photo, bg="#66cdaa")
        image_label.image = photo
        image_label.grid(row = 10, column= 0, columnspan= 2, pady=10)

        # Biến lưu giá trị Combobox
        var_tai_khoan_chuyen = tk.StringVar()
        var_tai_khoan_nhan = tk.StringVar()

        # Tạo ra list để sao chép accountName
        valueNameAccount = []
        for account in user.Get_Account_List():
            valueNameAccount.append(account.Get_Account_Name())

        # Combobox Tài khoản chuyển
        combobox_tai_khoan_chuyen = ttk.Combobox(frame_Main, textvariable=var_tai_khoan_chuyen, values=valueNameAccount, width=15)
        combobox_tai_khoan_chuyen.grid(row=2, column=0)
        combobox_tai_khoan_chuyen.bind("<<ComboboxSelected>>", SetSoDuTkChuyen)

        # Combobox Tài khoản nhận
        combobox_tai_khoan_nhan = ttk.Combobox(frame_Main, textvariable=var_tai_khoan_nhan, values=valueNameAccount, width=15)
        combobox_tai_khoan_nhan.grid(row=2, column=1)
        combobox_tai_khoan_nhan.bind("<<ComboboxSelected>>", SetSoDuTkNhan)

        frame_Main.columnconfigure(0, weight=1)
        frame_Main.columnconfigure(1, weight=1)

    # Chuyển giao diện tương tác
    Delete_Current_Info()

    # Hiển thị các thông tin của tài khoản
    tk.Label(frame_Main, text="Thông tin các tài khoản", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, sticky="we", padx=5, pady=10)
    tk.Button(frame_Main, text="Lịch sử chuyển khoản", font=("Arial", 12), bg="#778899", width=32, command=LichSuChuyenKhoan).grid(row=1, column=0, padx=5, pady=10)
    tk.Button(frame_Main, text="Thêm giao dịch chuyển khoản mới", font=("Arial", 12), bg="#778899", width=32, command=ChuyenKhoan).grid(row=1, column=1, padx=5, pady=10)

    # Hiển thị danh sách các tài khoản
    frame_DanhSachTaiKhoan = tk.Frame(frame_Main)
    frame_DanhSachTaiKhoan.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky="we")
    tk.Label(frame_DanhSachTaiKhoan, text="Danh sách các tài khoản", font=("Arial", 12, "bold")).pack(side=tk.TOP, fill=tk.X, expand=True)
    tree = ttk.Treeview(frame_DanhSachTaiKhoan, columns=("Loại tài khoản", "Tên tài khoản", "Số dư tài khoản"), show="headings")
    tree.heading("Loại tài khoản", text="Loại tài khoản")
    tree.heading("Tên tài khoản", text="Tên tài khoan")
    tree.heading("Số dư tài khoản", text="Số dư tài khoản")

    tree.column("Loại tài khoản", width=20, anchor="center")
    tree.column("Tên tài khoản", width=20, anchor="center")
    tree.column("Số dư tài khoản", width=20, anchor="center")

    accountList = user.Get_Account_List()
    # Xóa tất cả dữ liệu cũ trên Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Thêm từng dòng dữ liệu vào Treeview
    for account in accountList:
        tree.insert("", "end", values=(
                account.Get_Acount_Type(),
                account.Get_Account_Name(),
                account. Get_Balance()
            ))
    tree.pack(fill=tk.BOTH, expand=True)

    tk.Button(frame_DanhSachTaiKhoan, text="Tạo tài khoản", font=("Arial", 12), bg="#778899", width=32, command=TaoTaiKhoan).pack(pady=5)
    tk.Button(frame_DanhSachTaiKhoan, text="Xóa tài khoản", font=("Arial", 12), bg="#778899", width=32, command=XoaTaiKhoan).pack(pady=5)
    tk.Button(frame_DanhSachTaiKhoan, text="Chỉnh sửa tài khoản", font=("Arial", 12), bg="#778899", width=32, command=ChinhSuaTaiKhoan).pack(pady=5)

    frame_Main.columnconfigure(0, weight=1)
    frame_Main.columnconfigure(1, weight=1)

# Xử lý cho giao dịch
def QuanLyThuChi():

    def ThemGiaoDich():
        try:
            soTien = int(amount.get())
            datetime.datetime.strptime(timeEdit.get(), "%Y-%m-%d")
        except:
            messagebox.showerror("Lỗi", "Dữ liệu bạn nhập không hợp lệ")
            return

        if soTien > user.Get_Account_By_Name(account_name.get()).Get_Balance() and transaction_type.get() == "spend":
            messagebox.showerror("Lỗi", "Số tiền không đủ để thực hiện giao dịch")
            return

        user.Get_Account_By_Name(account_name.get()).Create_Transaction(category.get(), transaction_type.get(), soTien, timeEdit.get())
        messagebox.showinfo("Thêm giao dịch", "Thêm giao dịch thành công")
        writeData(user)
        QuanLyThuChi()

    def ChinhSuaGiaoDich():
        def ChinhSuaGiaoDichTheoID():
            def ThucHienCapNhatGiaoDich():
                try:
                    soTien = int(amount_new.get())
                except ValueError:
                    messagebox.showerror("Lỗi", "Kiểu dữ liệu hoặc định dạng không hợp lệ")
                    return

                user.Get_Account_By_Name(name_account).Edit_Transaction(
                    id, category_new.get(), transaction_type_new.get(), soTien, timeEdit.get()
                )
                messagebox.showinfo("Cập nhật giao dịch", "Cập nhật giao dịch thành công")
                windown.destroy()
                writeData(user)
                QuanLyThuChi()

            nonlocal windown
            name_account = nameAccountEdit.get()
            try:
                id = int(idGiaoDichCanSua.get())
            except ValueError:
                messagebox.showerror("Lỗi", "Mã ID hoặc tài khoản không hợp lệ")
                return

            transaction = user.Get_Account_By_Name(name_account).Get_Transaction_By_ID(id)
            windown.destroy()  # Hủy cửa sổ sau khi lấy dữ liệu
            if transaction:
                windown = tk.Toplevel()
                tk.Label(windown, text="Loại:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
                transaction_type_new = ttk.Combobox(windown, values=["income", "spend"], width=15)
                transaction_type_new.insert(0, transaction.Get_Fluctuation())
                transaction_type_new.grid(row=0, column=1, padx=5, pady=5)

                tk.Label(windown, text="Danh mục:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
                category_new = ttk.Combobox(windown, values=cataLogList, width=15)
                category_new.insert(0, transaction.Get_Catalog())
                category_new.grid(row=1, column=1, padx=5, pady=5)

                tk.Label(windown, text="Số tiền:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
                amount_new = tk.Entry(windown, width=17)
                amount_new.insert(0, transaction.Get_Amount())
                amount_new.grid(row=2, column=1, padx=5, pady=5)

                tk.Label(windown, text="Ngày giao dịch:", font=("Arial", 12)).grid(row=3,column=0, padx=5, pady=5)
                timeEdit = tk.Entry(windown, width=17)
                timeEdit.insert(0, transaction.Get_Time())
                timeEdit.grid(row=3, column=1, padx=5, pady=5)

                tk.Button(windown, text="Xác nhận", width=20, bg="#778899", command=ThucHienCapNhatGiaoDich).grid(row=4, column=1, padx=5, pady=10)
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy ID giao dịch cần chỉnh sửa")

        windown = tk.Toplevel()
        tk.Label(windown, text="Chọn tài khoản đã thực hiện giao dịch", font=("Arial", 10, "bold")).pack(pady=10)
        nameAccountEdit = ttk.Combobox(windown, value=[accout.Get_Account_Name() for accout in user.Get_Account_List()], width=15)
        nameAccountEdit.pack(pady=10)
        tk.Label(windown, text="Nhập ID giao dịch cần chỉnh sửa", font=("Arial", 10, "bold")).pack(pady=10)
        idGiaoDichCanSua = tk.Entry(windown, width=20)
        idGiaoDichCanSua.pack(pady=10)
        tk.Button(windown, text="Xác nhận", bg="#778899", command=ChinhSuaGiaoDichTheoID).pack(pady=10)

    def XoaGiaoDich():

        # Thực hiện xóa sau khi người dùng hòan tất việc nhập
        def XoaGiaoDichID():
            try:
                id = int(idGiaoDichXoa.get())
            except ValueError:
                messagebox.showerror("Lỗi", "Mã ID hoặc tài khoản không hợp lệ")
                return

            if user.Get_Account_By_Name(nameAccountEdit.get()).Delete_Transaction(id):
                messagebox.showinfo("Xóa giao dịch", "Giao dịch đã được xóa thành công")
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy ID giao dịch cần xóa")
            writeData(user)
            windown.destroy()
            QuanLyThuChi()

        windown = tk.Toplevel()
        tk.Label(windown, text="Chọn tài khoản đã thực hiện giao dịch", font=("Arial", 10, "bold")).pack(pady=10)
        nameAccountEdit = ttk.Combobox(windown, value=[accout.Get_Account_Name() for accout in user.Get_Account_List()], width=15)
        nameAccountEdit.pack(pady=10)
        tk.Label(windown, text="Nhập ID giao dịch cần chỉnh xóa", font=("Arial", 10, "bold")).pack(pady=10)
        idGiaoDichXoa = tk.Entry(windown, width=20)
        idGiaoDichXoa.pack(pady=10)
        tk.Button(windown, text="Xác nhận", bg="#778899", command=XoaGiaoDichID).pack(pady=10)

    Delete_Current_Info()

    tk.Label(frame_Main, text="Quản lý thu | chi", font=("Arial", 12, "bold")).pack(side="top", fill=tk.X, expand="false", padx=5, pady=10)

    # Form thêm giao dịch
    form_frame = tk.Frame(frame_Main, bg="#66cdaa")
    form_frame.pack(pady=10)
    tk.Label(form_frame, text="Tên tài khoản:", font=("Arial", 12), bg="#66cdaa").grid(row=0, column=0, padx=5, pady=5)
    account_name = ttk.Combobox(form_frame, value = [accout.Get_Account_Name() for accout in user.Get_Account_List()], width=15)
    account_name.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Loại:", font=("Arial", 12), bg="#66cdaa").grid(row=1, column=0, padx=5, pady=5)
    transaction_type = ttk.Combobox(form_frame, values=["income", "spend"], width=15)
    transaction_type.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Danh mục:", font=("Arial", 12), bg="#66cdaa").grid(row=2, column=0, padx=5, pady=5)
    category = ttk.Combobox(form_frame, values=cataLogList, width=15)
    category.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Số tiền:", font=("Arial", 12), bg="#66cdaa").grid(row=3, column=0, padx=5, pady=5)
    amount = tk.Entry(form_frame, width=17)
    amount.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Ngày giao dịch:", font=("Arial", 12), bg="#66cdaa").grid(row=4,column=0, padx=5, pady=5)
    timeEdit = tk.Entry(form_frame, width=17)
    timeEdit.grid(row=4, column=1, padx=5, pady=5)
    timeEdit.insert(0, "YYYY-MM-DD")

    tk.Button(form_frame, text="Thêm", bg="#778899", command=ThemGiaoDich).grid(row=5, columnspan=2, pady=10)

    # Danh sách giao dịch
    # Frame chứa danh sách các giao dịch
    frame_DanhSachGiaoDich = tk.Frame(frame_Main)
    frame_DanhSachGiaoDich.pack(pady=10, fill=tk.BOTH, expand=True)
    tk.Label(frame_DanhSachGiaoDich, text="Danh sách giao dịch:", font=("Arial", 14)).pack(side="top", fill=tk.X, expand="false", padx=5, pady=10)
    tree = ttk.Treeview(frame_DanhSachGiaoDich, columns=("Tên tài khoản", "ID", "Loại", "Danh mục", "Số tiền", "Ngày giao dịch"), show="headings")
    tree.heading("Tên tài khoản", text="Tên tài khoản")
    tree.heading("ID", text="ID")
    tree.heading("Loại", text="Loại")
    tree.heading("Danh mục", text="Danh mục")
    tree.heading("Số tiền", text="Số tiền")
    tree.heading("Ngày giao dịch", text="Ngày giao dịch")

    tree.column("Tên tài khoản", width=15, anchor="center")
    tree.column("ID", width=5, anchor="center")
    tree.column("Loại", width=10, anchor="center")
    tree.column("Danh mục", width=20, anchor="center")
    tree.column("Số tiền", width=20, anchor="center")
    tree.column("Ngày giao dịch", width=40, anchor="center")

    tree.pack(pady=10, fill=tk.BOTH, expand=True)
    transactionDataBase = pd.read_csv("data\\TransactionData.csv")

    # Xóa tất cả dữ liệu cũ trên Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Thêm từng dòng dữ liệu vào Treeview
    for index, row in transactionDataBase.iterrows():
        tree.insert(
            "",
            "end",
            values=(
                row["Account Name"],
                row["ID"],
                row["Fluctuation"],
                row["Transaction Attribute"].split("|")[0].strip(),
                row["Amount"],
                row["Time"],
            ),
        )

    # Các nút chức năng cho chỉnh sửa giao dịch
    tk.Button(frame_DanhSachGiaoDich, text="Chỉnh sửa giao dịch", width=20, bg="#778899", command=ChinhSuaGiaoDich).pack(pady=10)
    tk.Button(frame_DanhSachGiaoDich, text="Xóa giao dịch", width=20, bg="#778899", command=XoaGiaoDich).pack(pady=10)

def Delete_Current_Info():
    for widget in frame_Main.winfo_children():
        widget.destroy()

def Debt_Page():
    '''Xử lý giao diện Debt khi người dùng nhấp vào từ menu chương trình'''
    
    def __notice():
        __debtListId = []
        for debt in user.Get_Debt_List():
            if (datetime.datetime.strptime(GetPresentTime(), "%Y-%m-%d") >= datetime.datetime.strptime(debt.Get_DueDate(), "%Y-%m-%d")) and debt.Get_Remaining_Amount() > 0:
                __debtListId.append(debt.Get_ID())
                
        if len(__debtListId) > 0:
            __id = ""
            for i in __debtListId:
                __id += str(i) + " "
            messagebox.showinfo("Thông báo khoản vay", f"Bạn có khoản vay {__id}cần thanh toán!")
                
    #Xử lý cho chức năng thêm payment mới
    def ThemPayment():
        def setRemainAmount(event: None):
            tk.Label(input_window, text=f"Số tiền cần thanh toán: {user.Get_Debt_By_ID(int(__ID.get())).Get_Remaining_Amount()}", font=("Arial", 12)).grid(row=1, columnspan=2, padx=5, pady=10)
            tk.Label(input_window, text=f"Ngày bắt đầu: {user.Get_Debt_By_ID(int(__ID.get())).Get_Time()}", font=("Arial", 12)).grid(row=2, columnspan=2, padx=5, pady=10)

        input_window = tk.Toplevel(frame_Main)
        input_window.title(f"Thêm khoản thanh toán")
        input_window.geometry("350x320+700+200")

        __debtIDList = []
        __amount = tk.StringVar()
        __time = tk.StringVar()
        __ID = tk.StringVar()
        __time.set("YYYY-MM-DD")
        __sotienconlai = tk.StringVar()
        __sotienconlai.set("0")

        for debt in user.Get_Debt_List():
            __debtIDList.append(debt.Get_ID())

        tk.Label(input_window, text="Chọn ID khoản vay", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=10)
        box = ttk.Combobox(input_window, textvariable=__ID, values=__debtIDList)
        box.grid(row=0, column=1, padx=5, pady=10)
        box.bind("<<ComboboxSelected>>", setRemainAmount)
        
        tk.Label(input_window, text="Nhập số tiền thanh toán", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=10)
        tk.Entry(input_window, textvariable=__amount,font=("Arial", 12), width=20).grid(row=3, column=1, padx=5, pady=10)
        
        tk.Label(input_window, text="Nhập ngày thanh toán", font=("Arial", 12)).grid(row=4, column=0, padx=5, pady=10)
        tk.Entry(input_window, textvariable=__time,font=("Arial", 12), width=20).grid(row=4, column=1, padx=5, pady=10)

        def save():
            try:
                global user, cataLogList
                amount = int(__amount.get())
                time = __time.get()
                if (datetime.datetime.strptime(time, "%Y-%m-%d") > datetime.datetime.strptime(user.Get_Debt_By_ID(int(__ID.get())).Get_Time(), "%Y-%m-%d")) and amount > 0 and amount <= user.Get_Debt_By_ID(int(__ID.get())).Get_Remaining_Amount():
                    user.Get_Debt_By_ID(int(__ID.get())).Add_Payment(amount=amount,
                                                                     paymentDate=time)
                    input_window.destroy()
                    messagebox.showinfo("Thêm khoản thanh toán", "Thêm khoản thanh toán thành công!")
                    writeData(user)
                    user, cataLogList = readData()
                    LichSuThanhToan()
                    return
            except ValueError as e:
                print(e)
            
            messagebox.showinfo("Thêm khoản thanh toán", "Thêm khoản thanh toán thất bại, vui lòng kiểm tra lại dữ liệu nhập!")
            return

        tk.Button(input_window, text="Lưu", font=("Arial", 12), command=save, bg="#778899").grid(row=5, column=1, sticky='nsew', padx=5, pady=10)
    
    # Xử lý cho chức năng xem giao dịch đã diễn ra
    def LichSuThanhToan():
        # Chuyển màn hình giao dịch
        Delete_Current_Info()

        #Xử lý cho chức năng xóa payment mới
        def XoaPayment():
            global user, cataLogList
            selected_item = tree.selection()  
            if selected_item:
                item = selected_item[0] 
                item_info = tree.item(item) 
                values = item_info['values']
                __id = values[0]
                __date = values[2]
                if messagebox.askyesno("Xóa khoản thanh toán", "Xác nhận xóa?"):
                    user.Get_Debt_By_ID(int(__id)).Delete_Payment(paymentDate=__date)
                    messagebox.showinfo("Xóa khoản thanh toán", "Xóa khoản thanh toán thành công!")
                    writeData(user)
                    user, cataLogList = readData()
                    LichSuThanhToan()
                    return
            else:
                messagebox.showinfo("Xóa khoản thanh toán", "Vui lòng chọn khoản thanh toán cần xóa!")

        
        tk.Label(frame_Main, text="Lịch sử thanh toán", font=("Arial", 14, "bold")).grid(row=0, columnspan=2,padx=5, pady=10)
        tk.Button(frame_Main, text="Thêm khoản thanh toán", command=ThemPayment, bg="#778899").grid(row=1, column=0,padx=5, pady=10)
        tk.Button(frame_Main, text="Xóa khoản thanh toán", command=XoaPayment, bg="#778899").grid(row=1, column=1,padx=5, pady=10)
        
        image = Image.open(image_path3)
        image = image.resize((350, 350))
        photo = ImageTk.PhotoImage(image)
        
        image_label = tk.Label(frame_Main, image=photo, bg="#66cdaa")
        image_label.image = photo
        image_label.grid(row = 10, column= 0, columnspan= 2, pady=10)
        
        tree = ttk.Treeview(frame_Main, columns=("ID", "Amount", "PaymentDate"), show="headings")
        tree.heading("ID", text="ID khoản vay")
        tree.heading("Amount", text="Số tiền")
        tree.heading("PaymentDate", text="Ngày thanh toán")


        tree.column("ID", width=40, anchor="center")
        tree.column("Amount", width=30, anchor="center")
        tree.column("PaymentDate", width=50, anchor="center")

        tree.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=10)
        for debt in user.Get_Debt_List():
            for payment in debt.Get_PaymentHistory():
                tree.insert("", tk.END, values=(debt.Get_ID(), payment['amount'], payment['date']))

        frame_Main.grid_rowconfigure(3, weight=1)
        frame_Main.columnconfigure(0, weight=1)
        frame_Main.columnconfigure(1, weight=1)
    
        
    # Xử lý cho chức năng tạo khoản vay mới
    def ThemKhoanVay():
        input_window = tk.Toplevel(frame_Main)
        input_window.title(f"Thêm khoản vay")
        input_window.geometry("350x180+700+200")

        __amount = tk.StringVar()
        __dueDate = tk.StringVar()
        __dueDate.set("YYYY-MM-DD")
        __interestRate = tk.StringVar()
        __time = tk.StringVar()
        __time.set(GetPresentTime())
        __note = tk.StringVar()
        __fluc = tk.StringVar()


        tk.Label(input_window, text="Nhập số tiền", font=("Arial", 12)).grid(row=0, column=0)
        tk.Entry(input_window, textvariable=__amount, font=("Arial", 12), width=20).grid(row=0, column=1)
        tk.Label(input_window, text="Nhập lãi suất", font=("Arial", 12)).grid(row=1, column=0)
        tk.Entry(input_window, textvariable=__interestRate,font=("Arial", 12), width=20).grid(row=1, column=1)
        tk.Label(input_window, text="Nhập ngày vay", font=("Arial", 12)).grid(row=2, column=0)
        entrytime = tk.Entry(input_window, textvariable=__time, font=("Arial", 12), width=20)
        entrytime.grid(row=2, column=1)
        tk.Label(input_window, text="Nhập ngày đến hạn", font=("Arial", 12)).grid(row=3, column=0)
        entryduetime = tk.Entry(input_window, textvariable=__dueDate, font=("Arial", 12), width=20)
        entryduetime.grid(row=3, column=1)
        tk.Label(input_window, text="Nhập ghi chú", font=("Arial", 12)).grid(row=4, column=0)
        tk.Entry(input_window, textvariable=__note, font=("Arial", 12), width=20).grid(row=4, column=1)
        tk.Label(input_window, text="Chọn loại vay", font=("Arial", 12)).grid(row=5, column=0)
        ttk.Combobox(input_window, textvariable=__fluc, values=['Vay', 'Cho vay']).grid(row=5, column=1)

        def save():
            try:
                global user, cataLogList
                amount = int(__amount.get())
                dueDate = __dueDate.get()
                interestRate = float(__interestRate.get())
                time = __time.get()
                note = __note.get()
                fluc = 'spend' if __fluc.get() == 'Cho vay' else 'income'
                if (datetime.datetime.strptime(dueDate, "%Y-%m-%d") > datetime.datetime.strptime(time, "%Y-%m-%d")) and interestRate >= 0 and amount > 0:
                    user.Create_Debt(fluctuation=fluc,
                                     amount=amount,
                                     dueDate=dueDate,
                                     interestRate=interestRate,
                                     note=note,
                                     time=time)
                    input_window.destroy()
                    messagebox.showinfo("Thêm khoản vay", "Thêm khoản vay thành công!")
                    writeData(user)
                    user, cataLogList = readData()
                    Debt_Page()
                    return
                
            except ValueError as e:
                print(e)
            
            messagebox.showinfo("Thêm khoản vay", "Thêm khoản vay thất bại, vui lòng kiểm tra lại dữ liệu nhập!")
            return

        tk.Button(input_window, text="Lưu", font=("Arial", 12), command=save).grid(row=6, column=1, sticky='e')


    def XoaKhoanVay():
        input_window = tk.Toplevel(frame_Main)
        input_window.title(f"Xóa khoản vay")
        input_window.geometry("350x180+700+200")
        __id = tk.StringVar()

        def __del():
            global user, cataLogList
            try:
                if user.Delete_Debt(int(__id.get())):
                    messagebox.showinfo("Xóa khoản vay", "Xóa khoản vay thành công!")
                    input_window.destroy()
                    writeData(user)
                    user, cataLogList = readData()
                    Debt_Page()
                    return
            except ValueError as e:
                print(e)
                messagebox.showinfo("Xóa khoản vay", "Xóa khoản vay thất bại!")

        listDebtId = []
        for debt in user.Get_Debt_List():
            listDebtId.append(debt.Get_ID())
        tk.Label(input_window, text="Chọn ID của khoản vay cần xóa:", font=("Arial", 10)).place(relx=0.5, rely=0.25, anchor='center')
        ttk.Combobox(input_window, textvariable=__id, values=listDebtId).place(relx=0.5, rely=0.37, anchor='center')
        tk.Button(input_window, text="Xác nhận xóa", command=__del).place(relx=0.5, rely=0.6, anchor='center')
        
        
    # Chuyển giao diện tương tác
    Delete_Current_Info()
    
    # Hiển thị các thông tin các khoản vay
    tk.Label(frame_Main, text="Thông tin khoản vay", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, sticky="we", padx=5, pady=10)
    tk.Button(frame_Main, text="Lịch sử thanh toán", font=("Arial", 12), bg="#778899", command=LichSuThanhToan).grid(row=1, column=0, sticky="nsew", padx=5, pady=10)
    tk.Button(frame_Main, text="Thêm khoản vay mới", font=("Arial", 12), bg="#778899", command=ThemKhoanVay).grid(row=1, column=1, sticky="nsew", padx=5, pady=10)
    tk.Button(frame_Main, text="Xóa khoản vay", font=("Arial", 12), bg="#778899", command=XoaKhoanVay).grid(row=1, column=2, sticky="nsew", padx=5, pady=10)
    
    # Hiển thị danh sách các khoản vay
    tk.Label(frame_Main, text="Danh sách các khoản vay", font=("Arial", 12, "bold")).grid(row=2, column=0, columnspan=3, sticky="we", padx=5, pady=10)

    tree = ttk.Treeview(frame_Main, columns=("ID", "Fluctuation", "Amount", "Rate", "dueDate", "remainAmount"), show="headings")
    tree.heading("ID", text="ID khoản vay")
    tree.heading("Fluctuation", text="Biến động")
    tree.heading("Amount", text="Số tiền")
    tree.heading("Rate", text="Lãi suất")
    tree.heading("dueDate", text="Ngày đến hạn")
    tree.heading("remainAmount", text="Số tiền còn lại")

    tree.column("ID", width=40, anchor="center")
    tree.column("Fluctuation", width=40, anchor="center")
    tree.column("Amount", width=40, anchor="center")
    tree.column("Rate", width=40, anchor="center")
    tree.column("dueDate", width=40, anchor="center")
    tree.column("remainAmount", width=40, anchor="center")

    tree.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=5, pady=10)

    for debt in user.Get_Debt_List():
        tree.insert("", tk.END, values=(debt.Get_ID(),
                                        "vay" if debt.Get_Fluctuation() == 'income' else "cho vay",
                                        debt.Get_Amount(),
                                        debt.Get_InterestRate(),
                                        debt.Get_DueDate(),
                                        debt.Get_Remaining_Amount()))
        
    
    frame_Main.grid_rowconfigure(3, weight=1)
    frame_Main.columnconfigure(0, weight=1)
    frame_Main.columnconfigure(1, weight=1)
    __notice()

# Giao diện đăng nhập
frame_DangNhap = tk.Frame(root, bg="#66cdaa")
frame_DangNhap.pack(fill=tk.BOTH, expand=True)
tk.Label(frame_DangNhap, text="Chào mừng mọi người đến với đồ án nhóm chúng em", font=("Arial", 15, "bold"), bg="#66cdaa", pady=10).pack()
tk.Label(frame_DangNhap, text="Thành viên nhóm em bao gồm", font=("Arial", 12), bg="#66cdaa").pack()
tk.Label(frame_DangNhap, text="1. Trần Triều Dương - 23110200", font=("Arial", 13), bg="#66cdaa", width=35).pack()
tk.Label(frame_DangNhap, text="2. Võ Lê Khánh Duy - 23110196", font=("Arial", 13), bg="#66cdaa", width=35).pack()
tk.Label(frame_DangNhap, text="3. Văn Phú Hiền - 23110213", font=("Arial", 13), bg="#66cdaa", width=35).pack()
tk.Label(frame_DangNhap, text="4. Nguyễn Văn Kế - 23110234", font=("Arial", 13), bg="#66cdaa", width=35).pack()
tk.Label(frame_DangNhap, text="5. Nguyễn Phạm Bảo Trân - 23110348", font=("Arial", 13), bg="#66cdaa", width=35).pack()
tk.Button(frame_DangNhap, text="Bắt đầu chương trình", font=("Arial", 12, "bold"), bg="#778899", command=Login_Programe).pack(pady=10)

image = Image.open(image_path1)
image = image.resize((450, 450))
photo = ImageTk.PhotoImage(image)

image_label = tk.Label(frame_DangNhap, image=photo, bg="#66cdaa")
image_label.image = photo
image_label.pack(pady=10)

root.mainloop()
