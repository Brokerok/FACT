from mysql_config import MySQL_config
from sqlalchemy import create_engine
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


file_values_list = []
db_values_list = []


def select_and_process_file():
    file_path = filedialog.askopenfilename(
        title="Choose file",
        filetypes=[("CSV files", "*.csv")]
    )

    try:
        # Reading file
        df = pd.read_csv(file_path, engine='python')
        firm_edrpou_file_values = df['firm_edrpou']

        for value in firm_edrpou_file_values:
            try:
                file_values_list.append(int(value))
            except:
                pass

        # Reading db
        engine = create_engine(MySQL_config)
        df = pd.read_sql('SELECT * FROM court_data', engine)
        for row in df.iloc:
            try:
                value = int(row['firm_edrpou'])
                db_values_list.append(value)
            except:
                pass

        # Search for matches
        set1 = set(file_values_list)
        set2 = set(db_values_list)
        common = set1 & set2
        common = list(common)
        try:
            common.remove(0)
        except:
            pass

        # # Write a new file
        new_file_path = file_path[:-4] + '(result).csv'
        data = {
            'firm_edrpou': common
        }
        df = pd.DataFrame(data)
        df.to_csv(new_file_path, index=True, encoding='utf-8')

        messagebox.showinfo("DONE", f"File processed successfully! result -  {new_file_path}")
    except:
        messagebox.showerror("ERROR", f"Something went wrong!!! Сheck file integrity")


def main():
    root = tk.Tk()
    root.title("edrpou checker")
    root.geometry("800x600+300+200")
    info_label = tk.Label(root, text='Find all edrpou matches')
    info_label.pack(pady=10, padx=20)
    btn = tk.Button(root, text="Choose file", command=select_and_process_file, width=40, height=5,
                    relief="raised", bd=3)
    btn.pack(pady=20, expand=True)
    root.focus_force()
    root.mainloop()


if __name__ == "__main__":
    main()
